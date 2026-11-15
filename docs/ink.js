/* MedKOS 오답노트 필기 — 펜슬로 쓰고, 기기끼리 맞춘다 (2026-11-15)

   왜: 오답노트는 자동으로 쌓이지만 「왜 틀렸나」를 손으로 풀어 쓰는 자리가 없었다(글 메모 한 줄뿐).
   문항 하나마다 필기장을 연다 — 위에 문항 · 내 답 · 정답 · 해설(접힘), 아래에 줄 여백. 그 위 어디에든 쓴다.
   여는 곳 넷(2판 — 「오답만이 아니라 전부 · 푸는 것도 패드로 · 학습서도」):
     ① 오답노트의 「✍ 필기」  ② 문항 화면의 「✍ 펜으로 풀기」 — 필기장 안에서 보기를 톡 쳐 채점하고 다음 문항으로 넘어간다
        (채점 · 학습 기록 · 오답노트 저장은 앱이 그대로 한다. 전에 쓴 필기는 채점 뒤에 보인다 — 답을 미리 알려 주지 않게)
     ③ 개념 정리본(학습서의 단위)의 「✍ 이 정리본에 필기」  ④ 첫 화면의 「✍ 필기 모음」 — 필기가 있는 것 전부.
   맞힌 문항도 「★ 정리본에 넣기」를 누르면 표시(want_note)가 남아 개념 복습 · 정리본 큐에 들어간다(learn.js).

   - 펜슬 = 쓰기 · 손가락 = 화면 넘기기(「손가락 쓰기」를 켜면 손가락도 쓴다 — 그때는 두 손가락으로 넘긴다).
   - 필기는 획(벡터)으로 저장한다. 종이 폭을 820 으로 고정해 놓고 화면에 맞춰 통째로 늘이므로 기기가 달라도 같은 자리에 보인다.
     획의 세로 위치는 「문항 / 선지 / 해설 / 여백」 가운데 시작한 덩이의 윗변에서 잰다 — 글꼴이 달라 문항이 한 줄 길어져도
     선지 · 여백에 쓴 필기가 밀리지 않는다(문항 덩이 안의 밑줄만 조금 어긋날 수 있다).
   - 저장: 기기 안(IndexedDB)에 바로. 동기화 키가 있으면 `/api/ink` 로 올린다 — **동기화 키로 잠근 암호문만** 나간다
     (저장소가 공개라서. functions/api/ink.js). 서버는 열지 못하므로 합치기는 기기가 한다: 획 id 의 합집합, 지운 획은 묘비.
   - 키가 없거나 서버가 없는 주소면 이 기기에만 남고, 키가 생기면 그때 올라간다.

   순수 함수(pack · unpack · mergeDocs · seal · unseal)는 pipelines/test_ink.py 가 node 로 시험한다. */
var MEDKOS_INK = (function () {
  "use strict";

  const W = 820;                 // 종이 폭(논리 px) — 모든 기기 공통
  const TILE = 900;              // 필기 층을 이 높이의 캔버스 조각으로 나눈다(iOS 캔버스 크기 · 메모리 한도)
  const PAPER0 = 900, PAPER_STEP = 600;
  const SALT = "medkos-ink-v1";
  const COLORS = ["#1b2430", "#d92d20", "#1d4ed8", "#0f8a4f"];
  const HL = "#f5c518";
  const WIDTHS = [1.6, 2.6, 4.2];

  /* ───────── 순수 함수: 획 압축 · 병합 ───────── */
  // pts = [x, y, p, x, y, p, …] (논리 px · 압력 0~1) → 정수 차분 배열(좌표 ×10 · 압력 ×31)
  function pack(pts) {
    const out = [];
    let px = 0, py = 0;
    for (let i = 0; i + 2 < pts.length + 0.5 && i < pts.length; i += 3) {
      const X = Math.round(pts[i] * 10), Y = Math.round(pts[i + 1] * 10);
      out.push(X - px, Y - py, Math.max(0, Math.min(31, Math.round((pts[i + 2] == null ? 0.5 : pts[i + 2]) * 31))));
      px = X; py = Y;
    }
    return out;
  }
  function unpack(d) {
    const out = [];
    let px = 0, py = 0;
    for (let i = 0; i + 2 < (d || []).length + 0.5 && i < (d || []).length; i += 3) {
      px += d[i]; py += d[i + 1];
      out.push(px / 10, py / 10, d[i + 2] / 31);
    }
    return out;
  }
  function emptyDoc() { return { v: 1, ph: PAPER0, c: null, s: {}, g: {}, u: "" }; }      // c = 내가 고른 보기(맞힌 문항도 다시 열면 보이게)
  function normDoc(d) {
    const o = d && typeof d === "object" ? d : {};
    return {
      v: 1, ph: Math.max(PAPER0, Math.min(60000, Number(o.ph) || PAPER0)), c: Number.isInteger(o.c) ? o.c : null,
      s: o.s && typeof o.s === "object" ? o.s : {}, g: o.g && typeof o.g === "object" ? o.g : {}, u: String(o.u || ""),
    };
  }
  // 합집합. 지운 획(g = 묘비)은 어느 쪽에 남아 있든 사라진다. 같은 id 의 획은 내용이 같다(id 는 한 번만 쓴다).
  function mergeDocs(a, b) {
    a = normDoc(a); b = normDoc(b);
    const g = Object.assign({}, a.g);
    Object.keys(b.g).forEach((k) => { if (!g[k] || g[k] < b.g[k]) g[k] = b.g[k]; });
    const s = {};
    [a.s, b.s].forEach((m) => Object.keys(m).forEach((k) => { if (!g[k] && !s[k]) s[k] = m[k]; }));
    const nw = a.u > b.u ? a : b, od = nw === a ? b : a;
    return { v: 1, ph: Math.max(a.ph, b.ph), c: nw.c != null ? nw.c : od.c, s, g, u: nw.u };
  }
  function sameDoc(a, b) {
    const ka = Object.keys(a.s).sort().join(","), kb = Object.keys(b.s).sort().join(",");
    const ga = Object.keys(a.g).sort().join(","), gb = Object.keys(b.g).sort().join(",");
    return ka === kb && ga === gb && a.ph === b.ph;
  }
  function countStrokes(doc) { return Object.keys((doc && doc.s) || {}).length; }

  /* ───────── 잠그기(AES-GCM · 키 = 동기화 키에서 PBKDF2) ───────── */
  const subtle = typeof crypto !== "undefined" && crypto.subtle ? crypto.subtle : null;
  const keyCache = {};
  function b64(bytes) {
    let bin = "";
    for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    return btoa(bin);
  }
  function unb64(str) {
    const bin = atob(str), out = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }
  async function keyFor(pass) {
    if (keyCache[pass]) return keyCache[pass];
    const base = await subtle.importKey("raw", new TextEncoder().encode(pass), "PBKDF2", false, ["deriveKey"]);
    const key = await subtle.deriveKey({ name: "PBKDF2", salt: new TextEncoder().encode(SALT), iterations: 150000, hash: "SHA-256" },
      base, { name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]);
    keyCache[pass] = key;
    return key;
  }
  async function pipe(bytes, stream) {
    return new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(stream)).arrayBuffer());
  }
  async function seal(doc, pass) {
    let bytes = new TextEncoder().encode(JSON.stringify(normDoc(doc)));
    let z = 0;
    if (typeof CompressionStream === "function") { bytes = await pipe(bytes, new CompressionStream("gzip")); z = 1; }
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const ct = new Uint8Array(await subtle.encrypt({ name: "AES-GCM", iv }, await keyFor(pass), bytes));
    return { v: 1, alg: "A256GCM", z, iv: b64(iv), ct: b64(ct), n: countStrokes(doc), updated: doc.u || new Date().toISOString() };
  }
  // 키가 다르면 여기서 던진다(OperationError) — 부르는 쪽은 서버 것을 덮어쓰지 않는다.
  async function unseal(env, pass) {
    let bytes = new Uint8Array(await subtle.decrypt({ name: "AES-GCM", iv: unb64(env.iv) }, await keyFor(pass), unb64(env.ct)));
    if (env.z) {
      if (typeof DecompressionStream !== "function") throw new Error("이 브라우저는 압축된 필기를 풀지 못합니다");
      bytes = await pipe(bytes, new DecompressionStream("gzip"));
    }
    return normDoc(JSON.parse(new TextDecoder().decode(bytes)));
  }

  const core = { W, pack, unpack, mergeDocs, sameDoc, emptyDoc, normDoc, countStrokes, seal, unseal };
  if (typeof document === "undefined") return core;          // node 시험 — 아래는 화면이 있을 때만

  /* ───────── 기기 저장소(IndexedDB · 없으면 메모리) ───────── */
  const IDX_KEY = "medkos_ink_idx";                           // { "exam:id": 획 수 } — 오답노트 목록의 단추에 바로 쓴다
  const mem = {};
  let dbp = null;
  function db() {
    if (dbp) return dbp;
    dbp = new Promise((res) => {
      try {
        const rq = indexedDB.open("medkos_ink", 1);
        rq.onupgradeneeded = () => rq.result.createObjectStore("docs", { keyPath: "k" });
        rq.onsuccess = () => res(rq.result);
        rq.onerror = () => res(null);
      } catch (e) { res(null); }
    });
    return dbp;
  }
  function tx(mode, fn) {
    return db().then((d) => new Promise((res) => {
      if (!d) return res(null);
      try {
        const t = d.transaction("docs", mode), rq = fn(t.objectStore("docs"));
        rq.onsuccess = () => res(rq.result);
        rq.onerror = () => res(null);
      } catch (e) { res(null); }
    }));
  }
  const keyOf = (exam, id) => exam + ":" + id;
  const EXAMS = ["kmle", "usmle", "imaging", "variant", "concept"];      // 문항 넷 + 개념 정리본
  const fid = (id) => String(id).replace(/#/g, "--");                     // 서버 파일 이름(변형 문항 id 의 # → --)
  const unfid = (exam, f) => (exam === "variant" ? String(f).replace(/--(v\d+)$/, "#$1") : f);
  async function loadRec(exam, id) {
    const k = keyOf(exam, id);
    const r = (await tx("readonly", (s) => s.get(k))) || mem[k];
    return r ? Object.assign(r, { doc: normDoc(r.doc) }) : { k, exam, id, doc: emptyDoc(), sha: null, dirty: false };
  }
  async function saveRec(rec) {
    mem[rec.k] = rec;
    await tx("readwrite", (s) => s.put({ k: rec.k, exam: rec.exam, id: rec.id, doc: rec.doc, sha: rec.sha || null, dirty: !!rec.dirty, locked: !!rec.locked }));
    const idx = loadIdx(), n = countStrokes(rec.doc);
    if (n) idx[rec.k] = n; else delete idx[rec.k];
    try { localStorage.setItem(IDX_KEY, JSON.stringify(idx)); } catch (e) { /* 꽉 참 — 단추의 획 수만 못 쓴다 */ }
  }
  async function allRecs() { return (await tx("readonly", (s) => s.getAll())) || Object.keys(mem).map((k) => mem[k]); }
  function loadIdx() { try { return JSON.parse(localStorage.getItem(IDX_KEY) || "{}") || {}; } catch (e) { return {}; } }

  /* ───────── 동기화(/api/ink) ───────── */
  const NET = { url: (window.MEDKOS_API_BASE || "") + "api/ink", available: null, remote: {}, remoteAt: {} };
  function pass() {
    if (typeof MEDKOS_SYNC === "object") return MEDKOS_SYNC.get();
    try { return (localStorage.getItem("medkos_sync_key") || "").trim(); } catch (e) { return ""; }
  }
  function headers() { const h = { "content-type": "application/json" }; const k = pass(); if (k) h["x-sync-key"] = k; return h; }
  function device() { try { return localStorage.getItem("medkos_device") || "web"; } catch (e) { return "web"; } }
  function canSync() { return !!subtle && !!pass() && NET.available !== false && location.protocol !== "file:" && navigator.onLine !== false; }
  function noServer(status) { return status === 404 || status === 405 || status === 501; }

  async function pull(exam, id) {
    const r = await fetch(`${NET.url}?exam=${encodeURIComponent(exam)}&id=${encodeURIComponent(fid(id))}`, { headers: headers() });
    const ct = r.headers.get("content-type") || "";
    if (r.status === 404 && ct.indexOf("json") >= 0) { NET.available = true; return null; }     // 서버는 있고 이 문항 필기가 없다
    if (noServer(r.status)) { NET.available = false; return null; }
    if (!r.ok) throw new Error(r.status === 401 ? "동기화 키가 맞지 않습니다" : "받기 실패 " + r.status);
    NET.available = true;
    return r.json();
  }
  // 서버 것을 받아 합치고, 달라진 것이 있으면 올린다. 반환: "ok" | "local"(올릴 수 없음) | "locked"(다른 키) | "error"
  async function syncRec(rec, onMerged) {
    if (!canSync()) return "local";
    try {
      for (let attempt = 0; attempt < 3; attempt++) {
        const remote = await pull(rec.exam, rec.id);
        if (NET.available === false) return "local";
        if (remote && remote.sha !== rec.sha) {
          let theirs;
          try { theirs = await unseal(remote.env, pass()); }
          catch (e) { rec.locked = true; await saveRec(rec); return "locked"; }
          const merged = mergeDocs(rec.doc, theirs);
          const changed = !sameDoc(merged, rec.doc);
          rec.dirty = !sameDoc(merged, theirs);
          rec.doc = merged; rec.sha = remote.sha; rec.locked = false;
          await saveRec(rec);
          if (changed && onMerged) onMerged();
        } else if (!remote) { rec.sha = null; rec.dirty = countStrokes(rec.doc) > 0 || Object.keys(rec.doc.g).length > 0; }
        if (!rec.dirty) return "ok";
        const sent = JSON.stringify(rec.doc);
        const r = await fetch(NET.url, {
          method: "POST", headers: headers(),
          body: JSON.stringify({ exam: rec.exam, id: fid(rec.id), sha: rec.sha, env: await seal(rec.doc, pass()), device: device() }),
        });
        if (noServer(r.status)) { NET.available = false; return "local"; }
        if (r.status === 409) continue;                                   // 다른 기기가 먼저 올렸다 → 다시 받아 합친다
        if (!r.ok) throw new Error(r.status === 401 ? "동기화 키가 맞지 않습니다" : "올리기 실패 " + r.status);
        const out = await r.json();
        rec.sha = out.sha || rec.sha;
        rec.dirty = JSON.stringify(rec.doc) !== sent;                     // 올리는 사이에 더 썼으면 아직 남았다
        await saveRec(rec);
        (NET.remote[rec.exam] = NET.remote[rec.exam] || {})[fid(rec.id)] = rec.sha;
        return "ok";
      }
      return "error";
    } catch (e) { NET.lastError = String((e && e.message) || e); return "error"; }
  }
  // 올리지 못한 필기를 모두 올린다(앱을 열 때 · 다시 연결됐을 때).
  let flushing = false;
  async function flushAll() {
    if (flushing || !canSync()) return;
    flushing = true;
    try {
      const recs = await allRecs();
      for (const r of recs) {
        if (!r || !r.dirty || r.locked || (UI.rec && UI.rec.k === r.k)) continue;
        r.doc = normDoc(r.doc);
        await syncRec(r);
        if (NET.available === false) break;
      }
    } finally { flushing = false; }
  }
  // 다른 기기에서 쓴 필기가 있는 문항(목록의 ☁ 표시). 1분에 한 번만 묻는다.
  async function refreshRemote(exam) {
    if (!canSync() || Date.now() - (NET.remoteAt[exam] || 0) < 60000) return NET.remote[exam] || {};
    NET.remoteAt[exam] = Date.now();
    try {
      const r = await fetch(`${NET.url}?exam=${encodeURIComponent(exam)}`, { headers: headers() });
      if (noServer(r.status)) { NET.available = false; return {}; }
      if (r.ok) { NET.available = true; NET.remote[exam] = (await r.json()).files || {}; }
    } catch (e) { /* 오프라인 — 목록 표시만 못 한다 */ }
    return NET.remote[exam] || {};
  }

  /* ───────── 화면 ───────── */
  const UI = {
    el: null, rec: null, rt: {}, tops: {}, tiles: [], s: 1, q: 1, zoom: 1, sheetH: 0,
    tool: loadTool(), undo: [], mine: {}, st: null, saveT: null, pushT: null, raf: 0, lastPen: 0, act: null, dirtyTiles: null,
  };
  function loadTool() {
    let t = {};
    try { t = JSON.parse(localStorage.getItem("medkos_ink_tool") || "{}") || {}; } catch (e) { t = {}; }
    return { kind: t.kind === "hl" || t.kind === "erase" ? t.kind : "pen", color: COLORS.indexOf(t.color) >= 0 ? t.color : COLORS[0],
             width: WIDTHS.indexOf(t.width) >= 0 ? t.width : WIDTHS[1], finger: !!t.finger };
  }
  function saveTool() { try { localStorage.setItem("medkos_ink_tool", JSON.stringify(UI.tool)); } catch (e) { /* 무시 */ } }
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const g = (name) => { try { return (0, eval)("typeof " + name + " !== 'undefined' ? " + name + " : undefined"); } catch (e) { return undefined; } };
  function findQuestion(id) {
    const lists = ["KMLE", "USMLE", "IMAGING", "VARIANT"].map(g).filter(Array.isArray);
    for (const l of lists) for (const q of l) if (q && q.id === id) return q;
    return null;
  }
  function wrongEntry(exam, id) {
    const f = g("loadWrong");
    try { return (typeof f === "function" ? f(exam) : JSON.parse(localStorage.getItem("wrong_" + exam) || "{}"))[id] || null; } catch (e) { return null; }
  }
  function labels(q, w) {
    const f = g("labelsFor");
    if (typeof f === "function") { try { return f(q || w || {}); } catch (e) { /* 아래 기본값 */ } }
    return ["①", "②", "③", "④", "⑤"];
  }
  function explHtml(q) {
    const items = g("renderExplItems"), fmt = g("fmtExplValue");
    try {
      if (q.explanationItems && q.explanationItems.length && typeof items === "function") return items(q.explanationItems);
      if (q.explanationText) return `<pre class="expl-text">${esc(q.explanationText)}</pre>`;
      const ex = q.explanation || {};
      return ["진단", "정답근거", "오답감별", "임상핵심"].filter((k) => ex[k])
        .map((k) => `<div class="expl-item"><span class="k">${k}</span>${typeof fmt === "function" ? fmt(ex[k]) : esc(ex[k])}</div>`).join("");
    } catch (e) { return ""; }
  }
  function examOf(q) {
    if (!q || !q.id) return "";
    if (q.isVariant) return "variant";
    const f = g("wrongExamOf");
    let e = q.src || "";
    try { if (typeof f === "function") e = f(q); } catch (_) { /* 아래 검사 */ }
    return EXAMS.indexOf(e) >= 0 && e !== "concept" ? e : "";
  }
  // 문항 종이. solve = 푸는 중(정답 · 해설 · 옛 메모를 싣지 않고, 보기는 톡 쳐서 고르는 단추)
  function questionHtml(st) {
    const id = st.id, q = st.q, w = st.w, solve = st.solve;
    const lab = labels(q, w);
    const mineIdx = Number.isInteger(st.chosen) ? st.chosen : null;
    const head = `<div class="ink-h">#${esc(id)}<span>${esc((q && q.subject) || (w && w.subject) || "")}${!solve && w && w.date ? " · 틀린 날 " + esc(w.date) : ""}</span></div>`;
    let qb = head, ob = "", eb = "";
    if (q) {
      const fig = g("figureHtml"), data = g("dataBox");
      qb += (q.vignette || "").trim() ? `<div class="ink-vig">${esc(q.vignette.trim())}</div>` : "";
      try { qb += (typeof fig === "function" ? fig(q) : "") + (typeof data === "function" ? data(q) : ""); } catch (e) { /* 그림 없이 */ }
      qb += (q.question || "").trim() ? `<div class="ink-q">Q. ${esc(q.question.trim())}</div>` : "";
      ob = (q.options || []).map((o, i) => {
        const body = `<span class="num">${lab[i] || i + 1}</span><span class="t">${esc(o)}</span>`;
        if (solve) return `<button type="button" class="ink-opt ink-pick" data-pick="${i}">${body}</button>`;
        const mine = mineIdx === i, ans = q.answer - 1 === i;
        return `<div class="ink-opt${ans ? " ans" : ""}${mine && !ans ? " mine" : ""}">${body}`
          + `${ans ? '<span class="tg">정답</span>' : ""}${mine ? '<span class="tg">내 선택</span>' : ""}</div>`;
      }).join("");
      if (solve) ob += `<div class="ink-hint">보기를 톡 치면 채점됩니다 · 보기 위에 긋는 것은 필기로 남습니다</div>`;
      else eb = explHtml(q);
    } else if (w) {                                   // 문항 은행에서 빠진 옛 오답 — 오답노트에 남은 것만 보인다
      qb += `<div class="ink-q">Q. ${esc(w.question || "")}</div>`;
      ob = `<div class="ink-opt mine"><span class="num">${lab[w.chosen] || ""}</span><span class="t">${esc(w.chosenText || "")}</span><span class="tg">내 선택</span></div>`
        + `<div class="ink-opt ans"><span class="num">${lab[w.answer] || ""}</span><span class="t">${esc(w.answerText || "")}</span><span class="tg">정답</span></div>`;
      eb = w.coreNote ? `<div class="expl-item"><span class="k">핵심</span>${esc(w.coreNote)}</div>` : "";
    } else qb += `<div class="ink-q">문항을 찾지 못했습니다 — 필기만 보입니다.</div>`;
    if (!solve && w && w.note) ob += `<div class="ink-memo">✍ ${esc(w.note)}</div>`;
    return `<div class="ink-block" data-b="q">${qb}</div><div class="ink-block" data-b="o">${ob}</div>`
      + (eb ? `<details class="ink-block ink-ex" data-b="e"><summary>해설 펼치기</summary><div class="ink-exb explanation">${eb}</div></details>` : "")
      + PAPER_HTML;
  }
  const PAPER_HTML = `<div class="ink-block ink-paper" data-b="p"><span class="ink-ph">여기부터 내 필기 — 왜 틀렸나 · 헷갈린 점 · 다음에 볼 단서</span></div>`;
  // 개념 정리본 종이 — 앱의 정리본 그리기(learn.js)를 그대로 쓰고, 접힌 절을 모두 편다. 절마다 덩이 이름을 붙여
  // 정리본이 고쳐져 절이 늘거나 줄어도 다른 절의 필기가 밀리지 않게 한다(이름이 사라진 절의 필기는 맨 위 덩이로 간다).
  function conceptInto(st) {
    UI.content.innerHTML = `<div class="ink-cn"></div>` + PAPER_HTML;
    const box = UI.content.querySelector(".ink-cn"), L = g("LEARN");
    try { if (L && typeof L.renderConcept === "function") L.renderConcept(box, st.id, null, null); } catch (e) { /* 아래 안내 */ }
    const art = box.querySelector("article");
    if (!art) { box.innerHTML = `<div class="ink-q" data-b="c:none">정리본을 찾지 못했습니다(${esc(st.id)}) — 필기만 보입니다.</div>`; return; }
    art.querySelectorAll("details").forEach((d) => { d.open = true; });
    const seen = {};
    [].forEach.call(art.children, (el) => {
      const src = el.querySelector(":scope > summary") || el.querySelector(".cn-title, .cn-sec") || el;
      let k = "c:" + (src.textContent || el.className || "x").replace(/\s*\(\d+\)\s*$/, "").replace(/\s+/g, " ").trim().slice(0, 24);
      while (seen[k]) k += "_";
      seen[k] = 1;
      el.setAttribute("data-b", k);
    });
  }
  function renderSheet(openExpl) {
    const st = UI.st;
    if (st.kind === "concept") conceptInto(st); else UI.content.innerHTML = questionHtml(st);
    UI.content.querySelectorAll("img").forEach((im) => im.addEventListener("load", () => layout(false)));
    const d = UI.content.querySelector("details.ink-ex");
    if (d) {
      d.addEventListener("toggle", () => { d.querySelector("summary").textContent = d.open ? "해설 접기" : "해설 펼치기"; layout(false); UI.tiles.forEach((t) => { t.stale = true; }); ensureTiles(); });
      if (openExpl) d.open = true;
    }
    paintBar();
    layout(false);
    UI.tiles.forEach((t) => { t.stale = true; });
    ensureTiles();
  }
  // 푸는 중에 보기를 골랐다 — 채점은 앱의 문항 화면이 한다(학습 기록 · 오답노트 저장이 한 곳에서만 일어나게).
  function pick(i) {
    const st = UI.st;
    if (!st || !st.solve || !UI.rec) return;
    const deck = g("deck"), pos = g("pos");
    const cur = Array.isArray(deck) ? deck[pos] : null, btn = document.querySelectorAll("#options .opt")[i];
    if (!cur || cur.id !== UI.rec.id || !btn) return status("문항 화면과 어긋났습니다 — 닫고 다시 여세요", "bad");
    btn.click();
    st.solve = false; st.chosen = i; st.w = wrongEntry(st.exam, st.id);
    UI.rec.doc.c = i;
    UI.hideOld = false;
    if (countStrokes(UI.rec.doc)) touched();
    renderSheet(true);
    const ob = UI.content.querySelector('[data-b="o"]');
    if (ob) UI.scroll.scrollTop = Math.max(0, (UI.tops.o || 0) * UI.s - 60);
    status(i === cur.answer - 1 ? "정답 — 헷갈렸으면 ★ 정리본에 넣기" : "오답 — 오답노트에 저장됨", i === cur.answer - 1 ? "ok" : "bad");
  }

  function build() {
    if (UI.el) return;
    const el = document.createElement("div");
    el.id = "inkOverlay"; el.className = "ink-ov hidden";
    el.innerHTML = `<div class="ink-bar">
        <button data-a="close" class="ink-x">← 닫기</button>
        <span class="ink-tools">
          ${COLORS.map((c) => `<button data-a="color" data-c="${c}" class="ink-dot" style="--c:${c}" aria-label="펜 색"></button>`).join("")}
          <button data-a="width" title="굵기">굵기</button>
          <button data-a="hl">형광펜</button>
          <button data-a="erase">지우개</button>
          <button data-a="undo">↶</button>
          <button data-a="finger" title="손가락으로도 쓰기 — 켜면 두 손가락으로 넘긴다">☝ 손가락 쓰기</button>
          <button data-a="zout" aria-label="작게">−</button><button data-a="zin" aria-label="크게">＋</button>
          <button data-a="more">여백 ＋</button>
          <button data-a="flag" title="맞혔어도 헷갈린 문항 — 개념 복습 · 정리본 큐에 넣는다">★ 정리본에 넣기</button>
          <button data-a="next" class="primary">다음 문항 →</button>
        </span>
        <span class="ink-st" id="inkStatus"></span>
      </div>
      <div class="ink-scroll"><div class="ink-fit"><div class="ink-sheet"><div class="ink-content"></div><div class="ink-layer"></div></div></div></div>`;
    document.body.appendChild(el);
    UI.el = el;
    UI.scroll = el.querySelector(".ink-scroll"); UI.fit = el.querySelector(".ink-fit"); UI.sheet = el.querySelector(".ink-sheet");
    UI.content = el.querySelector(".ink-content"); UI.layer = el.querySelector(".ink-layer");
    el.querySelector(".ink-bar").addEventListener("click", onBar);
    UI.content.addEventListener("click", (e) => { const b = e.target.closest("[data-pick]"); if (b) pick(Number(b.getAttribute("data-pick"))); });
    UI.scroll.addEventListener("scroll", () => schedule(ensureTiles), { passive: true });
    // 화면 폭이 바뀌면(돌리기 · 창 크기) 종이를 다시 맞춘다. 스크롤의 조각 그리기와 예약 칸을 따로 쓴다(서로 취소하지 않게).
    const refit = () => {
      if (!UI.rec || UI.scroll.clientWidth === UI.fitW) return;
      cancelAnimationFrame(UI.rafL); UI.rafL = requestAnimationFrame(() => layout(true));
    };
    window.addEventListener("resize", refit);
    if (typeof ResizeObserver === "function") new ResizeObserver(refit).observe(UI.scroll);
    document.addEventListener("keydown", (e) => { if (UI.rec && e.key === "Escape") close(); });
    document.addEventListener("visibilitychange", () => { if (document.hidden && UI.rec) { flushLocal(); pushNow(); } });
    bindInput();
  }
  function schedule(fn) { cancelAnimationFrame(UI.raf); UI.raf = requestAnimationFrame(fn); }
  function status(text, cls) { const el = document.getElementById("inkStatus"); if (el) { el.textContent = text; el.className = "ink-st " + (cls || ""); } }
  function paintBar() {
    const t = UI.tool;
    UI.el.querySelectorAll("[data-a=color]").forEach((b) => b.classList.toggle("on", t.kind === "pen" && b.getAttribute("data-c") === t.color));
    UI.el.querySelector("[data-a=hl]").classList.toggle("on", t.kind === "hl");
    UI.el.querySelector("[data-a=erase]").classList.toggle("on", t.kind === "erase");
    UI.el.querySelector("[data-a=finger]").classList.toggle("on", t.finger);
    UI.el.querySelector("[data-a=width]").textContent = ["가늘게", "보통", "굵게"][WIDTHS.indexOf(t.width)] || "보통";
    UI.el.querySelector("[data-a=undo]").disabled = !UI.undo.length;
    UI.layer.style.touchAction = t.finger ? "none" : "pan-x pan-y";
    const st = UI.st || {}, L = g("LEARN"), fb = UI.el.querySelector("[data-a=flag]"), nb = UI.el.querySelector("[data-a=next]");
    const canFlag = st.kind === "q" && !st.solve && st.q && !st.q.isVariant && L && typeof L.setFlag === "function";
    fb.hidden = !canFlag; nb.hidden = !(st.quiz && !st.solve);
    if (canFlag) fb.classList.toggle("on", !!L.flagsOf(st.q).want_note);
  }
  function onBar(e) {
    const b = e.target.closest("button[data-a]");
    if (!b) return;
    const a = b.getAttribute("data-a"), t = UI.tool;
    if (a === "close") return close();
    if (a === "color") { t.kind = "pen"; t.color = b.getAttribute("data-c"); }
    else if (a === "width") t.width = WIDTHS[(WIDTHS.indexOf(t.width) + 1) % WIDTHS.length];
    else if (a === "hl") t.kind = t.kind === "hl" ? "pen" : "hl";
    else if (a === "erase") t.kind = t.kind === "erase" ? "pen" : "erase";
    else if (a === "finger") t.finger = !t.finger;
    else if (a === "undo") undo();
    else if (a === "zin" || a === "zout") { UI.zoom = Math.max(1, Math.min(2.5, UI.zoom + (a === "zin" ? 0.25 : -0.25))); layout(true); }
    else if (a === "more") { UI.rec.doc.ph += PAPER_STEP; touched(); layout(false); }
    else if (a === "next") return next();
    else if (a === "flag") { const L = g("LEARN"); L.setFlag(UI.st.q, "want_note", !L.flagsOf(UI.st.q).want_note); }
    saveTool(); paintBar();
  }

  /* 배치 — 종이를 화면 폭에 맞춰 통째로 늘인다. 덩이 윗변을 다시 재고, 보이는 조각만 다시 그린다. */
  function layout(resetTiles) {
    const paper = UI.content.querySelector('[data-b="p"]');
    if (paper) paper.style.height = UI.rec.doc.ph + "px";
    const top = UI.scroll.scrollTop / (UI.s || 1);
    UI.fitW = UI.scroll.clientWidth;
    const fitW = Math.min((UI.scroll.clientWidth - 12) / W, 1.5);
    UI.s = Math.max(0.3, fitW * UI.zoom);
    const q = Math.min(2.5, Math.max(1, UI.s * (window.devicePixelRatio || 1)));
    if (Math.abs(q - UI.q) > 0.01) { UI.q = q; resetTiles = true; }
    UI.sheet.style.transform = `scale(${UI.s})`;
    UI.tops = {}; UI.first = "";
    const c0 = UI.content.getBoundingClientRect().top;
    UI.content.querySelectorAll("[data-b]").forEach((b) => {
      const k = b.getAttribute("data-b");
      UI.tops[k] = (b.getBoundingClientRect().top - c0) / UI.s;
      if (!UI.first) UI.first = k;
    });
    UI.sheetH = UI.content.offsetHeight;
    UI.fit.style.width = Math.ceil(W * UI.s) + "px";
    UI.fit.style.height = Math.ceil(UI.sheetH * UI.s) + "px";
    UI.layer.style.height = UI.sheetH + "px";
    const need = Math.ceil(UI.sheetH / TILE);
    while (UI.tiles.length < need) {
      const c = document.createElement("canvas");
      c.className = "ink-tile"; c.style.top = UI.tiles.length * TILE + "px"; c.width = c.height = 0;
      UI.layer.appendChild(c); UI.tiles.push({ c, live: false });
    }
    UI.tiles.forEach((t, i) => { t.c.style.display = i < need ? "" : "none"; if (resetTiles || i >= need) dropTile(t); else t.stale = true; });
    if (resetTiles) UI.scroll.scrollTop = top * UI.s;
    ensureTiles();
  }
  function dropTile(t) { if (t.live) { t.c.width = t.c.height = 0; t.live = false; } }
  function ensureTiles() {
    const lo = Math.floor(UI.scroll.scrollTop / UI.s / TILE) - 1, hi = Math.floor((UI.scroll.scrollTop + UI.scroll.clientHeight) / UI.s / TILE) + 1;
    UI.tiles.forEach((t, i) => {
      if (i < lo || i > hi || i * TILE >= UI.sheetH) return dropTile(t);
      if (!t.live) {
        t.c.style.width = W + "px"; t.c.style.height = TILE + "px";
        t.c.width = Math.round(W * UI.q); t.c.height = Math.round(TILE * UI.q);
        t.live = true; t.stale = true;
      }
      if (t.stale) paintTile(i);
    });
  }
  const topOf = (b) => (b in UI.tops ? UI.tops[b] : UI.tops[UI.first] || 0);      // 이름이 사라진 덩이의 필기는 맨 위 덩이로
  const veiled = (sid) => UI.hideOld && !UI.mine[sid];                              // 푸는 중 — 전에 쓴 필기는 채점 뒤에
  function hiddenBlock(b) {
    if (b !== "e") return false;
    const d = UI.content.querySelector("details.ink-ex");
    return !d || !d.open;
  }
  function paintTile(i) {
    const t = UI.tiles[i];
    if (!t || !t.live) return;
    t.stale = false;
    const ctx = t.c.getContext("2d");
    ctx.setTransform(UI.q, 0, 0, UI.q, 0, 0);
    ctx.clearRect(0, 0, W, TILE);
    const y0 = i * TILE, y1 = y0 + TILE;
    Object.keys(UI.rt).forEach((sid) => {
      const st = UI.rt[sid];
      if (hiddenBlock(st.b) || veiled(sid)) return;
      const top = topOf(st.b);
      if (top + st.y1 + 12 < y0 || top + st.y0 - 12 > y1) return;
      drawStroke(ctx, st, top - y0);
    });
  }
  const widthAt = (w, p) => w * (0.45 + 1.1 * p);
  function drawStroke(ctx, st, dy) {
    const p = st.pts, n = p.length / 3;
    ctx.strokeStyle = ctx.fillStyle = st.c;
    ctx.lineJoin = "round";
    ctx.globalAlpha = st.t === 1 ? 0.3 : 1;
    ctx.lineCap = st.t === 1 ? "butt" : "round";
    if (n === 1) { ctx.beginPath(); ctx.arc(p[0], p[1] + dy, Math.max(0.8, st.w * 0.6), 0, 6.3); ctx.fill(); ctx.globalAlpha = 1; return; }
    if (st.t === 1 || st.flat) {                                 // 굵기가 고른 획 — 한 번에 그려 이음매가 겹쳐 보이지 않게
      ctx.lineWidth = st.w;
      ctx.beginPath(); ctx.moveTo(p[0], p[1] + dy);
      for (let i = 1; i < n - 1; i++) ctx.quadraticCurveTo(p[i * 3], p[i * 3 + 1] + dy, (p[i * 3] + p[i * 3 + 3]) / 2, (p[i * 3 + 1] + p[i * 3 + 4]) / 2 + dy);
      ctx.lineTo(p[(n - 1) * 3], p[(n - 1) * 3 + 1] + dy); ctx.stroke();
    } else {
      for (let i = 1; i < n; i++) {
        ctx.lineWidth = widthAt(st.w, (p[i * 3 + 2] + p[i * 3 - 1]) / 2);
        ctx.beginPath(); ctx.moveTo(p[i * 3 - 3], p[i * 3 - 2] + dy); ctx.lineTo(p[i * 3], p[i * 3 + 1] + dy); ctx.stroke();
      }
    }
    ctx.globalAlpha = 1;
  }
  function runtime(sid, s) {
    const pts = unpack(s.d);
    let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9, flat = true;
    for (let i = 0; i < pts.length; i += 3) {
      x0 = Math.min(x0, pts[i]); x1 = Math.max(x1, pts[i]); y0 = Math.min(y0, pts[i + 1]); y1 = Math.max(y1, pts[i + 1]);
      if (Math.abs(pts[i + 2] - pts[2]) > 0.02) flat = false;
    }
    return { id: sid, c: s.c || COLORS[0], w: s.w || WIDTHS[1], t: s.t ? 1 : 0, b: s.b || "p", pts, x0, x1, y0, y1, flat };
  }
  function rebuildRuntime() {
    UI.rt = {};
    Object.keys(UI.rec.doc.s).forEach((sid) => { UI.rt[sid] = runtime(sid, UI.rec.doc.s[sid]); });
  }
  function staleFor(st) {
    const top = topOf(st.b);
    for (let i = Math.max(0, Math.floor((top + st.y0 - 12) / TILE)); i <= Math.floor((top + st.y1 + 12) / TILE) && i < UI.tiles.length; i++) UI.tiles[i].stale = true;
  }

  /* 입력 — 펜 · 마우스는 쓰고, 손가락은 넘긴다(손가락 쓰기를 켜면 한 손가락 = 쓰기 · 두 손가락 = 넘기기). */
  function pt(e) {
    const r = UI.layer.getBoundingClientRect(), s = r.width / W;
    return [(e.clientX - r.left) / s, (e.clientY - r.top) / s];
  }
  function blockAt(y) {
    let best = "p", bt = -1;
    Object.keys(UI.tops).forEach((b) => { if (UI.tops[b] <= y && UI.tops[b] > bt && !hiddenBlock(b)) { bt = UI.tops[b]; best = b; } });
    return best;
  }
  function bindInput() {
    const L = UI.layer;
    // 펜슬이 화면을 끌지 않게(iPadOS 는 펜슬로도 스크롤한다) · 쓰는 동안 손바닥이 화면을 밀지 않게
    L.addEventListener("touchstart", (e) => {
      const stylus = [].some.call(e.changedTouches, (t) => t.touchType === "stylus");
      if (stylus || UI.tool.finger || UI.act || Date.now() - UI.lastPen < 500) e.preventDefault();
    }, { passive: false });
    L.addEventListener("pointerdown", (e) => {
      if (e.pointerType === "touch" && !UI.tool.finger) return;
      if (e.pointerType === "mouse" && e.button !== 0) return;
      if (UI.act) {                                              // 손가락 쓰기 중 둘째 손가락 → 쓰던 획을 버리고 넘기기로
        if (e.pointerType === "touch" && UI.act.type === "touch") { cancelStroke(); UI.act = { pan: true, id: e.pointerId, y: e.clientY, x: e.clientX }; }
        return;
      }
      e.preventDefault();
      try { L.setPointerCapture(e.pointerId); } catch (_) { /* 무시 */ }
      const p = pt(e), b = blockAt(p[1]);
      UI.act = { id: e.pointerId, type: e.pointerType, b, top: UI.tops[b], t0: Date.now(), cx: e.clientX, cy: e.clientY, moved: false,
                 pts: [p[0], p[1] - UI.tops[b], pressure(e)], erase: UI.tool.kind === "erase" };
      if (e.pointerType === "pen") UI.lastPen = Date.now();
      if (UI.act.erase) eraseAt(p);
    });
    L.addEventListener("pointermove", (e) => {
      const a = UI.act;
      if (!a || e.pointerId !== a.id) return;
      e.preventDefault();
      if (a.pan) { UI.scroll.scrollTop += a.y - e.clientY; UI.scroll.scrollLeft += a.x - e.clientX; a.y = e.clientY; a.x = e.clientX; return; }
      if (Math.abs(e.clientX - a.cx) + Math.abs(e.clientY - a.cy) > 4) a.moved = true;
      const evs = e.getCoalescedEvents ? e.getCoalescedEvents() : [];
      (evs.length ? evs : [e]).forEach((ev) => {
        const p = pt(ev);
        if (a.erase) return eraseAt(p);
        const n = a.pts.length, lx = a.pts[n - 3], ly = a.pts[n - 2];
        const x = p[0], y = p[1] - a.top;
        if (Math.abs(x - lx) + Math.abs(y - ly) < 0.4) return;
        const pr = pressure(ev);
        a.pts.push(x, y, pr);
        liveSegment(lx, ly + a.top, x, y + a.top, (pr + a.pts[n - 1]) / 2);
      });
      if (e.pointerType === "pen") UI.lastPen = Date.now();
    });
    const end = (e) => {
      const a = UI.act;
      if (!a || e.pointerId !== a.id) return;
      UI.act = null;
      if (a.pan || a.erase) { if (a.erase) flushErase(); return; }
      if (e.type === "pointercancel") { ensureStale(a); return; }
      if (!a.moved && Date.now() - a.t0 < 500) {                 // 톡 — 아래가 누르는 것(해설 펼치기 등)이면 그것을 누른다
        L.style.pointerEvents = "none";
        const under = document.elementFromPoint(e.clientX, e.clientY);
        L.style.pointerEvents = "";
        const hit = under && under.closest && under.closest(TAPPABLE);
        if (hit && UI.content.contains(hit)) { ensureStale(a); UI.tapAt = Date.now(); hit.click(); return; }
      }
      commitStroke(a);
    };
    L.addEventListener("pointerup", end);
    L.addEventListener("pointercancel", end);
    L.addEventListener("click", (e) => {                         // 손가락으로 톡 — 층이 가로채므로 아래 것을 대신 누른다
      if (Date.now() - (UI.tapAt || 0) < 500) return;
      L.style.pointerEvents = "none";
      const under = document.elementFromPoint(e.clientX, e.clientY);
      L.style.pointerEvents = "";
      const hit = under && under.closest && under.closest(TAPPABLE);
      if (hit && UI.content.contains(hit)) { UI.tapAt = Date.now(); hit.click(); }
    });
  }
  const TAPPABLE = "[data-pick], details.ink-ex > summary";      // 종이에서 누를 수 있는 것은 이 둘뿐(정리본 안 단추는 누르지 않는다)
  const pressure = (e) => (e.pointerType === "pen" && e.pressure > 0 ? e.pressure : 0.5);
  function liveStyle() {
    const t = UI.tool;
    return t.kind === "hl" ? { c: HL, w: 16, t: 1 } : { c: t.color, w: t.width, t: 0 };
  }
  function liveSegment(x0, y0, x1, y1, pr) {
    const st = liveStyle(), w = st.t ? st.w : widthAt(st.w, pr);
    for (let i = Math.max(0, Math.floor((Math.min(y0, y1) - w) / TILE)); i <= Math.floor((Math.max(y0, y1) + w) / TILE) && i < UI.tiles.length; i++) {
      const t = UI.tiles[i];
      if (!t.live) continue;
      const ctx = t.c.getContext("2d");
      ctx.setTransform(UI.q, 0, 0, UI.q, 0, 0);
      ctx.strokeStyle = st.c; ctx.lineWidth = w; ctx.lineJoin = "round";
      ctx.lineCap = st.t ? "butt" : "round"; ctx.globalAlpha = st.t ? 0.3 : 1;
      ctx.beginPath(); ctx.moveTo(x0, y0 - i * TILE); ctx.lineTo(x1, y1 - i * TILE); ctx.stroke();
      ctx.globalAlpha = 1;
    }
  }
  function ensureStale(a) {                                       // 버린 획의 흔적을 지운다
    let y0 = 1e9, y1 = -1e9;
    for (let i = 1; i < a.pts.length; i += 3) { y0 = Math.min(y0, a.pts[i]); y1 = Math.max(y1, a.pts[i]); }
    staleFor({ b: a.b, y0, y1 }); ensureTiles();
  }
  function cancelStroke() { if (UI.act && UI.act.pts) ensureStale(UI.act); }
  function newId() { return device().slice(-8) + "-" + Date.now().toString(36) + "-" + Math.floor(Math.random() * 46656).toString(36); }
  function commitStroke(a) {
    const st = liveStyle(), sid = newId();
    UI.rec.doc.s[sid] = { c: st.c, w: st.w, t: st.t, b: a.b, d: pack(a.pts) };
    UI.rt[sid] = runtime(sid, UI.rec.doc.s[sid]);
    UI.mine[sid] = 1;
    UI.undo.push({ add: sid });
    staleFor(UI.rt[sid]);
    // 여백 끝 가까이까지 썼으면 종이를 늘인다
    if (a.b === "p" && UI.rt[sid].y1 > UI.rec.doc.ph - 160) { UI.rec.doc.ph += PAPER_STEP; layout(false); } else ensureTiles();
    touched(); paintBar();
  }
  // 지우개 — 지나간 길(앞 점 → 지금 점)을 촘촘히 나눠, 획의 **선분**까지의 거리로 판정한다(획의 점만 보면 빨리 그은 획을 놓친다).
  function segDist(px, py, ax, ay, bx, by) {
    const dx = bx - ax, dy = by - ay, L = dx * dx + dy * dy;
    const t = L ? Math.max(0, Math.min(1, ((px - ax) * dx + (py - ay) * dy) / L)) : 0;
    return Math.hypot(px - ax - t * dx, py - ay - t * dy);
  }
  function eraseAt(p) {
    const R = 9, from = UI.erasePrev || p;
    UI.erasePrev = p;
    const steps = Math.max(1, Math.ceil(Math.hypot(p[0] - from[0], p[1] - from[1]) / (R / 2)));
    for (let k = 1; k <= steps; k++) {
      const ex = from[0] + (p[0] - from[0]) * k / steps, ey = from[1] + (p[1] - from[1]) * k / steps;
      Object.keys(UI.rt).forEach((sid) => {
        const st = UI.rt[sid];
        if (hiddenBlock(st.b) || veiled(sid)) return;
        const x = ex, y = ey - topOf(st.b), r = R + st.w / 2;
        if (x < st.x0 - r || x > st.x1 + r || y < st.y0 - r || y > st.y1 + r) return;
        const q = st.pts;
        for (let i = 0; i < q.length; i += 3) {
          const j = i + 3 < q.length ? i + 3 : i;
          if (segDist(x, y, q[i], q[i + 1], q[j], q[j + 1]) < r) { removeStroke(sid, true); UI.erased = true; break; }
        }
      });
    }
    if (UI.erased) ensureTiles();
  }
  function flushErase() { UI.erasePrev = null; if (UI.erased) { UI.erased = false; touched(); paintBar(); } }
  function removeStroke(sid, undoable) {
    const s = UI.rec.doc.s[sid];
    if (!s) return;
    staleFor(UI.rt[sid]);
    if (undoable) UI.undo.push({ del: s });
    delete UI.rec.doc.s[sid]; delete UI.rt[sid];
    UI.rec.doc.g[sid] = new Date().toISOString();
  }
  function undo() {
    const op = UI.undo.pop();
    if (!op) return;
    if (op.add) removeStroke(op.add, false);
    else { const sid = newId(); UI.rec.doc.s[sid] = op.del; UI.rt[sid] = runtime(sid, op.del); UI.mine[sid] = 1; staleFor(UI.rt[sid]); }   // 묘비가 있으니 새 id 로 되살린다
    ensureTiles(); touched();
  }

  /* 저장 — 기기에는 바로(0.6초 모아서), 서버에는 30초 쉬었을 때 · 닫을 때 · 앱이 가려질 때 */
  function touched() {
    UI.rec.doc.u = new Date().toISOString();
    UI.rec.dirty = true;
    clearTimeout(UI.saveT); UI.saveT = setTimeout(flushLocal, 600);
    clearTimeout(UI.pushT); UI.pushT = setTimeout(pushNow, 30000);
    status(canSync() ? "저장됨 · 곧 올림" : localWhy());
  }
  function localWhy() {
    if (!pass()) return "이 기기에만 저장 — 동기화 키 없음";
    if (!subtle) return "이 기기에만 저장 — 이 주소는 잠그기를 못 함";
    if (NET.available === false) return "이 기기에만 저장 — 이 주소엔 동기화 서버 없음";
    return "이 기기에 저장 — 연결되면 올림";
  }
  function flushLocal() { clearTimeout(UI.saveT); return UI.rec ? saveRec(UI.rec) : Promise.resolve(); }
  let pushing = false;
  async function pushNow(given) {
    clearTimeout(UI.pushT);
    const rec = given || UI.rec;
    if (!rec || pushing) return;
    if (!canSync()) return status(localWhy());
    pushing = true;
    status("☁ 맞추는 중…");
    const res = await syncRec(rec, () => { if (UI.rec === rec) { rebuildRuntime(); layout(false); UI.tiles.forEach((t) => { t.stale = true; }); ensureTiles(); } });
    pushing = false;
    if (UI.rec !== rec) return;
    if (res === "ok") status("☁ 맞춰짐 " + new Date().toTimeString().slice(0, 5), "ok");
    else if (res === "locked") status("다른 동기화 키로 잠긴 필기가 서버에 있습니다 — 올리지 않음", "bad");
    else if (res === "local") status(localWhy());
    else status("올리기 실패 — 이 기기에는 저장됨" + (NET.lastError ? " (" + NET.lastError + ")" : ""), "bad");
    if (rec.dirty && res === "ok") UI.pushT = setTimeout(pushNow, 30000);
  }

  // opts: chosen(내가 고른 보기) · solve(푸는 중) · quiz(문항 화면에서 열었다 — 「다음 문항」이 보인다) · q(문항 객체)
  async function open(exam, id, opts) {
    opts = opts || {};
    build();
    if (UI.rec) await leave();
    const isC = exam === "concept";
    const q = isC ? null : (opts.q || findQuestion(id)), w = isC ? null : wrongEntry(exam, id);
    UI.rec = await loadRec(exam, id);
    if (Number.isInteger(opts.chosen)) UI.rec.doc.c = opts.chosen;
    const chosen = Number.isInteger(opts.chosen) ? opts.chosen : (w && Number.isInteger(w.chosen) ? w.chosen : UI.rec.doc.c);
    UI.st = { exam, id, kind: isC ? "concept" : "q", q, w, solve: !!opts.solve && !!q, chosen, quiz: !!opts.quiz };
    UI.undo = []; UI.zoom = 1; UI.mine = {}; UI.hideOld = UI.st.solve;
    UI.el.classList.remove("hidden"); document.body.classList.add("ink-open");
    UI.scroll.scrollTop = 0;
    rebuildRuntime(); renderSheet(false); layout(true);
    const n = countStrokes(UI.rec.doc);
    status(UI.hideOld && n ? `전에 쓴 필기 ${n}획은 채점 뒤에 보입니다` : n ? "기기에 저장된 필기" : "");
    pushNow();                                                    // 열면서 서버 것과 맞춘다(다른 기기에서 쓴 것 받기)
  }
  // 지금 연 필기를 저장하고 손에서 놓는다(화면은 그대로) — 닫기 · 다음 문항이 함께 쓴다.
  async function leave() {
    if (!UI.rec) return;
    await flushLocal();
    const rec = UI.rec;
    pushNow(rec).then(() => { if (!UI.rec) refreshLists(); if (rec.dirty) flushAll(); });
    UI.rec = null; UI.act = null;
  }
  function refreshLists() {
    const list = document.getElementById("wbList");
    if (list) decorate(list);
    const all = document.getElementById("inkList");
    if (all && !all.classList.contains("hidden")) renderAll();
    document.querySelectorAll("button[data-ink-concept]").forEach((b) => {
      const n = loadIdx()[keyOf("concept", b.getAttribute("data-ink-concept"))] || 0;
      b.textContent = n ? `✍ 이 정리본에 필기 (${n}획)` : "✍ 이 정리본에 필기";
      b.classList.toggle("has", !!n);
    });
  }
  async function close() {
    if (!UI.el || UI.el.classList.contains("hidden")) return;
    await leave();
    UI.tiles.forEach(dropTile);
    UI.el.classList.add("hidden"); document.body.classList.remove("ink-open");
    refreshLists();
  }
  // 문항 화면에서 — 지금 문항을 필기장으로. 아직 안 풀었으면 푸는 중으로 연다.
  function openFromQuiz() {
    const deck = g("deck"), pos = g("pos"), answers = g("answers");
    const q = Array.isArray(deck) ? deck[pos] : null, ex = examOf(q);
    if (!ex) return;
    const a = Array.isArray(answers) ? answers[pos] : null;
    open(ex, q.id, { quiz: true, q, solve: a == null, chosen: a == null ? undefined : a });
  }
  async function next() {
    const nb = document.getElementById("nextBtn"), quiz = document.getElementById("quiz");
    if (!nb || nb.classList.contains("hidden")) return close();
    await leave();
    nb.click();                                                   // 앱이 다음 문항을 그리거나(끝이면) 결과 화면으로 간다
    if (!quiz || quiz.classList.contains("hidden")) return close();
    openFromQuiz();
  }

  /* 오답노트 목록 — 오답마다 「✍ 필기」 단추. 획 수는 기기 색인에서, ☁ 는 다른 기기에서 쓴 필기가 서버에 있을 때. */
  function decorate(list) {
    const idx = loadIdx(), exams = {};
    list.querySelectorAll("button[data-note]").forEach((nb) => {
      const id = nb.getAttribute("data-note"), ex = nb.getAttribute("data-ex");
      let b = nb.parentNode.querySelector("button[data-ink]");
      if (!b) {
        b = document.createElement("button");
        b.setAttribute("data-ink", id); b.setAttribute("data-ex", ex); b.className = "ink-open-btn";
        b.onclick = () => open(ex, id);
        nb.parentNode.insertBefore(b, nb);
      }
      const n = idx[keyOf(ex, id)] || 0, remote = (NET.remote[ex] || {})[fid(id)];
      b.textContent = n ? `✍ 필기 (${n}획)` : remote ? "✍ 필기 ☁" : "✍ 필기";
      b.classList.toggle("has", !!(n || remote));
      exams[ex] = true;
    });
    Object.keys(exams).forEach((ex) => {
      const before = JSON.stringify(NET.remote[ex] || {});
      refreshRemote(ex).then((files) => { if (JSON.stringify(files) !== before && document.body.contains(list)) decorate(list); });
    });
  }

  /* 필기 모음 — 필기가 있는 것 전부(이 기기 색인 + 다른 기기에서 올린 것). 문항이든 정리본이든 눌러서 이어 쓴다. */
  const KIND_NAME = { kmle: "KMLE", usmle: "USMLE", imaging: "영상", variant: "변형", concept: "정리본" };
  function showAll() {
    let el = document.getElementById("inkList");
    if (!el) {
      el = document.createElement("div");
      el.id = "inkList"; el.className = "ink-list hidden";
      el.innerHTML = `<section class="card"><h2>필기 모음 <span id="inkListCount" class="muted"></span></h2>
        <div class="row"><button data-a="back">← 돌아가기</button></div><div id="inkListBody"></div></section>`;
      document.body.appendChild(el);
      el.addEventListener("click", (e) => {
        const b = e.target.closest("button");
        if (!b) return;
        if (b.getAttribute("data-a") === "back") return el.classList.add("hidden");
        if (b.hasAttribute("data-open")) open(b.getAttribute("data-ex"), b.getAttribute("data-open"));
      });
    }
    el.classList.remove("hidden");
    renderAll();
    EXAMS.forEach((ex) => {
      const before = JSON.stringify(NET.remote[ex] || {});
      refreshRemote(ex).then((files) => { if (JSON.stringify(files) !== before && !el.classList.contains("hidden")) renderAll(); });
    });
  }
  function renderAll() {
    const idx = loadIdx(), items = {}, L = g("LEARN");
    Object.keys(idx).forEach((k) => { items[k] = { n: idx[k] }; });
    EXAMS.forEach((ex) => Object.keys(NET.remote[ex] || {}).forEach((f) => {
      const k = keyOf(ex, unfid(ex, f));
      (items[k] = items[k] || { n: 0 }).remote = true;
    }));
    const keys = Object.keys(items).sort().reverse();
    document.getElementById("inkListCount").textContent = `(${keys.length}개)`;
    document.getElementById("inkListBody").innerHTML = keys.length ? keys.map((k) => {
      const i = k.indexOf(":"), ex = k.slice(0, i), id = k.slice(i + 1), it = items[k];
      let title = "", sub = "";
      if (ex === "concept") { const c = L && typeof L.concept === "function" ? L.concept(id) : null; title = c ? c.title : id; sub = c ? c.topic || "" : ""; }
      else { const q = findQuestion(id); title = q ? (q.question || q.vignette || "").trim().slice(0, 90) : "(문항 은행에 없음)"; sub = q ? q.subject || "" : ""; }
      return `<div class="w"><div class="whead">${ex === "concept" ? "" : "#" + esc(id) + " "}<span class="muted">${esc(KIND_NAME[ex] || ex)}${sub ? " · " + esc(sub) : ""}</span></div>
        <div class="wmeta">${esc(title)}</div>
        <button data-open="${esc(id)}" data-ex="${esc(ex)}" class="ink-open-btn has">✍ 열기${it.n ? ` (${it.n}획)` : " ☁"}</button></div>`;
    }).join("") : `<p class="muted">아직 필기가 없습니다. 오답노트의 「✍ 필기」, 문항 화면의 「✍ 펜으로 풀기」, 개념 정리본의 「✍ 이 정리본에 필기」에서 시작합니다.</p>`;
  }
  // 개념 정리본 머리에 필기 단추(learn.js 의 renderConcept 가 부른다 — 필기장 안에서 그릴 때는 부르지 않는다)
  function conceptButton(box, cid) {
    const head = box.querySelector(".cn-h");
    if (!head || head.querySelector("[data-ink-concept]")) return;
    const b = document.createElement("button");
    b.type = "button"; b.className = "small ink-open-btn"; b.setAttribute("data-ink-concept", cid);
    const n = loadIdx()[keyOf("concept", cid)] || 0;
    b.textContent = n ? `✍ 이 정리본에 필기 (${n}획)` : "✍ 이 정리본에 필기";
    b.classList.toggle("has", !!n);
    b.onclick = () => open("concept", cid);
    head.appendChild(b);
  }
  // 문항 화면의 「✍ 펜으로 풀기」 · 첫 화면의 「✍ 필기 모음」 — 앱 껍데기(index.html)를 건드리지 않고 여기서 끼운다.
  function addButtons() {
    const quit = document.getElementById("quitBtn"), vw = document.getElementById("viewWrongBtn");
    if (quit && !document.getElementById("inkSolveBtn")) {
      const b = document.createElement("button");
      b.id = "inkSolveBtn"; b.textContent = "✍ 펜으로 풀기"; b.onclick = openFromQuiz;
      quit.parentNode.insertBefore(b, quit);
    }
    if (vw && !document.getElementById("inkAllBtn")) {
      const b = document.createElement("button");
      b.id = "inkAllBtn"; b.textContent = "✍ 필기 모음"; b.onclick = showAll;
      vw.parentNode.insertBefore(b, vw.nextSibling);
    }
  }
  addButtons();

  window.addEventListener("online", () => { flushAll(); });
  setTimeout(flushAll, 5000);

  return Object.assign(core, { open, close, decorate, flushAll, showAll, conceptButton, openFromQuiz, _net: NET });      // _net = 시험용(서버 유무 판정을 되돌릴 때)
})();
if (typeof module !== "undefined" && module.exports) module.exports = MEDKOS_INK;
