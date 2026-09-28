"""
test_traps.py — 함정 계열(traps.py) 회귀 테스트. **고정 픽스처만** 쓴다(실제 content/ 를 읽지 않는다).

지키는 것:
  - 등록부 형식: 필수 필드·정규식·파일 이름·출처·근거 표시·패턴 자기 일관성(truth/mirror 정답이 제 계열에 걸리는가)
  - 문항 검사: trap 쪽(단서·truth 정답·lure 오답 수·rival·when_right) / mirror 쪽(lure 정답·truth 오답) / 모르는 id
  - 부족분 큐: 시험 × 쪽 계산, retired 제외, want 덮어쓰기, 표시 안 된 후보(topics 범위 안에서만), 순서
  - 비슷한 문항 찾기: 보기 분리, 가장 가까운 문항이 먼저
  - 린터가 design.trap 을 실제로 검사하는가

실행: python pipelines/test_traps.py
"""
from __future__ import annotations

import copy
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import traps  # noqa: E402

ENTRY = textwrap.dedent("""\
    id: tr.test.weak-pulse-thrombotic
    title: "골절 뒤 약한 맥박 — 혈전 처치로 끌림"
    status: active
    found: 2026-09-29
    found_note: "시험용 픽스처"
    exams: [kmle, usmle]
    objectives: [cn.test.compartment.fasciotomy]
    topics: [Orthopedics]
    cue:
      text: "골절 뒤 원위 맥박이 약하다"
      patterns: ["맥박[^.]{0,10}약하", "weak[^.]{0,20}pulse"]
    lure:
      family: "혈전 처치"
      examples: ["헤파린", "혈전용해"]
      patterns: ["헤파린|혈전\\\\s*용해", "heparin|thromboly"]
      min: 2
    truth:
      family: "구획 감압"
      answer: "응급 근막절개술"
      patterns: ["근막\\\\s*절개", "fasciotomy"]
    why: "맥박 약화는 늦은 징후다 [[src-a]]"
    discriminators:
      - "통증이 진통제에 듣지 않는다 [[src-a]]"
      - "갑자기 차가워지면 동맥 폐색 [[src-b: p.1]]"
    mirror:
      when: "심방세동 환자의 갑작스러운 냉감 [[src-b]]"
      answer: "헤파린 정주 후 색전제거술"
    want: {trap: 1, mirror: 1}
    sources:
      - {id: src-a, org: "Journal A", title: "Review A", year: 2010, checked_at: 2026-09-29, checked: "본문", verified: text, url: "https://example.org/a"}
      - {id: src-b, org: "Textbook B", title: "Book B", year: 2022, checked_at: 2026-09-29, checked: "쪽", verified: text, kind: textbook, citation: "B 21e p.1"}
    review_status: unreviewed
    """)

TRAP_Q = {
    "id": "kmle-2026-9001", "type": "kmle", "topic": "Orthopedics", "date": "2026-09-29",
    "stem": "30세 남자가 경골 골절 뒤 종아리가 붓고 아프다. 발등동맥 맥박이 약하게 만져진다. 처치는?",
    "choices": ["A. 헤파린 정주", "B. 응급 근막절개술", "C. 카테터 혈전용해", "D. 경과 관찰", "E. 진통제 증량"],
    "answer": "B",
    "design": {"rival": "A", "trap": {"id": "tr.test.weak-pulse-thrombotic", "side": "trap"}},
    "distractors": {"A": {"tempting": "t", "answer_first": "a", "discriminator": "d", "when_right": "심방세동 환자의 갑작스러운 냉감"}},
}
MIRROR_Q = {
    "id": "kmle-2026-9002", "type": "kmle", "topic": "Orthopedics", "date": "2026-09-29",
    "stem": "70세 남자가 1시간 전 갑자기 다리가 차가워졌다. 발등동맥 맥박이 약하다. 처치는?",
    "choices": ["A. 응급 근막절개술", "B. 헤파린 정주 후 색전제거술", "C. 경과 관찰", "D. 진통제 증량", "E. 부목 고정"],
    "answer": "B",
    "design": {"rival": "A", "trap": {"id": "tr.test.weak-pulse-thrombotic", "side": "mirror"}},
}


def _codes(fs):
    return [c for _, c, _ in fs]


class RegistryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, text: str, name: str = "tr.test.weak-pulse-thrombotic.yaml"):
        (self.root / name).write_text(text, encoding="utf-8")

    def load(self):
        return traps.load_registry(self.root)

    def test_valid_entry_loads(self):
        self.write(ENTRY)
        ok, errs, _ = self.load()
        self.assertEqual(errs, {})
        e = ok["tr.test.weak-pulse-thrombotic"]
        self.assertEqual(e["want"], {"trap": 1, "mirror": 1})
        self.assertEqual(e["found"], "2026-09-29")          # YAML 날짜도 문자열로

    def test_filename_must_match_id(self):
        self.write(ENTRY, "tr.test.other.yaml")
        ok, errs, _ = self.load()
        self.assertFalse(ok)
        self.assertTrue(any("파일 이름" in x for x in errs["tr.test.other.yaml"]))

    def test_bad_regex_and_missing_sources(self):
        bad = ENTRY.replace('["맥박[^.]{0,10}약하", "weak[^.]{0,20}pulse"]', '["맥박(약"]')
        bad = bad[:bad.index("sources:")] + "review_status: unreviewed\n"
        self.write(bad)
        _, errs, _ = self.load()
        msgs = " ".join(next(iter(errs.values())))
        self.assertIn("정규식 오류", msgs)
        self.assertIn("sources 가 비어 있다", msgs)
        self.assertIn("[[src-a]]", msgs)                      # 없는 출처 인용도 잡는다

    def test_patterns_must_agree_with_answers(self):
        bad = ENTRY.replace('answer: "헤파린 정주 후 색전제거술"', 'answer: "경과 관찰"')
        self.write(bad)
        _, errs, _ = self.load()
        self.assertTrue(any("mirror.answer 가 lure.patterns" in x for x in next(iter(errs.values()))))
        bad2 = ENTRY.replace('answer: "응급 근막절개술"', 'answer: "헤파린"')
        self.write(bad2)
        _, errs2, _ = self.load()
        msgs = " ".join(next(iter(errs2.values())))
        self.assertIn("truth.answer 가 truth.patterns", msgs)
        self.assertIn("lure.patterns 에도 걸린다", msgs)

    def test_mirror_optional_when_not_wanted(self):
        no_mirror = ENTRY.replace("want: {trap: 1, mirror: 1}", "want: {trap: 1, mirror: 0}")
        no_mirror = no_mirror.replace('  when: "심방세동 환자의 갑작스러운 냉감 [[src-b]]"\n', "")
        no_mirror = no_mirror.replace('  answer: "헤파린 정주 후 색전제거술"\n', "").replace("mirror:\n", "")
        self.write(no_mirror)
        ok, errs, _ = self.load()
        self.assertEqual(errs, {})
        self.assertEqual(ok["tr.test.weak-pulse-thrombotic"]["want"]["mirror"], 0)

    def test_model_cannot_mark_reviewed(self):
        self.write(ENTRY.replace("review_status: unreviewed",
                                 "review_status: reviewed\nreviewed_by: Claude\nreview_note: ok"))
        _, errs, _ = self.load()
        self.assertTrue(any("모델" in x for x in next(iter(errs.values()))))


class QuestionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        (root / "tr.test.weak-pulse-thrombotic.yaml").write_text(ENTRY, encoding="utf-8")
        ok, errs, _ = traps.load_registry(root)
        assert not errs, errs
        cls.reg = (ok, {"tr.test.broken"})

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def check(self, q):
        return traps.question_findings(q, q["type"], self.reg)

    def test_untagged_question_is_ignored(self):
        q = copy.deepcopy(TRAP_Q)
        del q["design"]["trap"]
        self.assertEqual(self.check(q), [])

    def test_good_trap_side(self):
        self.assertEqual([f for f in self.check(TRAP_Q) if f[0] == "ERROR"], [])
        self.assertEqual(self.check(TRAP_Q), [])

    def test_trap_needs_cue_truth_answer_and_lures(self):
        q = copy.deepcopy(TRAP_Q)
        q["stem"] = q["stem"].replace("맥박이 약하게 만져진다", "맥박은 만져진다")
        self.assertIn("trap-cue-missing", _codes(self.check(q)))
        q = copy.deepcopy(TRAP_Q)
        q["answer"] = "A"
        self.assertIn("trap-answer-is-lure", _codes(self.check(q)))
        q = copy.deepcopy(TRAP_Q)
        q["answer"] = "D"
        self.assertIn("trap-answer-not-truth", _codes(self.check(q)))
        q = copy.deepcopy(TRAP_Q)
        q["choices"][2] = "C. 다리 거상"
        self.assertIn("trap-lure-few", _codes(self.check(q)))

    def test_trap_rival_and_when_right_are_warnings(self):
        q = copy.deepcopy(TRAP_Q)
        q["design"]["rival"] = "D"
        fs = self.check(q)
        self.assertIn(("WARN", "trap-rival-not-lure"), [(l, c) for l, c, _ in fs])
        q = copy.deepcopy(TRAP_Q)
        q["distractors"]["A"]["when_right"] = ""
        self.assertIn("trap-when-right", _codes(self.check(q)))

    def test_mirror_side(self):
        self.assertEqual(self.check(MIRROR_Q), [])
        q = copy.deepcopy(MIRROR_Q)
        q["answer"] = "A"
        self.assertIn("mirror-answer-is-truth", _codes(self.check(q)))
        q = copy.deepcopy(MIRROR_Q)
        q["choices"][0] = "A. CT 촬영"
        q["design"]["rival"] = "C"
        codes = _codes(self.check(q))
        self.assertIn("mirror-no-truth-option", codes)
        self.assertIn("mirror-rival-not-truth", codes)

    def test_unknown_invalid_side_and_shorthand(self):
        q = copy.deepcopy(TRAP_Q)
        q["design"]["trap"] = {"id": "tr.test.none", "side": "trap"}
        self.assertEqual(_codes(self.check(q)), ["trap-unknown"])
        q["design"]["trap"] = {"id": "tr.test.broken", "side": "trap"}
        self.assertEqual(_codes(self.check(q)), ["trap-invalid"])
        q["design"]["trap"] = {"id": "tr.test.weak-pulse-thrombotic", "side": "both"}
        self.assertEqual(_codes(self.check(q)), ["trap-side"])
        q["design"]["trap"] = "tr.test.weak-pulse-thrombotic"          # 문자열 = trap 쪽
        self.assertEqual(self.check(q), [])
        q["design"]["trap"] = ["x"]
        self.assertEqual(_codes(self.check(q)), ["trap-type"])

    def test_exam_not_registered_is_warning(self):
        q = copy.deepcopy(TRAP_Q)
        q["type"] = "imaging"
        self.assertIn(("WARN", "trap-exam"), [(l, c) for l, c, _ in self.check(q)])


class QueueTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "tr.test.weak-pulse-thrombotic.yaml").write_text(ENTRY, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def queue(self, questions, exam=None):
        ok, errs, _ = traps.load_registry(self.root)
        self.assertEqual(errs, {})
        return ok, traps.coverage(ok, questions), traps.build_queue(ok, traps.coverage(ok, questions), exam)

    def test_tagged_question_fills_its_side_only(self):
        _, cov, items = self.queue({"kmle-2026-9001": TRAP_Q})
        self.assertEqual(cov["tr.test.weak-pulse-thrombotic"]["tagged"]["kmle"]["trap"], ["kmle-2026-9001"])
        got = {(i["exam"], i["side"]) for i in items}
        self.assertEqual(got, {("kmle", "mirror"), ("usmle", "trap"), ("usmle", "mirror")})
        self.assertEqual({(i["exam"], i["side"]) for i in self.queue({"kmle-2026-9001": TRAP_Q}, "kmle")[2]},
                         {("kmle", "mirror")})

    def test_trap_side_comes_first_and_newer_first(self):
        newer = ENTRY.replace("tr.test.weak-pulse-thrombotic", "tr.test.newer").replace("found: 2026-09-29", "found: 2026-10-01")
        (self.root / "tr.test.newer.yaml").write_text(newer, encoding="utf-8")
        _, _, items = self.queue({}, "kmle")
        self.assertEqual([(i["trap"], i["side"]) for i in items],
                         [("tr.test.newer", "trap"), ("tr.test.weak-pulse-thrombotic", "trap"),
                          ("tr.test.newer", "mirror"), ("tr.test.weak-pulse-thrombotic", "mirror")])

    def test_retired_and_want_override(self):
        (self.root / "tr.test.weak-pulse-thrombotic.yaml").write_text(
            ENTRY.replace("status: active", "status: retired"), encoding="utf-8")
        self.assertEqual(self.queue({})[2], [])
        (self.root / "tr.test.weak-pulse-thrombotic.yaml").write_text(
            ENTRY.replace("want: {trap: 1, mirror: 1}", "want: {trap: 2, mirror: 0}"), encoding="utf-8")
        items = self.queue({"kmle-2026-9001": TRAP_Q}, "kmle")[2]
        self.assertEqual([(i["side"], i["need"]) for i in items], [("trap", 1)])

    def test_untagged_candidates_stay_inside_topics(self):
        cand = copy.deepcopy(MIRROR_Q)
        del cand["design"]
        other = copy.deepcopy(MIRROR_Q)
        del other["design"]
        other["topic"] = "Pulmonology"                 # 범위 밖(예: 쇼크의 약한 맥박 + 혈전용해) — 후보로 세지 않는다
        _, cov, items = self.queue({"kmle-2026-9002": cand, "kmle-2026-9003": other}, "kmle")
        self.assertEqual(cov["tr.test.weak-pulse-thrombotic"]["candidates"]["kmle"]["mirror"], [("kmle-2026-9002", False)])
        mirror = next(i for i in items if i["side"] == "mirror")
        self.assertEqual(mirror["candidates"], ["kmle-2026-9002"])
        self.assertEqual(mirror["taggable"], [])       # design 이 없으면 표시만 붙일 수 없다


class SimilarTest(unittest.TestCase):
    def test_split_external_choices(self):
        stem, ch = traps.split_external("22세 남자가 다리가 아프다. 치료는?\n○ 1) 근막절개\n○ 2) 혈관풍선확장술\n○ 3) 저분자량헤파린\n4) 혈전용해제")
        self.assertEqual(ch, ["근막절개", "혈관풍선확장술", "저분자량헤파린", "혈전용해제"])
        self.assertIn("치료는?", stem)
        self.assertEqual(traps.split_external("보기 없는 글")[1], [])

    def test_closest_question_first(self):
        qs = {"kmle-2026-9001": TRAP_Q, "kmle-2026-9002": MIRROR_Q,
              "kmle-2026-9004": {"stem": "소아의 열성경련 뒤 검사는?", "choices": ["A. 요추천자", "B. 뇌파"]}}
        top = traps.similar("경골 골절 뒤 종아리가 붓고 발등동맥 맥박이 약하다", qs, top=3)
        self.assertEqual(top[0][1], "kmle-2026-9001")
        self.assertNotIn("kmle-2026-9004", [q for _, q in top[:2]])

    def test_answer_arg(self):
        self.assertEqual(traps._answer_arg("3", 5), 2)
        self.assertEqual(traps._answer_arg("c", 5), 2)
        self.assertEqual(traps._answer_arg("③", 5), 2)
        self.assertEqual(traps._answer_arg("9", 5), -1)
        self.assertEqual(traps._answer_arg(None, 5), -1)


class LintIntegrationTest(unittest.TestCase):
    def test_linter_reports_trap_findings(self):
        from frontmatter import Doc
        import lint_questions as lq
        tmp = tempfile.TemporaryDirectory()
        try:
            root = Path(tmp.name)
            (root / "tr.test.weak-pulse-thrombotic.yaml").write_text(ENTRY, encoding="utf-8")
            ok, _, _ = traps.load_registry(root)
            saved = dict(traps._CACHE)
            traps._CACHE[str(traps.TRAP_DIR)] = (ok, set())
            try:
                meta = {k: v for k, v in copy.deepcopy(TRAP_Q).items() if k != "distractors"}
                meta["stem"] = meta["stem"].replace("맥박이 약하게 만져진다", "맥박은 만져진다")
                codes = [f.code for f in lq.lint_doc(Doc(path=Path("x.md"), meta=meta, body=""))]
            finally:
                traps._CACHE.clear()
                traps._CACHE.update(saved)
            self.assertIn("trap-cue-missing", codes)
        finally:
            tmp.cleanup()


if __name__ == "__main__":
    unittest.main(verbosity=1)
