"""오답 뒤 학습 흐름 · 개념 정리본 · 판단 도식 · 과별 PDF 학습서 · 드라이브 갱신 회귀 테스트.

python pipelines/test_learning_books.py            (PDF 렌더링 시험은 playwright 가 있을 때만)
완료 조건(2026-09-18 사용자 지시)을 하나씩 테스트로 둔다:
  새 개념 → 새 단원 / 같은 개념 반복 → 단원 중복 없음 / 같은 질환 다른 목표 → 따로 / 메모·기록 보존 /
  바뀐 것 없음 → 건너뜀 / 실패 → 최신본 유지 / 출처 변경 → 검토 표시 / 한글 검색·차례 링크 / 필기본 보호
"""
from __future__ import annotations

import copy
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import book_layout as bl
import build_books as bb
import check_sources as cs
import concepts as C
import decision_diagram as dd
import drive_books as db
import learning_log as ll
import outline as ol
import harrison_toc as ht
import concept_queue as cq

ROOT = Path(__file__).resolve().parent.parent

SPEC = {
    "title": "t",
    "nodes": [
        {"id": "s", "kind": "start", "text": "시작"},
        {"id": "d", "kind": "decision", "text": "판단?"},
        {"id": "i", "kind": "info", "text": "추가 정보"},
        {"id": "a", "kind": "end", "text": "결론 A"},
        {"id": "b", "kind": "end", "text": "결론 B"},
    ],
    "edges": [
        {"from": "s", "to": "d"},
        {"from": "d", "to": "a", "label": "예"},
        {"from": "d", "to": "i", "label": "정보 없음"},
        {"from": "d", "to": "b", "label": "아니오"},
        {"from": "i", "to": "a", "label": "해당"},
    ],
}


# 층을 건너뛰는 선이 여럿인 도식(2026-09-25 고칼륨혈증 도식 모양) — 옛 배치는 오른쪽 통로로 돌아 선이 겹쳤다
SKIP = {
    "title": "skip",
    "nodes": [
        {"id": "s", "kind": "start", "text": "시작"},
        {"id": "d", "kind": "decision", "text": "심전도 변화가 있는가?"},
        {"id": "i", "kind": "info", "text": "심전도를 판독한다"},
        {"id": "ca", "kind": "step", "text": "칼슘"},
        {"id": "k", "kind": "decision", "text": "칼륨 수치는?"},
        {"id": "sh", "kind": "step", "text": "세포 안으로"},
        {"id": "rm", "kind": "step", "text": "몸 밖으로"},
        {"id": "e", "kind": "end", "text": "재측정"},
    ],
    "edges": [
        {"from": "s", "to": "d"},
        {"from": "d", "to": "ca", "label": "P 소실·넓은 QRS·부정맥 등"},
        {"from": "d", "to": "i", "label": "판독 전"},
        {"from": "d", "to": "k", "label": "없음·뾰족한 T만"},
        {"from": "i", "to": "ca", "label": "변화 있음"},
        {"from": "i", "to": "k", "label": "변화 없음"},
        {"from": "ca", "to": "sh"},
        {"from": "k", "to": "sh", "label": "≥6.0"},
        {"from": "k", "to": "e", "label": "5.5–5.9"},
        {"from": "sh", "to": "rm"},
        {"from": "rm", "to": "e"},
    ],
}
TALL = {
 "title": "급성 흉통에서 박리 의심 — 첫 약물에서 확정 치료까지",
 "nodes": [
  {
   "id": "start",
   "kind": "start",
   "text": "갑작스러운 심한 흉·배부 통증 → 활력징후·양팔 혈압·맥박·잡음·신경학 진찰, 심전도"
  },
  {
   "id": "suspect",
   "kind": "decision",
   "text": "박리 단서(이동성 찢어지는 통증·맥박/혈압 비대칭·새 이완기 잡음·신경 결손)가 있는가?"
  },
  {
   "id": "acs",
   "kind": "end",
   "text": "박리 단서 없음 + 허혈 심전도 — 급성 관동맥증후군 경로(재관류)"
  },
  {
   "id": "hypo",
   "kind": "decision",
   "text": "저혈압·쇼크(심낭압전·파열·심한 대동맥판 역류)가 있는가?"
  },
  {
   "id": "shock",
   "kind": "alert",
   "text": "소생 + 응급 수술 — 혈압을 낮추는 약물 조절은 하지 않는다"
  },
  {
   "id": "bb",
   "kind": "step",
   "text": "정맥 베타차단제 먼저(심박 약 60회/분) + 통증 조절 · 중환자실 감시"
  },
  {
   "id": "vd",
   "kind": "step",
   "text": "수축기 >120 mmHg 가 남으면 니트로프루시드 추가(단독 투여 금지)"
  },
  {
   "id": "info",
   "kind": "info",
   "text": "영상으로 확인·분류 — CT 혈관조영(안정 시) 또는 경식도 심초음파(불안정 시)"
  },
  {
   "id": "type",
   "kind": "decision",
   "text": "상행대동맥을 침범했는가(Stanford A)?"
  },
  {
   "id": "surgery",
   "kind": "end",
   "text": "A형 — 응급·긴급 수술(인조혈관 치환, 필요 시 판막 처치)"
  },
  {
   "id": "comp",
   "kind": "decision",
   "text": "B형 — 합병증(진행·분지 폐쇄·파열 임박·지속 통증)이 있는가?"
  },
  {
   "id": "tevar",
   "kind": "end",
   "text": "합병증 있는 B형 — 혈관내 스텐트그라프트(불가하면 수술)"
  },
  {
   "id": "medical",
   "kind": "end",
   "text": "합병증 없는 B형 — 약물 치료 유지, 6–12개월마다 CT·MRI 추적"
  }
 ],
 "edges": [
  {
   "from": "start",
   "to": "suspect"
  },
  {
   "from": "suspect",
   "to": "acs",
   "label": "없음"
  },
  {
   "from": "suspect",
   "to": "hypo",
   "label": "있음"
  },
  {
   "from": "hypo",
   "to": "shock",
   "label": "저혈압"
  },
  {
   "from": "hypo",
   "to": "bb",
   "label": "정상·고혈압"
  },
  {
   "from": "bb",
   "to": "vd"
  },
  {
   "from": "vd",
   "to": "info"
  },
  {
   "from": "info",
   "to": "type"
  },
  {
   "from": "type",
   "to": "surgery",
   "label": "침범"
  },
  {
   "from": "type",
   "to": "comp",
   "label": "비침범"
  },
  {
   "from": "comp",
   "to": "tevar",
   "label": "있음"
  },
  {
   "from": "comp",
   "to": "medical",
   "label": "없음"
  }
 ]
}


def _segments(g):
    return [(k, a, b) for k, e in enumerate(g["edges"]) for a, b in zip(e["points"], e["points"][1:])]


def _boxes_touch(a, b):
    return a[0] < b[0] + b[2] - 0.5 and b[0] < a[0] + a[2] - 0.5 and a[1] < b[1] + b[3] - 0.5 and b[1] < a[1] + a[3] - 0.5


def ev(eid, kind, t, **kw):
    return {"eid": eid, "kind": kind, "t": t, **kw}


def wrong(eid, qid, obj, t, day, text="오답"):
    return ev(eid, "answer", t, qid=qid, objective=obj, ok=False, day=day, chosenText=text, answerText="정답", mode="deck")


def right(eid, qid, obj, t, day, mode="deck"):
    return ev(eid, "answer", t, qid=qid, objective=obj, ok=True, day=day, mode=mode)


class Sanitize(unittest.TestCase):
    def test_scripts_attributes_links_removed(self):
        out = C.md_to_html('안녕 <script>alert(1)</script><img src=x onerror=alert(1)> <a href="javascript:x">링크</a> **굵게**')
        self.assertNotIn("script", out)
        self.assertNotIn("onerror", out)
        self.assertNotIn("<img", out)
        self.assertNotIn("href", out)
        self.assertIn("<strong>굵게</strong>", out)
        self.assertIn("링크", out)

    def test_safe_url_https_only(self):
        self.assertEqual(C.safe_url("javascript:alert(1)"), "")
        self.assertEqual(C.safe_url("http://x.org"), "")
        self.assertEqual(C.safe_url("https://doi.org/10.1/x"), "https://doi.org/10.1/x")


class Diagram(unittest.TestCase):
    def test_valid_and_layout_keeps_all_nodes(self):
        self.assertEqual(dd.validate(SPEC), [])
        g = dd.layout(SPEC)
        self.assertEqual({n["id"] for n in g["nodes"]}, {n["id"] for n in SPEC["nodes"]})
        self.assertEqual(len(g["edges"]), len(SPEC["edges"]))
        ys = {n["id"]: n["y"] for n in g["nodes"]}
        self.assertLess(ys["s"], ys["d"])                    # 세로: 위에서 아래로
        self.assertLess(ys["d"], ys["i"])

    def test_forced_or_unlabeled_branches_rejected(self):
        bad = copy.deepcopy(SPEC)
        bad["edges"][1]["label"] = ""
        self.assertTrue(any("조건 라벨" in e for e in dd.validate(bad)))
        one = copy.deepcopy(SPEC)
        one["edges"] = [e for e in one["edges"] if not (e["from"] == "d" and e["to"] != "a")]
        self.assertTrue(any("2개 이상" in e for e in dd.validate(one)))

    def test_needs_info_path_and_no_cycle(self):
        noinfo = copy.deepcopy(SPEC)
        noinfo["nodes"][2]["kind"] = "step"
        self.assertTrue(any("추가 정보 필요" in e for e in dd.validate(noinfo)))
        cyc = copy.deepcopy(SPEC)
        cyc["nodes"][2]["kind"] = "info"
        cyc["edges"].append({"from": "i", "to": "d", "label": "다시"})
        self.assertTrue(any("순환" in e for e in dd.validate(cyc)))

    def test_case_path_must_follow_edges(self):
        self.assertEqual(dd.validate_case(SPEC, {"visit": [{"node": "s"}, {"node": "d"}, {"node": "a"}]}), [])
        errs = dd.validate_case(SPEC, {"visit": [{"node": "s"}, {"node": "a"}]})
        self.assertTrue(any("선이 도식에 없다" in e for e in errs))

    def test_skip_edges_do_not_overlap_cross_or_hide_labels(self):
        """사용자 지적(2026-09-25): 선이 겹치고 길게 돌아간다. 겹침 0·교차 0·바깥 통로 없음·라벨이 선·노드를 덮지 않고 글을 자르지 않음."""
        for nw in (196, 260, 330):
            g = dd.layout(SKIP, node_w=nw)
            segs = _segments(g)
            for i in range(len(segs)):
                for j in range(i + 1, len(segs)):
                    (ki, a, b), (kj, c, d) = segs[i], segs[j]
                    if ki == kj:
                        continue
                    ha, hc = a[1] == b[1], c[1] == d[1]
                    if ha and hc and abs(a[1] - c[1]) < 0.5:          # 같은 높이의 가로선이 겹치지 않는다
                        self.assertLessEqual(min(max(a[0], b[0]), max(c[0], d[0])) - max(min(a[0], b[0]), min(c[0], d[0])), 1)
                    if ha != hc:                                      # 가로·세로가 엇갈리지 않는다
                        H, V = ((a, b), (c, d)) if ha else ((c, d), (a, b))
                        x0, x1 = sorted([H[0][0], H[1][0]]); y0, y1 = sorted([V[0][1], V[1][1]])
                        self.assertFalse(x0 < V[0][0] < x1 and y0 < H[0][1] < y1, (nw, g["edges"][ki]["to"], g["edges"][kj]["to"]))
            right = max(n["x"] + n["w"] for n in g["nodes"])
            for k, a, b in segs:                                      # 바깥 통로로 돌지 않는다
                self.assertLessEqual(max(a[0], b[0]), right)
            nodes = [(n["x"], n["y"], n["w"], n["h"]) for n in g["nodes"]]
            for e, se in zip(g["edges"], SKIP["edges"]):
                if not e["label"]:
                    continue
                L = (e["label"]["x"], e["label"]["y"], e["label"]["w"], e["label"]["h"])
                self.assertEqual("".join(e["label"]["lines"]).replace(" ", ""), se["label"].replace(" ", ""))
                self.assertFalse(any(_boxes_touch(L, B) for B in nodes))
                for k, a, b in segs:
                    if g["edges"][k] is e:
                        continue
                    S = (min(a[0], b[0]) - 0.5, min(a[1], b[1]) - 0.5, abs(a[0] - b[0]) + 1, abs(a[1] - b[1]) + 1)
                    self.assertFalse(_boxes_touch(L, S), (e["label"]["lines"], g["edges"][k]["to"]))

    def test_label_sits_right_under_its_decision(self):
        g = dd.layout(SKIP)
        d = next(n for n in g["nodes"] if n["id"] == "d")
        for e in g["edges"]:
            if e["from"] == "d":
                self.assertLess(e["label"]["y"] - (d["y"] + d["h"]), 40)   # 질문 바로 아래에 답(갈래)
                self.assertTrue(e["label"]["x"] <= e["points"][0][0] <= e["label"]["x"] + e["label"]["w"])

    def test_text_and_svg_share_markers_and_escape(self):
        spec = copy.deepcopy(SPEC)
        spec["nodes"][0]["text"] = "<script>x</script>"
        case = {"visit": [{"node": "s", "state": "path"}, {"node": "d", "state": "unknown", "note": "문항에 없음"}]}
        svg = dd.to_svg(dd.layout(spec), dd.overlay(case, {"d": ["②"]}))
        self.assertNotIn("<script>", svg)
        self.assertIn("&lt;script&gt;", svg)
        txt = dd.text_alternative(spec, case, {"d": ["②"]})
        for mark in ("? 문항에 정보 없음", "◆ ② 보기와 갈림"):
            self.assertIn(mark, svg)
            self.assertIn(mark, txt)
        self.assertIn("이 사례: 문항에 없음", txt)


class ConceptContract(unittest.TestCase):
    def test_no_you_dont_know_wording(self):
        m = {"answer": "A", "choices": ["A. a", "B. b"], "distractors": {"B": {
            "tempting": "학습자가 기준을 모른다", "answer_first": "x", "discriminator": "y"}}}
        self.assertTrue(any("모른다" in msg for _, msg in C.question_learning_errors(m, None)))

    def test_cites_tables_pitfalls_contract(self):
        concepts, _ = C.load_concepts()
        c = copy.deepcopy(concepts["cn.neph.hyperkalemia.first-step"])
        c["_body"] = "본문 [[no-such-src: p.1]]"
        self.assertTrue(any("no-such-src" in e for e in C.validate_concept(c)))
        c["_body"] = ""
        c["tables"] = [{"id": "t", "title": "t", "role": "treatment", "span": "column",
                        "columns": list("abcde"), "rows": [list("abcde")]}]
        self.assertTrue(any("4열까지" in e for e in C.validate_concept(c)))
        c["tables"][0]["span"] = "full"
        c["tables"][0]["columns"] = list("abcdefg")
        c["tables"][0]["rows"] = [list("abcdefg")]
        self.assertTrue(any("역할별로 나눈다" in e for e in C.validate_concept(c)))
        c["tables"] = []
        c["pitfalls"] = [{"contrast": "a", "point": "학습자가 기준을 몰라서 골랐다"}]
        self.assertTrue(any("추측" in e for e in C.validate_concept(c)))

    def test_citation_dagger_marks_unverified(self):
        meta = {"sources": [{"id": "a", "verified": "text"}, {"id": "b", "verified": "abstract"}]}
        out = C.render_cites("x [[a: p.3]] y [[b]] z [[?a: 표 2]]", meta, "web")
        self.assertIn("<sup>[1 p.3]</sup>", out)
        self.assertIn("<sup>[2†]</sup>", out)
        self.assertIn("<sup>[1† 표 2]</sup>", out)

    def test_model_cannot_mark_reviewed(self):
        concepts, _ = C.load_concepts()
        c = copy.deepcopy(next(iter(concepts.values())))
        c.update(review_status="reviewed", reviewed_by="Claude + GPT 교차 검토", review_note="동의")
        self.assertTrue(any("모델" in e for e in C.validate_concept(c)))


class LearningStates(unittest.TestCase):
    OBJ = "cn.x.y.z"

    def test_merge_is_append_only_and_idempotent(self):
        base = [wrong("e1", "q1", self.OBJ, "2026-09-18T01:00:00Z", "2026-09-18")]
        new = [ev("e2", "memo", "2026-09-18T02:00:00Z", objective=self.OBJ, text="내 메모"), dict(base[0], chosenText="바꿔치기")]
        merged, n = ll.merge(base, new)
        self.assertEqual(n, 1)
        self.assertEqual(merged[0]["chosenText"], "오답")      # 같은 eid 의 기존 기록은 덮어쓰지 않는다
        again, n2 = ll.merge(merged, new)
        self.assertEqual((again, n2), (merged, 0))

    def test_viewing_is_not_learning_and_immediate_is_not_done(self):
        e = [wrong("e1", "q1", self.OBJ, "2026-09-18T01:00:00Z", "2026-09-18"),
             ev("e2", "view", "2026-09-18T01:01:00Z", objective=self.OBJ, what="note")]
        self.assertEqual(ll.states(e)[self.OBJ].status, "need")
        e.append(right("e3", "cn.x.y.z#v1", self.OBJ, "2026-09-18T01:02:00Z", "2026-09-18", mode="variant"))
        s = ll.states(e)[self.OBJ]
        self.assertEqual(s.status, "doing")
        self.assertFalse(s.applied)

    def test_next_day_other_question_is_done_same_question_is_not(self):
        e = [wrong("e1", "q1", self.OBJ, "2026-09-18T01:00:00Z", "2026-09-18")]
        same = e + [right("e2", "q1", self.OBJ, "2026-09-19T01:00:00Z", "2026-09-19")]
        self.assertNotEqual(ll.states(same)[self.OBJ].status, "done")
        other = e + [right("e3", "q2", self.OBJ, "2026-09-19T01:00:00Z", "2026-09-19")]
        self.assertEqual(ll.states(other)[self.OBJ].status, "done")
        back = other + [wrong("e4", "q3", self.OBJ, "2026-09-20T01:00:00Z", "2026-09-20")]
        s = ll.states(back)[self.OBJ]
        self.assertEqual(s.status, "need")                     # 다시 틀리면 되돌아간다
        self.assertEqual(s.wrongs, 2)

    def test_priority_rises_with_repeats_and_failed_followups(self):
        one = [wrong("e1", "q1", self.OBJ, "2026-09-18T01:00:00Z", "2026-09-18")]
        more = one + [wrong("e2", "q2", self.OBJ, "2026-09-18T02:00:00Z", "2026-09-18"),
                      ev("e3", "check", "2026-09-18T03:00:00Z", objective=self.OBJ, result="miss")]
        self.assertGreater(ll.states(more)[self.OBJ].priority, ll.states(one)[self.OBJ].priority)

    def test_js_and_python_agree(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("node 없음")
        events = [wrong("a1", "q1", "o1", "2026-09-18T01:00:00Z", "2026-09-18"),
                  ev("a2", "check", "2026-09-18T01:05:00Z", objective="o1", result="ok"),
                  wrong("b1", "q9", "o2", "2026-09-18T01:00:00Z", "2026-09-18"),
                  right("b2", "o2#v1", "o2", "2026-09-19T01:00:00Z", "2026-09-19", mode="variant"),
                  wrong("c1", "q5", None, "2026-09-18T01:00:00Z", "2026-09-18"),
                  ev("d1", "flag", "2026-09-18T01:00:00Z", qid="q7", objective=None, flag="guessed", on=True),
                  wrong("e1", "q2", "o3", "2026-09-18T01:00:00Z", "2026-09-18"),
                  right("e2", "q3", "o3", "2026-09-19T01:00:00Z", "2026-09-19"),
                  wrong("e3", "q4", "o3", "2026-09-20T01:00:00Z", "2026-09-20")]
        harness = (
            "const fs=require('fs');const vm=require('vm');const store={};"
            "const ctx={window:{},location:{hostname:'localhost',protocol:'https:'},localStorage:{getItem:k=>store[k]||null,setItem:(k,v)=>{store[k]=v}},"
            "KMLE:[],USMLE:[],IMAGING:[],console};vm.createContext(ctx);"
            f"store['medkos_learning_events']=JSON.stringify({json.dumps(events)});"
            f"vm.runInContext(fs.readFileSync({json.dumps(str(ROOT / 'docs' / 'learn.js'))},'utf8')+"
            "';this.__S=LEARN.states();',ctx);"
            "const out={};for(const [k,s] of Object.entries(ctx.__S)){out[k]=[s.status,s.priority,s.applied,s.wrongs]}"
            "const sc=ctx.LEARN_SC;"
            "console.log(JSON.stringify({states:out,schedule:sc}));")
        harness = harness.replace("';this.__S=LEARN.states();'", "';this.__S=LEARN.states();this.LEARN_SC=LEARN.schedule([1,7]);'")
        r = subprocess.run([node, "-e", harness], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)
        js = json.loads(r.stdout)
        py = {k: [s.status, s.priority, s.applied, s.wrongs] for k, s in ll.states(events).items()}
        self.assertEqual(js["states"], py)
        self.assertEqual(js["schedule"], ll.schedule(events, steps=(1, 7)))


class RetestSchedule(unittest.TestCase):
    """다시 풀 날(2026-09-23) — 틀린 날 +1일 · 맞히면 +7일 · 끝. 예정일 전 정답은 연습."""
    OBJ = "cn.x.y.z"

    def test_wrong_sets_first_due_and_early_practice_does_not_advance(self):
        e = [wrong("e1", "q1", self.OBJ, "2026-09-18T01:00:00Z", "2026-09-18")]
        self.assertEqual(ll.schedule(e)[self.OBJ], {"stage": 0, "total": 2, "anchor": "2026-09-18", "due": "2026-09-19"})
        same_day = e + [right("e2", "q2", self.OBJ, "2026-09-18T02:00:00Z", "2026-09-18")]
        self.assertEqual(ll.schedule(same_day)[self.OBJ]["stage"], 0)

    def test_on_time_success_advances_then_finishes_and_wrong_resets(self):
        e = [wrong("e1", "q1", self.OBJ, "2026-09-18T01:00:00Z", "2026-09-18"),
             right("e2", "cn.x.y.z#v1", self.OBJ, "2026-09-20T01:00:00Z", "2026-09-20", mode="variant")]
        s = ll.schedule(e)[self.OBJ]
        self.assertEqual((s["stage"], s["due"]), (1, "2026-09-27"))
        done = e + [right("e3", "q3", self.OBJ, "2026-09-27T01:00:00Z", "2026-09-27")]
        self.assertEqual(ll.schedule(done)[self.OBJ]["due"], "")
        again = done + [wrong("e4", "q4", self.OBJ, "2026-09-30T01:00:00Z", "2026-09-30")]
        self.assertEqual(ll.schedule(again)[self.OBJ], {"stage": 0, "total": 2, "anchor": "2026-09-30", "due": "2026-10-01"})

    def test_steps_are_configurable_and_bad_values_fall_back(self):
        e = [wrong("e1", "q1", self.OBJ, "2026-09-18T01:00:00Z", "2026-09-18")]
        self.assertEqual(ll.schedule(e, steps="3,10,30")[self.OBJ]["due"], "2026-09-21")
        for bad in ("", "0,7", "a", "1.5", [400]):
            self.assertEqual(ll.parse_steps(bad), ll.DEFAULT_STEPS)
        self.assertEqual(ll.parse_steps([2, 5]), (2, 5))


class ItemStats(unittest.TestCase):
    def test_first_attempt_only_and_no_verdict_on_small_groups(self):
        import item_stats as st
        e = [wrong("e1", "q1", "o", "2026-09-18T01:00:00Z", "2026-09-18"),
             right("e2", "q1", "o", "2026-09-19T01:00:00Z", "2026-09-19"),            # 두 번째 풀이 — 세지 않는다
             right("e3", "o#v1", "o", "2026-09-19T01:00:00Z", "2026-09-19", mode="variant")]
        qs = {"q1": {"difficulty": 4, "type": "kmle", "design": {"steps": 3, "target": "치료"}}}
        r = st.build(e, qs)
        self.assertEqual((r["first_attempts"], r["accuracy"]), (1, 0.0))
        self.assertEqual(r["label_inversions"], [])

    def test_inversion_needs_big_groups(self):
        import item_stats as st
        g = {"난이도 3": {"n": 25, "ok": 10, "acc": 0.4}, "난이도 4": {"n": 25, "ok": 15, "acc": 0.6}}
        self.assertEqual(len(st.inversions(g, ["난이도 3", "난이도 4"])), 1)
        g["난이도 4"]["n"] = 5
        self.assertEqual(st.inversions(g, ["난이도 3", "난이도 4"]), [])


class Planning(unittest.TestCase):
    def setUp(self):
        self.cfg = bb.load_config()
        self.cfg["include_all_concepts"] = False               # 이 묶음은 「오답 → 단원」 규칙만 본다(전체 싣기는 아래 따로)
        base, _ = C.load_concepts()
        self.c1 = copy.deepcopy(base["cn.derm.pityriasis-versicolor.treatment"])
        self.c2 = copy.deepcopy(self.c1)                      # 같은 질환, 다른 학습 목표
        self.c2.update(id="cn.derm.pityriasis-versicolor.diagnosis", title="어루러기 — 진단 단서", objective_kind="진단")
        self.concepts = {self.c1["id"]: self.c1, self.c2["id"]: self.c2}
        self.qs = {"q1": {"topic": "Dermatology", "objective": self.c1["id"], "choices": []},
                   "q2": {"topic": "Dermatology", "objective": self.c1["id"], "choices": []},
                   "q3": {"topic": "Dermatology", "objective": self.c2["id"], "choices": []},
                   "q4": {"topic": "Dermatology", "objective": "cn.derm.new.objective", "choices": []},
                   "q5": {"topic": "Dermatology", "choices": [], "stem": "목표 없는 문항"}}

    def _plan(self, events):
        return bb.plan(self.concepts, self.qs, ll.states(events), self.cfg, {})

    def test_all_concepts_are_included_when_merged(self):
        cfg = dict(self.cfg, include_all_concepts=True)        # 2026-09-22 학습서·학습서_검증 통합
        books = bb.plan(self.concepts, self.qs, ll.states([]), cfg, {})
        self.assertEqual(sorted(u.key for u in books["피부과"].units), sorted(self.concepts))
        e = [wrong("e1", "q1", self.c1["id"], "2026-09-18T01:00:00Z", "2026-09-18")]
        units = bb.plan(self.concepts, self.qs, ll.states(e), cfg, {})["피부과"].units
        self.assertEqual(len(units), 2)                        # 오답 단원과 겹치지 않는다
        self.assertEqual(next(u for u in units if u.key == self.c1["id"]).state.wrongs, 1)

    def test_new_concept_new_unit_and_repeat_no_duplicate(self):
        e = [wrong("e1", "q1", self.c1["id"], "2026-09-18T01:00:00Z", "2026-09-18")]
        units = self._plan(e)["피부과"].units
        self.assertEqual([u.key for u in units], [self.c1["id"]])
        e.append(wrong("e2", "q2", self.c1["id"], "2026-09-18T02:00:00Z", "2026-09-18", text="다른 오답"))
        units = self._plan(e)["피부과"].units
        self.assertEqual(len(units), 1)                        # 같은 목표 → 한 단원
        self.assertEqual([c["qid"] for c in units[0].state.chosen], ["q1", "q2"])   # 문항마다의 혼동은 보존

    def test_same_disease_different_objective_stays_separate(self):
        e = [wrong("e1", "q1", self.c1["id"], "2026-09-18T01:00:00Z", "2026-09-18"),
             wrong("e2", "q3", self.c2["id"], "2026-09-18T01:00:00Z", "2026-09-18")]
        keys = sorted(u.key for u in self._plan(e)["피부과"].units)
        self.assertEqual(keys, sorted([self.c1["id"], self.c2["id"]]))

    def test_missing_concept_becomes_stub_and_no_objective_is_pending(self):
        e = [wrong("e1", "q4", "cn.derm.new.objective", "2026-09-18T01:00:00Z", "2026-09-18"),
             wrong("e2", "q5", None, "2026-09-18T01:00:00Z", "2026-09-18")]
        b = self._plan(e)["피부과"]
        self.assertEqual(len(b.units), 1)
        self.assertIsNone(b.units[0].concept)
        self.assertNotIn("cn.", b.units[0].title)             # 내부 ID 를 제목으로 쓰지 않는다
        self.assertEqual([s.key for s, _ in b.pending], ["q:q5"])   # 앱에만 남고 PDF 에는 싣지 않는다

    def test_book_without_concept_units_is_not_built(self):
        e = [wrong("e2", "q5", None, "2026-09-18T01:00:00Z", "2026-09-18")]
        self.assertEqual(self._plan(e), {})

    def test_hash_follows_printed_content_not_learning_activity(self):
        e = [wrong("e1", "q1", self.c1["id"], "2026-09-18T01:00:00Z", "2026-09-18")]
        h = lambda ev_: bb.volume_hash("피부과", self._plan(ev_)["피부과"].units, [], self.cfg, self.qs)
        base = h(e)
        self.assertEqual(base, h(list(e)))
        # 메모·열람은 PDF 에 싣지 않으므로 책을 다시 만들 이유가 아니다
        more = e + [ev("m", "memo", "2026-09-18T03:00:00Z", objective=self.c1["id"], text="메모"),
                    ev("v", "view", "2026-09-18T03:01:00Z", objective=self.c1["id"], what="note")]
        self.assertEqual(base, h(more))
        self.c1["hash"] = "changed"                           # 정리본 내용이 바뀌면 다시 만든다
        self.assertNotEqual(base, h(e))

    def test_volumes_split_by_config(self):
        b = bb.Book("피부과", units=[bb.Unit(f"cn.a.b.u{i}", "피부과", None, ll.State(f"cn.a.b.u{i}", None), [], f"t{i}") for i in range(5)])
        vols = bb.volumes(b, {"volume_max_units": 2})
        self.assertEqual([t for t, _ in vols], ["피부과 1권", "피부과 2권", "피부과 3권"])

    def test_source_change_flags_unit(self):
        e = [wrong("e1", "q1", self.c1["id"], "2026-09-18T01:00:00Z", "2026-09-18")]
        src = self.c1["sources"][0]
        state = {bb.source_key(src): {"status": "changed", "note": "UpdateIn 추가"}}
        u = bb.plan(self.concepts, self.qs, ll.states(e), self.cfg, state)["피부과"].units[0]
        self.assertTrue(any("개정 확인 필요" in f for f in u.flags))

    def test_wide_body_tables_become_rows(self):
        t = "<table><thead><tr>" + "".join(f"<th>h{i}</th>" for i in range(6)) + "</tr></thead><tbody><tr>" \
            + "".join(f"<td>c{i}</td>" for i in range(6)) + "</tr></tbody></table>"
        out = bb.stack_wide_tables(t)
        self.assertNotIn("<table>", out)
        self.assertIn("<b>h0</b> c0", out)
        three = bb.stack_wide_tables(t.replace("<th>h5</th>", "").replace("<th>h4</th>", "").replace("<th>h3</th>", ""))
        self.assertIn('<table class="c3">', three)                            # 한 단 폭 — 3칸까지 표, 칸 수 class 로 글씨 크기

    def test_wide_tables_become_record_tables(self):
        c = {"sources": []}
        tb = {"title": "검사", "columns": ["검사", "보여 주는 것", "할 수 없는 것", "자리", "근거"],
              "rows": [["흉부 X선", "중심 폐동맥 확장이 보이는 긴 설명", "압력을 재지 못한다 — 긴 설명", "초기 평가", "—"]]}
        h = bb.table_html(tb, c, "u-x")
        self.assertIn('<table class="rec">', h)                              # 카드 대신 진짜 표(머리줄 + 이름|내용)
        self.assertIn('<tr class="rh"><th colspan="2"><b>흉부 X선</b></th></tr>', h)
        self.assertNotIn(">근거</td>", h)                                     # 빈 칸(—)은 줄을 만들지 않는다
        short = dict(tb, columns=tb["columns"][:3], rows=[r[:3] for r in tb["rows"]])
        self.assertIn('<table class="c3">', bb.table_html(short, c, "u-x"))

    def test_phrase_wrap_breaks_between_items(self):
        w = bb.dd.phrase_wrap
        self.assertEqual(w("중추신경·중증 혈액학 침범 — 고용량/펄스 스테로이드 ± 면역억제제(이 도식 범위 밖)", 17),
                         ["중추신경·중증 혈액학 침범", "— 고용량/펄스 스테로이드", "± 면역억제제(이 도식 범위 밖)"])
        self.assertEqual(w("소변검사(단백·적혈구·원주)·크레아티닌·혈구·흉부 영상·신경 증상을 확인한다", 17),
                         ["소변검사(단백·적혈구·원주)·", "크레아티닌·혈구·흉부 영상·", "신경 증상을 확인한다"])
        self.assertEqual(w("짧다", 17), ["짧다"])

    def test_auto_pitfalls_generalize_without_guessing(self):
        q = {"topic": "Dermatology", "objective": self.c1["id"], "answer": "A",
             "choices": ["A. 정답약", "B. 오답약"],
             "distractors": {"B": {"tempting": "학습자가 끌렸을 이유", "answer_first": "x",
                                   "discriminator": "가르는 소견", "when_right": "맞는 경우"}}}
        self.qs["q9"] = q
        e = [wrong("e1", "q9", self.c1["id"], "2026-09-18T01:00:00Z", "2026-09-18", text="오답약")]
        u = self._plan(e)["피부과"].units[0]
        pits = bb.auto_pitfalls(u, self.qs)
        self.assertEqual(pits[0]["contrast"], "오답약 ↔ 정답약")
        self.assertEqual(pits[0]["point"], "가르는 소견")
        self.assertNotIn("끌렸을", json.dumps(pits, ensure_ascii=False))      # tempting 은 쓰지 않는다
        self.c1["pitfalls"] = [{"contrast": "x", "point": "y", "covers": ["q9:B"]}]
        self.assertEqual(bb.auto_pitfalls(u, self.qs), [])                     # 정리본이 이미 다룬 혼동은 중복하지 않는다

    def test_table_helpers(self):
        w = bb.col_widths(["기준", "내용"], [["짧다", "훨씬 더 긴 설명이 들어가는 칸이다" * 3]])
        self.assertAlmostEqual(sum(w), 100, delta=0.5)
        self.assertGreater(w[1], w[0])
        blocks = bb.split_blocks("<p>가</p><ul><li>나<ul><li>다</li></ul></li></ul><table><tr><td>라</td></tr></table>")
        self.assertEqual(len(blocks), 3)

    def test_tall_chain_fits_readably(self):
        # 9층 사슬(2026-09-24 실패한 대동맥 박리 도식 그대로) — 층 사이를 필요한 만큼만 두면 한 쪽에 읽을 크기로 들어간다
        fit = bb.fit_diagram(TALL)
        self.assertTrue(fit["ok"])
        self.assertGreaterEqual(fit["pt"], bb.DIA_FLOOR_PT if fit["place"] == "column" else bb.DIA_FULL_FLOOR_PT)
        small = bb.fit_diagram(TALL, shrink=0.88)
        self.assertAlmostEqual(small["scale"], round(fit["scale"] * 0.88, 3), places=2)


SRC_FIXTURE = ({"cn.x.y.z": {"id": "cn.x.y.z", "sources": [
    {"id": "p", "pmid": "111", "title": "PubMed 출처", "checked_at": "2026-09-18"},
    {"id": "g", "url": "https://example.org/guideline.pdf", "title": "지침", "checked_at": "2026-09-18",
     "watch": {"pattern": r"HYPERKALAEMIA GUIDELINE - (\w+ \d{4})"}},
    {"id": "h", "kind": "textbook", "citation": "Harrison 21e", "title": "교과서", "checked_at": "2026-09-18"},
]}}, [])


class _FixtureSources(unittest.TestCase):
    """출처 확인 시험은 실제 정리본이 아니라 고정 출처로 한다 — 루틴이 새 정리본을 쓸 때마다 시험이 깨지지 않게
    (2026-09-23·24 학습서 실패: DOI 만 있는 새 출처가 가짜 응답으로 「실패」가 되어 시험을 세웠다)."""

    def setUp(self):
        from unittest import mock
        p = mock.patch.object(cs, "load_concepts", lambda: copy.deepcopy(SRC_FIXTURE))
        p.start()
        self.addCleanup(p.stop)


class IdMentions(unittest.TestCase):
    def test_other_concept_id_becomes_its_title(self):
        titles = C.concept_titles()
        cid, title = next(iter(titles.items()))
        out = C.render_cites(f"이어지는 목표는 <code>{cid}</code> 가 다룬다. 모르는 cn.zz.yy.xx 는 그대로", {"sources": []}, "pdf")
        self.assertIn(f"「{title}」", out)
        self.assertNotIn(cid, out)
        self.assertIn("cn.zz.yy.xx", out)


class SourceChecks(_FixtureSources):
    def test_method_change_rebaselines_instead_of_flagging(self):
        # 2026-09-25: 출판사 url 도달(reachable)로 기록된 출처가 DOI→PubMed 로 바뀌자 「지문 변경」으로 찍혔다
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "sc.json"
            out.write_text(json.dumps({"111": {"status": "ok", "method": "reachability", "baseline": "reachable"}}), encoding="utf-8")
            xml = "<PubmedArticleSet><PubmedArticle></PubmedArticle></PubmedArticleSet>"
            r = cs.run(getter=lambda u: xml if "eutils" in u else "HYPERKALAEMIA GUIDELINE - JULY 2022 V2.pdf", out=out, today="2026-09-26")
            self.assertEqual((r["111"]["status"], r["111"]["baseline"]), ("ok", "[]"))
            self.assertIn("확인 방법이 바뀌어", r["111"]["note"])

    def test_doi_with_publisher_url_is_checked_by_doi_not_the_site(self):
        SRC_FIXTURE[0]["cn.x.y.z"]["sources"].append({"id": "u", "doi": "10.1/pub", "url": "https://publisher.example/x",
                                                      "title": "출판사", "checked_at": "2026-09-18"})
        self.addCleanup(SRC_FIXTURE[0]["cn.x.y.z"]["sources"].pop)

        def net(url):
            if "publisher.example" in url:
                raise AssertionError("출판사 사이트를 열었다")
            if "esearch" in url:
                return "<eSearchResult><IdList><Id>7</Id></IdList></eSearchResult>"
            if "efetch" in url:
                return "<PubmedArticleSet><PubmedArticle></PubmedArticle></PubmedArticleSet>"
            return "HYPERKALAEMIA GUIDELINE - JULY 2022 V2.pdf"
        with tempfile.TemporaryDirectory() as td:
            r = cs.run(getter=net, out=Path(td) / "sc.json", today="2026-09-25")
        self.assertEqual((r["10.1/pub"]["status"], r["10.1/pub"]["method"]), ("ok", "pubmed"))

    def test_doi_only_source_resolves_to_pubmed_once_then_falls_back_to_doi_org(self):
        SRC_FIXTURE[0]["cn.x.y.z"]["sources"].append({"id": "d", "doi": "10.1/abc", "title": "DOI 출처", "checked_at": "2026-09-18"})
        self.addCleanup(SRC_FIXTURE[0]["cn.x.y.z"]["sources"].pop)
        calls = []

        def net(url):
            calls.append(url)
            if "esearch" in url:
                return "<eSearchResult><IdList><Id>999</Id></IdList></eSearchResult>"
            if "efetch" in url:
                return "<PubmedArticleSet><PubmedArticle></PubmedArticle></PubmedArticleSet>"
            return "HYPERKALAEMIA GUIDELINE - JULY 2022 V2.pdf"
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "sc.json"
            r = cs.run(getter=net, out=out, today="2026-09-25")
            self.assertEqual((r["10.1/abc"]["status"], r["10.1/abc"]["method"], r["10.1/abc"]["doi_pmid"]), ("ok", "pubmed", "999"))
            calls.clear()
            cs.run(getter=net, out=out, today="2026-09-26")
            self.assertFalse(any("esearch" in u for u in calls))              # 찾은 PMID 는 기억한다

            def not_in_pubmed(url):
                if "esearch" in url:
                    return "<eSearchResult><IdList></IdList></eSearchResult>"
                if "doi.org/api/handles" in url:
                    return '{"responseCode": 1, "handle": "10.1/abc"}'
                return net(url)
            r = cs.run(getter=not_in_pubmed, out=Path(td) / "sc2.json", today="2026-09-25")
            self.assertEqual((r["10.1/abc"]["status"], r["10.1/abc"]["method"]), ("ok", "doi"))
            self.assertIn("알 수 없음", r["10.1/abc"]["note"])                 # 개정을 확인했다고 쓰지 않는다

    def test_baseline_change_failure_and_human_recheck(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "sc.json"
            xml0 = "<PubmedArticleSet><PubmedArticle></PubmedArticle></PubmedArticleSet>"
            xml1 = ('<PubmedArticleSet><PubmedArticle><CommentsCorrections RefType="UpdateIn">'
                    "<RefSource>x</RefSource><PMID>1</PMID></CommentsCorrections></PubmedArticle></PubmedArticleSet>")
            ok = lambda body: (lambda url: body if "eutils" in url else "HYPERKALAEMIA GUIDELINE - JULY 2022 V2.pdf")
            r = cs.run(getter=ok(xml0), out=out, today="2026-09-18")
            self.assertTrue(all(v["status"] == "ok" for v in r.values()))
            r = cs.run(getter=ok(xml1), out=out, today="2026-09-25")
            self.assertTrue(any(v["status"] == "changed" for v in r.values()))

            def boom(url):
                raise ValueError("지문을 읽지 못했다")                 # 일시 오류가 아닌 진짜 실패
            r = cs.run(getter=boom, out=out, today="2026-09-26")
            net = {k: v for k, v in r.items() if v.get("method") != "manual"}      # 교과서는 사람이 확인(네트워크와 무관)
            self.assertTrue(net and all(v["status"] == "failed" and "업데이트 확인 필요" in v["note"] for v in net.values()))
            self.assertTrue(all(v["status"] == "ok" for k, v in r.items() if k not in net))


class FakeRemote:
    files: dict = {}

    def __init__(self, *a):
        pass

    def ls(self, sub=""):
        pre = (sub + "/") if sub else ""
        return [{"Name": k[len(pre):], "ID": v["id"], "Hashes": {"md5": v["md5"]}} for k, v in self.files.items()
                if k.startswith(pre) and "/" not in k[len(pre):]]

    def put(self, local, name):
        cur = self.files.get(name)
        self.files[name] = {"id": cur["id"] if cur else f"id-{len(self.files)}", "md5": db.md5(Path(local))}


class DriveUpload(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.dir = Path(self.td.name)
        (self.dir / "out").mkdir()
        self.pdf = self.dir / "out" / "MedKOS_학습서_피부과.pdf"
        self.pdf.write_bytes(b"%PDF-1.4 v1")
        self.manifest = {"books": {"피부과": {"file": self.pdf.name, "version": 1, "date": "2026-09-18"}}}
        (self.dir / "manifest.json").write_text(json.dumps(self.manifest), encoding="utf-8")
        self._orig = (db.Remote, db.rclone_bin)
        db.Remote, db.rclone_bin = FakeRemote, (lambda: "rclone")
        FakeRemote.files = {}
        self.cfg = {"drive": {"remote": "gdrive", "folder_id": "FOLDER", "archive": True}}

    def tearDown(self):
        db.Remote, db.rclone_bin = self._orig
        self.td.cleanup()

    def _up(self):
        return db.upload(self.cfg, self.dir, self.dir / "out", {"built": ["피부과"]})

    def test_not_configured_does_not_claim_upload(self):
        r = db.upload({"drive": {"folder_id": ""}}, self.dir, self.dir / "out", {"built": ["피부과"]})
        self.assertEqual(r["result"], "not_configured")

    def test_same_file_id_archive_and_user_annotation_protection(self):
        r = self._up()
        first_id = r["items"]["피부과"]["id"]
        self.assertEqual(r["items"]["피부과"]["status"], "uploaded")
        self.assertIn("archive/MedKOS_학습서_피부과_v1_2026-09-18.pdf", FakeRemote.files)
        # 새 판 → 같은 ID 로 갱신
        m = json.loads((self.dir / "manifest.json").read_text(encoding="utf-8"))
        m["books"]["피부과"].update(version=2)
        (self.dir / "manifest.json").write_text(json.dumps(m), encoding="utf-8")
        self.pdf.write_bytes(b"%PDF-1.4 v2")
        r = self._up()
        self.assertEqual((r["items"]["피부과"]["status"], r["items"]["피부과"]["id"]), ("uploaded", first_id))
        # 아이패드에서 최신본에 필기 → 덮어쓰지 않는다
        FakeRemote.files[self.pdf.name]["md5"] = "annotated"
        m = json.loads((self.dir / "manifest.json").read_text(encoding="utf-8"))
        m["books"]["피부과"].update(version=3)
        (self.dir / "manifest.json").write_text(json.dumps(m), encoding="utf-8")
        self.pdf.write_bytes(b"%PDF-1.4 v3")
        r = self._up()
        self.assertEqual(r["items"]["피부과"]["status"], "skipped")
        self.assertEqual(FakeRemote.files[self.pdf.name]["md5"], "annotated")

    def test_unknown_same_name_file_is_not_touched(self):
        FakeRemote.files = {self.pdf.name: {"id": "user-file", "md5": "abc"}}
        r = self._up()
        self.assertEqual(r["items"]["피부과"]["status"], "skipped")
        self.assertEqual(FakeRemote.files[self.pdf.name]["md5"], "abc")


class RenderedBook(unittest.TestCase):
    """실제로 렌더링해 본다 — 한글 검색·차례 링크·책갈피·건너뜀·실패 시 최신본 유지."""

    @classmethod
    def setUpClass(cls):
        try:
            import playwright  # noqa: F401
            import pymupdf  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("playwright/pymupdf 없음")

    def test_build_skip_and_failure_keeps_latest(self):
        import pymupdf
        cfg = bb.load_config()
        cfg["include_all_concepts"] = False           # 오답이 만든 책만 — 건너뜀·실패 규칙을 한 권으로 본다
        events = [wrong("e1", "kmle-2026-0675", "cn.peds.febrile-seizure.workup", "2026-09-18T01:00:00Z", "2026-09-18",
                        text="뇌척수액검사 시행")]
        with tempfile.TemporaryDirectory() as td:
            st, out = Path(td) / "state", Path(td) / "out"
            r = bb.build(cfg, events, st, out)
            self.assertEqual(r["built"], ["소아청소년과"], r)
            pdf = out / "MedKOS_학습서_소아청소년과.pdf"
            with pymupdf.open(pdf) as d:
                self.assertLess(d[0].rect.width, d[0].rect.height)               # A4 세로 2단(2026-09-27)
                man = json.loads((st / "manifest.json").read_text(encoding="utf-8"))
                self.assertTrue(all(v["page"] >= 2 for v in man["books"]["소아청소년과"]["units"].values()))   # 1쪽 = 목차 쪽만
                text = " ".join(" ".join(p.get_text().split()) for p in d)
                self.assertTrue([p.number for p in d if p.search_for("열성경련")])    # 한글 글자 검색
                self.assertTrue(any(t[0] >= 2 for t in d.get_toc()))               # 책갈피
                for gone in ("스스로 묻기", "해설 열람", "kmle-2026-0675", "cn.peds", "단원 ID", ".md"):
                    self.assertNotIn(gone, text)                                   # 학습 활동·내부 ID 없음
                self.assertIn("혼동하기 쉬운 점", text)                            # 오답 혼동은 일반화해 본문으로
                links = [ln for p in d for ln in p.get_links() if str(ln.get("nameddest", "")).startswith("u-")]
                self.assertTrue(any("-ref-" in ln["nameddest"] for ln in links))   # 근거 번호 → 참고문헌 링크
            before = pdf.read_bytes()
            self.assertEqual(bb.build(cfg, events, st, out)["result"], "skipped")
            memo = events + [ev("m1", "memo", "2026-09-18T02:00:00Z", objective="cn.peds.febrile-seizure.workup", text="메모")]
            self.assertEqual(bb.build(cfg, memo, st, out)["result"], "skipped")   # 학습 기록만 바뀌면 다시 만들지 않는다
            r = bb.build(cfg, events, st, out, force=True, fail_on="소아청소년과")
            self.assertEqual(r["retry"], ["소아청소년과"])
            self.assertEqual(pdf.read_bytes(), before)            # 실패해도 이전 판 그대로
            man = json.loads((st / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(man["books"]["소아청소년과"]["version"], 1)
            last = json.loads((st / "last_run.json").read_text(encoding="utf-8"))
            self.assertIn("소아청소년과", last["failed"])


class ConceptQueueTest(unittest.TestCase):
    """내 오답 → 이론 정리본 큐(매일 루틴이 읽는다)."""

    def setUp(self):
        import concept_queue as cq
        self.cq = cq
        self._orig = (cq.load_concepts, cq.load_questions, cq.load_kr)
        cq.load_kr = lambda: ([], {})                       # 코드 시험은 실제 대조 파일을 읽지 않는다
        self.concepts = {"cn.derm.a.b": {"id": "cn.derm.a.b"}}
        self.qs = {"q1": {"topic": "Dermatology", "subtopic": "어루러기", "objective": "cn.derm.a.b"},
                   "q2": {"topic": "Dermatology", "subtopic": "백선", "objective": "cn.derm.c.d"},
                   "q3": {"topic": "Cardiology", "subtopic": "심부전"},
                   "q4": {"topic": "Cardiology", "subtopic": "심부전"}}
        cq.load_concepts = lambda: (self.concepts, [])
        cq.load_questions = lambda: self.qs

    def tearDown(self):
        self.cq.load_concepts, self.cq.load_questions, self.cq.load_kr = self._orig

    def test_krdiff_pairs_by_slot_and_skips_done_items(self):
        """국내 vs 해리슨(2026-11-25 사용자 결정) — 정리본 슬롯에 닿는 차이 항목 중 아직 반영 · 제외 표시가 없는 것만 낸다."""
        items = [
            {"id": "diff.c.af.a", "slot": "h251", "kr_guideline_id": "kr-af", "diff_type": "threshold", "subject_slug": "cardiology"},
            {"id": "diff.c.af.b", "slot": "h251", "kr_guideline_id": "kr-af", "diff_type": "same", "subject_slug": "cardiology"},
            {"id": "diff.c.af.c", "slot": "h251", "kr_guideline_id": "kr-af", "diff_type": "algorithm", "subject_slug": "cardiology"},
            {"id": "diff.s.t.a", "slot": "h385", "kr_guideline_id": "kr-thy", "diff_type": "threshold", "subject_slug": "endocrinology"},
        ]
        reg = {"guidelines": [{"id": "kr-af", "slots": ["h251"]}, {"id": "kr-thy", "slots": ["h385", "surg.x"]}]}
        concepts = {
            "cn.c.af.x": {"id": "cn.c.af.x", "outline": "h251", "kr_diffs": ["diff.c.af.a"]},
            "cn.s.t.y": {"id": "cn.s.t.y", "outline": "surg.x"},                      # 트랙 slots 로 닿는다
            "cn.c.af.z": {"id": "cn.c.af.z", "outline": "h251", "kr_diffs": ["diff.c.af.a"], "kr_diffs_skip": ["diff.c.af.c"]},
            "cn.b.p.q": {"id": "cn.b.p.q", "outline": "h251", "layer": "basic"},      # 기초 정리본은 대상이 아니다
            "cn.o.n.e": {"id": "cn.o.n.e"},                                           # 슬롯 없음
        }
        out = self.cq._krdiffs(concepts, {}, (items, reg))
        self.assertEqual({k["objective"]: k["items"] for k in out},
                         {"cn.c.af.x": ["diff.c.af.c"], "cn.s.t.y": ["diff.s.t.a"]})  # same · 반영 · 제외는 빠진다
        self.assertEqual(out[0]["files"] if out[0]["objective"] == "cn.c.af.x" else out[1]["files"],
                         ["content/outline/kr_vs_harrison/cardiology.yaml"])
        self.assertEqual(self.cq._krdiffs(concepts, {}, ([], reg)), [])

    def test_kr_diff_fields_shape(self):
        import concepts as cs
        self.assertEqual(cs.kr_diff_errors({"kr_diffs": ["diff.c.af.a"], "kr_diffs_skip": ["diff.c.af.c"]}), [])
        self.assertTrue(cs.kr_diff_errors({"kr_diffs": "diff.c.af.a"}))             # 목록이어야 한다
        self.assertTrue(cs.kr_diff_errors({"kr_diffs": ["af-a"]}))                  # diff.<과>.<주제>.<요점>
        self.assertTrue(cs.kr_diff_errors({"kr_diffs": ["diff.c.af.a"], "kr_diffs_skip": ["diff.c.af.a"]}))

    def test_wrong_note_fills_answers_missing_from_learning_log(self):
        """학습 흐름(2026-09-18) 전의 오답은 오답 목록에만 있다 — 큐가 그것도 집어야 한다(2026-09-23)."""
        e = [wrong("e2", "q2", "cn.derm.c.d", "2026-09-20T01:00:00Z", "2026-09-20")]
        note = {"q2": {"id": "q2", "date": "2026-09-20", "chosenText": "x"},            # 학습 기록에 이미 있음 → 중복 안 셈
                "q3": {"id": "q3", "date": "2026-09-13", "chosenText": "a", "answerText": "b"},   # 목표 없음 → link
                "q9": {"id": "q9", "date": "2026-09-13"}}                                # 없는 문항 → 무시
        q = self.cq.build(e, note)
        self.assertEqual([(n["objective"], n["wrongs"]) for n in q["note"]], [("cn.derm.c.d", 1)])
        self.assertEqual([l["questions"] for l in q["link"]], [["q3"]])
        self.assertEqual(q["counts"]["from_wrongnote"], 2)
        self.assertEqual(self.cq.build(e)["counts"]["from_wrongnote"], 0)            # 넘기지 않으면 학습 기록만

    def test_wrong_note_with_objective_and_existing_concept_becomes_touch(self):
        self.qs["q1"]["choices"] = ["A. 가", "B. 나"]
        self.concepts["cn.derm.a.b"]["pitfalls"] = []
        q = self.cq.build([], {"q1": {"id": "q1", "date": "2026-09-10", "chosenText": "나", "answerText": "가"}})
        self.assertEqual([x["cover"] for x in q["touch"]], ["q1:B"])

    def test_load_wrong_notes_reads_every_exam_file(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "kmle.json").write_text(json.dumps({"items": {"k1": {"id": "k1"}}}), encoding="utf-8")
            Path(d, "usmle.json").write_text(json.dumps({"items": [{"id": "u1"}]}), encoding="utf-8")
            Path(d, "broken.json").write_text("{", encoding="utf-8")
            self.assertEqual(sorted(self.cq.load_wrong_notes(Path(d))), ["k1", "u1"])

    def test_queue_splits_note_and_link_and_skips_existing_notes(self):
        e = [wrong("e1", "q1", "cn.derm.a.b", "2026-09-20T01:00:00Z", "2026-09-20"),     # 정리본 있음 → 큐에 없음
             wrong("e2", "q2", "cn.derm.c.d", "2026-09-20T01:00:00Z", "2026-09-20"),     # 목표만 있음 → note
             wrong("e3", "q3", None, "2026-09-20T01:00:00Z", "2026-09-20"),              # 목표 없음 → link
             wrong("e4", "q4", None, "2026-09-20T01:00:00Z", "2026-09-20"),              # 같은 주제 → 한 줄로
             wrong("e5", "q9", None, "2026-09-20T01:00:00Z", "2026-09-20")]              # 없는 문항 → 무시
        q = self.cq.build(e)
        self.assertEqual([n["objective"] for n in q["note"]], ["cn.derm.c.d"])
        self.assertEqual([(l["topic"], l["subtopic"], sorted(l["questions"])) for l in q["link"]],
                         [("Cardiology", "심부전", ["q3", "q4"])])
        self.assertEqual(q["counts"]["wrong_objectives_with_note"], 1)

    def test_variant_queue_per_wrong_question_until_two_exist(self):
        self.qs["q1"].update(type="kmle", choices=["A. 가", "B. 나"], answer="A", design={"switch": {"choice": "B", "condition": "x"}})
        e = [wrong("e1", "q1", "cn.derm.a.b", "2026-09-20T01:00:00Z", "2026-09-20", text="나")]
        q = self.cq.build(e)
        self.assertEqual([(v["qid"], v["need"], v["due"], v["seed"]) for v in q["variant"]], [("q1", 2, "2026-09-21", "design.switch")])
        self.concepts["cn.derm.a.b"]["variants"] = [{"id": "v1", "of": "q1"}, {"id": "v2", "of": "q1"}]
        self.assertEqual(self.cq.build(e)["variant"], [])

    def test_variant_seed_is_the_other_side_of_a_trap_family(self):
        """함정 계열 문항(design.trap)을 틀리면 변형 A 의 씨앗은 그 계열의 반대쪽이다(2026-09-29)."""
        self.qs["q1"].update(type="kmle", choices=["A. 가", "B. 나"], answer="A",
                             design={"switch": {"choice": "B", "condition": "x"}, "trap": {"id": "tr.t.x", "side": "trap"}})
        e = [wrong("e1", "q1", "cn.derm.a.b", "2026-09-20T01:00:00Z", "2026-09-20", text="나")]
        self.assertEqual([v["seed"] for v in self.cq.build(e)["variant"]], ["design.trap(tr.t.x) → mirror.when"])
        self.qs["q1"]["design"]["trap"] = {"id": "tr.t.x", "side": "mirror"}
        self.assertEqual([v["seed"] for v in self.cq.build(e)["variant"]], ["design.trap(tr.t.x) → trap 조건"])

    def test_dist_queue_only_for_chosen_letter_without_explanation(self):
        self.qs["q1"].update(type="kmle", choices=["A. 가", "B. 나", "C. 다"], answer="A", path="content/kmle/x.md")
        e = [wrong("e1", "q1", "cn.derm.a.b", "2026-09-20T01:00:00Z", "2026-09-20", text="나")]
        self.assertEqual([d["key"] for d in self.cq.build(e)["dist"]], ["q1:B"])
        self.qs["q1"]["distractors"] = {"B": {"tempting": "x"}}
        self.assertEqual(self.cq.build(e)["dist"], [])
        self.qs["q1"].update(type="imaging", distractors={})             # 영상 문항은 빌더 파생물 — 제외
        self.assertEqual(self.cq.build(e)["dist"], [])

    def test_figure_queue_question_then_assess(self):
        import concept_figures as cf
        pool = {"PTBXL-1": {"asset_id": "PTBXL-1", "source_id": "PTBXL", "status": "AUTO_READY", "file": "x.png",
                            "license_name": "CC BY 4.0", "label": {"grade": "A", "primary": "atrial flutter", "primary_code": "AFLT",
                                                                 "scp_codes": {"AFLT": 100.0}}}}
        self.qs["img1"] = {"type": "imaging", "objective": "cn.derm.a.b", "attribution": {"asset_id": "PTBXL-1"}}
        orig = cf.load_pool
        cf.load_pool = lambda builder=None: pool
        try:
            q = self.cq.build([])
            kinds = [(f["kind"], f["concept"]) for f in q["figure"]]
            self.assertEqual(kinds[0], ("question", "cn.derm.a.b"))
            self.assertIn(("assess", "cn.derm.a.b"), kinds)
            self.concepts["cn.derm.a.b"]["figures_none"] = "그림이 필요 없는 주제"
            self.assertNotIn(("assess", "cn.derm.a.b"), [(f["kind"], f["concept"]) for f in self.cq.build([])["figure"]])
        finally:
            cf.load_pool = orig

    def test_correct_answers_do_not_queue(self):
        e = [right("e1", "q2", "cn.derm.c.d", "2026-09-20T01:00:00Z", "2026-09-20")]
        q = self.cq.build(e)
        self.assertEqual((q["note"], q["link"]), ([], []))


class NewQuestionsNeedObjective(unittest.TestCase):
    def _doc(self, date):
        from frontmatter import Doc
        return Doc(path=Path("x.md"), body="", meta={"type": "kmle", "date": date, "id": "kmle-2026-9999",
                                                     "topic": "t", "confidence": "high", "answer_separated": True,
                                                     "stem": "x", "choices": ["A. a", "B. b"], "answer": "A"})

    def test_warn_only_after_cutoff(self):
        import lint_questions as L
        from concepts import OBJECTIVE_REQUIRED_FROM
        codes = lambda d: [f.code for f in L.lint_doc(d)]
        self.assertIn("objective-missing", codes(self._doc(OBJECTIVE_REQUIRED_FROM)))
        self.assertNotIn("objective-missing", codes(self._doc("2026-09-18")))   # 옛 문항은 막지 않는다
        d = self._doc(OBJECTIVE_REQUIRED_FROM)
        d.meta["objective"] = "cn.x.y.z"
        self.assertNotIn("objective-missing", codes(d))


class TransientSourceErrors(_FixtureSources):
    """요청 제한(429)은 「출처 개정」이 아니다 — 학습서에 경고를 찍지 않는다(2026-09-21)."""

    def test_rate_limit_keeps_status_and_does_not_flag_the_book(self):
        from urllib.error import HTTPError
        self.assertTrue(cs.transient(HTTPError("u", 403, "Forbidden", {}, None)))          # 출판사 봇 차단
        self.assertFalse(cs.transient(HTTPError("u", 410, "Gone", {}, None)))
        self.assertTrue(cs.transient(HTTPError("u", 429, "Too Many Requests", {}, None)))
        self.assertTrue(cs.transient(TimeoutError()))
        self.assertFalse(cs.transient(HTTPError("u", 404, "Not Found", {}, None)))
        self.assertFalse(cs.transient(ValueError("지문을 읽지 못했다")))

    def test_rate_limited_run_keeps_the_previous_verdict(self):
        from urllib.error import HTTPError
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "sc.json"
            xml = "<PubmedArticleSet><PubmedArticle></PubmedArticle></PubmedArticleSet>"
            ok = lambda url: xml if "eutils" in url else "HYPERKALAEMIA GUIDELINE - JULY 2022 V2.pdf"
            first = cs.run(getter=ok, out=out, today="2026-09-20")
            self.assertTrue(all(v["status"] == "ok" for v in first.values()))

            def limited(url):
                raise HTTPError(url, 429, "Too Many Requests", {}, None)
            r = cs.run(getter=limited, out=out, today="2026-09-21")
            net = {k: v for k, v in r.items() if v.get("method") != "manual"}
            self.assertTrue(net)
            for v in net.values():
                self.assertEqual(v["status"], "ok")                   # 배너를 찍지 않는다
                self.assertIn("일시 오류", v["note"])
                self.assertNotIn("업데이트 확인 필요", v["note"])

            r = cs.run(getter=ok, out=out, today="2026-09-22")        # 다음 실행에서 정상 확인
            self.assertTrue(all("일시 오류" not in v["note"] for v in r.values()))


class OutlineFrame(unittest.TestCase):
    """과별 기본틀(해리슨 서술 순서) — 2026-09-21 사용자 요청."""

    def test_frame_is_complete_and_unambiguous(self):
        books, errs = ol.load()
        self.assertEqual(errs, [])                            # 빠진 장·중복 장·모르는 책 이름이 없다
        self.assertIn("순환기내과", books)
        ids = [s.id for slots in books.values() for s in slots]
        self.assertEqual(len(ids), len(set(ids)))

    def test_harrison_toc_matches_known_anchors(self):
        self.assertEqual(ht.main(["--check"]), 0)             # PDF 없이 JSON 만으로 검사(Actions 에서도 돈다)

    def test_harrison22_map_is_complete_and_keeps_known_anchors(self):
        # 2026-10-31: 대조는 해리슨 22판 DB. 슬롯 id 는 21판 장 번호 그대로 두고 from21 로 22판 장을 찾는다.
        h = ol.load_h22()
        self.assertEqual(h.get("edition"), 22)
        toc21 = ol.load_toc()
        self.assertEqual(set(h["from21"]), {str(n) for n in toc21})                 # 21판 모든 장에 대응(빈 목록 = 22판에 없음)
        self.assertTrue(all(c.get("doc") for c in h["chapters"].values()))          # 22판 모든 장에 드라이브 문서
        self.assertEqual(ol.to22([42], h), [44])                                     # 심잡음 42장 → 44장
        self.assertEqual(ol.to22([17], h), [18, 19])                                 # 등·목 통증 → 두 장
        self.assertEqual(ol.to22([417], h), [])                                      # 퓨린 대사 — 22판에 없음
        idx = ol.index(ol.load()[0])
        self.assertEqual(idx["h42"].chapters22, [44])
        self.assertEqual(idx["h42"].source, "해리슨 22판 44장")
        self.assertEqual(idx["h417"].source, "해리슨 21판 417장")                   # 22판에 없으면 21판으로 돌아간다

    def test_range_parsing(self):
        self.assertEqual(ol.parse_range("236-238"), [236, 237, 238])
        self.assertEqual(ol.parse_range("392"), [392])
        self.assertEqual(ol.parse_range([21, "41-42"]), [21, 41, 42])

    def test_units_follow_frame_order_and_unplaced_go_last(self):
        base, _ = C.load_concepts()
        c_late = copy.deepcopy(base["cn.cardio.long-qt-syndrome.first-line-drug"])      # outline h255
        c_early = copy.deepcopy(c_late)
        c_early.update(id="cn.cardio.ecg.basics", title="심전도 기초", outline="h240")   # 해리슨 240장(심전도)
        c_none = copy.deepcopy(c_late)
        c_none.update(id="cn.cardio.unplaced.x", title="아직 배치 안 함", outline=None)
        concepts = {c["id"]: c for c in (c_late, c_early, c_none)}
        qs = {f"q{i}": {"topic": "Cardiology", "objective": c["id"], "choices": []}
              for i, c in enumerate(concepts.values())}
        ev = [wrong(f"e{i}", f"q{i}", c["id"], "2026-09-20T01:00:00Z", "2026-09-20")
              for i, c in enumerate(concepts.values())]
        units = bb.plan(concepts, qs, ll.states(ev), bb.load_config(), {})["순환기내과"].units
        self.assertEqual([u.key for u in units], [c_early["id"], c_late["id"], c_none["id"]])
        self.assertTrue(units[0].group)                        # 차례의 중간 머리글(해리슨 절 이름)

    def test_unknown_slot_is_an_error_and_missing_slot_is_a_warning(self):
        base, _ = C.load_concepts()
        c = copy.deepcopy(base["cn.cardio.long-qt-syndrome.first-line-drug"])
        c["outline"] = "h9999"
        self.assertTrue(any("기본틀에 없다" in e for e in C.validate_concept(c)))
        c.pop("outline")
        errs = C.validate_concept(c)
        self.assertTrue(any("[WARN]" in e and "outline" in e for e in errs))
        self.assertFalse([e for e in errs if "[WARN]" not in e])

    def test_harrison_check_is_the_default(self):
        base, _ = C.load_concepts()
        c = copy.deepcopy(base["cn.derm.pityriasis-versicolor.treatment"])            # 슬롯 h57(해리슨 57장)
        self.assertFalse([e for e in C.validate_concept(c) if "해리슨 대조 없음" in e])
        c["sources"] = [x for x in c["sources"] if not str(x.get("id", "")).startswith("harrison")]
        self.assertTrue([e for e in C.validate_concept(c) if "[WARN]" in e and "해리슨 대조 없음" in e])
        peds = copy.deepcopy(base["cn.peds.febrile-seizure.workup"])                  # 손 슬롯 — 해리슨 대상 아님
        self.assertFalse([e for e in C.validate_concept(peds) if "해리슨 대조 없음" in e])

    def test_export_warns_do_not_block_publish(self):
        # 2026-09-23 실측: 해리슨 대조 없음 [WARN] 하나가 export_concepts_web 을 exit 1 로 만들어
        # publish.py 가 그날 문항 32개까지 통째로 못 올렸다. WARN 은 보고만, ERROR 만 막는다(concepts.py CLI 와 동일).
        import export_concepts_web as ex
        self.assertEqual(ex.blocking(["a.md: [WARN] 해리슨 대조 없음 — …", "b.md: [WARN] outline 없음"]), [])
        self.assertEqual(ex.blocking(["a.md: [WARN] x", "b.md: sources 가 비어 있다"]), ["b.md: sources 가 비어 있다"])

    def test_new_confusion_on_existing_note_is_a_touch_not_a_new_note(self):
        base, _ = C.load_concepts()
        c = base["cn.cardio.long-qt-syndrome.first-line-drug"]
        q = {"topic": "Cardiology", "objective": c["id"],
             "choices": ["A. 프로프라놀롤", "B. 아미오다론", "C. 소탈롤", "D. 플레카이니드", "E. 딜티아젬"]}
        ev = [wrong("e1", "qx", c["id"], "2026-09-22T01:00:00Z", "2026-09-22", text="딜티아젬")]
        S = ll.states(ev)
        touches = cq._touches(S[c["id"]], c, {"qx": q})
        self.assertEqual([t["cover"] for t in touches], ["qx:E"])              # 새 혼동 → 손질 1건
        c2 = dict(c, pitfalls=list(c["pitfalls"]) + [{"contrast": "x", "point": "y", "covers": ["qx:E"]}])
        self.assertEqual(cq._touches(S[c["id"]], c2, {"qx": q}), [])           # 이미 다룬 혼동이면 할 일 없음

    def test_gap_queue_continues_after_the_last_written_slot(self):
        base, _ = C.load_concepts()
        c = copy.deepcopy(base["cn.neph.hyperkalemia.first-step"])                      # outline h53
        gaps = cq._gaps({c["id"]: c}, {}, {})
        neph = next(g for g in gaps if g["book"] == "신장내과")
        self.assertEqual(neph["slot"], "h54")                  # 앞(h51)이 아니라 쓴 자리 다음

    def test_gap_queue_puts_the_thinnest_book_first(self):
        # 2026-11-23 — 많은 책 먼저였을 때 루틴이 하루 하나씩 같은 과만 채웠다(10월 류마티스 12 · 11월 순환기 23).
        base, _ = C.load_concepts()
        cardio = [copy.deepcopy(c) for c in base.values() if c.get("topic") == "Cardiology"][:3]
        neph = copy.deepcopy(base["cn.neph.hyperkalemia.first-step"])
        concepts = {c["id"]: c for c in cardio + [neph]}
        gaps = cq._gaps(concepts, {}, {})
        self.assertEqual([(g["book"], g["have"]) for g in gaps], [("신장내과", 1), ("순환기내과", 3)])
        # 하나 채우면 그 책이 뒤로 물러난다 — 같은 수가 되면 기본틀 순서(순환기내과가 신장내과보다 앞)
        more = [dict(copy.deepcopy(neph), id=f"cn.neph.x{i}", outline="") for i in range(2)]
        gaps = cq._gaps({**concepts, **{c["id"]: c for c in more}}, {}, {})
        self.assertEqual([g["book"] for g in gaps], ["순환기내과", "신장내과"])
        real = cq._gaps(base, {}, {})
        # 같은 날 뒤이은 사용자 결정(국시 핵심 공백 과목 먼저 — `gap_priority`)으로 기대값을 고쳤다: 「적은 책 먼저」는
        # 전체가 아니라 **묶음 안에서** 성립한다 — 핵심 책(기준 수 미만) 묶음이 앞, 나머지가 뒤, 각 묶음 안은 적은 책부터.
        keys = [(not g["core"], g["have"]) for g in real]
        self.assertEqual(keys, sorted(keys))
        core_books, until = cq.gap_priority(cq._books_cfg())
        self.assertTrue(all(g["book"] in core_books and g["have"] < until for g in real if g["core"]))
        self.assertTrue(all(g["have"] > 0 for g in real))                        # 0개인 책은 오답이 이끈다
        # 기초의학 학문별 책은 [gap] 대상이 아니다 — 기초 정리본은 [root] 에서만(2026-11-21 사용자 결정)
        import yaml
        cfg = yaml.safe_load((ROOT / "pipelines" / "books_config.yaml").read_text(encoding="utf-8"))
        basic = dict(next(c for c in base.values() if C.is_basic(c)))
        self.assertIn(cfg["books"].get(basic["topic"]), set(cfg["disciplines"].values()))
        self.assertFalse({g["book"] for g in real} & set(cfg["disciplines"].values()))
        self.assertEqual(cq._gaps({basic["id"]: basic}, {}, {}), [])

    def test_quiz_deck_rotates_subjects_least_solved_first(self):
        # 2026-11-23 — 번들이 id 내림차순(= 과목 영어 이름 역순)이라 섞기를 끄면 늘 류마티스부터 나왔다.
        app = (ROOT / "docs" / "app.js").read_text(encoding="utf-8")
        self.assertIn('const BALANCED_MODES = ["latest", "unsolved"];', app)     # 오늘 다시 풀 것 · 오답노트는 그대로
        self.assertIn('if (!$("shuffle").checked) return orderedList();', app)
        a, b = app.index("/* <subject-balance>"), app.index("/* </subject-balance> */")
        block = app[a:b]
        self.assertNotIn("$(", block)                                            # DOM 없이 도는 덩이
        node = shutil.which("node")
        if not node:
            self.skipTest("node 없음")
        subs = ["Cardiology", "Neurology", "Pulmonology", "Rheumatology"]
        qs = [{"id": f"q{d}{s[0]}{i}", "subject": s, "created": d}
              for d in ("2026-11-22", "2026-11-23") for s in reversed(subs) for i in (1, 2)]
        days = [f"2026-11-{d}" for d in range(23, 29)]
        script = (block + ";const qs=" + json.dumps(qs) + ";"
                  "const run=(c,day)=>balanceBySubject(qs,c,day).map(q=>q.created+'|'+q.subject);"
                  "const c={Rheumatology:14,Pulmonology:3};"
                  "console.log(JSON.stringify({a:run(c,'2026-11-23'),b:run(c,'2026-11-23'),"
                  "days:" + json.dumps(days) + ".map(d=>run({},d)[0]),"
                  "cnt:solvedBySubject(qs.concat(qs),new Set(['q2026-11-23C1','q2026-11-22C2','zz']))}));")
        r = subprocess.run([node, "-e", script], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        a = out["a"]
        self.assertEqual(a, out["b"])                                            # 같은 날 · 같은 기록이면 같은 순서
        self.assertEqual(len(a), len(qs))
        self.assertTrue(all(x.startswith("2026-11-23|") for x in a[:8]))         # 최신 날짜 묶음 먼저
        first = [x.split("|")[1] for x in a[:4]]
        self.assertEqual(sorted(first), sorted(subs))                            # 한 바퀴에 과목마다 한 문항
        self.assertEqual(first[2:], ["Pulmonology", "Rheumatology"])             # 많이 푼 과목이 뒤
        self.assertEqual([x.split("|")[1] for x in a[4:8]], first)               # 둘째 바퀴도 같은 순서 — 한 과가 붙지 않는다
        self.assertGreater(len(set(out["days"])), 1)                             # 푼 수가 같으면 날마다 시작 과목이 다르다
        self.assertEqual(out["cnt"], {"Cardiology": 2})                          # 겹친 문항은 한 번만


class ConceptFigures(unittest.TestCase):
    """정리본 그림(2026-09-27) — 확실한 라벨만 · 라벨은 풀 기록에서 · 공개 저장소에 실을 수 있는 라이선스."""

    def setUp(self):
        import concept_figures as cf
        self.cf = cf
        self.ptbxl = {"asset_id": "PTBXL-1", "source_id": "PTBXL", "status": "AUTO_READY", "file": "PTBXL/x.png", "modality": "ECG",
                      "license_name": "Creative Commons Attribution 4.0 International",
                      "gates": {"rights": {"status": "PASS"}, "privacy": {"status": "PASS"}},
                      "label": {"grade": "A", "primary": "atrial flutter", "primary_code": "AFLT", "scp_codes": {"AFLT": 100.0}}}

    def test_eligibility_accepts_expert_label_and_rejects_author_reads(self):
        cf = self.cf
        self.assertEqual(cf.eligibility(self.ptbxl), [])
        self.assertIn("가능도 100", cf.dataset_label(self.ptbxl))
        weak = copy.deepcopy(self.ptbxl); weak["label"]["scp_codes"]["AFLT"] = 50.0
        self.assertTrue(any("가능도" in w for w in cf.eligibility(weak)))
        lidc = dict(self.ptbxl, source_id="TCIA_LIDC_IDRI")
        self.assertTrue(any("작성자 판독" in w for w in cf.eligibility(lidc)))
        nc = dict(self.ptbxl, license_name="CC BY-NC 4.0")
        self.assertTrue(any("라이선스" in w for w in cf.eligibility(nc)))
        isic = dict(self.ptbxl, source_id="ISIC", label={"grade": "A", "primary": "Nevus", "confirm_type": "single image expert consensus"})
        self.assertTrue(any("조직병리" in w for w in cf.eligibility(isic)))
        gone = dict(self.ptbxl, status="REJECTED")
        self.assertTrue(any("폐기" in w for w in cf.eligibility(gone)))

    def _fig(self, root, **kw):
        (root / "docs" / "assets" / "figures").mkdir(parents=True, exist_ok=True)
        (root / "docs" / "assets" / "figures" / "a.png").write_bytes(b"x")
        f = {"id": "f1", "file": "docs/assets/figures/a.png", "kind": "ecg", "at": "진단", "shows": "톱니 모양 F파",
             "look_for": ["II·III·aVF"], "label": "atrial flutter", "label_basis": "dataset_expert", "reference": "전문의 판독",
             "paper": "Wagner 2020", "doi": "10.1038/x", "credit": "PTB-XL", "license": "CC BY 4.0", "asset": "PTBXL-1"}
        f.update(kw)
        return f

    def test_contract(self):
        cf = self.cf
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            ok = {"figures": [self._fig(root)]}
            self.assertEqual(cf.validate_figures(ok, ["진단"], root), [])
            model = {"figures": [self._fig(root, label_basis="model_read")]}
            self.assertTrue(any("모델 판독" in e for e in cf.validate_figures(model, ["진단"], root)))
            nopaper = {"figures": [self._fig(root, paper="")]}
            self.assertTrue(any("데이터 논문" in e for e in cf.validate_figures(nopaper, ["진단"], root)))
            outside = {"figures": [self._fig(root, file="https://x/y.png")]}
            self.assertTrue(any("docs/assets/figures" in e for e in cf.validate_figures(outside, ["진단"], root)))
            wrong_at = {"figures": [self._fig(root, at="없는 절")]}
            self.assertTrue(any("절이 본문에 없다" in e for e in cf.validate_figures(wrong_at, ["진단"], root)))
            many = {"figures": [self._fig(root, id=f"f{i}") for i in range(1, 5)]}
            self.assertTrue(any("3개까지" in e for e in cf.validate_figures(many, ["진단"], root)))
            both = {"figures": [self._fig(root)], "figures_none": "그림이 필요 없는 주제"}
            self.assertTrue(any("하나만" in e for e in cf.validate_figures(both, ["진단"], root)))

    def test_lidc_only_contour_selected_slices(self):
        cf = self.cf
        base = {"asset_id": "L1", "source_id": "TCIA_LIDC_IDRI", "status": "AUTO_READY", "file": "x.png", "modality": "CT",
                "license_name": "Creative Commons Attribution 3.0 Unported", "gates": {"rights": {"status": "PASS"}, "privacy": {"status": "PASS"}},
                "label": {"grade": "B", "primary": "chest CT lung window"}}
        self.assertTrue(any("작성자 판독" in w for w in cf.eligibility(base)))
        good = copy.deepcopy(base)
        good["label"] = {"grade": "A", "primary": "pulmonary nodule — solid",
                         "annotation": {"source": "LIDC XML", "readers_on_slice": 4, "diameter_mm_est": 21.4,
                                        "characteristics_mean": {"malignancy": 4.25}}}
        self.assertEqual(cf.eligibility(good), [])
        self.assertIn("4/4", cf.dataset_label(good))
        self.assertIn("병리 확진 아님", cf.dataset_label(good))
        two = copy.deepcopy(good); two["label"]["annotation"]["readers_on_slice"] = 2
        self.assertTrue(cf.eligibility(two))

    def test_request_key_matches_exam_builder(self):
        # exam-builder opendata/demand.py request_key 와 같은 벡터(PMC 그림 ↔ 요청 연결)
        self.assertEqual(self.cf.request_key("cn.x.y.z", {"source": "PMC_OA", "query": "q"}), "9b23ada3fb8c")

    def test_wanted_is_fulfilled_only_by_eligible_matching_asset(self):
        cf = self.cf
        pool = {"PTBXL-1": self.ptbxl, "PTBXL-2": dict(self.ptbxl, asset_id="PTBXL-2", status="REJECTED")}
        self.assertEqual(cf.wanted_fulfilled({"source": "PTBXL", "codes": ["AFLT"], "shows": "x"}, pool), ["PTBXL-1"])
        self.assertEqual(cf.wanted_fulfilled({"source": "PTBXL", "codes": ["AFIB"], "shows": "x"}, pool), [])
        self.assertEqual(cf.wanted_fulfilled({"source": "ISIC", "codes": ["AFLT"], "shows": "x"}, pool), [])

    def test_set_fm_key_changes_one_key_and_bumps_version(self):
        cf = self.cf
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "c.md"
            p.write_text("---\nid: cn.x.y.z\n# 주석은 남는다\nversion: 2\ntitle: \"제목\"\n---\n## 진단\n본문\n", encoding="utf-8")
            cf.set_fm_key(p, "figures_none", "그림이 필요 없는 주제", bump=False)
            cf.set_fm_key(p, "figures", [{"id": "f1"}])
            t = p.read_text(encoding="utf-8")
            self.assertIn("# 주석은 남는다", t)
            self.assertIn("version: 3", t)
            self.assertIn("figures:\n- id: f1", t)
            cf.set_fm_key(p, "figures_none", None, bump=False)
            self.assertNotIn("figures_none", p.read_text(encoding="utf-8"))
            self.assertTrue(p.read_text(encoding="utf-8").endswith("## 진단\n본문\n"))

    def test_figure_sizes_keep_aspect_in_one_column(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "docs" / "assets" / "figures").mkdir(parents=True)
            Image.new("RGB", (2236, 1385), "white").save(root / "docs/assets/figures/e.png")
            Image.new("RGB", (800, 1000), "white").save(root / "docs/assets/figures/x.jpg")
            old = bb.ROOT
            bb.ROOT = root
            try:
                kind, h, info = bb.figure_html(self._fig(root, file="docs/assets/figures/e.png"))
                self.assertEqual((kind, info["place"]), ("flow", "column"))      # 심전도도 한 단 폭(폭이 중간에 바뀌지 않게)
                self.assertAlmostEqual(info["w"], bb.COLW - 3, places=1)
                self.assertIn("데이터 라벨", h)
                kind, h, info = bb.figure_html(self._fig(root, file="docs/assets/figures/x.jpg", kind="radiograph"))
                self.assertEqual(kind, "flow")
                self.assertAlmostEqual(info["w"] / info["h"], 0.8, places=2)
                self.assertLessEqual(info["h"], bb.FIG_MAX_H + 0.1)
            finally:
                bb.ROOT = old


class BasicRoots(unittest.TestCase):
    """기초 뿌리(2026-11-21) — 임상 정리본의 roots 계약 · [root] 큐 · 기초의학 학문별 책."""

    BASIC = {"id": "cn.physio.x.y", "topic": "Physiology", "layer": "basic", "discipline": "physiology",
             "system": "renal", "textbook_check": "pending"}

    def test_root_fields_contract(self):
        E = C.root_errors
        self.assertEqual(E({"id": "cn.neph.a.b"}), [])                                   # 옛 정리본은 그대로 통과
        self.assertEqual(E({"id": "cn.neph.a.b", "roots": ["cn.physio.x.y"]}), [])
        self.assertEqual(E({"id": "cn.neph.a.b", "roots_none": "검진 주기 — 기전으로 내려가지 않는다"}), [])
        self.assertTrue(any("함께 쓰지" in e for e in E({"id": "cn.neph.a.b", "roots": ["cn.physio.x.y"], "roots_none": "x"})))
        self.assertTrue(any("id 목록" in e for e in E({"id": "cn.neph.a.b", "roots": "cn.physio.x.y"})))
        self.assertTrue(any("자기 자신" in e for e in E({"id": "cn.neph.a.b", "roots": ["cn.neph.a.b"]})))
        self.assertTrue(any("이유" in e for e in E({"id": "cn.neph.a.b", "roots_none": " "})))
        self.assertTrue(any("discipline" in e for e in E({"id": "cn.neph.a.b", "discipline": "nephrology"})))
        self.assertEqual(E({"id": "cn.path.a.b", "discipline": "pathology"}), [])        # 임상 정리본의 학문 꼬리표

    def test_basic_note_contract(self):
        E, b = C.root_errors, self.BASIC
        self.assertEqual(E(b), [])
        self.assertTrue(any("system" in e for e in E(dict(b, system="kidney"))))
        self.assertTrue(any("학문별 책" in e for e in E(dict(b, topic="Nephrology"))))      # 학문 책으로 가지 않는 topic
        self.assertTrue(any("textbook_check 가 필요" in e for e in E({k: v for k, v in b.items() if k != "textbook_check"})))
        self.assertTrue(any("전공 교과서 출처" in e for e in E(dict(b, textbook_check="checked"))))
        ok = dict(b, textbook_check="checked", sources=[{"id": "guyton-14", "kind": "textbook", "verified": "text"}])
        self.assertEqual(E(ok), [])
        harrison_only = dict(b, textbook_check="checked", sources=[{"id": "harrison-22", "kind": "textbook", "verified": "text"}])
        self.assertTrue(any("전공 교과서 출처" in e for e in E(harrison_only)))             # 해리슨은 전공 교과서가 아니다
        self.assertTrue(any("달지 않는다" in e for e in E(dict(b, roots_none="x"))))
        self.assertTrue(any("[WARN]" in e and "unavailable" in e for e in
                            E(dict(b, topic="Biochemistry", discipline="biochemistry"))))   # 교과서 없는 학문의 pending

    def test_roots_must_point_to_existing_basic_notes(self):
        cs = {"cn.neph.a.b": {"id": "cn.neph.a.b", "roots": ["cn.physio.x.y", "cn.neph.c.d", "cn.none.x.y"]},
              "cn.neph.g.h": {"id": "cn.neph.g.h", "roots": ["cn.physio.x.y"]},
              "cn.physio.x.y": {"id": "cn.physio.x.y", "layer": "basic"},
              "cn.neph.c.d": {"id": "cn.neph.c.d"}}
        errs = C.root_link_errors(cs)
        self.assertEqual(list(errs), ["cn.neph.a.b"])
        self.assertEqual(len(errs["cn.neph.a.b"]), 2)                                    # 임상 정리본을 가리킴 · 없는 정리본
        self.assertEqual(C.root_supports(cs)["cn.physio.x.y"], ["cn.neph.a.b", "cn.neph.g.h"])   # 기전 하나가 임상 여러 개를 받친다

    def test_root_queue_only_new_wrongs_on_clinical_notes_without_roots(self):
        concepts = {"cn.neph.a.b": {"id": "cn.neph.a.b", "title": "임상", "topic": "Nephrology"},
                    "cn.neph.c.d": {"id": "cn.neph.c.d", "roots": ["cn.physio.x.y"]},
                    "cn.neph.e.f": {"id": "cn.neph.e.f", "roots_none": "검진 주기"},
                    "cn.physio.x.y": {"id": "cn.physio.x.y", "layer": "basic"},
                    "cn.neph.old.old": {"id": "cn.neph.old.old"}}
        qs = {f"q{i}": {"topic": "Nephrology", "objective": o} for i, o in enumerate(concepts, 1)}
        orig = (cq.load_concepts, cq.load_questions)
        cq.load_concepts, cq.load_questions = (lambda: (concepts, [])), (lambda: qs)
        try:
            e = [wrong(f"e{i}", f"q{i}", o, "2026-11-22T01:00:00Z", "2026-11-22") for i, o in enumerate(list(concepts)[:4], 1)]
            e.append(wrong("e5", "q5", "cn.neph.old.old", "2026-11-01T01:00:00Z", "2026-11-01"))   # 기준일 전 오답 — 소급하지 않는다
            q = cq.build(e)
        finally:
            cq.load_concepts, cq.load_questions = orig
        self.assertEqual([r["objective"] for r in q["root"]], ["cn.neph.a.b"])
        self.assertEqual(q["counts"]["root"], 1)

    def test_discipline_book_lists_units_printed_in_other_books(self):
        cfg = bb.load_config()
        self.assertEqual(cfg["books"]["Physiology"], "생리학")                            # 「기초의학」 한 권이 아니다
        self.assertNotIn("기초의학", cfg["books"].values())
        base, _ = C.load_concepts()
        clin = copy.deepcopy(base["cn.derm.pityriasis-versicolor.treatment"])
        clin["discipline"] = "physiology"                                                # 피부과 책에 실린 채 꼬리표만
        basic = copy.deepcopy(clin)
        basic.update(self.BASIC, title="기초 단원")
        other = copy.deepcopy(clin)
        other.update(id="cn.derm.other.other", title="꼬리표 없는 단원")
        del other["discipline"]
        concepts = {c["id"]: c for c in (clin, basic, other)}
        books = bb.plan(concepts, {}, ll.states([]), cfg, {})
        self.assertEqual(books["생리학"].elsewhere, [(clin["title"], "피부과")])
        self.assertEqual(books["피부과"].elsewhere, [])
        self.assertEqual([u.key for u in books["생리학"].units], ["cn.physio.x.y"])       # 본문은 한 책에만
        self.assertIn("전공 교과서 미대조", books["생리학"].units[0].flags)
        self.assertNotIn("전공 교과서 미대조", [f for u in books["피부과"].units for f in u.flags])
        us = books["생리학"].units
        h0 = bb.volume_hash("생리학", us, [], cfg, {})
        self.assertEqual(h0, bb.volume_hash("생리학", us, [], cfg, {}, []))               # 목록이 없으면 해시는 그대로
        self.assertNotEqual(h0, bb.volume_hash("생리학", us, [], cfg, {}, books["생리학"].elsewhere))
        fonts = {"regular": bb.find_font(cfg["fonts"]["regular"]), "bold": bb.find_font(cfg["fonts"]["bold"])}
        html_text, _ = bb.book_html("생리학", [], cfg, {}, {"version": 1, "date": "2026-11-21",
                                                         "elsewhere": books["생리학"].elsewhere}, None, fonts, [])
        self.assertIn("다른 책에 실린 생리학 단원", html_text)
        self.assertIn("(피부과)", html_text)
        plain, _ = bb.book_html("피부과", [], cfg, {}, {"version": 1, "date": "2026-11-21"}, None, fonts, [])
        self.assertNotIn("다른 책에 실린", plain)

    def test_discipline_books_have_outline_slots(self):
        books, errs = ol.load()
        self.assertEqual(errs, [])
        cfg = bb.load_config()
        for book in set(cfg["disciplines"].values()):
            self.assertTrue(books.get(book), book)                                       # 학문별 책마다 기본틀 슬롯
        self.assertTrue(set(cfg["textbooks"]) <= set(cfg["disciplines"]))


class QueueWeightsBackfillVerify(unittest.TestCase):
    """2026-11-23 사용자 결정 — [gap] 국시 핵심 공백 과목 먼저 · [root] 반복 오답 상위 20 소급 · [verify] · 분량·중복 린트.
    모두 지어낸 정리본 사전으로만 본다(실제 콘텐츠를 읽지 않는다)."""

    TOPIC = {"소화기내과": "Gastroenterology", "신경과": "Neurology", "외과": "Surgery",
             "순환기내과": "Cardiology", "신장내과": "Nephrology"}

    def _cfg(self, **gp):
        import yaml
        cfg = yaml.safe_load((ROOT / "pipelines" / "books_config.yaml").read_text(encoding="utf-8"))
        cfg.pop("gap_priority", None)
        if gp:
            cfg["gap_priority"] = gp
        return cfg

    def _notes(self, **counts):
        """{책 이름: 개수} → 슬롯을 차지하지 않는 정리본 사전(outline 빈칸 — 책마다 첫 빈 슬롯이 [gap] 으로 나온다)."""
        out = {}
        for book, n in counts.items():
            for i in range(n):
                cid = f"cn.t.{self.TOPIC[book].lower()}.n{i}"
                out[cid] = {"id": cid, "topic": self.TOPIC[book], "outline": ""}
        return out

    def test_real_config_names_the_six_core_books(self):
        books, until = cq.gap_priority(cq._books_cfg())
        self.assertEqual(books, {"혈액종양내과", "소화기내과", "신경과", "감염내과", "내분비내과", "외과"})
        self.assertEqual(until, 12)
        cfg = bb.load_config()
        self.assertTrue(books <= set(cfg["books"].values()))                    # 책 이름이 topic → 책 표에 있다
        self.assertTrue(books <= set(ol.load()[0]))                              # 기본틀에도 있다
        self.assertFalse(books & set(cfg["disciplines"].values()))              # 기초의학 학문별 책은 아니다

    def test_gap_core_books_come_first_until_they_reach_the_threshold(self):
        cfg = self._cfg(books=["소화기내과", "신경과", "외과"], until=3)        # 외과는 0개 — 핵심 책이라도 넣지 않는다
        notes = self._notes(순환기내과=1, 소화기내과=2, 신경과=1)
        gaps = cq._gaps(notes, {}, {}, cfg)
        self.assertEqual([(g["book"], g["have"], g["core"]) for g in gaps],
                         [("신경과", 1, True), ("소화기내과", 2, True), ("순환기내과", 1, False)])
        self.assertEqual(gaps[0]["core_until"], 3)
        self.assertNotIn("core_until", gaps[-1])
        self.assertTrue({"book", "slot", "title", "source", "chapters", "have"} <= set(gaps[0]))   # 옛 필드는 그대로
        # 기준 수(3)에 이른 책은 앞 묶음에서 빠져 일반 순서로 간다
        gaps = cq._gaps(self._notes(순환기내과=1, 소화기내과=2, 신경과=3), {}, {}, cfg)
        self.assertEqual([(g["book"], g["core"]) for g in gaps],
                         [("소화기내과", True), ("순환기내과", False), ("신경과", False)])
        # 핵심 책이 모두 기준 수에 이르면 가중치가 없을 때와 똑같다
        full = self._notes(순환기내과=1, 소화기내과=3, 신경과=4, 신장내과=2)
        self.assertEqual([g["book"] for g in cq._gaps(full, {}, {}, cfg)],
                         [g["book"] for g in cq._gaps(full, {}, {}, self._cfg())])
        self.assertFalse(any(g["core"] for g in cq._gaps(full, {}, {}, cfg)))

    def test_gap_without_the_config_key_is_the_old_thinnest_first_order(self):
        notes = self._notes(순환기내과=3, 소화기내과=5, 신경과=2, 신장내과=1)
        order = {b: i for i, b in enumerate(ol.load()[0])}
        want = sorted(((n, order[b]), b) for b, n in (("순환기내과", 3), ("소화기내과", 5), ("신경과", 2), ("신장내과", 1)))
        for cfg in (self._cfg(), self._cfg(books=[], until=12), self._cfg(books=["소화기내과"]),
                    self._cfg(books=["소화기내과"], until=0), self._cfg(books="소화기내과", until=12)):
            gaps = cq._gaps(notes, {}, {}, cfg)
            self.assertEqual([g["book"] for g in gaps], [b for _, b in want])   # 적은 책 먼저 · 같으면 기본틀 순서
            self.assertFalse(any(g["core"] for g in gaps))
        self.assertEqual(cq.gap_priority({}), (set(), 0))

    def test_gap_weight_has_no_feedback_loop(self):
        """루틴은 맨 앞 [gap] 하나만 쓴다 — 하나 쓰면 그 책이 물러나야 한다(한 과만 불어나면 안 된다)."""
        cfg = self._cfg(books=["소화기내과", "신경과", "외과"], until=4)
        have = {"소화기내과": 1, "신경과": 1, "외과": 2, "순환기내과": 1, "신장내과": 5}
        picks = []
        for _ in range(8):                                                       # 핵심 세 책이 4개씩 되기까지 3 + 3 + 2 = 8번
            g = cq._gaps(self._notes(**have), {}, {}, cfg)[0]
            self.assertTrue(g["core"])
            self.assertEqual(g["have"], min(have[b] for b in ("소화기내과", "신경과", "외과") if have[b] < 4))
            picks.append(g["book"])
            have[g["book"]] += 1
        self.assertEqual({b: have[b] for b in ("소화기내과", "신경과", "외과")}, {"소화기내과": 4, "신경과": 4, "외과": 4})
        self.assertFalse([i for i in range(1, 7) if picks[i] == picks[i - 1]])    # 두 책 이상 남은 동안 같은 책이 연달아 오지 않는다
        # 핵심 책이 모두 기준 수에 이른 뒤에는 전체 「적은 책 먼저」 — 가장 얇은 책(순환기내과 1개)이 앞에 온다
        g = cq._gaps(self._notes(**have), {}, {}, cfg)[0]
        self.assertEqual((g["book"], g["core"]), ("순환기내과", False))

    def _build(self, concepts, events):
        qs = {f"q.{cid}": {"topic": c.get("topic", "Nephrology"), "objective": cid} for cid, c in concepts.items()}
        orig = (cq.load_concepts, cq.load_questions)
        cq.load_concepts, cq.load_questions = (lambda: (concepts, [])), (lambda: qs)
        try:
            return cq.build(events)
        finally:
            cq.load_concepts, cq.load_questions = orig

    def _wrongs(self, cid, n, day="2026-10-01"):
        return [wrong(f"e.{cid}.{day}.{i}", f"q.{cid}", cid, f"{day}T0{i}:00:00Z", day) for i in range(n)]

    def test_root_backfill_is_capped_at_the_top_twenty_repeat_wrongs(self):
        self.assertEqual((cq.ROOT_BACKFILL_TOP, cq.ROOT_BACKFILL_MIN_WRONGS), (20, 2))
        ids = [f"cn.neph.c{i:02d}.x" for i in range(25)]
        concepts = {cid: {"id": cid, "title": cid, "topic": "Nephrology"} for cid in ids}
        concepts["cn.neph.once.x"] = {"id": "cn.neph.once.x", "topic": "Nephrology"}
        concepts["cn.physio.x.y"] = {"id": "cn.physio.x.y", "topic": "Physiology", "layer": "basic"}
        e = []
        for i, cid in enumerate(ids):
            e += self._wrongs(cid, 3 if i >= 22 else 2)                          # 뒤의 셋(c22~c24)만 세 번 — 오답 수가 순위를 정한다
        e += self._wrongs("cn.neph.once.x", 1)                                   # 한 번 틀린 것은 「반복 오답」이 아니다
        e += self._wrongs("cn.physio.x.y", 5)                                    # 기초 정리본은 순위에서 뺀다
        q = self._build(concepts, e)
        top = [r["objective"] for r in q["root"]]
        self.assertEqual(len(top), 20)                                           # 옛 오답 27개 목표 가운데 20개만
        self.assertEqual(top[:3], ids[22:])                                      # 오답 수 → 우선순위 → id
        self.assertEqual(top[3:], ids[:17])
        self.assertTrue(all(r["backfill"] for r in q["root"]))
        self.assertEqual([r["rank"] for r in q["root"]], list(range(1, 21)))
        self.assertEqual(q["counts"]["root_backfill"], 20)
        self.assertNotIn("cn.neph.once.x", top)
        self.assertNotIn("cn.physio.x.y", top)
        # 뿌리를 붙여도 21위가 그 자리를 채우지 않는다 — 상위 20 은 뿌리와 무관하게 뽑는다
        for cid in top[:5]:
            concepts[cid]["roots"] = ["cn.physio.x.y"]
        for cid in top[5:7]:
            concepts[cid]["roots_none"] = "지침 수치"
        left = [r["objective"] for r in self._build(concepts, e)["root"]]
        self.assertEqual(left, top[7:])
        for cid in top[7:]:
            concepts[cid]["roots_none"] = "지침 수치"
        self.assertEqual(self._build(concepts, e)["root"], [])                   # 20개에서 끝난다 — c17~c21 은 다시 틀릴 때만
        # 새로 틀린 목표(기준일 뒤)는 소급 표시 없이 맨 앞에 온다. c20 은 세 번째 오답으로 순위에 들어오고 20위(c16)가 밀려난다
        del concepts[top[10]]["roots_none"]
        del concepts[top[-1]]["roots_none"]
        new = self._wrongs(ids[20], 1, day="2026-11-22")
        rows = self._build(concepts, e + new)["root"]
        self.assertEqual([(r["objective"], r["backfill"]) for r in rows], [(ids[20], False), (top[10], True)])

    def test_verify_queue_counts_marks_and_orders_wrong_first(self):
        marks = C.unverified_marks({"_body": "가 [[?x: p.1]] 나 [[y: 표 2]] 원문 미대조(†)",
                                    "tables": [{"note": "용량은 대조 전(†) [[?z]]", "rows": [["[[?x]]"]]}],
                                    "sections": [{"html": "[[?twice]]"}],          # _body 가 있으면 본문은 한 번만 센다
                                    "errors": ["근거 표시 [[?e]] 가 sources 에 없다"]})
        self.assertEqual(marks, {"claims": 3, "dagger": 2, "marks": 5, "sources": ["x", "z"]})
        self.assertEqual(C.unverified_marks({"sections": [{"html": "<p>나 [[?k: 3장]]</p>"}], "summary": ["결론: 가 [[h: p.1]]"]})["claims"], 1)

        def note(cid, n_claim, n_dag=0):
            return {"id": cid, "title": cid, "topic": "Nephrology", "path": f"content/concepts/{cid}.md",
                    "sections": [{"title": "판단", "deep": False, "html": " ".join(["[[?src-a]]"] * n_claim + ["†"] * n_dag)}]}
        concepts = {c["id"]: c for c in (note("cn.neph.a.x", 1), note("cn.neph.b.x", 5), note("cn.neph.c.x", 2, 1),
                                         note("cn.neph.d.x", 3), note("cn.neph.e.x", 7), note("cn.neph.f.x", 0))}
        e = self._wrongs("cn.neph.a.x", 2) + self._wrongs("cn.neph.b.x", 1)       # a 가 우선순위가 높다(표시는 적다)
        q = self._build(concepts, e)
        self.assertEqual([v["objective"] for v in q["verify"]],
                         ["cn.neph.a.x", "cn.neph.b.x", "cn.neph.e.x", "cn.neph.c.x", "cn.neph.d.x"])   # 오답 → 표시 수 → id
        self.assertEqual([v["wrong"] for v in q["verify"]], [True, True, False, False, False])
        self.assertEqual((q["counts"]["verify"], q["counts"]["verify_marks"]), (5, 19))
        self.assertEqual(q["verify"][3]["dagger"], 1)
        self.assertEqual(q["verify"][0]["sources"], ["src-a"])

    def test_verify_lines_print_only_when_asked(self):
        """[verify] 는 PC 세션 · Actions 전용 — 루틴이 보는 기본 출력에는 건수 한 줄만, JSON 파일에는 늘 있다."""
        import contextlib
        import io
        concepts = {"cn.neph.a.x": {"id": "cn.neph.a.x", "title": "가", "topic": "Nephrology", "path": "p.md",
                                    "sections": [{"title": "판단", "deep": False, "html": "[[?src-a]] †"}]}}
        orig = (cq.load_concepts, cq.load_questions, cq.OUT)
        with tempfile.TemporaryDirectory() as d:
            ev_file = Path(d, "events.json")
            ev_file.write_text("[]", encoding="utf-8")
            cq.load_concepts, cq.load_questions, cq.OUT = (lambda: (concepts, [])), (lambda: {}), Path(d, "queue.json")
            try:
                def run(*args):
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        self.assertEqual(cq.main(["--events", str(ev_file), "--no-wrongnote", *args]), 0)
                    return buf.getvalue()
                plain = run("--limit", "5")
                self.assertIn("미대조 표시 보강 대기(verify) 1건 · 표시 2개", plain)
                self.assertNotIn("[verify]", plain)
                self.assertIn("[verify] cn.neph.a.x", run("--verify"))
                self.assertNotIn('"verify": [', run("--json"))
                self.assertEqual(json.loads(run("--json"))["counts"]["verify"], 1)
                self.assertEqual([v["objective"] for v in json.loads(run("--json", "--verify"))["verify"]], ["cn.neph.a.x"])
                saved = json.loads(Path(d, "queue.json").read_text(encoding="utf-8"))
                self.assertEqual([v["objective"] for v in saved["verify"]], ["cn.neph.a.x"])
            finally:
                cq.load_concepts, cq.load_questions, cq.OUT = orig

    def test_polish_lint_warns_but_never_blocks(self):
        import export_concepts_web as ex
        W = C.polish_warnings
        ok = {"_body": "## 판단 — 왜 먼저인가\n- 가나다라마바사.\n", "summary": ["결론: 다른 이야기를 한 줄로 적는다."],
              "diagram_notes": ["1", "2", "3", "4"], "variants": [{"id": "v1"}]}
        self.assertEqual(W(ok), [])
        kinds = lambda m: [C.polish_kind(x) for x in W(m)]
        # 본문 3,200자 — frontmatter 뒤의 글 전체(앞뒤 공백 · \r 은 세지 않는다)
        self.assertEqual(kinds(dict(ok, _body="\r\n" + "가" * 3200 + "\r\n")), [])
        self.assertEqual(kinds(dict(ok, _body="가" * 3201)), ["분량"])
        self.assertEqual(kinds({k: v for k, v in dict(ok, summary=["가" * 9000]).items() if k != "_body"}), [])   # 본문을 못 받으면 건너뛴다
        self.assertEqual(kinds(dict(ok, diagram_notes=list("12345"))), ["도식 설명"])
        self.assertEqual(kinds(dict(ok, variants=[])), ["변형 없음"])
        self.assertEqual(kinds({k: v for k, v in ok.items() if k != "variants"}), ["변형 없음"])
        # summary 가 「## 판단」 절의 문장을 되풀이 — 머리말 · 글머리표 · 근거 표시 · 굵은 글씨는 떼고 견준다
        sent = "정맥 베타차단제를 먼저 주어 심박수를 분당 60회 안팎으로 낮춘다"
        dup = dict(ok, summary=[f"결론: {sent}.", "시험 단서: 찢어지는 흉통과 양팔 혈압 차이."],
                   _body=f"## 판단 — 왜 베타차단제가 먼저인가\n- **첫 약**: {sent} [[harrison-22: 280장 p.2104]].\n- 다른 줄.\n")
        w = W(dup)
        self.assertEqual([C.polish_kind(x) for x in w], ["중복"])
        self.assertIn("summary 1번째 줄", w[0])
        self.assertEqual(kinds(dict(dup, _body=dup["_body"].replace("## 판단", "## 기전"))), [])      # 판단 절만 본다
        self.assertEqual(kinds(dict(dup, summary=["결론: 혈관확장제는 베타차단제 뒤에만 더한다."])), [])
        self.assertEqual(kinds(dict(dup, summary=["결론: 짧은 말."], _body="## 판단 — 왜\n- 짧은 말.\n")), [])   # 짧은 구절은 견주지 않는다
        # 넷 모두 [WARN] — 게시 · 시험 관문이 쓰는 기준(blocking)을 통과한다
        allw = W(dict(dup, _body=dup["_body"] + "가" * 3300, diagram_notes=list("12345"), variants=[]))
        self.assertEqual(sorted(C.polish_kind(x) for x in allw), sorted(C.POLISH_KINDS))
        self.assertTrue(all(x.startswith("[WARN] ") for x in allw))
        self.assertEqual(ex.blocking([f"a.md: {x}" for x in allw]), [])
        self.assertIsNone(C.polish_kind("a.md: [WARN] 해리슨 대조 없음 — …"))
        # 계약 검사(validate_concept)에 실려도 오류는 늘지 않는다
        base = {"id": "cn.neph.a.b", "title": "가 — 나", "objective": "고른다", "condition": "가", "objective_kind": "치료",
                "version": 1, "review_status": "unreviewed", "summary": ["결론: 가."], "exams": ["kmle"],
                "sources": [{"id": "s", "org": "o", "title": "t", "year": 2024, "checked_at": "2026-11-23", "checked": "c",
                             "url": "https://example.org/x", "verified": "text"}]}
        before = [x for x in C.validate_concept(dict(base, variants=[{"id": "v1", "stem": "s", "choices": ["A. a", "B. b"],
                                                                       "answer": "A", "explanation": "e"}]))
                  if "[WARN]" not in x]
        after = C.validate_concept(dict(base, _body="가" * 4000, diagram_notes=list("12345")))
        self.assertEqual([x for x in after if "[WARN]" not in x], before)
        self.assertEqual(sorted(k for k in map(C.polish_kind, after) if k), ["도식 설명", "변형 없음", "분량"])


class NoteParts(unittest.TestCase):
    """판형 12(2026-11-23 vNext Phase 3) — 원고의 머리말을 풀어 보여 주는 조각. 웹 앱과 PDF 가 같은 함수(note_parts)를 쓴다."""

    @classmethod
    def setUpClass(cls):
        cls.base, _ = C.load_concepts()          # 정리본 전부를 한 번만 읽는다(읽기가 이 시험 묶음에서 가장 느리다)
        cls.cfg = bb.load_config()

    def test_summary_lines_become_labelled_slots(self):
        import note_parts as np_
        slots = np_.summary_slots(["결론: A 면 B", "시험 단서： 넓은 맥압", "왜: 용적 과부하", "쓰지 않는 약: 베타차단제", "쓰지 않는다: 풍선 펌프",
                                   "피할 약: 딜티아젬", "그 밖의 한 줄"])
        self.assertEqual([x["kind"] for x in slots], ["conclusion", "cue", "why", "avoid", "avoid", "avoid", "more"])
        self.assertEqual([x["label"] for x in slots[:4]], ["핵심 결론", "발문 단서", "왜 이 판단인가", "금기 · 피할 약"])
        self.assertEqual(slots[0]["text"], "A 면 B")                       # 머리말은 떼고 내용만
        self.assertEqual(slots[1]["raw"], "시험 단서：")
        self.assertEqual((slots[6]["label"], slots[6]["text"]), ("", "그 밖의 한 줄"))
        for lab in np_.SLOT_LABEL.values():                               # 글자 라벨만 — 장식 이모티콘을 넣지 않는다(시각 절제)
            self.assertFalse(re.search("[\U0001F300-\U0001FAFF☀-➿]", lab), lab)
        # 실제 정리본 전부: 판형 2 의 세 머리말(결론 · 시험 단서 · 왜)을 모두 읽는다
        for cid, c in self.base.items():
            kinds = [x["kind"] for x in np_.summary_slots(c.get("summary"))]
            if c.get("note_form") == 2:
                self.assertTrue({"conclusion", "cue", "why"} <= set(kinds), cid)

    def test_slot_text_breaks_into_lines_only_where_it_is_a_list(self):
        # 2026-11-23 사용자 「약제 같은 부분이 다 한 줄이라 읽기 어렵다 — 줄을 띄워」. 원고는 한 줄 그대로 두고 보여 줄 때 덩이마다 줄을 바꾼다.
        import note_parts as np_
        flat = lambda gs: [(g["lead"], g["items"]) for g in gs]
        # 금기 — 괄호 밖 쉼표마다 한 줄(괄호 안 쉼표 · 근거 표시 안 쉼표에서는 자르지 않는다)
        self.assertEqual(flat(np_.slot_groups("avoid", "베라파밀·딜티아젬(음성 변력), NSAID·티아졸리딘디온, ACE 억제제+ARB+MRA 3제 [[harrison-22: 265장 p.1990, p.1994]]")),
                         [("", ["베라파밀·딜티아젬(음성 변력)", "NSAID·티아졸리딘디온", "ACE 억제제+ARB+MRA 3제 [[harrison-22: 265장 p.1990, p.1994]]"])])
        self.assertEqual(flat(np_.slot_groups("avoid", "스테로이드·NSAID(동반 염증 질환에만, 섬유근육통 자체엔 무효)")),
                         [("", ["스테로이드·NSAID(동반 염증 질환에만, 섬유근육통 자체엔 무효)"])])
        # 금기 — 가운뎃점으로 셋 이상 이은 순수한 나열도 한 줄씩
        self.assertEqual(flat(np_.slot_groups("avoid", "도파민 1차·전분(starch) 수액·CVP 8–12 같은 고정 목표. 승압제는 중심정맥관을 기다리지 않는다.")),
                         [("", ["도파민 1차", "전분(starch) 수액", "CVP 8–12 같은 고정 목표", "승압제는 중심정맥관을 기다리지 않는다."])])
        # 발문 단서 — 쉼표 · 문장마다 한 줄
        self.assertEqual(flat(np_.slot_groups("cue", "노인, 한쪽 이마의 화끈한 통증 뒤 물집, 코끝 물집(Hutchinson sign), 눈 충혈·시림.")),
                         [("", ["노인", "한쪽 이마의 화끈한 통증 뒤 물집", "코끝 물집(Hutchinson sign)", "눈 충혈·시림."])])
        self.assertEqual(flat(np_.slot_groups("cue", "LVEF ≤ 40 % + 「예후·사망률을 낮추는 약은?」 → 이 넷. 「증상을 바로 푸는 약은?」 → 고리 이뇨제.")),
                         [("", ["LVEF ≤ 40 % + 「예후·사망률을 낮추는 약은?」 → 이 넷", "「증상을 바로 푸는 약은?」 → 고리 이뇨제."])])
        # 결론 — 「… 약은 A·B·C·D다」만 머리 줄 + 항목 줄로 편다(괄호 안의 가운뎃점 · 「또는」에 걸리지 않는다)
        self.assertEqual(flat(np_.slot_groups("conclusion", "HFrEF 의 기본 약은 RAAS 차단(ACE 억제제·ARB 또는 ARNI)·검증된 β차단제·MRA·SGLT2 억제제다 [[h: p.1992, p.1996]]")),
                         [("HFrEF 의 기본 약은", ["RAAS 차단(ACE 억제제·ARB 또는 ARNI)", "검증된 β차단제", "MRA", "SGLT2 억제제다 [[h: p.1992, p.1996]]"])])
        # 결론 · 왜 — 문장은 쉼표 · 가운뎃점에서 자르지 않는다(조각나면 뜻이 흐려진다)
        for kind, text in (("conclusion", "만성 중증 역류는 증상이 있거나 박출률 ≤ 55 %·수축기말 지름 > 50 mm 면 판막 교체, 급성 중증은 24시간 안 수술"),
                           ("conclusion", "되돌릴 원인이 없는 후천성 완전·고도·Mobitz II 방실차단은 증상이 없어도 영구 심박조율기다."),
                           ("conclusion", "10대의 빠르게 커지는 한쪽 고형 난소 종괴는 수술 전에 알파태아단백(AFP)·β-hCG·LDH 를 잰다."),
                           ("why", "약물 유발 루푸스는 신장·뇌를 거의 침범하지 않고 항dsDNA·항Sm 같은 다른 자가항체가 드물다."),
                           ("why", "외분비샘의 림프구 침윤이 분비를 줄인다 — 같은 건조는 약·바이러스·육아종으로도 생겨 원인을 따로 가려야 한다.")):
            self.assertEqual(flat(np_.slot_groups(kind, text)), [("", [text])], text)
        self.assertEqual(np_.slot_groups("why", ""), [])
        # 실제 정리본 전부: 줄을 나눠도 글자를 잃거나 더하지 않는다(구분 기호와 띄어쓰기만 다르다)
        squash = lambda t: re.sub(r"[\s,·/.]", "", t)
        split = 0
        for c in self.base.values():
            for sl in np_.summary_slots(c.get("summary")):
                joined = "".join(g["lead"] + "".join(g["items"]) for g in sl["groups"])
                self.assertEqual(squash(joined), squash(sl["text"]), sl["text"])
                split += sum(len(g["items"]) + bool(g["lead"]) for g in sl["groups"]) > 1
        self.assertGreater(split, 100)                                      # 발문 단서 · 금기 칸의 절반쯤이 줄로 나뉜다
        # 그리는 쪽: PDF 와 앱이 같은 덩이를 쓴다
        u, c = self._unit("cn.cardio.heart-failure.hfref-gdmt-selection", "순환기내과")
        h, _ = bb.unit_html(u, self.cfg, {}, "순환기내과")
        self.assertIn('<div class="sll">HFrEF 의 기본 약은</div><ul class="sl sub"><li>RAAS 차단(ACE 억제제·ARB 또는 ARNI)</li>', h)
        self.assertIn('<ul class="sl"><li>베라파밀·딜티아젬(음성 변력)</li><li>NSAID·티아졸리딘디온</li>', h)
        learn = (ROOT / "docs" / "learn.js").read_text(encoding="utf-8")
        self.assertIn("function slotLinesHtml(s)", learn)
        import export_concepts_web as ew
        self.assertIn("groups=[{", (ROOT / "pipelines" / "export_concepts_web.py").read_text(encoding="utf-8"))

    def test_exam_issue_section_is_none_or_four_fields(self):
        import note_parts as np_
        self.assertTrue(np_.is_issue_title("시험 쟁점 — 충돌·맥락·새 근거"))
        self.assertFalse(np_.is_issue_title("권고와 예외"))
        none = np_.exam_issues("<ul>\n<li>해당 없음(대조: 해리슨 353장 p.2727~2728)</li>\n</ul>")
        self.assertEqual(none, {"none": True, "ref": "대조: 해리슨 353장 p.2727~2728"})
        z = np_.exam_issues("<ul><li><strong>Z1 충돌 · 박출률 기준</strong> — 시험 기준: ≤ 55 % [[h: p.1]] / 다른 기준: &lt; 55 % / 왜 다른가: 그림과 본문 / "
                            "시험에서는: KMLE · USMLE 모두 수술 쪽</li><li>그 밖에 어긋난 곳 없음(대조: 250장).</li></ul>")
        self.assertFalse(z["none"])
        a, b = z["issues"]
        self.assertEqual((a["id"], a["kind"], a["title"]), ("Z1", "충돌", "박출률 기준"))
        self.assertEqual((a["exam"], a["other"], a["why"], a["onexam"]),
                         ("≤ 55 % [[h: p.1]]", "&lt; 55 %", "그림과 본문", "KMLE · USMLE 모두 수술 쪽"))
        self.assertEqual((b["exam"], b["body"]), ("", "그 밖에 어긋난 곳 없음(대조: 250장)."))     # 네 칸이 없는 항목은 글 그대로
        # 실제 정리본: 쟁점 항목의 대부분이 네 칸으로 풀린다(풀리지 않는 것은 「그 밖에 없음」 같은 덧글)
        four = total = 0
        for c in self.base.values():
            for sec in c["sections"]:
                if np_.is_issue_title(sec["title"]):
                    r = np_.exam_issues(sec["html"])
                    for it in ([] if r["none"] else r["issues"]):
                        total += 1
                        four += bool(it["exam"] and it["other"] and it["why"] and it["onexam"])
        self.assertGreater(total, 50)
        self.assertGreater(four / total, 0.9)

    def test_series_orders_one_disease_by_the_flow_of_judgement(self):
        import note_parts as np_
        cs = {"cn.cardio.hf.tx": {"title": "치료", "objective_kind": "치료"}, "cn.cardio.hf.dx": {"title": "진단", "objective_kind": "진단"},
              "cn.peds.hf.mech": {"title": "기전", "objective_kind": "기전"}, "cn.cardio.af.rate": {"title": "혼자", "objective_kind": "치료"}}
        se = np_.series(cs)
        self.assertEqual([x["id"] for x in se["cn.cardio.hf.dx"]], ["cn.peds.hf.mech", "cn.cardio.hf.dx", "cn.cardio.hf.tx"])   # 과가 달라도 같은 질환
        self.assertNotIn("cn.cardio.af.rate", se)                           # 혼자인 단원에는 줄을 세우지 않는다

    def _unit(self, cid, book):
        c = copy.deepcopy(self.base[cid])
        return bb.Unit(cid, book, c, ll.State(cid, cid), [], str(c.get("title")), slot=str(c.get("outline") or "")), c

    def test_pdf_unit_uses_slots_cards_and_puts_criteria_before_the_choice_section(self):
        cfg = self.cfg
        self.assertEqual(cfg["template_version"], 13)
        u, c = self._unit("cn.cardio.aortic-regurgitation.surgery-timing", "순환기내과")
        h, info = bb.unit_html(u, cfg, {}, "순환기내과")
        for lab in ("핵심 결론", "발문 단서", "왜 이 판단인가"):
            self.assertIn(f'<div class="sk">{lab}</div>', h)
        self.assertNotIn("<b>한눈에</b>", h)
        # 기준은 한 단 카드로, 「선택 — …」 절 앞에 온다(판형 11 은 「치료…」만 찾아 판형 2 정리본에서 맨 끝으로 밀렸다)
        self.assertNotIn('class="tb rec"><div class="tt">기준', h)
        self.assertLess(h.index('<div class="crit">'), h.index("선택 — 수술 적응과 방법"))
        self.assertGreater(h.index('<div class="crit">'), h.index("가르는 소견 — 만성과 급성"))
        # 혼동은 「혼동 / 기준」 카드
        self.assertEqual(h.count('<div class="pc">'), len(c["pitfalls"]))
        self.assertNotIn('<ul class="pit">', h)
        # 시험 쟁점: 쟁점이 있으면 네 칸 카드
        self.assertIn('<span class="pk">시험 기준</span>', h)
        self.assertIn('<span class="pk">시험에서는</span>', h)
        self.assertNotIn("시험 쟁점 — 충돌·맥락·새 근거", h)                   # 긴 절 이름 대신 「시험 쟁점」
        self.assertIn("시험 쟁점", info["sections"][-1] if "시험 쟁점" in info["sections"][-1] else " ".join(info["sections"]))

    def test_pdf_unit_folds_an_empty_exam_issue_into_a_header_mark(self):
        cfg = self.cfg
        u, c = self._unit("cn.allergy.anaphylaxis.im-epinephrine-first", "알레르기내과")
        h, info = bb.unit_html(u, cfg, {}, "알레르기내과")
        self.assertIn('<span class="ok">해리슨 대조 · 충돌 없음</span>', h)
        self.assertNotIn(">시험 쟁점<", h)                                    # 절을 세우지 않는다
        self.assertFalse([t for t in info["sections"] if "시험 쟁점" in t])
        self.assertNotIn("해당 없음", h)

    def test_pdf_links_series_roots_and_chapter_map(self):
        cfg = self.cfg
        concepts = self.base
        books = bb.plan(concepts, {}, {}, cfg, {})
        hf = next(u for u in books["순환기내과"].units if u.key == "cn.cardio.heart-failure.hfref-gdmt-selection")
        self.assertEqual([x["kind"] for x in hf.links["series"]], ["진단", "치료"])
        h, _ = bb.unit_html(hf, cfg, {}, "순환기내과")
        self.assertIn('<span class="k">같은 질환</span>', h)
        self.assertIn('<span class="here">치료</span>', h)
        self.assertIn('href="#u-cn-cardio-heart-failure-natriuretic-peptide-echo-diagnosis"', h)   # 같은 책이면 그 단원으로
        self.assertIn("links", bb.unit_fingerprint(hf))                     # 이음이 바뀌면 책을 다시 만든다
        lone = next(u for u in books["순환기내과"].units if not u.links)
        self.assertNotIn("links", bb.unit_fingerprint(lone))
        # 기초 뿌리 — 임상 단원 머리의 줄 · 기초 단원 끝의 「받치는 임상 단원」
        basic = next(c for c in concepts.values() if C.is_basic(c))
        cs = dict(concepts)                                               # 얕은 사본 — 고칠 정리본 하나만 따로 뜬다
        cs["cn.cardio.heart-failure.hfref-gdmt-selection"] = dict(concepts["cn.cardio.heart-failure.hfref-gdmt-selection"], roots=[basic["id"]])
        b2 = bb.plan(cs, {}, {}, cfg, {})
        hf2 = next(u for u in b2["순환기내과"].units if u.key == "cn.cardio.heart-failure.hfref-gdmt-selection")
        h2, _ = bb.unit_html(hf2, cfg, {}, "순환기내과")
        self.assertIn('<span class="k">기초 뿌리</span>', h2)
        self.assertIn(html.escape(str(basic["title"])), h2)
        bu = next(u for b in b2.values() for u in b.units if u.key == basic["id"])
        h3, _ = bb.unit_html(bu, cfg, {}, bu.book)
        self.assertIn("이 기전이 받치는 임상 단원", h3)
        # 절 지도 — 한 절에 단원이 셋 이상이면 그 절 첫머리에 「단원 · 목표 종류 · 핵심 결론」
        units = books["순환기내과"].units
        full, _ = bb.book_html("순환기내과", units, cfg, {}, {"version": 1, "date": "2026-11-23"}, None,
                               {"regular": "x.ttf", "bold": "x.ttf"}, [])
        self.assertIn('<div class="cmap"><div class="mh">', full)
        groups = {}
        for u in units:
            if u.group:
                groups.setdefault(u.group, []).append(u)
        self.assertEqual(full.count('<div class="cmap">'), sum(1 for g in groups.values() if len(g) >= 3))

    def test_web_bundle_carries_the_same_parts(self):
        import export_concepts_web as ew
        data, _ = ew.build()
        ar = data["cn.cardio.aortic-regurgitation.surgery-timing"]
        self.assertEqual([s["kind"] for s in ar["slots"][:3]], ["conclusion", "cue", "why"])
        self.assertIn("<sup", ar["slots"][0]["html"])                       # 근거 표시는 번호로 바꿔 싣는다
        self.assertFalse(ar["issues"]["none"])
        self.assertTrue(ar["issues"]["items"][0]["onexam"])
        self.assertTrue(any(s["issue"] for s in ar["sections"]))            # 옛 판형(필기가 있는 종이)이 쓸 절은 그대로 싣는다
        self.assertTrue(data["cn.allergy.anaphylaxis.im-epinephrine-first"]["issues"]["none"])
        self.assertTrue(all(isinstance(c["order"], int) for c in data.values()))      # 서가를 기본틀 순서로 늘어놓는다
        self.assertEqual([x["kind"] for x in data["cn.cardio.heart-failure.hfref-gdmt-selection"]["series"]], ["진단", "치료"])
        self.assertTrue(all(c["layer"] in ("basic", "clinical") for c in data.values()))
        # 앱이 그 조각을 그린다 — 종이(필기장) 안에서 누를 수 있게 단추가 아니라 <a data-…> 로
        learn = (ROOT / "docs" / "learn.js").read_text(encoding="utf-8")
        for needle in ("function slotsHtml(c)", "function issuesHtml(c)", "function headExtrasHtml(c)", 'data-goto="', 'data-root="',
                       'data-tape="1"', "Harrison 대조 · 충돌 없음"):
            self.assertIn(needle, learn)
        css = (ROOT / "docs" / "style.css").read_text(encoding="utf-8")
        body = css[css.index("/* 판형 12(2026-11-23 vNext Phase 3)"):]
        self.assertFalse(re.findall(r"#[0-9a-fA-F]{3,8}\b", body))           # 새 상자도 색은 변수로만(한 가지 톤)

    def test_optional_exam_points_and_checklists_render(self):
        cfg = self.cfg
        u, c = self._unit("cn.allergy.anaphylaxis.im-epinephrine-first", "알레르기내과")
        c["exam_points"] = {"kmle": "국내는 성인 0.3~0.5 mg 표기", "usmle": ""}
        c["checklists"] = [{"name": "CURB-65", "items": [{"label": "혼돈", "points": "1"}, "요소 > 7 mmol/L"], "cutoffs": "2점 이상이면 입원"}]
        h, _ = bb.unit_html(u, cfg, {}, "알레르기내과")
        self.assertIn('<span class="k">KMLE 포인트</span>국내는 성인 0.3~0.5 mg 표기', h)
        self.assertNotIn("USMLE 포인트", h)                                   # 빈 쪽은 싣지 않는다
        self.assertIn('<div class="lh">CURB-65</div>', h)
        self.assertEqual(h.count('<span class="bx"></span>'), 2)
        self.assertIn('<span class="pk">판정</span>2점 이상이면 입원', h)


class LayoutRules(unittest.TestCase):
    """한 번 올려 재는 배치(2026-11-23) — 측정값 → 배치 문제 계산과 탐색의 가지치기를 손으로 만든 값으로 고정한다(브라우저 없이)."""

    H = 1000.0

    def _page(self, left=None, right=None, **kw):
        """한 쪽의 측정값 — left/right = 그 단의 글 구간. 비우면 꽉 찬 단."""
        full = [[0.0, self.H]]
        pg = {"t": [left if left is not None else full, right if right is not None else full], "b": [[], []], "x1": [], "wide": [], "orph": []}
        pg.update(kw)
        return pg

    def _m(self, *pages):
        return {"pages": len(pages), "PH": self.H, "P": list(pages)}

    def test_gap_and_coverage_use_the_validator_thresholds(self):
        ok = self._page()
        # 2쪽: 왼쪽 단이 60% 에서 끝난다(빈칸 40% > 30%) · 3쪽: 두 단 모두 45% 만 찼다(내용 45% < 50%)
        m = self._m(ok, self._page(left=[[0, 600]]), self._page(left=[[0, 450]], right=[[0, 450]]), ok)
        errs = bl.problems(m)
        self.assertEqual(errs, ["2쪽 왼쪽 단 아래가 비어 있다(빈 공간 40%)", "3쪽에 빈 공간이 크다(내용 45%)",
                                "3쪽 왼쪽 단 아래가 비어 있다(빈 공간 55%)", "3쪽 오른쪽 단 아래가 비어 있다(빈 공간 55%)"])
        self.assertEqual(bl.layout_errors(errs), errs)                       # 검증의 배치 오류와 같은 글귀다(탐색 · 참고 강등이 글귀로 고른다)
        # 1쪽(목차 쪽)과 마지막 쪽은 비어도 정상
        self.assertEqual(bl.problems(self._m(self._page(left=[[0, 100]], right=[]), ok, self._page(left=[[0, 100]], right=[]))), [])
        # 단 아래의 상자(표 · 그림)도 내용이다 · 6pt(8px) 안의 틈은 이어진 것으로 센다
        boxed = self._page(left=[[0, 500]], b=[[[505, 1000]], []])
        self.assertEqual(bl.problems(self._m(ok, boxed, ok)), [])
        apart = self._page(left=[[0, 300], [700, 1000]], right=[[0, 300], [700, 1000]])     # 가운데 40% 가 빈 쪽 — 아래는 차 있다
        self.assertEqual(bl.problems(self._m(ok, apart, ok)), [])                            # 내용 60% — 문제 아님
        self.assertEqual(bl.problems(self._m(ok, self._page(left=[[0, 200], [800, 1000]], right=[[0, 200], [800, 1000]]), ok)),
                         ["2쪽에 빈 공간이 크다(내용 40%)"])

    def test_margin_makes_the_search_avoid_borderline_layouts(self):
        ok = self._page()
        m = self._m(ok, self._page(left=[[0, 705]]), ok)                    # 빈칸 29.5%
        self.assertEqual(bl.problems(m), [])
        self.assertEqual(bl.problems(m, 0.01), ["2쪽 왼쪽 단 아래가 비어 있다(빈 공간 30%)"])
        self.assertEqual(bb.MEASURE_MARGIN, 0.01)

    def test_narrow_bands_around_a_full_width_diagram(self):
        ok = self._page()
        dia = [[200.0, 880.0]]                                               # 두 단 폭 도식(높이 680) — 아래에 12% 남는다
        below = self._page(left=[[0, 190], [900, 1000]], right=[[0, 190], [900, 1000]], b=[dia, dia], wide=dia)
        self.assertEqual(bl.problems(self._m(ok, below, ok)), ["2쪽 두 단 도식 아래 좁은 띠(빈 공간 아님, 12%) — 좌우로 오가며 읽힌다"])
        # 도식 아래에 글이 없으면 띠가 아니다(그 쪽은 도식으로 끝난다)
        end = self._page(left=[[0, 190]], right=[[0, 190]], b=[dia, dia], wide=dia)
        self.assertEqual(bl.problems(self._m(ok, end, ok)), [])
        # 위 띠: 도식 위 10% 에 오른쪽 단 글이 있어야 한다(왼쪽 단에만 있으면 한 줄로 읽힌다)
        top = [[100.0, 1000.0]]
        both = self._page(left=[[0, 90]], right=[[0, 90]], x1=[[0, 90]], b=[top, top], wide=top)
        self.assertEqual(bl.problems(self._m(ok, both, ok)), ["2쪽 두 단 도식 위 좁은 띠(10%) — 좌우로 오가며 읽힌다"])
        left_only = self._page(left=[[0, 90]], right=[], b=[top, top], wide=top)
        self.assertEqual(bl.problems(self._m(ok, left_only, ok)), [])
        # 낮은 두 단 폭 상자(40pt 미만 — 머리 밑줄 따위)는 도식이 아니다
        thin = [[880.0, 900.0]]
        self.assertEqual(bl.problems(self._m(ok, self._page(left=[[0, 870], [905, 1000]], right=[[0, 870], [905, 1000]], b=[thin, thin], wide=thin), ok)), [])

    def test_orphan_headings_and_error_keys(self):
        ok = self._page()
        errs = bl.problems(self._m(ok, self._page(orph=["권고와 예외"]), ok))
        self.assertEqual(errs, ["2쪽 고립된 제목: '권고와 예외'"])
        # 예측과 실제는 (쪽, 종류)로 맞댄다 — % 값이 조금 달라도 같은 문제다
        self.assertEqual(bl.error_key("12쪽 왼쪽 단 아래가 비어 있다(빈 공간 31%)"), bl.error_key("12쪽 왼쪽 단 아래가 비어 있다(빈 공간 33%)"))
        self.assertNotEqual(bl.error_key("12쪽 왼쪽 단 아래가 비어 있다(빈 공간 31%)"), bl.error_key("12쪽 오른쪽 단 아래가 비어 있다(빈 공간 31%)"))
        self.assertNotEqual(bl.error_key("12쪽 두 단 도식 아래 좁은 띠(빈 공간 아님, 9%) — 좌우로 오가며 읽힌다"),
                            bl.error_key("12쪽 두 단 도식 위 좁은 띠(9%) — 좌우로 오가며 읽힌다"))
        self.assertEqual(bl.layout_errors(["임베드되지 않은 글꼴: ['x']", "3쪽에 빈 공간이 크다(내용 40%)"]), ["3쪽에 빈 공간이 크다(내용 40%)"])

    # ── 탐색 ──
    def _units(self):
        mk = lambda k: bb.Unit(key=k, book="책", concept={"diagram": SPEC}, state=ll.State(key=k, objective=k), questions=[], title=k)
        us = [mk("cn.t.a.x"), mk("cn.t.b.x"), mk("cn.t.c.x")]
        info = lambda: {"diagram": {"place": "column", "pt": 7.0}, "dia_default": 3, "dia_choices": [1, 2, 3, 4, 5], "dia_at": 3,
                        "fig_choices": {}, "fig_at": {}}
        infos = {u.anchor: info() for u in us}
        pm = {us[0].anchor: 2, us[1].anchor: 4, us[2].anchor: 6}
        return us, infos, pm

    def test_search_stops_when_solved_and_skips_units_after_the_last_problem(self):
        us, infos, pm = self._units()
        a, b, c = (u.anchor for u in us)
        bad = "4쪽 왼쪽 단 아래가 비어 있다(빈 공간 40%)"
        calls = []

        def trial(pos):                       # 둘째 단원의 도식을 다섯째 자리로 옮기면 풀린다
            calls.append(dict(pos))
            return ([] if pos.get(b) == 5 else [bad]), 8, infos, pm

        pos, tried = bb.search_placement(us, trial, ([bad], 8, infos, pm), prune=True)
        self.assertEqual((pos.get(b), tried), (5, 10))                       # 첫 단원 8번 + 둘째 단원 2번 — 풀리면 멈춘다
        self.assertFalse(any(c in p for p in calls))                         # 셋째 단원은 건드리지 않았다
        # 옛 탐색(가지치기 없음)은 풀린 뒤에도 남은 단원마다 한 번씩 더 그려 본다 — 같은 배치, 더 많은 시도
        calls.clear()
        pos2, tried2 = bb.search_placement(us, trial, ([bad], 8, infos, pm))
        self.assertEqual((pos2.get(b), tried2), (5, 11))
        self.assertTrue(any(c in p for p in calls))
        # 문제가 2쪽뿐이면 4쪽 · 6쪽에서 시작하는 단원은 바꿔 봐야 소용없다
        only2 = "2쪽 왼쪽 단 아래가 비어 있다(빈 공간 40%)"
        calls.clear()
        _, tried3 = bb.search_placement(us, lambda p: (calls.append(dict(p)) or [only2], 8, infos, pm), ([only2], 8, infos, pm), prune=True)
        self.assertEqual(tried3, 8)
        self.assertTrue(all(set(p) <= {a, a + "#shrink", a + "#pad", a + "#col"} for p in calls))
        # 쪽을 모르는 오류(배치 외)가 섞이면 어느 단원도 건너뛰지 않는다
        mixed = [only2, "도식이 한 쪽에 온전히 있지 않다: x"]
        _, tried4 = bb.search_placement(us, lambda p: (mixed, 8, infos, pm), (mixed, 8, infos, pm), prune=True)
        self.assertEqual(tried4, 24)

    def test_search_budget_goal_and_unit_filter(self):
        us, infos, pm = self._units()
        a, b, c = (u.anchor for u in us)
        bad = "4쪽 왼쪽 단 아래가 비어 있다(빈 공간 40%)"
        trial = lambda pos: (([] if pos.get(b) == 5 else [bad]), 8, infos, pm)
        pos, tried = bb.search_placement(us, trial, ([bad], 8, infos, pm), prune=True, budget=3)
        self.assertEqual((pos, tried), ({}, 3))                              # 예산 안에서 못 풀면 처음 배치 그대로
        pos, tried = bb.search_placement(us, trial, ([bad], 8, infos, pm), prune=True, only={b})
        self.assertEqual((pos.get(b), tried), (5, 2))
        # 시작 배치(pos0)를 이어받고, 목표를 「알던 오류만 남는다」로 줄 수 있다(예측에 없던 오류만 PDF 로 고칠 때)
        known = "2쪽 왼쪽 단 아래가 비어 있다(빈 공간 40%)"
        trial2 = lambda pos: ([known] + ([] if pos.get(b) == 5 else [bad]), 8, infos, pm)
        pos, tried = bb.search_placement(us, trial2, ([known, bad], 8, infos, pm), pos0={a: 1}, prune=True, only={b},
                                         goal=lambda es: all(e == known for e in es))
        self.assertEqual((pos.get(a), pos.get(b), tried), (1, 5, 2))
        # 그 쪽들에 닿는 단원: 앞쪽 첫머리를 차지한 단원부터 그 쪽에서 시작하는 단원까지
        self.assertEqual(bb.units_near(us, pm, [4]), {a, b})
        self.assertEqual(bb.units_near(us, pm, [5]), {b})
        self.assertEqual(bb.units_near(us, pm, [6, 7]), {b, c})

    def test_band_padding_pass(self):
        us, infos, pm = self._units()
        a = us[0].anchor
        infos[a]["diagram"] = {"place": "full", "pt": 7.0}
        band = "3쪽 두 단 도식 아래 좁은 띠(빈 공간 아님, 9%) — 좌우로 오가며 읽힌다"
        trial = lambda pos: (([] if pos.get(a + "#pad") == 28 else [band]), 8, infos, pm)
        pos, tried = bb.settle_bands(us, trial, ([band], 8, infos, pm), {a: 3}, prune=True)
        self.assertEqual((pos, tried), ({a: 3, a + "#pad": 28}, 3))
        pos, _ = bb.settle_bands(us, lambda p: ([band], 8, infos, pm), ([band], 8, infos, pm), {a: 3})
        self.assertEqual(pos, {a: 3})                                        # 나아지지 않으면 원래 배치

    def test_same_diagram_title_prefix_in_two_units_is_not_a_split_diagram(self):
        # 순환기내과(2026-11-23): 도식 제목 앞 16자가 같은 단원이 둘 — 처음 나온 쪽만 보면 뒤 단원의 도식을 「쪼개졌다」고 오판해 책이 실패했다
        head = "[도식] 규칙적 좁은 QRS 빈맥 — 국소 심방빈맥 가르기"[:16]
        self.assertEqual(head, "[도식] 규칙적 좁은 QRS 빈맥 — P파 없는 빈맥"[:16])
        texts = ["목차", "[도식] 규칙적 좁은 QRS 빈맥 — 국소 심방빈맥 가르기 시작 … 결론 국소 심방빈맥", "본문만 있는 쪽",
                 "[도식] 규칙적 좁은 QRS 빈맥 — P파 없는 빈맥 시작 … 결론 발작성 상심실빈맥"]
        self.assertTrue(bb.diagram_on_one_page(texts, head, "국소 심방빈맥"))
        self.assertTrue(bb.diagram_on_one_page(texts, head, "발작성 상심실빈"))      # 둘째 단원의 도식은 4쪽에 온전히 있다
        # 정말 쪼개진 도식(제목은 2쪽, 마지막 노드는 3쪽)과 아예 없는 도식은 그대로 잡는다
        self.assertFalse(bb.diagram_on_one_page(["목차", "[도식] 규칙적 좁은 QRS 빈맥 — 시작", "결론 발작성 상심실빈맥"], head, "발작성 상심실빈"))
        self.assertFalse(bb.diagram_on_one_page(["목차", "본문"], head, "발작성 상심실빈"))

    def test_diagram_fit_is_computed_once(self):
        calls = []
        real = dd.layout
        spec = copy.deepcopy(SPEC)
        spec["title"] = "한 번만 짠다"
        try:
            dd.layout = lambda *a, **k: (calls.append(1), real(*a, **k))[1]
            f1 = bb.fit_diagram(spec)
            n = len(calls)
            f2 = bb.fit_diagram(copy.deepcopy(spec))                         # 같은 내용이면 다시 짜지 않는다
            f3 = bb.fit_diagram(spec, shrink=0.88)                           # 축소는 같은 계산에 배율만 곱한다
        finally:
            dd.layout = real
        self.assertGreater(n, 0)
        self.assertEqual(len(calls), n)
        self.assertEqual((f1["scale"], f1["place"], f1["node_w"]), (f2["scale"], f2["place"], f2["node_w"]))
        self.assertAlmostEqual(f3["scale"], round(f1["scale"] * 0.88, 3))


class MeasuredLayout(unittest.TestCase):
    """실제로 올려 재 본다 — 측정이 PDF 의 쪽 나눔 · 배치 오류와 맞는가, 빌드가 PDF 를 몇 번 그리는가, 측정이 안 되면 옛 탐색으로 가는가.

    책은 지금의 알레르기내과 정리본 두 편으로 고정한다(정리본이 늘어도 이 시험의 책은 커지지 않는다)."""

    IDS = ("cn.allergy.anaphylaxis.im-epinephrine-first", "cn.allergy.x-linked-agammaglobulinemia.btk-pre-b-arrest")
    TITLE = "알레르기내과"

    @classmethod
    def setUpClass(cls):
        try:
            import playwright  # noqa: F401
            import pymupdf  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("playwright/pymupdf 없음")
        base, _ = C.load_concepts()
        cls.concepts = {i: base[i] for i in cls.IDS if i in base}
        if len(cls.concepts) != len(cls.IDS):
            raise unittest.SkipTest("고정한 정리본이 없다")
        cls.cfg = bb.load_config()

    def _patched(self):
        """build() 가 정리본 두 편 · 문항 없음으로 돌게 한다(전부 읽으면 호출마다 1분)."""
        from unittest import mock
        return mock.patch.multiple(bb, load_concepts=lambda: (dict(self.concepts), []), load_questions=lambda: {})

    def test_measurement_predicts_pdf_pages_and_layout_errors(self):
        from playwright.sync_api import sync_playwright
        cfg = self.cfg
        book = bb.plan(self.concepts, {}, {}, cfg, {})[self.TITLE]
        units = [bb.et.unit(u) for u in book.units]
        fonts = {"regular": bb.find_font(cfg["fonts"]["regular"]), "bold": bb.find_font(cfg["fonts"]["bold"])}
        meta = {"version": 1, "date": "2026-11-23", "elsewhere": []}
        with tempfile.TemporaryDirectory() as td, sync_playwright() as pw:
            browser = pw.chromium.launch()
            try:
                box = bl.print_box(lambda h, p: bb.render_pdf(browser, h, p, ""), bb.PAGE)
                # 쪽과 여백을 정수 px 로 맞춘 상자다 — mm 를 그대로 바꾼 값(718.11 × 1046.92)으로 재면 줄바꿈이 어긋난다
                self.assertEqual(box, (float(round(box[0])), float(round(box[1]))), box)
                self.assertLess(abs(box[0] - 718.11) + abs(box[1] - 1046.92), 4, box)
                mb = bb.MeasuredBook(browser, box, self.TITLE, units, cfg, {}, meta, fonts, [])
                try:
                    errs0, pages0, infos, pm0 = mb.evaluate({})
                    m0 = mb.last
                    again = mb.evaluate({})
                    self.assertEqual((again[0], again[1], again[3]), (errs0, pages0, pm0))      # 되풀이해도 같은 값
                    # 단원 하나의 도식 자리를 바꿔 끼우고 잰 값 = 그 배치로 처음부터 올려 잰 값
                    u = next(x for x in units if infos[x.anchor].get("diagram") and len(infos[x.anchor]["dia_choices"]) > 1)
                    alt = next(q for q in infos[u.anchor]["dia_choices"] if q != infos[u.anchor]["dia_at"])
                    pos = {u.anchor: alt, u.anchor + "#shrink": 1.0, u.anchor + "#pad": 0, u.anchor + "#col": False}
                    swapped = mb.evaluate(pos)
                    m1 = mb.last
                finally:
                    mb.close()
                html_text, _ = bb.book_html(self.TITLE, units, cfg, {}, meta, None, fonts, [], pos)
                lab = bl.Lab(browser, html_text, box)
                try:
                    fresh = lab.measure()
                finally:
                    lab.close()
                self.assertEqual((swapped[1], swapped[3], swapped[0]), (fresh["pages"], fresh["pm"], bl.problems(fresh, bb.MEASURE_MARGIN)))
                # 실제 PDF 와: 쪽 수 · 단원이 시작하는 쪽 · 배치 오류의 (쪽, 종류)
                for p_, m_ in (({}, m0), (pos, m1)):
                    pages_m, pm_m, errs_m = m_["pages"], m_["pm"], bl.problems(m_)
                    pdf = Path(td) / "t.pdf"
                    h, inf = bb.book_html(self.TITLE, units, cfg, {}, meta, pm_m, fonts, [], p_)
                    bb.render_pdf(browser, h, pdf, "시험")
                    pm = bb.locate(pdf)
                    import pymupdf
                    with pymupdf.open(pdf) as d:
                        self.assertEqual(d.page_count, pages_m)
                    self.assertEqual({x.anchor: pm.get(x.anchor) for x in units}, {x.anchor: pm_m.get(x.anchor) for x in units})
                    real, _ = bb.validate_pdf(pdf, self.TITLE, units, pm, inf)
                    self.assertEqual({bl.error_key(e) for e in bl.layout_errors(real)},
                                     {bl.error_key(e) for e in errs_m}, (real, errs_m))
            finally:
                browser.close()

    def test_build_draws_the_book_once_and_is_not_worse_than_the_old_search(self):
        import pymupdf
        cfg = dict(self.cfg)
        res = {}
        with self._patched(), tempfile.TemporaryDirectory() as td:
            for mode in ("measure", "search"):
                st, out = Path(td) / mode / "state", Path(td) / mode / "out"
                r = bb.build(cfg, [], st, out, only=self.TITLE, layout=mode)
                self.assertEqual(r["built"], [self.TITLE], r)
                self.assertEqual(r["validation"][self.TITLE], [])
                with pymupdf.open(out / f"MedKOS_학습서_{self.TITLE}.pdf") as d:
                    pages = d.page_count
                left = [n for n in r["notes"][self.TITLE] if "배치 탐색 뒤에도 남은" in n]
                res[mode] = (r["renders"][self.TITLE], len(left), pages, (r.get("layout_trials") or {}).get(self.TITLE) or {})
            print(f"\n  배치 — 측정: PDF {res['measure'][0]}번 · 남은 문제 {res['measure'][1]} · {res['measure'][2]}쪽 / "
                  f"옛 탐색: PDF {res['search'][0]}번 · 남은 문제 {res['search'][1]} · {res['search'][2]}쪽")
            # 측정이 실제와 맞으면 책은 한 번만 그린다. 안 맞아도(예측에 없던 오류를 PDF 로 고친다) 예산 안이다.
            self.assertLessEqual(res["measure"][0], 2 + bb.REPAIR_RENDERS, res)
            if not res["measure"][3].get("unpredicted"):
                self.assertEqual(res["measure"][0], 1, res)
            self.assertLessEqual(res["measure"][0], res["search"][0], res)
            self.assertLessEqual(res["measure"][1], res["search"][1], res)      # 옛 탐색보다 배치 문제가 늘지 않는다
            self.assertEqual(res["measure"][3].get("mode", "measure"), "measure")
            # 책 이름을 설정에 적어 두면 그 책만 옛 탐색으로 간다
            st, out = Path(td) / "pin" / "state", Path(td) / "pin" / "out"
            r = bb.build(dict(cfg, layout_search=[self.TITLE]), [], st, out, only=self.TITLE)
            self.assertEqual(r["renders"][self.TITLE], res["search"][0])

    def test_falls_back_to_the_old_search_when_measuring_fails(self):
        from unittest import mock
        with self._patched(), tempfile.TemporaryDirectory() as td, \
                mock.patch.object(bl, "print_box", side_effect=RuntimeError("탐침 실패")):
            r = bb.build(dict(self.cfg), [], Path(td) / "state", Path(td) / "out", only=self.TITLE)
        self.assertEqual(r["built"], [self.TITLE], r)
        self.assertEqual(r["validation"][self.TITLE], [])
        rec = r["layout_trials"][self.TITLE]
        self.assertEqual(rec["mode"], "search")
        self.assertIn("탐침 실패", rec["measure_failed"])
        with self.assertRaises(ValueError):
            bb.build(dict(self.cfg), [], Path("x"), Path("y"), layout="guess")


if __name__ == "__main__":
    unittest.main(verbosity=1)
