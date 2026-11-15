"""test_related.py — 정리본 ↔ 스크랩 논문 연결(export_related_web.py) 회귀 시험(2026-11-15).

지키는 것: 연결은 **글자가 겹친다는 사실**로만 하고, 틀린 연결을 내느니 안 잇는다.
  ① 제목에 질환 이름이 있으면 잇는다. 초록만이면 여러 번 나와야 한다(한 낱말 용어는 3번).
  ② 약어는 제목에서만, 그 정리본의 긴 용어가 글에 함께 나올 때만(AMR = 항체매개 거부 / 항균제 내성).
  ③ 제목 끝의 발행 기관 이름은 주제가 아니다(「… from the Committee on Rheumatic Fever, Endocarditis, and Kawasaki Disease」).
  ④ 화면이 읽는 묶음의 모양(concepts · papers · titles)과 앱의 연결 지점.

    python pipelines/test_related.py
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipelines"))

import export_related_web as rel  # noqa: E402

DOCS = ROOT / "docs"


class Terms(unittest.TestCase):
    def test_terms_come_from_the_id_and_the_parenthesised_english(self):
        t = rel.concept_terms("cn.cardio.atrial-fibrillation.doac-nonvalvular-anticoagulation", {"condition": "심방세동(atrial fibrillation, AF)"})
        self.assertEqual(t, ["atrial fibrillation"])                 # 두 글자 약어 AF 는 버린다
        t = rel.concept_terms("cn.cardio.cardiac-mri-lge.pattern-etiology",
                              {"condition": "심장 자기공명영상(cardiac magnetic resonance, CMR)의 지연 조영증강(late gadolinium enhancement, LGE)"})
        self.assertIn("CMR", t)
        self.assertIn("late gadolinium enhancement", t)
        self.assertEqual(rel.concept_terms("cn.cardio.edema.generalized-cause", {"condition": "전신 부종(generalized edema)"}), ["generalized edema"])   # 흔한 한 낱말은 안 쓴다

    def test_title_match_links_and_abstract_needs_repeats(self):
        terms = ["atrial fibrillation"]
        self.assertEqual(rel.match(terms, "Postoperative Atrial Fibrillation after CABG", ""), ("t", "atrial fibrillation"))
        self.assertIsNone(rel.match(terms, "Heart failure outcomes", "One patient had atrial fibrillation."))
        self.assertEqual(rel.match(terms, "Heart failure outcomes", "Atrial fibrillation was common. Atrial-fibrillation burden rose."), ("a", "atrial fibrillation"))
        self.assertIsNone(rel.match(["gout"], "Uric acid", "gout and gout"))                    # 한 낱말은 3번
        self.assertEqual(rel.match(["gout"], "Uric acid", "gout, gout, and gout")[0], "a")
        self.assertIsNone(rel.match(["gout"], "Gouty tophi? No: goutweed extract", ""))        # 낱말 경계

    def test_abbreviation_needs_the_long_form_and_the_title(self):
        terms = ["antibody mediated rejection", "AMR"]
        self.assertIsNone(rel.match(terms, "AMR surveillance in Salmonella", "Antimicrobial resistance (AMR) is rising. AMR genes. AMR."))
        self.assertEqual(rel.match(terms, "AMR after kidney transplant", "Antibody-mediated rejection remains ..."), ("t", "AMR"))
        self.assertIsNone(rel.match(["cardiac magnetic resonance", "CMR"], "Outcomes", "CMR CMR CMR"))   # 초록의 약어는 세지 않는다

    def test_publisher_names_at_the_end_of_a_title_are_not_the_topic(self):
        title = ("Infective endocarditis: diagnosis, antimicrobial therapy, and management of complications: a statement for healthcare "
                 "professionals from the Committee on Rheumatic Fever, Endocarditis, and Kawasaki Disease")
        self.assertIsNone(rel.match(["rheumatic fever"], title, ""))
        self.assertIsNone(rel.match(["kawasaki"], title, ""))
        self.assertEqual(rel.match(["infective endocarditis"], title, "")[0], "t")


class Bundle(unittest.TestCase):
    def test_bundle_shape_and_limits(self):
        concepts = {"cn.x.gout.a": {"condition": "통풍(gout)", "title": "통풍 — 가"}, "cn.x.arrhythmia-mechanism.b": {"condition": "기전", "title": "나"}}
        papers = [{"id": f"paper-{i}", "title": "Gout flare trial %d" % i, "abstract": "", "journal": "J", "pubdate": "2026-01-%02d" % (i + 1)} for i in range(12)]
        papers.append({"id": "paper-z", "title": "Hyperuricemia", "abstract": "gout gout gout", "journal": "J", "pubdate": "2026-12-01"})
        d = rel.build(concepts, papers)
        rows = d["concepts"]["cn.x.gout.a"]
        self.assertEqual(len(rows), rel.MAX_PER_CONCEPT)
        self.assertTrue(all(r["how"] == "t" for r in rows))          # 제목 일치가 초록 일치보다 먼저
        self.assertEqual(rows[0]["id"], "paper-11")                  # 그 안에서는 최신순
        self.assertNotIn("cn.x.arrhythmia-mechanism.b", d["concepts"])
        self.assertEqual(set(d["papers"]), {r["id"] for r in rows})  # 연결된 논문만 싣는다
        self.assertEqual(d["papers"]["paper-11"]["c"], ["cn.x.gout.a"])
        self.assertEqual(d["titles"], {"cn.x.gout.a": "통풍 — 가"})


class Wiring(unittest.TestCase):
    def test_app_shows_related_papers_and_papers_show_related_notes(self):
        learn = (DOCS / "learn.js").read_text(encoding="utf-8")
        papers = (DOCS / "papers-app.js").read_text(encoding="utf-8")
        self.assertIn("selfHtml(c) + papersHtml(c) + sourcesHtml(c)", learn)
        self.assertIn("내용을 검토한 추천은 아닙니다", learn)                 # 글자 겹침일 뿐임을 화면에 적는다
        self.assertIn('href="papers.html?id=', learn)
        self.assertIn("if (ONLY) return p.id === ONLY;", papers)
        self.assertIn('href="index.html?concept=', papers)
        self.assertIn('<script src="related.js"></script>', (DOCS / "index.html").read_text(encoding="utf-8"))
        self.assertIn('<script src="related.js"></script>', (DOCS / "papers.html").read_text(encoding="utf-8"))
        self.assertIn(r"related\.js", (DOCS / "sw.js").read_text(encoding="utf-8"))
        self.assertIn('"export_related_web.py"', (ROOT / "pipelines" / "publish.py").read_text(encoding="utf-8"))   # 루틴이 매일 다시 만든다
        self.assertTrue((DOCS / "related.js").exists())


if __name__ == "__main__":
    unittest.main(verbosity=1)
