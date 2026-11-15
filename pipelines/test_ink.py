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
            "out.comm=I.sameDoc(I.mergeDocs(b,a),m);out.idem=I.sameDoc(I.mergeDocs(m,m),m)"))
        self.assertEqual(out["s"], ["b1", "x"])          # a1 은 b 가 지웠다 — a 에 남아 있어도 되살아나지 않는다
        self.assertEqual(out["g"], ["a1"])
        self.assertEqual(out["ph"], 1500)
        self.assertEqual(out["u"], "2026-02-01")
        self.assertTrue(out["comm"] and out["idem"])

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
            "out.target=[M.validTarget('kmle','kmle-2026-1859'),M.validTarget('kmle','../x'),M.validTarget('zzz','a')];"
            "r=await M.onRequestPost({request:req('POST','',{exam:'kmle',id:'a',env:{v:1,s:{x:1}}},'secret'),env:ENV});out.plain=r.status;"
            "r=await M.onRequestPost({request:req('POST','',{exam:'kmle',id:'a',env:envOk},'nope'),env:ENV});out.auth=r.status"), module=True)
        self.assertEqual(out["clean"], [True, None, None])
        self.assertEqual(out["target"], [True, False, False])
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


class Wiring(unittest.TestCase):
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
        self.assertEqual(len(posts), 1)
        self.assertIn("env: await seal(rec.doc, pass())", posts[0])
        self.assertNotIn("doc:", posts[0])               # 잠그지 않은 필기를 보내지 않는다
        self.assertIn("if (!canSync()) return \"local\";", ink)   # 키 · 서버가 없으면 기기에만

    def test_function_keeps_main_untouched(self):
        fn = (ROOT / "functions" / "api" / "ink.js").read_text(encoding="utf-8")
        self.assertIn('env.INK_BRANCH || "ink-data"', fn)
        self.assertIn('const SKIP = "[CF-Pages-Skip] ";', fn)
        self.assertNotIn('"main"', fn)


if __name__ == "__main__":
    unittest.main(verbosity=1)
