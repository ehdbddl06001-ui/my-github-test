"""english_terms — 확인된 약 이름만 english(한글), 원고의 한글(English) 순서 뒤집기(2026-09-27)."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml

import english_terms as et

T = {"히드록시클로로퀸": "hydroxychloroquine", "딜티아젬": "diltiazem", "베라파밀": "verapamil",
     "칼슘통로차단제": "calcium channel blocker", "사이클로스포린": "cyclosporine"}


class EnglishFirst(unittest.TestCase):
    def f(self, s, seen=None):
        return et.text(s, set() if seen is None else seen, T)

    def test_first_mention_then_english_only(self):
        seen = set()
        self.assertEqual(self.f("경증은 히드록시클로로퀸으로 시작한다", seen), "경증은 hydroxychloroquine(히드록시클로로퀸)으로 시작한다")
        self.assertEqual(self.f("히드록시클로로퀸을 유지", seen), "hydroxychloroquine을 유지")

    def test_parentheses_do_not_nest(self):
        self.assertEqual(self.f("칼슘통로차단제(딜티아젬·베라파밀)를"),
                         "calcium channel blocker(칼슘통로차단제; diltiazem 딜티아젬·verapamil 베라파밀)를")
        self.assertEqual(self.f("(+필요 시 딜티아젬 추가)"), "(+필요 시 diltiazem 딜티아젬 추가)")
        self.assertEqual(self.f("사이클로스포린(cyclosporine) 대신"), "cyclosporine(사이클로스포린) 대신")

    def test_existing_pairs_swap_only_when_safe(self):
        self.assertEqual(self.f("환자는 급성호흡곤란증후군(ARDS)에서"), "환자는 ARDS(급성호흡곤란증후군)에서")
        for keep in ("세균성 혈관종증(bacillary angiomatosis)", "기준(TG18)", "세침으로 전이가 확인되면(cN1)"):
            self.assertEqual(self.f(keep), keep)

    def test_concept_keeps_ids_and_sources(self):
        c = {"id": "cn.x.히드록시클로로퀸", "title": "히드록시클로로퀸", "sources": [{"title": "히드록시클로로퀸"}],
             "summary": ["히드록시클로로퀸 유지"]}
        old = et.TERM, et._TERM_RE
        et.TERM, et._TERM_RE = T, et._term_re(T)
        try:
            out = et.concept(c)
        finally:
            et.TERM, et._TERM_RE = old
        self.assertEqual(out["title"], "hydroxychloroquine(히드록시클로로퀸)")
        self.assertEqual(out["summary"], ["hydroxychloroquine 유지"])            # 단원 안 두 번째부터 영어만
        self.assertEqual(out["id"], c["id"])
        self.assertEqual(out["sources"], c["sources"])
        self.assertEqual(c["title"], "히드록시클로로퀸")                           # 원본은 그대로

    def test_verified_file_matches_glossary(self):
        d = Path(et.VERIFIED).parent
        g = yaml.safe_load((d / "drugs_ko_en.yaml").read_text(encoding="utf-8"))
        v = json.loads((d / "verified.json").read_text(encoding="utf-8"))
        for ko, x in v["drugs"].items():
            self.assertEqual(g["drugs"][ko], x["en"], ko)                     # 확인 뒤 표를 바꾸면 다시 확인해야 한다
            self.assertTrue(x["rxcui"])
        for ko, x in v["classes"].items():
            self.assertEqual(g["classes"][ko]["en"], x["en"], ko)
            self.assertTrue(x["mesh"].startswith("D"))


if __name__ == "__main__":
    unittest.main()
