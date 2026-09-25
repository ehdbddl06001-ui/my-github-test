"""오답 뒤 학습 흐름 · 개념 정리본 · 판단 도식 · 과별 PDF 학습서 · 드라이브 갱신 회귀 테스트.

python pipelines/test_learning_books.py            (PDF 렌더링 시험은 playwright 가 있을 때만)
완료 조건(2026-09-18 사용자 지시)을 하나씩 테스트로 둔다:
  새 개념 → 새 단원 / 같은 개념 반복 → 단원 중복 없음 / 같은 질환 다른 목표 → 따로 / 메모·기록 보존 /
  바뀐 것 없음 → 건너뜀 / 실패 → 최신본 유지 / 출처 변경 → 검토 표시 / 한글 검색·차례 링크 / 필기본 보호
"""
from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

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
        self.assertIn("<table>", bb.stack_wide_tables(t.replace("<th>h5</th>", "").replace("<th>h4</th>", "")))

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
        self.assertGreaterEqual(fit["scale"], bb.DIAGRAM_MIN_SCALE)


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


class SourceChecks(_FixtureSources):
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
                self.assertGreater(d[0].rect.width, d[0].rect.height)            # A4 가로
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
        self._orig = (cq.load_concepts, cq.load_questions)
        self.concepts = {"cn.derm.a.b": {"id": "cn.derm.a.b"}}
        self.qs = {"q1": {"topic": "Dermatology", "subtopic": "어루러기", "objective": "cn.derm.a.b"},
                   "q2": {"topic": "Dermatology", "subtopic": "백선", "objective": "cn.derm.c.d"},
                   "q3": {"topic": "Cardiology", "subtopic": "심부전"},
                   "q4": {"topic": "Cardiology", "subtopic": "심부전"}}
        cq.load_concepts = lambda: (self.concepts, [])
        cq.load_questions = lambda: self.qs

    def tearDown(self):
        self.cq.load_concepts, self.cq.load_questions = self._orig

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

    def test_dist_queue_only_for_chosen_letter_without_explanation(self):
        self.qs["q1"].update(type="kmle", choices=["A. 가", "B. 나", "C. 다"], answer="A", path="content/kmle/x.md")
        e = [wrong("e1", "q1", "cn.derm.a.b", "2026-09-20T01:00:00Z", "2026-09-20", text="나")]
        self.assertEqual([d["key"] for d in self.cq.build(e)["dist"]], ["q1:B"])
        self.qs["q1"]["distractors"] = {"B": {"tempting": "x"}}
        self.assertEqual(self.cq.build(e)["dist"], [])
        self.qs["q1"].update(type="imaging", distractors={})             # 영상 문항은 빌더 파생물 — 제외
        self.assertEqual(self.cq.build(e)["dist"], [])

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


if __name__ == "__main__":
    unittest.main(verbosity=1)
