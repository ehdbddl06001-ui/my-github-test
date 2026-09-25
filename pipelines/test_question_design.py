"""
test_question_design.py — 출제 설계(design)·정보 선별 해설의 형식 회귀 테스트.

의학적 타당성은 여기서 검증하지 않는다(코드로 판정할 수 없다 — review_questions.py 로 사람이 본다).
여기서는 코드로 확인 가능한 것만 고정한다:
  - 기존 문항(design 없음)과 새 문항의 형식 호환성, 필드 누락·파싱
  - 웹 번들에 design 이 실리고, 해설은 채점 뒤에만 그려지는 구조가 유지되는지(정적 점검)
  - 오답노트 기록·동기화가 깨지지 않는지

실행: python pipelines/test_question_design.py
"""
from __future__ import annotations

import copy
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from frontmatter import load, validate  # noqa: E402
from lint_questions import collect_paths, iter_question_docs, lint_doc  # noqa: E402
from question_design import (DESIGN_REQUIRED_FROM, design_record, format_findings,  # noqa: E402
                             review_flags)

ROOT = HERE.parent
EXAMPLES = sorted((ROOT / "experiments" / "review" / "question-design-2026-09").glob("ex*.md"))
APP = (ROOT / "docs" / "app.js").read_text(encoding="utf-8")


def _codes(findings):
    return [f[1] for f in findings]


class ExistingContentCompat(unittest.TestCase):
    def test_existing_questions_gain_no_errors(self):
        """design 도입 전 문항(기준일 이전)은 design 관련 지적을 받지 않고, ERROR 도 새로 생기지 않는다."""
        docs = iter_question_docs(collect_paths([]))
        self.assertGreater(len(docs), 1000)
        errs, design_hits = [], []
        for d in docs:
            for f in lint_doc(d):
                if f.level == "ERROR":
                    errs.append((d.id, f.code))
                if f.code.startswith("design") and str(d.meta.get("date", "")) < DESIGN_REQUIRED_FROM:
                    design_hits.append((d.id, f.code))
        self.assertEqual(errs, [], errs[:5])
        self.assertEqual(design_hits, [], design_hits[:5])

    def test_existing_records_export_design_as_null(self):
        from export_kmle_web import build_record
        rec = build_record(ROOT / "content" / "kmle" / "2026" / "kmle-2026-1063.md")
        self.assertIsNone(rec["design"])
        self.assertEqual(rec["reviewStatus"], "unreviewed")
        self.assertTrue(rec["explanationItems"])      # 기존 해설은 그대로 파싱된다


class ReviewExamples(unittest.TestCase):
    def test_three_examples_exist(self):
        self.assertEqual(len(EXAMPLES), 3, [p.name for p in EXAMPLES])

    def test_examples_pass_contract_and_format(self):
        for p in EXAMPLES:
            d = load(p)
            self.assertEqual(d.errors, [], p.name)
            self.assertEqual(format_findings(d.meta, d.type), [], p.name)
            rec = design_record(d.meta)
            self.assertTrue(rec["key"] and rec["summary"], p.name)

    def test_examples_are_not_in_deployed_content(self):
        """검토용 예시는 content/ 밖에 있어 일일 배포·웹 번들에 섞이지 않는다."""
        for p in EXAMPLES:
            self.assertNotIn("content", p.relative_to(ROOT).parts)
        bundle = (ROOT / "docs" / "questions_kmle_content.js").read_text(encoding="utf-8")
        self.assertNotIn("review-kmle-", bundle)


class FormatChecks(unittest.TestCase):
    def setUp(self):
        self.base = copy.deepcopy(load(EXAMPLES[0]).meta)

    def test_missing_design_is_error_only_for_new_questions(self):
        m = copy.deepcopy(self.base)
        del m["design"]
        self.assertIn("design-missing", _codes(format_findings(m, "kmle")))
        m["date"] = "2026-09-18"
        self.assertEqual(format_findings(m, "kmle"), [])

    def test_item_must_exist_in_question(self):
        m = copy.deepcopy(self.base)
        m["design"]["findings"].append({"item": "혈청 IgE", "role": "rule_out", "why": "x"})
        self.assertIn("design-item-not-in-question", _codes(format_findings(m, "kmle")))

    def test_rival_cannot_be_answer_and_switch_needs_condition(self):
        m = copy.deepcopy(self.base)
        m["design"]["rival"] = m["answer"]
        m["design"]["switch"] = {"choice": "B", "condition": ""}
        codes = _codes(format_findings(m, "kmle"))
        self.assertIn("design-rival", codes)
        self.assertIn("design-switch", codes)

    def test_bad_target_and_role(self):
        m = copy.deepcopy(self.base)
        m["design"]["target"] = "암기"
        m["design"]["findings"][0]["role"] = "decoy"
        codes = _codes(format_findings(m, "kmle"))
        self.assertIn("design-target", codes)
        self.assertIn("design-role", codes)

    def test_chain_length_must_match_steps_and_is_required_for_new_items(self):
        m = copy.deepcopy(self.base)
        m["design"]["steps"] = 2
        m["design"]["chain"] = ["단서 → 진단"]
        self.assertIn("design-chain-steps", _codes(format_findings(m, "kmle")))
        m["design"]["chain"] = ["단서 → 진단", "중증도 → 치료"]
        self.assertNotIn("design-chain-steps", _codes(format_findings(m, "kmle")))
        self.assertEqual(design_record(m)["chain"], ["단서 → 진단", "중증도 → 치료"])
        del m["design"]["chain"]
        m["date"] = "2026-09-24"
        self.assertIn("design-chain-missing", _codes(format_findings(m, "kmle")))
        m["date"] = "2026-09-23"
        self.assertNotIn("design-chain-missing", _codes(format_findings(m, "kmle")))

    def test_mix_report_warns_on_shallow_or_one_target_sets(self):
        from question_design import mix_report
        shallow = [{"design": {"steps": 2, "target": "치료"}}] * 6
        _, w = mix_report(shallow)
        self.assertEqual(len(w), 3)                                   # 3단계 이상 0 % · 한 목표 100 % · 치료+다음 처치 100 %
        good = ([{"design": {"steps": 3, "target": t}} for t in ("진단", "감별", "치료")]
                + [{"design": {"steps": 2, "target": t}} for t in ("기전", "검사 선택")])
        self.assertEqual(mix_report(good)[1], [])
        self.assertEqual(mix_report(shallow[:3])[1], [])              # 묶음이 작으면 따지지 않는다
        mg = ([{"design": {"steps": 3, "target": "치료"}}] * 2 + [{"design": {"steps": 3, "target": "다음 처치"}}] * 2
              + [{"design": {"steps": 3, "target": "진단"}}])
        self.assertTrue(any("치료」+「다음 처치" in x for x in mix_report(mg)[1]))   # 따로는 40 %씩이라도 합이 80 %

    def test_answer_order_cycle_is_flagged_but_shuffled_is_not(self):
        from question_design import answer_order_warnings
        cyc = [{"id": f"kmle-2026-{1000 + i}", "date": "2026-09-25", "answer": "ABCDE"[i % 5]} for i in range(15)]
        self.assertEqual(len(answer_order_warnings(cyc)), 1)                       # 09-25 세트가 ABCDE… 였다
        mixed = "CAEBDDBACEAEBDC"
        ok = [{"id": f"kmle-2026-{1000 + i}", "date": "2026-09-26", "answer": a} for i, a in enumerate(mixed)]
        self.assertEqual(answer_order_warnings(ok), [])
        self.assertEqual(answer_order_warnings(cyc[:8]), [])                       # 작은 묶음은 따지지 않는다

    def test_difficulty_follows_reasoning_steps_not_volume(self):
        m = copy.deepcopy(self.base)
        m["difficulty"], m["design"]["steps"] = 5, 1
        self.assertIn("difficulty-vs-steps", _codes(format_findings(m, "kmle")))

    def test_reviewed_status_needs_reviewer_and_note(self):
        m = copy.deepcopy(self.base)
        m["review_status"] = "reviewed"
        self.assertIn("review-unbacked", _codes(format_findings(m, "kmle")))
        m["reviewed_by"], m["review_note"] = "검토자", "근거 확인"
        self.assertNotIn("review-unbacked", _codes(format_findings(m, "kmle")))

    def test_contract_rejects_non_dict_design(self):
        m = copy.deepcopy(self.base)
        m["design"] = "치료"
        self.assertTrue(any("design" in e for e in validate(m)))


class ReviewSignalsAreNotVerdicts(unittest.TestCase):
    def test_absolute_exclusion_is_flagged_for_review(self):
        m = copy.deepcopy(load(EXAMPLES[0]).meta)
        m["design"]["findings"][5]["why"] = "한센병을 완전히 배제한다"
        self.assertIn("absolute-exclusion", [c for c, _ in review_flags(m)])
        # 신호는 형식 오류가 아니다 — 실패로 치지 않는다
        self.assertNotIn("absolute-exclusion", _codes(format_findings(m, "kmle")))


class WebRendering(unittest.TestCase):
    def _func(self, name):
        m = re.search(r"function " + name + r"\([^)]*\)\s*\{", APP)
        self.assertIsNotNone(m, name)
        depth, i = 0, m.end() - 1
        for j in range(i, len(APP)):
            depth += {"{": 1, "}": -1}.get(APP[j], 0)
            if depth == 0:
                return APP[m.start():j + 1]
        self.fail(name)

    def test_triage_rendered_only_inside_explanation(self):
        """정보 선별 블록은 renderExplanation 안에서만 그려진다 → 채점 전에는 나오지 않는다."""
        calls = [m.start() for m in re.finditer(r"(?<!function )renderTriage\(q\)", APP)]
        body = self._func("renderExplanation")
        self.assertTrue(calls)
        self.assertEqual(len(re.findall(r"renderTriage\(q\)", body)), len(calls))

    def test_explanation_hidden_until_graded(self):
        rq = self._func("renderQuestion")
        self.assertIn('ex.classList.add("hidden")', rq)
        self.assertIn('ex.innerHTML = ""', rq)
        callers = re.findall(r"renderExplanation\(", APP)
        self.assertEqual(len(callers), 2)          # 정의 1 + showGraded 호출 1
        self.assertIn("renderExplanation(q, chosenIdx", self._func("showGraded"))
        self.assertIn("showGraded(chosenIdx)", self._func("grade"))

    def test_triage_is_collapsible_and_handles_missing_design(self):
        t = self._func("renderTriage")
        self.assertIn('if (!d || typeof d !== "object") return ""', t)
        self.assertIn("<details", t)

    def test_wrong_record_keeps_old_fields(self):
        rw = self._func("recordWrong")
        for field in ("chosen:", "answer:", "coreNote:", "differ:", "note:", "decision:"):
            self.assertIn(field, rw)


class WrongSync(unittest.TestCase):
    def test_decision_row_rendered_when_present(self):
        from import_wrong_sync import render
        data = {"items": {"x": {"id": "x", "subject": "S", "question": "q", "chosen": 1, "answer": 0,
                                "chosenText": "b", "answerText": "a", "decision": "핵심 판단 요약"}}}
        self.assertIn("| 핵심 판단 | 핵심 판단 요약 |", render("kmle", data))
        del data["items"]["x"]["decision"]
        self.assertNotIn("핵심 판단", render("kmle", data))


class QualityRules0925(unittest.TestCase):
    """2026-09-25 문항 감사에서 나온 규칙 — 한정어 요령·subtopic 결론·USMLE 한국어 검사명."""

    def _doc(self, **meta):
        from frontmatter import Doc
        base = {"type": "kmle", "date": "2026-09-26", "id": "kmle-2026-9999", "topic": "t", "subtopic": "대상포진",
                "stem": "x", "choices": ["A. 발라시클로버", "B. 아시클로버 연고만", "C. 스테로이드 단독", "D. 진통제만 투여", "E. 관찰"],
                "answer": "A"}
        base.update(meta)
        return Doc(path=Path("x.md"), body="", meta=base)

    def codes(self, d):
        return [f.code for f in lint_doc(d)]

    def test_qualifier_only_on_distractors(self):
        self.assertIn("qualifier-tell", self.codes(self._doc()))
        self.assertNotIn("qualifier-tell", self.codes(self._doc(choices=["A. 발라시클로버", "B. 아시클로버", "C. 스테로이드",
                                                                          "D. 진통제", "E. 관찰"])))

    def test_subtopic_conclusion_only_for_new_questions(self):
        self.assertIn("subtopic-conclusion", self.codes(self._doc(subtopic="Herpes Zoster — Oral Valacyclovir")))
        self.assertNotIn("subtopic-conclusion", self.codes(self._doc(subtopic="Herpes Zoster — Oral Valacyclovir", date="2026-09-25")))

    def test_usmle_labs_in_english(self):
        d = self._doc(type="usmle", id="usmle-2026-9999", labs=[{"name": "나트륨", "value": "128 mEq/L", "ref": "135-145"}])
        self.assertIn("usmle-labs-korean", self.codes(d))
        d.meta["labs"] = [{"name": "Sodium", "value": "128 mEq/L", "ref": "135-145 mEq/L"}]
        self.assertNotIn("usmle-labs-korean", self.codes(d))


if __name__ == "__main__":
    unittest.main(verbosity=1)
