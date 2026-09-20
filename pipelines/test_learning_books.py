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


class RealContent(unittest.TestCase):
    def test_concepts_and_linked_questions_valid(self):
        concepts, errs = C.load_concepts()
        self.assertEqual(errs, [])
        qs = C.load_questions()
        for qid, m in qs.items():
            if m.get("objective"):
                problems = [x for x in C.question_learning_errors(m, concepts.get(m["objective"])) if x[0] == "ERROR"]
                self.assertEqual(problems, [], qid)

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
            "const ctx={window:{},localStorage:{getItem:k=>store[k]||null,setItem:(k,v)=>{store[k]=v}},"
            "KMLE:[],USMLE:[],IMAGING:[],console};vm.createContext(ctx);"
            f"store['medkos_learning_events']=JSON.stringify({json.dumps(events)});"
            f"vm.runInContext(fs.readFileSync({json.dumps(str(ROOT / 'docs' / 'learn.js'))},'utf8')+"
            "';this.__S=LEARN.states();',ctx);"
            "const out={};for(const [k,s] of Object.entries(ctx.__S)){out[k]=[s.status,s.priority,s.applied,s.wrongs]}"
            "console.log(JSON.stringify(out));")
        r = subprocess.run([node, "-e", harness], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)
        js = json.loads(r.stdout)
        py = {k: [s.status, s.priority, s.applied, s.wrongs] for k, s in ll.states(events).items()}
        self.assertEqual(js, py)


class Planning(unittest.TestCase):
    def setUp(self):
        self.cfg = bb.load_config()
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

    def test_real_diagrams_fit_readably(self):
        concepts, _ = C.load_concepts()
        for c in concepts.values():
            fit = bb.fit_diagram(c["diagram"])
            self.assertTrue(fit["ok"], c["id"])
            self.assertGreaterEqual(fit["scale"], bb.DIAGRAM_MIN_SCALE)


class SourceChecks(unittest.TestCase):
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
                raise TimeoutError("network")
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


if __name__ == "__main__":
    unittest.main(verbosity=1)
