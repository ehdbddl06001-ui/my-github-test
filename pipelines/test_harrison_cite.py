"""
test_harrison_cite.py — 문항 해리슨 인용 검사(harrison_cite.py) 회귀 테스트.

22판 표(`content/outline/harrison22.json`)는 커밋된 고정 자료라 그대로 읽는다(test_learning_books 도 같은 표를 본다).

지키는 것:
  - 21판 인용 = ERROR(번호·제목으로 22판 장을 제안) · 22판에 없는 21판 장(7·417·484)은 허용
  - 22판 인용: 표에 없는 장 번호 · 21판 번호를 쓴 제목 불일치 = ERROR / 장 번호 없음 · 판 없음 = WARN
  - 정리본식 `22e. 247장 p.1872` 의 쪽 표기를 제목으로 읽지 않는다
  - 찾기: 단어 AND · 대문자 약어(ARDS)
  - 린터가 기준일 이후 문항에만 harrison-* 를 낸다

실행: python pipelines/test_harrison_cite.py
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import harrison_cite as hc  # noqa: E402


def codes(text: str) -> list[tuple[str, str]]:
    return [(lv, code) for lv, code, _ in hc.check_text(text)]


class CheckText(unittest.TestCase):
    def test_21e_is_error_with_22e_suggestion(self):
        fs = hc.check_text("Loscalzo J, et al. Harrison's Principles of Internal Medicine, 21st ed. McGraw-Hill; 2022. "
                           "Chapter 301: Acute Respiratory Distress Syndrome")
        self.assertEqual([(lv, c) for lv, c, _ in fs], [("ERROR", "harrison-21e")])
        self.assertIn("312장 Acute Respiratory Distress Syndrome", fs[0][2])

    def test_21e_title_only_suggests_by_title(self):
        fs = hc.check_text("- **출처**: X 지침 / Harrison's Principles of Internal Medicine 21e(Peripheral Neuropathy — 척골).")
        self.assertEqual(fs[0][1], "harrison-21e")
        self.assertIn("457장 Peripheral Neuropathy", fs[0][2])

    def test_21e_gone_chapter_allowed(self):
        self.assertEqual(codes("Harrison's Principles of Internal Medicine, 21st ed. Chapter 417"), [])

    def test_22e_good_forms_pass(self):
        for t in ("Harrison's Principles of Internal Medicine, 22e. 312장 Acute Respiratory Distress Syndrome",
                  "Harrison's Principles of Internal Medicine, 22e. 247장 p.1872–1874",
                  "Loscalzo J, Fauci AS, Kasper DL, et al., eds. Harrison's Principles of Internal Medicine, 22nd ed. "
                  "McGraw Hill; 2025. Chapter 312: Acute Respiratory Distress Syndrome",
                  "해리슨 / Harrison's Principles of Internal Medicine, 22e. 120장 Disorders of Platelets and Vessel Wall p.923"):
            self.assertEqual(codes(t), [], t)

    def test_22e_with_21e_number_is_error(self):
        fs = hc.check_text("Harrison's Principles of Internal Medicine, 22nd ed. Chapter 301: Acute Respiratory Distress Syndrome")
        self.assertEqual([(lv, c) for lv, c, _ in fs], [("ERROR", "harrison-chapter")])
        self.assertIn("312", fs[0][2])

    def test_22e_unknown_chapter_is_error(self):
        self.assertEqual(codes("Harrison's Principles of Internal Medicine, 22e. 999장 Nothing"), [("ERROR", "harrison-chapter")])

    def test_missing_chapter_or_edition_is_warn(self):
        self.assertEqual(codes("Harrison's Principles of Internal Medicine, 22e(Peripheral Neuropathy)"),
                         [("WARN", "harrison-no-chapter")])
        self.assertEqual(codes("2023 ESC 지침, Harrison's"), [("WARN", "harrison-edition")])

    def test_two_citations_separated(self):
        t = ("Harrison's Principles of Internal Medicine, 21e(Peripheral Neuropathy) / "
             "Harrison's Principles of Internal Medicine, 22e. 312장 Acute Respiratory Distress Syndrome")
        self.assertEqual(codes(t), [("ERROR", "harrison-21e")])


class Find(unittest.TestCase):
    def test_words_and_acronym(self):
        self.assertIn(312, [n for n, _ in hc.find("respiratory distress")])
        self.assertIn(312, [n for n, _ in hc.find("ARDS")])
        self.assertEqual(hc.find("zzzz nothing"), [])


class LinterHook(unittest.TestCase):
    def _doc(self, date: str):
        from frontmatter import Doc
        meta = {"id": "kmle-2026-9999", "type": "kmle", "date": date, "stem": "x", "choices": [], "answer": "A"}
        body = "## 정답 및 해설\n- **출처**: Harrison's Principles of Internal Medicine 21e(Peripheral Neuropathy).\n"
        return Doc(path=Path("x.md"), meta=meta, body=body)

    def test_only_new_items(self):
        import lint_questions as lq
        new = [f.code for f in lq.lint_doc(self._doc(hc.HARRISON22_FROM))]
        old = [f.code for f in lq.lint_doc(self._doc("2026-11-01"))]
        self.assertIn("harrison-21e", new)
        self.assertNotIn("harrison-21e", old)


if __name__ == "__main__":
    unittest.main()
