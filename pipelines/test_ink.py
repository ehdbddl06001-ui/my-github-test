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

    def test_smoothing_follows_fast_strokes_and_calms_slow_ones(self):
        # 엔진 2 의 떨림 보정(1-Euro · EURO 값). 240 Hz 펜슬을 흉내 낸 모의 필기:
        #   서 있을 때 ±0.5 px 떨림은 절반 아래로 · 멈춤에서 700 px/s 로 출발해도 3 px 안쪽으로 따라붙고 · ㄱ 꺾임의 꼭짓점을 1.5 px 안으로 지난다.
        # 빠르기 추정 차단을 1 Hz(흔한 기본값)로 두면 출발이 6 px 늦는다 — 값을 바꿀 때 이 시험이 잡는다.
        out = run_node(CORE % (
            "const E=I.EURO,hz=240,dt=1000/hz,rnd=(i,k)=>((Math.sin(i*k)*43758.5453)%1)*0.5;"
            "let f=I.euroNew(E[0],E[1],E[2]),t=0,dev=0;"
            "for(let i=0;i<hz;i++){t+=dt;const p=I.euroStep(f,100+rnd(i,12.9898),100+rnd(i,78.233),t);if(i>60)dev=Math.max(dev,Math.hypot(p[0]-100,p[1]-100));}"
            "out.jitter=dev;"
            "f=I.euroNew(E[0],E[1],E[2]);t=0;let lag=0,x=0,v=0;I.euroStep(f,0,0,0);"
            "for(let i=0;i<hz/2;i++){t+=dt;v=Math.min(700,v+700*dt/40);x+=v*dt/1000;const p=I.euroStep(f,x,0,t);lag=Math.max(lag,x-p[0]);}"
            "out.lag=lag;"
            "f=I.euroNew(E[0],E[1],E[2]);t=0;let miss=1e9;const n=36,d=60;"
            "for(let i=0;i<=2*n;i++){t+=dt;const X=i<=n?d*i/n:d,Y=i<=n?0:d*(i-n)/n;const p=I.euroStep(f,X,Y,t);miss=Math.min(miss,Math.hypot(p[0]-d,p[1]));}"
            "out.corner=miss;"
            "f=I.euroNew(E[0],E[1],E[2]);let far=0;for(let i=0;i<40;i++){const p=I.euroStep(f,i*5,0,1000);far=p[0];}out.same=far;out.E=E"))
        self.assertEqual(out["E"], [4, 0.06, 10])
        self.assertLess(out["jitter"], 0.35)
        self.assertLess(out["lag"], 3.0)
        self.assertLess(out["corner"], 1.5)
        self.assertGreater(out["same"], 150)             # 시각이 모두 같은 점(묶여 온 입력)이어도 멈추지 않고 따라간다(끝점 195)

    def test_fountain_ribbon_has_no_holes_and_one_winding(self):
        # 만년필 — 굵기가 변하는 획을 띠 + 원으로 바꿔 한 번에 채운다. 모두 같은 방향으로 감아야 겹친 곳(되짚어 긋기)에 구멍이 안 난다.
        out = run_node(CORE % (
            "const penW=(w,p)=>w*(0.4+1.2*p);"
            "const mk=(pts)=>{const ws=pts.filter((_,i)=>i%3===2).map(p=>penW(3,p));const s=I.strokeSamples(pts,ws,1.2,0,0);return [s,I.ribbon(s)];};"
            "const cases={curve:[0,0,.5,10,0,.6,20,5,.7,20,25,.4,5,30,.3],corner:[0,0,.5,30,0,.6,30,0.2,.6,30,30,.5],"
            "hairpin:[0,10,.5,40,10,.6,0,10.5,.6,40,11,.5,0,11.5,.5],dot:[5,5,.5]};"
            "for(const k in cases){const [s,r]=mk(cases[k]);"
            "out[k]={n:s.length/3,bands:r.filter(q=>q[0]===2).length,circles:r.filter(q=>q[0]===0).length,"
            "cw:r.filter(q=>q[0]===2).every(q=>I.polyTurn(q)>0),first:s.slice(0,2),last:s.slice(-3,-1)};}"
            # 쓰는 동안 마디마다 그린 표본을 이으면 다시 그릴 때의 표본과 같다
            "const p=cases.curve,ws=p.filter((_,i)=>i%3===2).map(x=>penW(3,x));const whole=I.strokeSamples(p,ws,1.2,0,0);"
            "let ax=p[0],ay=p[1],wa=ws[0],acc=[ax,ay,wa];const n=p.length/3;"
            "for(let i=1;i<n-1;i++){const mx=(p[i*3]+p[i*3+3])/2,my=(p[i*3+1]+p[i*3+4])/2,wm=(ws[i]+ws[i+1])/2;I.curveSamples(acc,ax,ay,p[i*3],p[i*3+1],mx,my,wa,wm,1.2);ax=mx;ay=my;wa=wm;}"
            "const lx=p[(n-1)*3],ly=p[(n-1)*3+1];I.curveSamples(acc,ax,ay,(ax+lx)/2,(ay+ly)/2,lx,ly,wa,ws[n-1],1.2);"
            "out.same=JSON.stringify(acc)===JSON.stringify(whole);"
            "out.even=[I.evenStroke([0,0,.5,1,1,.5,2,2,.5]),I.evenStroke([0,0,.5,1,1,.6])]"))
        for k in ("curve", "corner", "hairpin"):
            self.assertTrue(out[k]["cw"], k)
            self.assertEqual(out[k]["circles"], out[k]["bands"] + 1, k)      # 양 끝 + 띠 사이마다 원 하나
        self.assertEqual(out["curve"]["bands"], 1)                           # 완만한 굽이는 띠 하나
        self.assertEqual(out["corner"]["bands"], 2)                          # 직각은 띠를 끊고 원으로 잇는다
        self.assertGreaterEqual(out["hairpin"]["bands"], 4)                  # 되짚는 곳마다 끊는다(한 띠 안에서 좌우가 뒤집히지 않게)
        self.assertEqual((out["curve"]["first"], out["curve"]["last"]), ([0, 0], [5, 30]))
        self.assertEqual((out["dot"]["bands"], out["dot"]["circles"]), (0, 1))
        self.assertTrue(out["same"])
        self.assertEqual(out["even"], [True, False])

    def test_highlighter_straightens_only_near_horizontal_strokes(self):
        out = run_node(CORE % (
            "out.flat=I.straightenH([10,50,.5,60,52,.5,120,49,.5,200,51,.5]);"
            "out.wavy=I.straightenH([10,50,.5,60,70,.5,120,49,.5]);"
            "out.short=I.straightenH([10,50,.5,20,50,.5]);"
            "out.back=I.straightenH([10,50,.5,100,50,.5,40,51,.5,120,50,.5])"))
        self.assertEqual(out["flat"], [10, 50.5, 0.5, 200, 50.5, 0.5])        # 평균 높이의 수평선 두 점
        self.assertEqual((out["wavy"], out["short"], out["back"]), (None, None, None))

    def test_undo_and_redo_hand_the_inverse_step_to_each_other(self):
        out = run_node(CORE % (
            "const doc={s:{a:{d:[1]}},g:{}};let n=0;const id=()=>'n'+(++n);"
            "const u1=I.histApply(doc,{add:'a'},id,'T1');out.afterUndo=JSON.parse(JSON.stringify(doc));out.u1=u1;"
            "const r1=I.histApply(doc,u1,id,'T2');out.afterRedo=JSON.parse(JSON.stringify(doc));out.r1=r1;"
            "out.gone=I.histApply(doc,{add:'zz'},id,'T3')"))
        self.assertEqual(out["afterUndo"], {"s": {}, "g": {"a": "T1"}})          # 뺀 획은 묘비를 남긴다(다른 기기와 합칠 때 되살아나지 않게)
        self.assertEqual(out["u1"], {"put": {"d": [1]}, "was": "a"})
        self.assertEqual(out["afterRedo"], {"s": {"n1": {"d": [1]}}, "g": {"a": "T1"}})   # 되살릴 때는 새 id
        self.assertEqual(out["r1"], {"add": "n1"})
        self.assertIsNone(out["gone"])                                           # 이미 없는 획은 걸음을 버린다

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
        # 메뉴 줄 맨 위에 「학습서 필기」, 「필기 모음」은 그 안에(첫 화면 단추 줄에는 필기 단추를 두지 않는다)
        self.assertIn('document.getElementById("navShelf")', ink)
        self.assertNotIn("inkShelfBtn", ink)
        self.assertNotIn("inkAllBtn", ink)
        self.assertIn('<button data-a="all" title="필기가 있는 문항 · 정리본 전부">✍ 필기 모음</button>', ink)
        self.assertIn('if (b.getAttribute("data-a") === "all") return showAll();', ink)
        for page in ("index.html", "papers.html", "search.html", "whatsnew.html", "ailab.html", "atlas3d.html"):
            self.assertIn('<a href="index.html?view=shelf" id="navShelf">📖 학습서 필기</a>', (DOCS / page).read_text(encoding="utf-8"), page)
        try:
            import yaml
        except ImportError:
            self.skipTest("pyyaml 없음")
        books = yaml.safe_load((ROOT / "pipelines" / "books_config.yaml").read_text(encoding="utf-8"))["books"]
        self.assertEqual(json.loads(re.search(r"const BOOKS = (\{.*?\});", ink).group(1)), books)   # 과목 → 책 이름은 PDF 학습서와 같게

    def test_note_collection_is_split_by_kind_field_and_result(self):
        # 필기 모음(2026-11-15 2차) — 종류(KMLE · USMLE · 정리본 · 논문) → 분야 → KMLE · USMLE 는 틀린 문항 / 맞힌 문항.
        ink = (DOCS / "ink.js").read_text(encoding="utf-8")
        self.assertIn('const TABS = ["kmle", "usmle", "concept", "paper", "imaging", "variant"], ALWAYS = 4;', ink)
        self.assertIn("wrong: !!wrongEntry(ex, id)", ink)                              # 틀린 문항 = 지금 오답노트에 있는 문항
        self.assertIn("rows = rows.filter((x) => x.wrong === (ALLV.sub === \"wrong\"));", ink)
        self.assertIn("const fieldName = (t) => BOOKS[t] || t || \"기타\";", ink)        # 분야 이름은 학습서의 책 이름과 같게
        self.assertIn('localStorage.getItem("medkos_paper_notes")', ink)               # 논문 칸 = 논문 화면에서 적은 메모
        self.assertIn('s.src = "papers.js";', ink)                                     # 논문 묶음은 그 칸을 열 때만 읽는다

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
        colors = re.search(r'const COLORS = \[(.*?)\];', ink, re.S).group(1)
        self.assertEqual(len(re.findall(r'"#[0-9a-f]{6}"', colors)), 24)   # 펜 색 24(엔진 2 — 3판은 12)
        self.assertEqual(len(set(re.findall(r'"#[0-9a-f]{6}"', colors))), 24)
        self.assertEqual(len(re.findall(r'"#[0-9a-f]{6}"', re.search(r'const HLS = \[(.*?)\];', ink).group(1))), 10)
        self.assertIn("function holdToLine(a)", ink)                 # 긋다가 멈추면 직선
        self.assertIn("x: blk ? left : Math.max(0, Math.round((r.left - a0) / UI.s))", ink)   # 획은 덩이 왼쪽 위 기준(정리본 절은 단의 왼쪽 끝)
        self.assertIn(".ink-content.side{display:grid; grid-template-columns:820px 820px;", css)
        self.assertIn("async function loginTry(id, pw, pw2)", ink)
        self.assertIn("even: t.even !== false", ink)                  # 기본은 고른 굵기(직선과 같은 선)
        self.assertIn("if (UI.tool.even) return 0.5;", ink)
        # 보이는 지우개 원과 실제 지우는 범위가 같은 값 — 크기를 바꿔도(엔진 2: 지름 6~44) 둘이 함께 바뀐다
        self.assertIn("const eraseR = () => UI.tool.eraseD / 2;", ink)
        self.assertIn("const ctx = liveCtx(), R = eraseR();", ink)
        self.assertIn("const R = eraseR(), hlOnly = UI.tool.hlOnly, from = UI.erasePrev || p;", ink)

    def test_engine_two_writes_without_measuring_and_draws_once_per_segment(self):
        # 필기 엔진 2(2026-11-23 vNext Phase 2) — 「느리다」의 원인 둘: 점마다 getBoundingClientRect(강제 배치 계산) ·
        # 마디마다 최대 96 번 stroke. 미리보기에서 120 점짜리 획으로 세어 보니 재기 1074 → 3 회, 덧층 전체 지우기 120 → 2 회.
        ink = (DOCS / "ink.js").read_text(encoding="utf-8")
        css = (DOCS / "style.css").read_text(encoding="utf-8")
        body = lambda name: ink[ink.index(f"  function {name}("):ink.index("\n  }\n", ink.index(f"  function {name}("))]
        self.assertNotIn("getBoundingClientRect", body("pt"))                  # 좌표는 자리 값(UI.rc)으로만
        self.assertNotIn("getBoundingClientRect", body("liveCtx"))
        self.assertNotIn("getBoundingClientRect", body("tipRect"))
        self.assertIn("if (UI.rc && eng2()) return UI.rc;", body("measure"))   # 한 번 재면 다시 재지 않는다(이전 엔진은 매번)
        self.assertIn("UI.rc = null;                                              // 획을 시작할 때 자리 값을 한 번 잰다", ink)
        self.assertIn('UI.scroll.addEventListener("scroll", () => { UI.rc = null;', ink)   # 스크롤 · 배치가 바뀌면 버린다
        self.assertIn("if (eng2() && UI.tip) ctx.clearRect(UI.tip[0], UI.tip[1],", ink)     # 덧층은 앞에 그린 네모만 지운다
        # 한 마디에 그리기 한 번 — 볼펜은 곡선 하나, 만년필은 띠 한 번 채우기. 다시 그릴 때도 획 하나에 한 번.
        piece = body("inkPiece")
        self.assertIn("ctx.quadraticCurveTo(cx, cy, bx, by); ctx.stroke();", piece)
        self.assertIn("else if (shapes) fillShapes(ctx, shapes);", piece)
        self.assertIn("if (st.even) { ctx.lineWidth = ws[0]; hlPath(ctx, p, dx, dy); }", ink)
        self.assertIn("else fillShapes(ctx, ribbon(strokeSamples(p, ws, ribbonStep(), dx, dy)));", ink)
        self.assertEqual(body("fillShapes").count("ctx.fill()"), 1)
        # 떨림 보정 · 예측 점 · 뗀 자리로 끝 맞추기
        self.assertIn("const EURO = [4, 0.06, 10];", ink)
        self.assertIn("euroStep(a.f, ev.clientX, ev.clientY, ev.timeStamp || 0)", ink)
        self.assertIn('typeof e.getPredictedEvents === "function"', ink)
        self.assertIn('if (a.f && e.type === "pointerup") {', ink)
        # 형광펜 — 따로 된 층에서 곱하기로 섞는다(덧칠해도 아래 글자가 검다) · 자동 수평 직선 · 형광펜만 지우기
        self.assertIn(".ink-hl{position:absolute; left:0; top:0; width:100%; height:100%; pointer-events:none; mix-blend-mode:multiply}", css)
        self.assertIn(".ink-live.mul{mix-blend-mode:multiply}", css)
        self.assertIn("if (split ? !!st.t !== !!t.hl : t.hl) return;", ink)
        self.assertIn("if (a.st.t && UI.tool.hlStraight && eng2()) {", ink)
        self.assertIn("(hlOnly && !st.t)) return;", ink)
        # 이전 엔진 스위치 — 기기에서 새 엔진이 이상하면 되돌린다. 저장 형식은 같다(획에 엔진 표시를 남기지 않는다).
        self.assertIn("engine: t.engine === 1 ? 1 : 2 };", ink)
        self.assertIn('<button data-a="engine" data-v="1"', ink)
        self.assertIn("else piece(ctx, ax, ay, cx, cy, bx, by, wa, wb);", piece)       # 이전 엔진의 그리기가 남아 있다
        self.assertIn("UI.rec.doc.s[sid] = { c: st.c, w: st.w, t: st.t, b: a.b, d: pack(a.pts) };", ink)
        self.assertIn(".ink-ov.eng1 .ink-hl{display:none}", css)

    def test_dock_redo_gestures_laser_and_cornell_margin(self):
        ink = (DOCS / "ink.js").read_text(encoding="utf-8")
        css = (DOCS / "style.css").read_text(encoding="utf-8")
        for k in ("ball", "fountain", "laser"):
            self.assertIn(f'<button data-a="tool" data-k="{k}"', ink)
        self.assertIn("const NQUICK = 6;", ink)                                  # 빠른 색 6칸
        self.assertIn('<input type="color" data-in="custom"', ink)               # 직접 고른 색
        self.assertIn('data-a="wslot"', ink)                                     # 굵기 3칸 + 슬라이더
        self.assertIn('<input type="range" data-in="width"', ink)
        self.assertIn("const ERASE_SIZES = [8, 16, 30], ERASE_MIN = 6, ERASE_MAX = 44;", ink)
        self.assertIn('<input type="range" data-in="erase"', ink)
        # 다시실행 — 되돌리기와 같은 걸음(histApply)을 서로 주고받는다. 새로 쓰면 다시실행 더미를 비운다.
        self.assertIn("function undo() { histMove(UI.undo, UI.redo); }", ink)
        self.assertIn("function redo() { histMove(UI.redo, UI.undo); }", ink)
        self.assertIn("UI.redo = [];                                                 // 새로 쓰면 다시실행 더미는 비운다", ink)
        self.assertIn("if (o.add === op.was) o.add = inv.add;", ink)             # 지웠다 되살린 획의 id 가 바뀌어도 더미가 따라간다
        self.assertIn("Math.abs(p.k - 1) < 0.04 && Math.hypot(p.x - p.x0, p.y - p.y0) < 10) { ensureTiles(); undo();", ink)   # 두 손가락 톡
        self.assertIn("if (e.touches.length === 3 && !palm) {", ink)             # 세 손가락 톡 = 다시실행
        # 레이저 — 저장하지 않는다(획 더미 · 문서에 들어가지 않는다)
        self.assertIn("const LASER_MS = 2500;", ink)
        laser = ink[ink.index("  function drawLaser("):ink.index("  function laserLoop(")]
        self.assertNotIn("doc.s", laser)
        self.assertNotIn("commitStroke", laser)
        # 코넬 여백 — 덩이 이름 "m". 다른 덩이의 자리 · 폭은 그대로(종이 폭만 352 늘어난다)
        self.assertIn("const MARGIN_W = 352;", ink)
        self.assertIn('data-b="m"', ink)
        self.assertIn("const SW = (side ? 2 * W + GAP : cols ? 2 * W : W) + mg;", ink)
        self.assertIn('if (b === "m") return !UI.geo.m;', ink)                   # 여백이 없는 종이에서는 여백 필기를 그리지 않는다
        self.assertIn(".ink-content.margin{padding-right:352px}", css)
        self.assertIn("width:352px;", css)

    def test_function_keeps_main_untouched(self):
        fn = (ROOT / "functions" / "api" / "ink.js").read_text(encoding="utf-8")
        self.assertIn('env.INK_BRANCH || "ink-data"', fn)
        self.assertIn('const SKIP = "[CF-Pages-Skip] ";', fn)
        self.assertNotIn('"main"', fn)


if __name__ == "__main__":
    unittest.main(verbosity=1)
