"""test_ink.py — 오답노트 필기(docs/ink.js · functions/api/ink.js) 회귀 시험(2026-11-15).

지키는 것:
  ① 획 압축은 되돌릴 수 있고(0.1 px), 두 기기의 필기는 합집합으로 합쳐지며 지운 획은 되살아나지 않는다.
  ② 서버로 나가는 것은 **동기화 키로 잠근 암호문뿐**이다 — 저장소가 공개라서. 다른 키로는 열리지 않는다.
  ③ 서버 함수는 암호문이 아닌 본문을 받지 않고, 별도 가지(ink-data)에만 쓰며, sha 가 낡으면 409 로 돌려보낸다.

    python pipelines/test_ink.py
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
NODE = shutil.which("node")


def run_node(src: str, module: bool = False):
    args = [NODE] + (["--input-type=module"] if module else []) + ["-e", src]
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
    if r.returncode:
        raise AssertionError(r.stderr)
    return json.loads(r.stdout.strip().splitlines()[-1])


CORE = ("if(!globalThis.crypto)globalThis.crypto=require('crypto').webcrypto;"
        "const I=require('./docs/ink.js');"
        "(async()=>{const out={};%s;console.log(JSON.stringify(out))})().catch(e=>{console.error(e);process.exit(1)});")


@unittest.skipUnless(NODE, "node 없음")
class Core(unittest.TestCase):
    def test_pack_round_trip(self):
        out = run_node(CORE % "out.v=I.unpack(I.pack([10.04,20.5,0.5, 11.2,22.33,0.7, 300,400.1,1])).map(x=>Math.round(x*100)/100);"
                              "out.ints=I.pack([1,2,0.5, 1.5,2.5,0.5]).every(Number.isInteger)")
        self.assertEqual(out["v"][:2], [10, 20.5])
        self.assertEqual(out["v"][3:5], [11.2, 22.3])
        self.assertEqual(out["v"][6:8], [300, 400.1])
        self.assertTrue(out["ints"])

    def test_merge_is_union_and_erased_strokes_stay_erased(self):
        out = run_node(CORE % (
            "const a={v:1,ph:900,s:{a1:{d:[1,2,3]},x:{d:[1,1,1]}},g:{},u:'2026-01-01'};"
            "const b={v:1,ph:1500,s:{b1:{d:[4,5,6]},x:{d:[1,1,1]}},g:{a1:'2026-02-01'},u:'2026-02-01'};"
            "const m=I.mergeDocs(a,b);out.s=Object.keys(m.s).sort();out.g=Object.keys(m.g);out.ph=m.ph;out.u=m.u;"
            "out.comm=I.sameDoc(I.mergeDocs(b,a),m);out.idem=I.sameDoc(I.mergeDocs(m,m),m);"
            "out.c=[I.mergeDocs(Object.assign({},a,{c:3}),b).c,I.mergeDocs(a,Object.assign({},b,{c:1})).c,I.mergeDocs(a,b).c]"))
        self.assertEqual(out["c"], [3, 1, None])         # 내가 고른 보기 — 새 쪽 것, 없으면 옛 쪽 것
        self.assertEqual(out["s"], ["b1", "x"])          # a1 은 b 가 지웠다 — a 에 남아 있어도 되살아나지 않는다
        self.assertEqual(out["g"], ["a1"])
        self.assertEqual(out["ph"], 1500)
        self.assertEqual(out["u"], "2026-02-01")
        self.assertTrue(out["comm"] and out["idem"])

    def test_my_copy_of_a_note_is_frozen_and_merges_by_time(self):
        # 4판(2026-11-15) — 내 필기본은 쓰기 시작한 날의 원본을 떠 둔 사본. 원본이 고쳐져도 그대로이고, 두 기기가 다르면 나중에 뜬 쪽.
        out = run_node(CORE % (
            "const c1={id:'cn.x',title:'T',version:1,updated:'2026-11-01',hash:'h1',summary:['a'],sections:[{title:'S1',html:'<p>x</p>'}],pitfalls:[]};"
            "const c2=Object.assign({},c1,{version:2,hash:'h2',summary:['a','b'],sections:[{title:'S1',html:'<p>y</p>'},{title:'S2',html:'z'}]});"
            "const n1=I.snapOf(c1,'2026-11-10T00:00:00Z'),n2=I.snapOf(c2,'2026-11-12T00:00:00Z');"
            "c1.title='changed later';"
            "out.frozen=n1.c.title;out.stale=[I.snapStale(n1,c2),I.snapStale(n2,c2),I.snapStale(null,c2)];"
            "out.parts=I.changedParts(n1.c,c2);"
            "const a={v:1,ph:900,n:n1,s:{a1:{d:[1,2,3]}},g:{},u:'2026-11-10'},b={v:1,ph:900,n:n2,s:{b1:{d:[1,2,3]}},g:{},u:'2026-11-09'};"
            "const m=I.mergeDocs(a,b);out.ver=[m.n.ver,I.mergeDocs(b,a).n.ver,I.mergeDocs(a,{v:1,s:{},g:{},u:''}).n.ver];"
            "out.same=[I.sameDoc(m,I.mergeDocs(b,a)),I.sameDoc(I.normDoc(a),I.normDoc(Object.assign({},a,{n:n2})))];"
            "out.norm=[I.normDoc({n:{at:1}}).n,I.normDoc({}).n];"
            "out.sealed=(await I.unseal(await I.seal(a,'k'),'k')).n.c.id"))
        self.assertEqual(out["frozen"], "T")                       # 원본 객체를 나중에 고쳐도 사본은 그대로
        self.assertEqual(out["stale"], [True, False, False])
        self.assertEqual(out["parts"], ["빠른 요약", "S1", "S2(새 절)"])
        self.assertEqual(out["ver"], [2, 2, 1])                    # 나중에 뜬 판 · 한쪽에만 있으면 그것
        self.assertEqual(out["same"], [True, False])               # 판이 다르면 「같은 문서」가 아니다 → 올린다
        self.assertEqual(out["norm"], [None, None])
        self.assertEqual(out["sealed"], "cn.x")                    # 사본도 잠긴 봉투 안에 들어간다

    def test_sealed_note_opens_only_with_the_same_key(self):
        out = run_node(CORE % (
            "const d={v:1,ph:900,s:{a:{c:'#1b2430',w:2.6,t:0,b:'p',d:[10,10,15,5,5,15]}},g:{},u:'2026-11-15T00:00:00Z'};"
            "const e=await I.seal(d,'key-1');out.env=Object.keys(e).sort();out.alg=e.alg;out.n=e.n;"
            "out.leak=JSON.stringify(e).includes('#1b2430');"
            "out.back=JSON.stringify((await I.unseal(e,'key-1')).s)===JSON.stringify(d.s);"
            "try{await I.unseal(e,'key-2');out.wrong='opened'}catch(x){out.wrong='rejected'}"))
        self.assertEqual(out["env"], ["alg", "ct", "iv", "n", "updated", "v", "z"])
        self.assertEqual(out["alg"], "A256GCM")
        self.assertEqual(out["n"], 1)
        self.assertFalse(out["leak"])                    # 봉투에 획 내용이 그대로 보이지 않는다
        self.assertTrue(out["back"])
        self.assertEqual(out["wrong"], "rejected")


FN = ("import fs from 'fs';import {createRequire} from 'module';const require=createRequire(process.cwd()+'/');"
      "const M=await import('data:text/javascript,'+encodeURIComponent(fs.readFileSync('functions/api/ink.js','utf8')));"
      "const I=require('./docs/ink.js');const out={};"
      "const envOk=await I.seal({v:1,ph:900,s:{a:{d:[1,2,3]}},g:{},u:'2026-11-15T00:00:00Z'},'k1');"
      "const real=globalThis.fetch;"
      "function gh(script){const calls=[];globalThis.fetch=async(url,opt)=>{const m=(opt&&opt.method)||'GET',"
      "path=String(url).split('/repos/ehdbddl06001-ui/my-github-test/')[1];const body=opt&&opt.body?JSON.parse(opt.body):null;"
      "calls.push({m,path,body});const [s,d]=script(m,path,body);return new Response(JSON.stringify(d),{status:s})};return calls}"
      "const req=(method,qs,body,key)=>new Request('https://x.pages.dev/api/ink'+(qs||''),{method,"
      "headers:Object.assign({'content-type':'application/json'},key?{'x-sync-key':key}:{}),body:body?JSON.stringify(body):undefined});"
      "const ENV={GITHUB_TOKEN:'t',SYNC_KEY:'secret'};let r,calls;%s;globalThis.fetch=real;console.log(JSON.stringify(out));")


@unittest.skipUnless(NODE, "node 없음")
class Endpoint(unittest.TestCase):
    def test_only_ciphertext_and_valid_targets_are_accepted(self):
        out = run_node(FN % (
            "out.clean=[!!M.cleanEnvelope(envOk),M.cleanEnvelope({v:1,s:{}}),M.cleanEnvelope({v:1,alg:'A256GCM',iv:'<b>',ct:envOk.ct})];"
            "out.target=[M.validTarget('kmle','kmle-2026-1859'),M.validTarget('kmle','../x'),M.validTarget('zzz','a'),"
            "M.validTarget('concept','cn.allergy.anaphylaxis.im-epinephrine-first'),M.validTarget('variant','cn.a.b--v1'),M.validTarget('variant','cn.a.b#v1'),M.validTarget('meta','login-check')];"
            "r=await M.onRequestPost({request:req('POST','',{exam:'kmle',id:'a',env:{v:1,s:{x:1}}},'secret'),env:ENV});out.plain=r.status;"
            "r=await M.onRequestPost({request:req('POST','',{exam:'kmle',id:'a',env:envOk},'nope'),env:ENV});out.auth=r.status"), module=True)
        self.assertEqual(out["clean"], [True, None, None])
        self.assertEqual(out["target"], [True, False, False, True, True, False, True])
        self.assertEqual(out["plain"], 400)              # 잠그지 않은 필기는 저장소에 들어가지 않는다
        self.assertEqual(out["auth"], 401)

    def test_first_save_creates_the_side_branch_and_skips_pages_build(self):
        out = run_node(FN % (
            "let puts=0;calls=gh((m,p)=>{if(m==='PUT'){puts++;return puts===1?[404,{}]:[201,{content:{sha:'newsha'}}]}"
            "if(m==='GET'&&p.startsWith('git/ref/'))return[404,{}];if(p==='git/trees')return[201,{sha:'t1'}];"
            "if(p==='git/commits')return[201,{sha:'c1'}];if(p==='git/refs')return[201,{}];return[500,{}]});"
            "r=await M.onRequestPost({request:req('POST','',{exam:'kmle',id:'kmle-2026-1859',sha:null,env:envOk,device:'pc-abc'},'secret'),env:ENV});"
            "out.status=r.status;out.sha=(await r.json()).sha;out.seq=calls.map(c=>c.m+' '+c.path);out.msg=calls[0].body.message;"
            "out.branch=calls[0].body.branch;out.parents=calls.find(c=>c.path==='git/commits').body.parents;"
            "out.ref=calls.find(c=>c.path==='git/refs').body.ref;"
            "out.stored=Object.keys(JSON.parse(Buffer.from(calls[0].body.content,'base64').toString('utf8'))).sort()"), module=True)
        self.assertEqual(out["status"], 200)
        self.assertEqual(out["sha"], "newsha")
        self.assertEqual(out["seq"][0], "PUT contents/state/ink_sync/kmle/kmle-2026-1859.json")
        self.assertEqual(out["seq"][1:5], ["GET git/ref/heads/ink-data", "POST git/trees", "POST git/commits", "POST git/refs"])
        self.assertEqual(out["branch"], "ink-data")      # main 이 아니다 — 루틴의 푸시 · 배포를 건드리지 않는다
        self.assertEqual(out["parents"], [])
        self.assertEqual(out["ref"], "refs/heads/ink-data")
        self.assertTrue(out["msg"].startswith("[CF-Pages-Skip] "))
        self.assertEqual(out["stored"], ["alg", "ct", "iv", "n", "updated", "v", "z"])

    def test_stale_sha_is_a_conflict_and_lists_read_the_side_branch(self):
        out = run_node(FN % (
            "gh(()=>[409,{}]);r=await M.onRequestPost({request:req('POST','',{exam:'kmle',id:'a',sha:'old',env:envOk},'secret'),env:ENV});out.c409=r.status;"
            "gh(()=>[422,{}]);r=await M.onRequestPost({request:req('POST','',{exam:'kmle',id:'a',env:envOk},'secret'),env:ENV});out.c422=r.status;"
            "gh(()=>[404,{}]);r=await M.onRequestGet({request:req('GET','?exam=kmle',null,'secret'),env:ENV});out.empty=(await r.json()).files;"
            "calls=gh(()=>[200,[{type:'file',name:'q1.json',sha:'s1'},{type:'file',name:'README.md',sha:'x'}]]);"
            "r=await M.onRequestGet({request:req('GET','?exam=kmle',null,'secret'),env:ENV});out.files=(await r.json()).files;out.ref=calls[0].path;"
            "gh(()=>[404,{}]);r=await M.onRequestGet({request:req('GET','?exam=kmle&id=nope',null,'secret'),env:ENV});"
            "out.none=[r.status,(r.headers.get('content-type')||'').includes('json')]"), module=True)
        self.assertEqual(out["c409"], 409)
        self.assertEqual(out["c422"], 409)               # sha 없이 이미 있는 파일 = 다른 기기가 먼저 썼다
        self.assertEqual(out["empty"], {})
        self.assertEqual(out["files"], {"q1": "s1"})
        self.assertTrue(out["ref"].endswith("?ref=ink-data"))
        self.assertEqual(out["none"], [404, True])       # 「필기 없음」은 JSON 404 — 앱이 「서버 없음」과 구별한다


@unittest.skipUnless(NODE, "node 없음")
class Login(unittest.TestCase):
    def test_same_id_and_password_give_the_same_key_on_any_device(self):
        # 2026-11-15 — 키를 손으로 옮기지 않는다: 아이디 · 비밀번호에서 기기가 계산한다
        out = run_node(CORE % (
            "out.a=await I.loginKey('Dong ','correct horse battery');out.b=await I.loginKey('dong','correct horse battery');"
            "out.c=await I.loginKey('dong','correct horse batterz');out.d=await I.loginKey('dong2','correct horse battery')"))
        self.assertEqual(out["a"], out["b"])             # 아이디는 공백 · 대소문자를 가리지 않는다
        self.assertNotEqual(out["a"], out["c"])
        self.assertNotEqual(out["a"], out["d"])          # 아이디가 소금이다
        self.assertRegex(out["a"], r"^lk1-[A-Za-z0-9_-]{43}$")

    def test_check_blob_opens_only_with_the_right_password(self):
        out = run_node(CORE % (
            "const k=await I.loginKey('dong','correct horse battery'),bad=await I.loginKey('dong','wrong password!');"
            "const e=await I.seal(I.emptyDoc(),k);out.ok=!!(await I.unseal(e,k));"
            "try{await I.unseal(e,bad);out.bad='opened'}catch(x){out.bad='rejected'}"))
        self.assertTrue(out["ok"])
        self.assertEqual(out["bad"], "rejected")


@unittest.skipUnless(NODE, "node 없음")
class Syntax(unittest.TestCase):
    def test_app_scripts_parse(self):
        # 2026-11-15 — 따옴표 안에 줄바꿈 하나가 들어가 ink.js 가 통째로 안 돌았는데 글자 찾기 시험은 전부 통과했다.
        for name in ("ink.js", "app.js", "learn.js", "synckey.js", "pwa.js", "sw.js"):
            r = subprocess.run([NODE, "--check", str(DOCS / name)], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(r.returncode, 0, name + "\n" + r.stderr[-400:])


class Wiring(unittest.TestCase):
    def test_no_raw_newline_inside_double_quoted_strings(self):
        # node 가 없는 PC 에서도 잡히게 — 한 줄에 큰따옴표가 홀수 개면 문자열이 줄을 넘은 것이다(주석 · 백틱 줄은 뺀다)
        ink = (DOCS / "ink.js").read_text(encoding="utf-8")
        bad = []
        for i, line in enumerate(ink.split("\n"), 1):
            code = line.split("//")[0]
            if "`" in code or "/*" in code or code.lstrip().startswith("*"):
                continue
            if code.replace('\\"', "").count('"') % 2:
                bad.append(i)
        self.assertEqual(bad, [])

    def test_login_never_sends_the_password(self):
        ink = (DOCS / "ink.js").read_text(encoding="utf-8")
        fn = (ROOT / "functions" / "api" / "ink.js").read_text(encoding="utf-8")
        body = ink[ink.index("async function loginTry("):ink.index("async function applyKey(")]
        self.assertNotIn("pw }", body)
        self.assertNotIn("password", body)               # 서버로 가는 것은 확인용 암호문뿐
        self.assertIn('env: await seal(emptyDoc(), key)', body)
        self.assertIn('autocomplete="current-password"', ink)       # 기기의 비밀번호 저장이 채워 주게
        self.assertIn('"medkos-login-v1:"', ink)
        self.assertIn('"meta"', fn)

    def test_app_asks_for_login_on_entry_but_never_traps(self):
        # 2026-11-15 — 키가 없는 기기는 앱을 열 때 로그인 화면을 본다. 잠금장치가 아니므로 빠져나갈 길을 둔다.
        ink = (DOCS / "ink.js").read_text(encoding="utf-8")
        self.assertIn("  addButtons();\n  gateIfNeeded();", ink)
        self.assertIn("if (pass() || skipped || !subtle || location.protocol === \"file:\") return;", ink)
        self.assertIn("로그인 없이 쓰기(이 기기에만 저장)", ink)

    def test_index_loads_ink_after_app_with_the_cache_version(self):
        html = (DOCS / "index.html").read_text(encoding="utf-8")
        ver = re.search(r'const VERSION = "medkos-v(\d+)"', (DOCS / "sw.js").read_text(encoding="utf-8")).group(1)
        self.assertIn(f'<script src="ink.js?v={ver}"></script>', html)
        self.assertLess(html.index('<script src="app.js'), html.index('<script src="ink.js'))
        self.assertIn('"./ink.js"', (DOCS / "sw.js").read_text(encoding="utf-8"))

    def test_wrongbook_offers_the_ink_button(self):
        app = (DOCS / "app.js").read_text(encoding="utf-8")
        self.assertIn("MEDKOS_INK.decorate(list)", app)
        ink = (DOCS / "ink.js").read_text(encoding="utf-8")
        self.assertIn('button[data-note]', ink)          # 글 메모 단추 옆에 붙는다 — 그 표식이 바뀌면 필기 단추가 사라진다

    def test_app_uploads_only_the_sealed_envelope(self):
        ink = (DOCS / "ink.js").read_text(encoding="utf-8")
        posts = re.findall(r'method: "POST".*?body: JSON\.stringify\((\{.*?\})\)', ink, flags=re.S)
        self.assertEqual(len(posts), 2)                  # 필기 올리기 · 로그인 확인용 암호문 — 둘뿐
        self.assertIn("env: await seal(rec.doc, pass())", posts[0])
        self.assertIn("env: await seal(emptyDoc(), key)", posts[1])
        for body in posts:
            self.assertNotIn("doc:", body)               # 잠그지 않은 필기를 보내지 않는다
        self.assertIn("if (!canSync()) return \"local\";", ink)   # 키 · 서버가 없으면 기기에만

    def test_every_question_and_concept_note_can_be_written_on(self):
        # 2판(2026-11-15) — 오답만이 아니라 푸는 문항 전부 · 개념 정리본(학습서의 단위)에도 쓴다.
        ink = (DOCS / "ink.js").read_text(encoding="utf-8")
        learn = (DOCS / "learn.js").read_text(encoding="utf-8")
        fn = (ROOT / "functions" / "api" / "ink.js").read_text(encoding="utf-8")
        self.assertIn('getElementById("quitBtn")', ink)                 # 문항 화면에 「펜으로 풀기」를 끼우는 자리
        self.assertIn('querySelectorAll("#options .opt")[i]', ink)      # 채점은 앱의 보기 단추가 한다(기록이 한 곳에서만)
        self.assertIn("const veiled = (sid) => UI.hideOld && !UI.mine[sid];", ink)   # 푸는 중엔 전에 쓴 필기를 가린다
        self.assertIn("MEDKOS_INK.conceptButton(box, c.id)", learn)
        self.assertIn("load, concept, STATUS, flagsOf, setFlag };", learn)
        self.assertIn('L.setFlag(UI.st.q, "want_note"', ink)            # 맞힌 문항도 정리본 큐로
        self.assertIn('new Set(["kmle", "usmle", "imaging", "variant", "concept", "meta"])', fn)
        self.assertIn('replace(/#/g, "--")', ink)                       # 변형 문항 id 의 # 은 파일 이름에 못 쓴다

    def test_study_book_writes_on_the_latest_note_and_tells_what_changed(self):
        # 학습서 필기(2026-11-15 2차 「항상 최신판 위에 필기」) — 종이는 늘 최신 정리본, 필기는 그 위에 남는다. 「내 필기본」 구분은 없다.
        # 필기할 때의 판은 조용히 떠 두었다가 정리본이 고쳐지면 바뀐 곳을 알리고 「전에 쓴 판 보기」(읽기만)로 다시 볼 수 있게 한다.
        ink = (DOCS / "ink.js").read_text(encoding="utf-8")
        learn = (DOCS / "learn.js").read_text(encoding="utf-8")
        css = (DOCS / "style.css").read_text(encoding="utf-8")
        self.assertIn("const c = over || concept(cid);", learn)
        self.assertIn("const use = st.old ? n.c : (st.live || (n && n.c));", ink)      # 기본은 최신판 · 목록에서 빠지면 떠 둔 판
        self.assertIn("L.renderConcept(box, st.id, null, null, use)", ink)
        self.assertEqual(ink.count("rec.doc.n = snapOf(st.live)"), 2)                # 판을 뜨는 곳은 둘뿐 — 첫 필기 · 「확인」
        self.assertIn('data-note-act="ack"', ink)
        self.assertIn('data-note-act="old"', ink)
        self.assertNotIn("✍ 내 필기본", ink)                                             # 구분을 없앴다
        self.assertIn('UI.el.classList.toggle("old", st.kind === "concept" && !!st.old);', ink)
        self.assertIn(".ink-ov.old .ink-layer{pointer-events:none}", css)             # 전에 쓴 판 = 읽기만
        self.assertIn('b.id = "inkShelfBtn"', ink)
        self.assertIn('document.getElementById("navInk")', ink)                       # 「필기 모음」은 메뉴 줄 맨 위에
        for page in ("index.html", "papers.html", "search.html", "whatsnew.html", "ailab.html", "atlas3d.html"):
            self.assertIn('<a href="index.html?view=ink" id="navInk">✍ 필기 모음</a>', (DOCS / page).read_text(encoding="utf-8"), page)
        try:
            import yaml
        except ImportError:
            self.skipTest("pyyaml 없음")
        books = yaml.safe_load((ROOT / "pipelines" / "books_config.yaml").read_text(encoding="utf-8"))["books"]
        self.assertEqual(json.loads(re.search(r"const BOOKS = (\{.*?\});", ink).group(1)), books)   # 과목 → 책 이름은 PDF 학습서와 같게

    def test_paper_stays_sharp_and_fits_one_page(self):
        # 5판(2026-11-15) — 「PDF 를 필기 앱으로 연 것만큼 선명하게 · 한 내용이 한 쪽에 · 확대 축소」.
        ink = (DOCS / "ink.js").read_text(encoding="utf-8")
        css = (DOCS / "style.css").read_text(encoding="utf-8")
        # 필기 캔버스는 transform 을 건 종이의 **밖**(형제)에 둔다 — 안에 두면 Safari 가 종이를 저해상도 그림으로 굳혀 늘린다
        self.assertIn('<div class="ink-sheet"><div class="ink-content"></div></div><div class="ink-layer"></div>', ink)
        self.assertIn(".ink-sheet .deep-body table, .ink-sheet .cn-body table{display:table !important; overflow:visible !important}", css)
        self.assertIn("c.width = c.height = Math.max(1, Math.round(TPX * UI.q / s));", ink)   # 조각 화소 = 화면 px × 기기 배율(확대와 무관)
        self.assertIn("UI.q = UI.s * (window.devicePixelRatio || 1);", ink)                    # 선명도 상한 없음
        self.assertIn("function zoomTo(z, lx, ly, cx, cy)", ink)
        self.assertIn('sc.addEventListener("touchmove"', ink)                                  # 두 손가락 확대 · 축소
        self.assertIn(".ink-content.cols .ink-cn .concept{column-count:2; column-gap:56px}", css)   # 둘째 단의 덩이가 정확히 820 오른쪽
        self.assertIn("break-inside:avoid", css)                                               # 덩이는 단 사이에서 쪼개지지 않는다
        self.assertIn("const WIDTHS = [0.5, 0.8, 1.2, 1.8, 2.6, 4.0];", ink)

    def test_pen_feel_and_layout_stay_wired(self):
        # 3판(2026-11-15) — 써 본 뒤의 요청: 획 부드럽게 · 색 여러 개 · 직선 · 문항이 한 화면에 · 필기장에서 키 넣기
        ink = (DOCS / "ink.js").read_text(encoding="utf-8")
        css = (DOCS / "style.css").read_text(encoding="utf-8")
        self.assertIn("inkPiece(a.st, a.mx, a.my,", ink)               # 쓰는 동안에도 다시 그릴 때와 같은 곡선 조각으로
        self.assertIn("function widthsOf(pts, w)", ink)
        self.assertEqual(len(re.search(r'const COLORS = \[(.*?)\];', ink).group(1).split(',')), 12)
        self.assertIn("function holdToLine(a)", ink)                 # 긋다가 멈추면 직선
        self.assertIn("x: blk ? left : Math.max(0, Math.round((r.left - a0) / UI.s))", ink)   # 획은 덩이 왼쪽 위 기준(정리본 절은 단의 왼쪽 끝)
        self.assertIn(".ink-content.side{display:grid; grid-template-columns:820px 820px;", css)
        self.assertIn("async function loginTry(id, pw, pw2)", ink)
        self.assertIn("even: t.even !== false", ink)                  # 기본은 고른 굵기(직선과 같은 선)
        self.assertIn("if (UI.tool.even) return 0.5;", ink)
        self.assertIn("const R = ERASE_R, from = UI.erasePrev || p;", ink)   # 보이는 지우개 원과 실제 지우는 범위가 같은 값

    def test_function_keeps_main_untouched(self):
        fn = (ROOT / "functions" / "api" / "ink.js").read_text(encoding="utf-8")
        self.assertIn('env.INK_BRANCH || "ink-data"', fn)
        self.assertIn('const SKIP = "[CF-Pages-Skip] ";', fn)
        self.assertNotIn('"main"', fn)


if __name__ == "__main__":
    unittest.main(verbosity=1)
