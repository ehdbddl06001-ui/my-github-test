"""실제 콘텐츠(정리본·문항) 계약 검사 — 코드 회귀 테스트(test_learning_books.py)와 따로 돈다.

2026-09-25 분리: 매일 학습서 워크플로가 이 검사까지 「시험」 단계에 넣어 두어서, 루틴이 새로 쓴 정리본 하나
(읽을 크기로 안 들어가는 도식·DOI 만 있는 출처)가 **모든 책의 PDF 를 멈췄다**(09-23·09-24 실패 메일).
지금은 코드 시험만 관문이고, 이 검사는 books.yml 에서 따로 돌아 실패해도 다른 책은 만들어 올린 뒤
작업을 실패로 끝내 알린다. 콘텐츠를 쓰는 쪽(루틴)은 커밋 전에 `python pipelines/concepts.py` 로 같은 것을 막는다.

python pipelines/test_content.py
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_books as bb
import concepts as C


class LiveContent(unittest.TestCase):
    def test_concepts_and_linked_questions_valid(self):
        concepts, errs = C.load_concepts()
        # [WARN](해리슨 대조 없음 등)은 클라우드 루틴이 드라이브를 못 읽을 때 정상적으로 남는다 — ERROR 만 막는다
        self.assertEqual([e for e in errs if "[WARN]" not in e], [])
        qs = C.load_questions()
        for qid, m in qs.items():
            if m.get("objective"):
                problems = [x for x in C.question_learning_errors(m, concepts.get(m["objective"])) if x[0] == "ERROR"]
                self.assertEqual(problems, [], qid)

    def test_real_diagrams_fit_readably(self):
        concepts, _ = C.load_concepts()
        bad = []
        for c in concepts.values():
            if c.get("diagram"):
                fit = bb.fit_diagram(c["diagram"])
                if not fit["ok"]:
                    bad.append(f'{c["id"]} (배율 {fit["scale"]})')
        self.assertEqual(bad, [], "도식이 읽을 크기로 한 쪽에 들어가지 않는다 — 노드 글을 줄이거나 의미 단위로 나눈다")


if __name__ == "__main__":
    unittest.main(verbosity=1)
