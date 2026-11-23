"""test_sync_key.py — 동기화 키 연결 구조 회귀 시험(2026-09-23).

사고: 동기화 키를 설정 칸에 손으로 넣어야만 했고, 키 없는 기기의 오답·학습 기록은 조용히 그 기기에만 쌓였다
(저장소 오답 KMLE 21개 · USMLE 0개). 그래서 ① #k= 연결 링크로 키를 옮기고 ② /api/status 로 키 상태를 묻고
③ 키가 없으면 첫 화면에 경고하며 ④ 기록이 있는 모든 시험을 보낸다. 이 시험이 그 구조를 지킨다.

    python pipelines/test_sync_key.py
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
        a, b, c = (re.search(rf'<script src="{re.escape(n)}(\?v=\d+)?"></script>', html).start()
                   for n in ("synckey.js", "learn.js", "app.js"))
        self.assertLess(a, b)
        self.assertLess(b, c)
        for el in ("syncNeedKey", "syncNeedKeyText", "syncLinkBtn", "syncAuthInfo"):
            self.assertIn(f'id="{el}"', html)

    def test_app_code_urls_carry_service_worker_version(self):
        # 배포 직후 브라우저 캐시가 새 index.html 과 옛 app.js 를 섞지 않게 — 앱 코드 주소의 ?v= 는 sw.js VERSION 과 같다
        html = (DOCS / "index.html").read_text(encoding="utf-8")
        ver = re.search(r'const VERSION = "medkos-v(\d+)"', (DOCS / "sw.js").read_text(encoding="utf-8")).group(1)
        for n in ("style.css", "synckey.js", "learn.js", "app.js", "pwa.js"):
            self.assertIn(f'{n}?v={ver}"', html, n)

    def test_due_deck_is_wired(self):
        # 「오늘 다시 풀 것」 덱(2026-11-10) — 학습 구역 선택지 · 첫 화면 버튼 · learn.js 내보내기가 서로 맞물려 있다.
        # 복습 일정은 계산되고 있었지만 퀴즈 화면에 덱이 없어 예정 74개가 전부 밀렸다.
        html = (DOCS / "index.html").read_text(encoding="utf-8")
        app = (DOCS / "app.js").read_text(encoding="utf-8")
        learn = (DOCS / "learn.js").read_text(encoding="utf-8")
        self.assertIn('<option value="due">', html)
        self.assertIn('id="dueStartBtn"', html)
        self.assertIn('if (mode === "due") return ctx.dueQs.slice();', app)      # 종목 선택과 무관하게 전부
        self.assertIn("LEARN.pickRetest(k)", app)                                # 고르는 규칙은 개념 복습 화면과 같다
        self.assertIn('$("mode").value = "due"', app)
        self.assertIn("dueKeys, pickRetest, reviewSteps", learn)                 # learn.js 가 pickRetest 를 내보낸다
        manifest = (DOCS / "manifest.webmanifest").read_text(encoding="utf-8")
        self.assertIn("./index.html?mode=due", manifest)

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


class Theme(unittest.TestCase):
    """밝은 화면(기본) / 어두운 화면 — 2026-11-23 vNext Phase 1. 색은 style.css 맨 위 변수 두 묶음에만 있다."""

    PAGES = ("index.html", "papers.html", "search.html", "whatsnew.html", "ailab.html")

    def test_pages_load_theme_before_the_stylesheet(self):
        # 스타일보다 먼저 읽어야 첫 그림 전에 html[data-theme] 가 걸린다(어두운 화면을 고른 사람에게 흰 화면이 번쩍이지 않게)
        for page in self.PAGES:
            html = (DOCS / page).read_text(encoding="utf-8")
            a = re.search(r'<script src="theme\.js(\?v=\d+)?"></script>', html)
            b = re.search(r'<link rel="stylesheet" href="style\.css', html)
            self.assertTrue(a and b and a.start() < b.start(), page)
        index = (DOCS / "index.html").read_text(encoding="utf-8")
        ver = re.search(r'const VERSION = "medkos-v(\d+)"', (DOCS / "sw.js").read_text(encoding="utf-8")).group(1)
        self.assertIn(f'theme.js?v={ver}"', index)
        self.assertIn('"./theme.js"', (DOCS / "sw.js").read_text(encoding="utf-8"))          # 오프라인에서도 테마가 걸린다

    def test_light_is_the_default_and_dark_is_opt_in(self):
        js = (DOCS / "theme.js").read_text(encoding="utf-8")
        self.assertIn('var KEY = "medkos_theme";', js)
        self.assertIn('localStorage.getItem(KEY) === "dark" ? "dark" : "light"', js)       # 저장값이 없으면 밝은 화면
        css = (DOCS / "style.css").read_text(encoding="utf-8")
        self.assertIn(":root, .ink-sheet{", css)                                            # 필기 종이는 앱이 어두워도 밝은 변수
        self.assertIn('html[data-theme="dark"]{', css)
        for tok in ("--bg:#f3f6fa", "--card:#ffffff", "--surface:#f8fafd", "--border:#dce4ef", "--ink:#182334",
                    "--muted:#5c6c82", "--accent:#1d57a8"):
            self.assertIn(tok, css, tok)

    def test_colors_live_only_in_the_token_blocks(self):
        # 변수 묶음 밖에 색을 직접 적으면 한쪽 테마에서만 보이는 글자가 생긴다. 예외: 그림 뒤 흰 바탕 · 확대/로그인 창의 검은 막.
        css = (DOCS / "style.css").read_text(encoding="utf-8")
        body = css[css.index("*{box-sizing:border-box}"):]
        left = set(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)", body))
        self.assertLessEqual(left, {"#fff", "#ffffff", "#aab6c6", "rgba(0,0,0,.25)", "rgba(4,8,14,.72)", "rgba(4,8,14,.96)"}, left)
        ailab = (DOCS / "ailab.html").read_text(encoding="utf-8")
        style = ailab[ailab.index("<style>"):ailab.index("</style>")]
        self.assertLessEqual(set(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)", style)), {"#f8fafc"})
        learn = (DOCS / "learn.js").read_text(encoding="utf-8")
        self.assertIn("zoomCss(box)", learn)                                                # 확대 창 도식도 지금 테마의 변수에서 색을 읽는다
        self.assertNotIn(".ink-sheet .concept .dia-box{background:#0f1620", css)            # 종이 안 검은 도식 바탕 제거


if __name__ == "__main__":
    unittest.main(verbosity=2)
