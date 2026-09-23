"""test_sync_key.py — 동기화 키 연결 구조 회귀 시험(2026-09-23).

사고: 동기화 키를 설정 칸에 손으로 넣어야만 했고, 키 없는 기기의 오답·학습 기록은 조용히 그 기기에만 쌓였다
(저장소 오답 KMLE 21개 · USMLE 0개). 그래서 ① #k= 연결 링크로 키를 옮기고 ② /api/status 로 키 상태를 묻고
③ 키가 없으면 첫 화면에 경고하며 ④ 기록이 있는 모든 시험을 보낸다. 이 시험이 그 구조를 지킨다.

    python pipelines/test_sync_key.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
NODE = shutil.which("node")


def run_node(src: str, module: bool = False) -> dict:
    args = [NODE] + (["--input-type=module"] if module else []) + ["-e", src]
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
    if r.returncode:
        raise AssertionError(r.stderr)
    return json.loads(r.stdout.strip().splitlines()[-1])


@unittest.skipUnless(NODE, "node 없음")
class PairingLink(unittest.TestCase):
    HARNESS = (
        "const vm=require('vm'),fs=require('fs');"
        "const mem={};const store={getItem:k=>k in mem?mem[k]:null,setItem:(k,v)=>{mem[k]=String(v)},removeItem:k=>{delete mem[k]}};"
        "const calls=[];const ctx={localStorage:store,"
        "location:{hash:%s,pathname:'/',search:'?exam=kmle'},"
        "history:{replaceState:(a,b,u)=>calls.push(u)}};vm.createContext(ctx);"
        "vm.runInContext(fs.readFileSync('docs/synckey.js','utf8')+';this.S=MEDKOS_SYNC;',ctx);"
        "const S=ctx.S;"
    )

    def page(self, hash_: str, body: str) -> dict:
        return run_node(self.HARNESS % json.dumps(hash_) + body)

    def test_link_on_load_stores_key_and_clears_address(self):
        out = self.page("#k=abc%20123&tab=2",
                        "console.log(JSON.stringify({cap:S.captured,stored:mem.medkos_sync_key,url:calls[0]}))")
        self.assertEqual(out["cap"], "abc 123")
        self.assertEqual(out["stored"], "abc 123")
        self.assertEqual(out["url"], "/?exam=kmle#tab=2")        # 키는 주소창에서 사라지고 나머지는 남는다

    def test_no_key_in_address_changes_nothing(self):
        out = self.page("#tab=2", "console.log(JSON.stringify({cap:S.captured,n:Object.keys(mem).length,c:calls.length}))")
        self.assertEqual(out, {"cap": "", "n": 0, "c": 0})

    def test_alias_and_round_trip(self):
        out = self.page("", "const l=S.linkFor('k#&=1');"
                        "console.log(JSON.stringify({l,back:S.parseHash(l.slice(l.indexOf('#'))),alias:S.parseHash('#sync=x')}))")
        self.assertTrue(out["l"].startswith("https://my-github-test.pages.dev/#k="))
        self.assertEqual(out["back"], "k#&=1")                  # 특수문자도 그대로 돌아온다
        self.assertEqual(out["alias"], "x")


@unittest.skipUnless(NODE, "node 없음")
class StatusEndpoint(unittest.TestCase):
    def status(self, env: dict, sent: str) -> dict:
        src = (
            "import fs from 'fs';"
            "const m=await import('data:text/javascript,'+encodeURIComponent(fs.readFileSync('functions/api/status.js','utf8')));"
            f"console.log(JSON.stringify(m.syncStatus({json.dumps(env)},{json.dumps(sent)})));"
        )
        return run_node(src, module=True)

    def test_states(self):
        env = {"GITHUB_TOKEN": "t", "SYNC_KEY": "secret"}
        self.assertEqual(self.status(env, ""), {"server": True, "keyRequired": True, "keySent": False, "keyOk": False})
        self.assertFalse(self.status(env, "nope")["keyOk"])
        self.assertTrue(self.status(env, "secret")["keyOk"])
        self.assertTrue(self.status({"GITHUB_TOKEN": "t"}, "")["keyOk"])   # 서버에 키가 없으면 누구나 통과

    def test_never_echoes_the_key(self):
        out = self.status({"GITHUB_TOKEN": "t", "SYNC_KEY": "secret"}, "secret")
        self.assertNotIn("secret", json.dumps(out))


class Wiring(unittest.TestCase):
    def test_index_loads_synckey_before_learn_and_app(self):
        html = (DOCS / "index.html").read_text(encoding="utf-8")
        a, b, c = (html.index(f'<script src="{n}"></script>') for n in ("synckey.js", "learn.js", "app.js"))
        self.assertLess(a, b)
        self.assertLess(b, c)
        for el in ("syncNeedKey", "syncNeedKeyText", "syncLinkBtn", "syncAuthInfo"):
            self.assertIn(f'id="{el}"', html)

    def test_service_worker_caches_synckey(self):
        self.assertIn('"./synckey.js"', (DOCS / "sw.js").read_text(encoding="utf-8"))

    def test_app_uses_status_banner_and_all_exams(self):
        app = (DOCS / "app.js").read_text(encoding="utf-8")
        self.assertIn('api/status', app)
        self.assertIn('res.status === 401', app)                  # 401 은 경고로 드러낸다
        self.assertIn('SYNC_EXAMS.forEach', app)                   # 연 덱만이 아니라 모든 시험
        self.assertIn('checkSyncAuth();', app)

    def test_learning_sync_stops_retrying_on_401(self):
        learn = (DOCS / "learn.js").read_text(encoding="utf-8")
        self.assertIn("r.status === 401", learn)


if __name__ == "__main__":
    unittest.main(verbosity=2)
