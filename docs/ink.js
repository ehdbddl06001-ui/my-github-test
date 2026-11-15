/* MedKOS 오답노트 필기 — 펜슬로 쓰고, 기기끼리 맞춘다 (2026-11-15)

   왜: 오답노트는 자동으로 쌓이지만 「왜 틀렸나」를 손으로 풀어 쓰는 자리가 없었다(글 메모 한 줄뿐).
   문항 하나마다 필기장을 연다 — 위에 문항 · 내 답 · 정답 · 해설(접힘), 아래에 줄 여백. 그 위 어디에든 쓴다.
   여는 곳 넷(2판 — 「오답만이 아니라 전부 · 푸는 것도 패드로 · 학습서도」):
     ① 오답노트의 「✍ 필기」  ② 문항 화면의 「✍ 펜으로 풀기」 — 필기장 안에서 보기를 톡 쳐 채점하고 다음 문항으로 넘어간다
        (채점 · 학습 기록 · 오답노트 저장은 앱이 그대로 한다. 전에 쓴 필기는 채점 뒤에 보인다 — 답을 미리 알려 주지 않게)
     ③ 개념 정리본(학습서의 단위)의 「✍ 이 정리본에 필기」  ④ 메뉴 줄의 「📖 학습서 필기」 → 그 안의 「✍ 필기 모음」 — 필기가 있는 것 전부.
   3판(써 본 뒤 — 「펜 해상도 · 색 여러 개 · 촉감 · 직선 · 문제 전체가 한 화면에」): 획을 곡선으로 잇고 잘게 나눠 굵기를 바꿔 가며
   그린다(압력 · 빠르기) · 펜 색 12 + 형광펜 색 5 + 굵기 5 · 직선(단추를 켜거나, 긋다가 멈추면 펴진다 · 수평 · 수직에 맞춘다) ·
   가로 화면에서는 문항 옆에 여백을 나란히 놓고 문항 + 보기가 한 화면에 담기게 줄인다 · 🔑 로그인(아이디 · 비밀번호로 키를 만든다).
   맞힌 문항도 「★ 정리본에 넣기」를 누르면 표시(want_note)가 남아 개념 복습 · 정리본 큐에 들어간다(learn.js).

   5판(「PDF 를 필기 앱으로 연 것만큼 선명하게 · 한 내용이 한 쪽에 · 확대 축소」): 필기 캔버스를 종이(transform) 밖에 두어 글자가
   흐려지지 않게 하고(Safari 는 캔버스를 품은 transform 층을 저해상도 그림으로 굳혀 늘린다), 조각을 화면 512 px 격자로 바꿔 확대해도
   선명하다 · 정리본은 두 단으로 한 화면에(▥ 두 단) · 두 손가락 확대 축소(Ctrl + 휠) · 가는 펜(0.5 부터) · 정리본은 늘 최신판 위에 필기.

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
  const TPX = 512;               // 필기 층을 화면 512 px 정사각 캔버스 조각의 격자로 나눈다(확대해도 조각 화소 수가 같다 — iOS 캔버스 한도)
  const PAPER0 = 900, PAPER_STEP = 600;
  const SALT = "medkos-ink-v1";
  const COLORS = ["#1b2430", "#6b7280", "#d92d20", "#e8710a", "#b7791f", "#0f8a4f", "#0e7490", "#1d4ed8", "#4338ca", "#7c3aed", "#db2777", "#7c4a2d"];
  const HLS = ["#f5c518", "#7ddc6f", "#ff8fb3", "#7cc4ff", "#ffb347"];      // 형광펜
  const WIDTHS = [0.5, 0.8, 1.2, 1.8, 2.6, 4.0];                // 종이 px — 두 단 보기(종이를 줄여 본다)에서도 가는 선이 나오게 0.5 부터
  const QUICK = ["#1b2430", "#d92d20", "#1d4ed8", "#0f8a4f"];             // 막대에 늘 보이는 색(쓴 색이 앞으로 온다)

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
  // c = 내가 고른 보기(맞힌 문항도 다시 열면 보이게)
  // n = 정리본에 필기할 때의 판 { at, ver, updated, hash, c: 정리본 } — 조용히 떠 둔다. 종이는 늘 최신 정리본을 그리지만(「항상 최신판 위에
  //     필기」), 정리본이 고쳐지면 이 판과 견줘 바뀐 곳을 알리고 「전에 쓴 판 보기」로 필기가 맞던 글을 다시 볼 수 있게 한다.
  function emptyDoc() { return { v: 1, ph: PAPER0, c: null, n: null, s: {}, g: {}, u: "" }; }
  const sigOf = (c) => String((c && c.hash) || ((c && c.version) || 1) + "|" + ((c && c.updated) || ""));
  function snapOf(c, at) {
    return { at: at || new Date().toISOString(), ver: c.version || 1, updated: String(c.updated || ""), hash: sigOf(c), c: JSON.parse(JSON.stringify(c)) };
  }
  function normSnap(n) { return n && typeof n === "object" && n.c && typeof n.c === "object" && typeof n.at === "string" ? n : null; }
  const snapStale = (n, live) => !!(n && live && sigOf(live) !== n.hash);
  // 필기본(o)과 원본 새 판(n)에서 달라진 곳의 이름 — 필기본 머리에 「바뀐 곳」으로 보인다.
  function changedParts(o, n) {
    const j = (x) => JSON.stringify(x == null ? null : x), out = [];
    const add = (name, x, y) => { if (j(x) !== j(y)) out.push(name); };
    add("제목 · 학습 목표", [o.title, o.objective], [n.title, n.objective]);
    add("빠른 요약", o.summary, n.summary);
    add("그림", o.figures, n.figures);
    add("임상 판단 도식", [o.geo, o.steps, o.diagramNotes], [n.geo, n.steps, n.diagramNotes]);
    const sec = (c) => {
      const m = {};
      (c.sections || []).forEach((s) => { m[s.title] = j(s.html); });
      (c.tables || []).forEach((t) => { m[t.title] = j(t); });
      return m;
    };
    const so = sec(o), sn = sec(n);
    Object.keys(sn).forEach((k) => { if (!(k in so)) out.push(k + "(새 절)"); else if (so[k] !== sn[k]) out.push(k); });
    Object.keys(so).forEach((k) => { if (!(k in sn)) out.push(k + "(빠짐)"); });
    add("혼동하기 쉬운 점", o.pitfalls, n.pitfalls);
    add("기준·권고", o.criteria, n.criteria);
    add("인출 확인", o.checks, n.checks);
    add("근거", o.sources, n.sources);
    return out;
  }
  function normDoc(d) {
    const o = d && typeof d === "object" ? d : {};
    return {
      v: 1, ph: Math.max(PAPER0, Math.min(60000, Number(o.ph) || PAPER0)), c: Number.isInteger(o.c) ? o.c : null, n: normSnap(o.n),
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
    const n = a.n && b.n ? (a.n.at >= b.n.at ? a.n : b.n) : (a.n || b.n);      // 필기본의 판 — 나중에 뜬(새 판으로 옮긴) 쪽
    return { v: 1, ph: Math.max(a.ph, b.ph), c: nw.c != null ? nw.c : od.c, n, s, g, u: nw.u };
  }
  function sameDoc(a, b) {
    const ka = Object.keys(a.s).sort().join(","), kb = Object.keys(b.s).sort().join(",");
    const ga = Object.keys(a.g).sort().join(","), gb = Object.keys(b.g).sort().join(",");
    return ka === kb && ga === gb && a.ph === b.ph && ((a.n && a.n.at) || "") === ((b.n && b.n.at) || "");
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

  // 아이디 · 비밀번호 → 동기화 키. 아이디는 앞뒤 공백 · 대소문자를 가리지 않는다. 같은 입력이면 어느 기기에서나 같은 키.
  async function loginKey(id, pw) {
    const enc = new TextEncoder(), salt = enc.encode("medkos-login-v1:" + String(id).trim().toLowerCase());
    const base = await subtle.importKey("raw", enc.encode(String(pw)), "PBKDF2", false, ["deriveBits"]);
    const bits = await subtle.deriveBits({ name: "PBKDF2", salt, iterations: 300000, hash: "SHA-256" }, base, 256);
    return "lk1-" + b64(new Uint8Array(bits)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }

  const core = { W, pack, unpack, mergeDocs, sameDoc, emptyDoc, normDoc, countStrokes, seal, unseal, loginKey, snapOf, snapStale, changedParts, sigOf };
  if (typeof document === "undefined") return core;          // node 시험 — 아래는 화면이 있을 때만

  /* ───────── 기기 저장소(IndexedDB · 없으면 메모리) ───────── */
  const SNAP_KEY = "medkos_ink_snap";                         // { 정리본 id: 필기본이 뜬 판의 지문 } — 목록에서 「원본 갱신됨」을 바로 보인다
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
    if (rec.exam === "concept") {
      const sx = loadSnapIdx();
      if (rec.doc.n) sx[rec.id] = rec.doc.n.hash; else delete sx[rec.id];
      try { localStorage.setItem(SNAP_KEY, JSON.stringify(sx)); } catch (e) { /* 위와 같다 */ }
    }
  }
  function loadSnapIdx() { try { return JSON.parse(localStorage.getItem(SNAP_KEY) || "{}") || {}; } catch (e) { return {}; } }
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
    el: null, rec: null, rt: {}, geo: {}, tiles: new Map(), s: 1, q: 1, zoom: 1, TL: TPX, pinch: null, sheetH: 0, SW: W, step: 1,
    tool: loadTool(), undo: [], mine: {}, st: null, saveT: null, pushT: null, raf: 0, lastPen: 0, act: null, dirtyTiles: null,
  };
  function loadTool() {
    let t = {};
    try { t = JSON.parse(localStorage.getItem("medkos_ink_tool") || "{}") || {}; } catch (e) { t = {}; }
    const hex = (c) => typeof c === "string" && /^#[0-9a-f]{6}$/i.test(c);
    const recent = (Array.isArray(t.recent) ? t.recent.filter(hex) : []).concat(QUICK).filter((c, i, l) => l.indexOf(c) === i).slice(0, 4);
    return { kind: t.kind === "hl" || t.kind === "erase" ? t.kind : "pen", color: hex(t.color) ? t.color : COLORS[0],
             hlColor: HLS.indexOf(t.hlColor) >= 0 ? t.hlColor : HLS[0], width: WIDTHS.indexOf(t.width) >= 0 ? t.width : WIDTHS[2],
             line: !!t.line, side: t.side !== false, cols: t.cols !== false, even: t.even !== false, finger: !!t.finger, recent };
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
  // 정리본 필기(2026-11-15 2차 — 「항상 최신판 위에 필기」) — 종이는 늘 **최신 정리본**이고 필기는 절 제목을 따라 그 위에 남는다.
  // 「내 필기본」이라는 구분은 없다. 다만 필기한 뒤 정리본이 고쳐지면 밑줄이 글자와 어긋날 수 있으므로, 필기할 때의 판(doc.n)을 조용히
  // 떠 두었다가 ① 무엇이 바뀌었는지 머리띠로 알리고 ② 「전에 쓴 판 보기」(읽기만)로 필기가 맞던 글을 다시 볼 수 있게 한다.
  // 「확인」을 누르면 떠 둔 판을 지금 판으로 바꾼다(머리띠가 사라진다). 정리본이 목록에서 빠지면 떠 둔 판을 그린다.
  const liveConcept = (id) => { const L = g("LEARN"); return (L && typeof L.concept === "function" && L.concept(id)) || null; };
  const verText = (ver, upd) => "v" + ver + (upd ? " · " + upd : "");
  function noteBarHtml(st, n) {
    const live = st.live, stale = snapStale(n, live);
    let msg = "", btn = "";
    if (st.old && n) {
      msg = `<b>전에 쓴 판</b> ${esc(verText(n.ver, n.updated))} — 읽기만`;
      btn = `<button type="button" data-note-act="live">← 최신판으로</button>`;
    } else if (n && !live) {
      msg = `정리본 목록에서 빠진 정리본입니다 — 필기할 때의 판(${esc(verText(n.ver, n.updated))})을 보여 줍니다.`;
    } else if (stale) {
      const ch = changedParts(n.c, live);
      msg = `<b>정리본이 고쳐졌습니다</b>(${esc(verText(n.ver, n.updated))} → ${esc(verText(live.version || 1, live.updated))})`
        + (ch.length ? `<br>바뀐 곳: ${esc(ch.join(" / "))}` : "") + `<br>글이 바뀐 절에서는 필기가 글자와 어긋날 수 있습니다.`;
      btn = `<button type="button" data-note-act="ack">확인</button><button type="button" data-note-act="old">전에 쓴 판 보기</button>`;
    }
    return msg ? `<div class="ink-note${stale && !st.old ? " stale" : ""}"><span>${msg}</span>${btn ? `<span class="ink-note-b">${btn}</span>` : ""}</div>` : "";
  }
  // 필기가 생겼는데 떠 둔 판이 아직 없으면 지금 정리본을 떠 둔다(첫 획 · 예전에 쓴 필기 · 다른 기기에서 받은 필기).
  function ensureSnap() {
    const st = UI.st, rec = UI.rec;
    if (!st || !rec || st.kind !== "concept" || st.old || rec.doc.n || !st.live || !countStrokes(rec.doc)) return false;
    rec.doc.n = snapOf(st.live); rec.dirty = true;
    st.snapAt = rec.doc.n.at;
    return true;
  }
  function noteAct(a) {
    const st = UI.st;
    if (!st || st.kind !== "concept" || !UI.rec) return;
    if (a === "old" || a === "live") st.old = a === "old" && !!UI.rec.doc.n;
    else if (a === "ack") {                                       // 바뀐 것을 봤다 — 떠 둔 판을 지금 판으로
      if (!st.live) return;
      UI.rec.doc.n = snapOf(st.live); st.old = false; touched();
    } else return;
    closePalette();
    renderSheet(false);
    UI.scroll.scrollTop = 0;
  }
  function conceptInto(st) {
    const L = g("LEARN"), n = UI.rec && UI.rec.doc.n;
    if (st.old && !n) st.old = false;
    const use = st.old ? n.c : (st.live || (n && n.c));
    st.snapAt = n ? n.at : "";
    UI.content.innerHTML = noteBarHtml(st, n) + `<div class="ink-cn"></div>` + PAPER_HTML;
    const box = UI.content.querySelector(".ink-cn");
    try { if (use && L && typeof L.renderConcept === "function") L.renderConcept(box, st.id, null, null, use); } catch (e) { /* 아래 안내 */ }
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
    UI.el.classList.toggle("old", st.kind === "concept" && !!st.old);
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
    if (ob && !UI.content.classList.contains("side")) UI.scroll.scrollTop = Math.max(0, org("o").y * UI.s - 60);
    status(i === cur.answer - 1 ? "정답 — 헷갈렸으면 ★ 정리본에 넣기" : "오답 — 오답노트에 저장됨", i === cur.answer - 1 ? "ok" : "bad");
  }

  function build() {
    if (UI.el) return;
    const el = document.createElement("div");
    el.id = "inkOverlay"; el.className = "ink-ov hidden";
    el.innerHTML = `<div class="ink-bar">
        <button data-a="close" class="ink-x">← 닫기</button>
        <span class="ink-tools">
          <span class="ink-quick"></span>
          <button data-a="pal" title="펜 색 · 굵기 · 형광펜 색">🎨 색 · 굵기</button>
          <button data-a="hl"><i class="ink-sw"></i>형광펜</button>
          <button data-a="erase">지우개</button>
          <button data-a="line" title="직선 — 켜지 않아도 긋다가 잠깐 멈추면 직선으로 펴진다">📏 직선</button>
          <button data-a="undo">↶</button>
          <button data-a="finger" title="손가락으로도 쓰기 — 켜면 두 손가락으로 넘긴다">☝ 손가락 쓰기</button>
          <button data-a="zout" class="ink-nav" aria-label="작게">−</button><button data-a="zin" class="ink-nav" aria-label="크게">＋</button>
          <button data-a="zfit" class="ink-nav" title="화면 폭에 맞춤 — 두 손가락을 벌리고 오므려 확대 · 축소한다">⤢ 맞춤</button>
          <button data-a="side" title="가로 화면 — 문항 옆에 여백을 나란히">⇆ 나란히</button>
          <button data-a="cols" title="정리본을 책처럼 두 단으로 — 한 정리본이 한 화면에 들어온다">▥ 두 단</button>
          <button data-a="more">여백 ＋</button>
          <button data-a="key" title="아이디 · 비밀번호로 이 기기의 동기화 키를 만든다 — 다른 기기에서도 같은 것을 넣으면 필기가 맞춰진다">🔑 로그인(필기 맞추기)</button>
          <button data-a="flag" title="맞혔어도 헷갈린 문항 — 개념 복습 · 정리본 큐에 넣는다">★ 정리본에 넣기</button>
          <button data-a="next" class="primary">다음 문항 →</button>
          <button data-a="cprev" class="ink-nav" title="학습서 목록의 앞 정리본">← 앞 정리본</button>
          <button data-a="cnext" class="ink-nav primary" title="학습서 목록의 다음 정리본">다음 정리본 →</button>
        </span>
        <span class="ink-st" id="inkStatus"></span>
        <div class="ink-pal" hidden>
          <div class="ink-pal-h">펜 색</div>
          <div class="ink-pal-r">${COLORS.map((c) => `<button data-a="color" data-c="${c}" class="ink-dot" style="--c:${c}" aria-label="펜 색"></button>`).join("")}</div>
          <div class="ink-pal-h">획</div>
          <div class="ink-pal-r"><button data-a="even" data-v="1">고른 굵기</button><button data-a="even" data-v="0">힘 · 빠르기에 따라</button></div>
          <div class="ink-pal-h">굵기</div>
          <div class="ink-pal-r">${WIDTHS.map((w) => `<button data-a="w" data-w="${w}" class="ink-wd" aria-label="굵기"><i style="height:${Math.max(1.5, w * 1.6)}px"></i></button>`).join("")}</div>
          <div class="ink-pal-h">형광펜 색</div>
          <div class="ink-pal-r">${HLS.map((c) => `<button data-a="hlc" data-c="${c}" class="ink-dot" style="--c:${c}" aria-label="형광펜 색"></button>`).join("")}</div>
        </div>
      </div>
      <div class="ink-scroll"><div class="ink-fit"><div class="ink-sheet"><div class="ink-content"></div></div><div class="ink-layer"></div></div></div>
      <canvas class="ink-live"></canvas>`;
    document.body.appendChild(el);
    UI.el = el;
    UI.scroll = el.querySelector(".ink-scroll"); UI.fit = el.querySelector(".ink-fit"); UI.sheet = el.querySelector(".ink-sheet");
    UI.content = el.querySelector(".ink-content"); UI.layer = el.querySelector(".ink-layer");
    UI.live = el.querySelector(".ink-live"); UI.pal = el.querySelector(".ink-pal");
    el.querySelector(".ink-bar").addEventListener("click", onBar);
    UI.content.addEventListener("click", (e) => {
      const b = e.target.closest("[data-pick]"), nb = e.target.closest("[data-note-act]");
      if (b) pick(Number(b.getAttribute("data-pick")));
      else if (nb) noteAct(nb.getAttribute("data-note-act"));
    });
    UI.scroll.addEventListener("scroll", () => schedule(ensureTiles), { passive: true });
    // 화면 폭이 바뀌면(돌리기 · 창 크기) 종이를 다시 맞춘다. 스크롤의 조각 그리기와 예약 칸을 따로 쓴다(서로 취소하지 않게).
    const refit = () => {
      if (!UI.rec || (UI.scroll.clientWidth === UI.fitW && UI.scroll.clientHeight === UI.fitH)) return;
      cancelAnimationFrame(UI.rafL); UI.rafL = requestAnimationFrame(() => layout(true));
    };
    window.addEventListener("resize", refit);
    if (typeof ResizeObserver === "function") new ResizeObserver(refit).observe(UI.scroll);
    document.addEventListener("keydown", (e) => { if (UI.rec && e.key === "Escape") close(); });
    document.addEventListener("visibilitychange", () => { if (document.hidden && UI.rec) { flushLocal(); pushNow(); } });
    bindInput();
    bindZoom();
  }
  function schedule(fn) { cancelAnimationFrame(UI.raf); UI.raf = requestAnimationFrame(fn); }
  function status(text, cls) { const el = document.getElementById("inkStatus"); if (el) { el.textContent = text; el.className = "ink-st " + (cls || ""); } }
  function closePalette() { if (UI.pal) UI.pal.hidden = true; }
  function paintBar() {
    const t = UI.tool, on = (sel, v) => UI.el.querySelector(sel).classList.toggle("on", !!v);
    UI.el.querySelector(".ink-quick").innerHTML = t.recent.map((c) =>
      `<button data-a="color" data-c="${c}" class="ink-dot${t.kind === "pen" && c === t.color ? " on" : ""}" style="--c:${c}" aria-label="펜 색"></button>`).join("");
    UI.pal.querySelectorAll("[data-a=color]").forEach((b) => b.classList.toggle("on", b.getAttribute("data-c") === t.color));
    UI.pal.querySelectorAll("[data-a=hlc]").forEach((b) => b.classList.toggle("on", b.getAttribute("data-c") === t.hlColor));
    UI.pal.querySelectorAll("[data-a=even]").forEach((b) => b.classList.toggle("on", (b.getAttribute("data-v") === "1") === t.even));
    UI.pal.querySelectorAll("[data-a=w]").forEach((b) => b.classList.toggle("on", Number(b.getAttribute("data-w")) === t.width));
    on("[data-a=hl]", t.kind === "hl"); on("[data-a=erase]", t.kind === "erase"); on("[data-a=line]", t.line);
    on("[data-a=finger]", t.finger); on("[data-a=side]", t.side); on("[data-a=cols]", t.cols);
    UI.el.querySelector(".ink-sw").style.background = t.hlColor;
    UI.el.querySelector("[data-a=undo]").disabled = !UI.undo.length;
    UI.layer.style.touchAction = t.finger ? "none" : "pan-x pan-y";
    const st = UI.st || {}, L = g("LEARN"), fb = UI.el.querySelector("[data-a=flag]"), nb = UI.el.querySelector("[data-a=next]");
    const canFlag = st.kind === "q" && !st.solve && st.q && !st.q.isVariant && L && typeof L.setFlag === "function";
    fb.hidden = !canFlag; nb.hidden = !(st.quiz && !st.solve);
    if (canFlag) fb.classList.toggle("on", !!L.flagsOf(st.q).want_note);
    UI.el.querySelector("[data-a=side]").hidden = !UI.wide;
    UI.el.querySelector("[data-a=key]").hidden = !!pass() || !subtle;
    const li = st.list ? st.list.indexOf(st.id) : -1;
    UI.el.querySelector("[data-a=cprev]").hidden = !(li > 0);
    UI.el.querySelector("[data-a=cnext]").hidden = !(li >= 0 && li < st.list.length - 1);
  }
  function onBar(e) {
    const b = e.target.closest("button[data-a]");
    if (!b) return;
    const a = b.getAttribute("data-a"), t = UI.tool;
    if (a === "close") return close();
    if (a === "pal") { UI.pal.hidden = !UI.pal.hidden; return; }
    if (a === "color") {
      t.kind = "pen"; t.color = b.getAttribute("data-c");
      if (t.recent.indexOf(t.color) < 0) t.recent = [t.color].concat(t.recent).slice(0, 4);
    }
    else if (a === "w") { t.width = Number(b.getAttribute("data-w")); if (t.kind === "erase") t.kind = "pen"; }
    else if (a === "even") t.even = b.getAttribute("data-v") === "1";
    else if (a === "hlc") { t.hlColor = b.getAttribute("data-c"); t.kind = "hl"; }
    else if (a === "hl") t.kind = t.kind === "hl" ? "pen" : "hl";
    else if (a === "erase") { t.kind = t.kind === "erase" ? "pen" : "erase"; clearLive(); }
    else if (a === "line") t.line = !t.line;
    else if (a === "finger") t.finger = !t.finger;
    else if (a === "undo") undo();
    else if (a === "zin" || a === "zout" || a === "zfit") {
      const sr = UI.scroll.getBoundingClientRect(), fr = UI.fit.getBoundingClientRect(), cx = sr.left + sr.width / 2, cy = sr.top + sr.height / 3;
      zoomTo(a === "zfit" ? 1 : UI.zoom * (a === "zin" ? 1.25 : 0.8), (cx - fr.left) / UI.s, (cy - fr.top) / UI.s, cx, cy);
    }
    else if (a === "side") { t.side = !t.side; UI.zoom = 1; layout(true); }
    else if (a === "cols") { t.cols = !t.cols; UI.zoom = 1; layout(true); UI.scroll.scrollTop = 0; }
    else if (a === "more") { UI.rec.doc.ph = Math.max(UI.rec.doc.ph, Math.round((UI.geo.p || { h: 0 }).h)) + PAPER_STEP; touched(); layout(false); }
    else if (a === "next") return next();
    else if (a === "cprev" || a === "cnext") {
      const st = UI.st, to = st.list && st.list[st.list.indexOf(st.id) + (a === "cnext" ? 1 : -1)];
      return to ? open("concept", to, { list: st.list }) : undefined;
    }
    else if (a === "key") return openLogin(false);
    else if (a === "flag") { const L = g("LEARN"); L.setFlag(UI.st.q, "want_note", !L.flagsOf(UI.st.q).want_note); }
    if (a !== "color" && a !== "w" && a !== "hlc" && a !== "even") closePalette();
    saveTool(); paintBar();
  }
  /* 로그인 — 아이디 · 비밀번호로 이 기기의 동기화 키를 만든다(2026-11-15 사용자 「아이디 · 비밀번호가 맞으면 키가 자동으로 들어가게」).
     키는 기기에서 계산한다(loginKey) — 비밀번호도 키도 서버로 가지 않는다. 「맞는지」는 서버에 둔 확인용 암호문(meta/login-check)이
     그 키로 열리는지로 판정한다. 확인용 암호문이 아직 없으면 처음 만드는 로그인이다(비밀번호를 한 번 더 받는다).
     어느 기기에서든 같은 아이디 · 비밀번호를 넣으면 같은 키가 나온다 → 연결 링크가 필요 없다. */
  async function loginTry(id, pw, pw2) {
    if (!subtle) return { msg: "이 주소에서는 잠그기를 쓸 수 없습니다(https 주소에서 여세요)." };
    const key = await loginKey(id, pw), h = { "content-type": "application/json" };
    let r;
    try { r = await fetch(`${NET.url}?exam=meta&id=login-check`, { headers: h }); }
    catch (e) { return { msg: "서버에 닿지 않아 확인하지 못했습니다 — 연결된 뒤 다시 하세요." }; }
    const isJson = (r.headers.get("content-type") || "").indexOf("json") >= 0;
    if (r.ok) {
      try { await unseal((await r.json()).env, key); } catch (e) { return { msg: "아이디 또는 비밀번호가 다릅니다." }; }
      return { key };
    }
    if (r.status === 404 && isJson) {                             // 아직 로그인이 만들어진 적이 없다
      if (pw2 == null) return { first: true, msg: "처음 만드는 로그인입니다 — 비밀번호를 한 번 더 넣고 「연결」을 누르세요." };
      if (pw2 !== pw) return { first: true, msg: "두 비밀번호가 다릅니다." };
      const w = await fetch(NET.url, { method: "POST", headers: h,
        body: JSON.stringify({ exam: "meta", id: "login-check", sha: null, env: await seal(emptyDoc(), key), device: device() }) });
      if (w.status === 409) return { msg: "방금 다른 기기에서 로그인이 만들어졌습니다 — 다시 「연결」을 누르세요." };
      if (!w.ok) return { msg: "로그인을 저장하지 못했습니다(" + w.status + ")." };
      return { key, created: true };
    }
    if (noServer(r.status)) return { msg: "이 주소에는 동기화 서버가 없습니다 — my-github-test.pages.dev 에서 여세요." };
    return { msg: "확인하지 못했습니다(" + r.status + ")." };
  }
  async function applyKey(key) {
    const f = g("onSyncKeyChange"), inp = document.getElementById("syncKey");
    if (inp) inp.value = key;
    if (typeof MEDKOS_SYNC === "object") MEDKOS_SYNC.set(key);
    else try { localStorage.setItem("medkos_sync_key", key); } catch (e) { /* 저장 못 함 — 아래 pass() 가 빈 값 */ }
    NET.available = null;
    if (UI.el) paintBar();
    if (UI.rec) pushNow(); else flushAll();
    try { if (typeof f === "function") await f(key); } catch (e) { /* 오답 · 학습 기록 동기화는 앱이 다시 시도한다 */ }
  }
  // gate = 앱을 열 때 띄우는 로그인 화면(뒤가 보이지 않는다). 아니면 필기장 · 동기화 설정에서 연 작은 창.
  const SKIP = "medkos_login_skip";                              // 이번에 연 동안은 로그인 화면을 다시 띄우지 않는다
  /* 앱을 열 때 로그인(2026-11-15 사용자 「필기에만 걸지 말고 MedKOS 들어갈 때」) — 이 기기에 키가 없으면 첫 화면 위에 로그인 화면을 띄운다.
     한 번 로그인하면 키가 기기에 남아 다시 묻지 않는다. 이것은 **기록을 맞추는 문**이지 잠금장치가 아니다 — 문항과 앱은 공개 저장소에 있어
     화면을 가려도 막지 못한다. 그래서 「로그인 없이 쓰기」를 둔다(연결이 없을 때 · 비밀번호를 잊었을 때 앱에 갇히지 않게). */
  function gateIfNeeded() {
    let skipped = false;
    try { skipped = sessionStorage.getItem(SKIP) === "1"; } catch (e) { /* 저장소 없음 — 띄운다 */ }
    if (pass() || skipped || !subtle || location.protocol === "file:") return;
    openLogin(true);
  }
  function logout() {
    if (!pass()) return alert("이 기기는 로그인돼 있지 않습니다.");
    if (!confirm("이 기기에서 로그아웃합니다(동기화 키를 지웁니다).\n기기에 저장된 오답 · 필기는 남고, 다시 로그인하면 이어서 맞춰집니다.")) return;
    applyKey("").then(() => { try { sessionStorage.removeItem(SKIP); } catch (e) { /* 무시 */ } gateIfNeeded(); });
  }
  function openLogin(gate) {
    gate = gate === true;
    closePalette();
    let el = document.getElementById("inkLogin");
    if (!el) {
      el = document.createElement("div");
      el.id = "inkLogin"; el.className = "ink-login hidden";
      el.innerHTML = `<form class="card" autocomplete="on">
        <h2>🔑 MedKOS 로그인</h2>
        <p class="muted small">아이디와 비밀번호로 이 기기의 동기화 키를 만듭니다. 다른 기기에서도 <b>같은 아이디 · 비밀번호</b>를 넣으면 같은 키가 들어가 오답 · 학습 기록 · 필기가 맞춰집니다.
          비밀번호는 서버로 보내지 않습니다 — 잊으면 되찾을 방법이 없으니 기기의 비밀번호 저장에 맡기세요.</p>
        <label>아이디<input name="username" autocomplete="username" autocapitalize="none" autocorrect="off" spellcheck="false" required /></label>
        <label>비밀번호<input name="password" type="password" autocomplete="current-password" minlength="8" required /></label>
        <label class="ink-login-2" hidden>비밀번호 한 번 더(처음 만들 때)<input name="password2" type="password" autocomplete="new-password" /></label>
        <p class="ink-login-m" role="status"></p>
        <div class="row"><button type="submit" class="primary">연결</button><button type="button" data-a="cancel">닫기</button></div>
      </form>`;
      document.body.appendChild(el);
      const form = el.querySelector("form"), msg = el.querySelector(".ink-login-m"), two = el.querySelector(".ink-login-2");
      el.querySelector("[data-a=cancel]").onclick = () => {
        if (el.classList.contains("gate")) { try { sessionStorage.setItem(SKIP, "1"); } catch (e) { /* 다음에 또 묻는다 */ } }
        el.classList.add("hidden");
      };
      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const id = form.username.value.trim(), pw = form.password.value, btn = form.querySelector("[type=submit]");
        if (!id || pw.length < 8) { msg.textContent = "아이디와 8자 이상의 비밀번호를 넣으세요."; return; }
        btn.disabled = true; msg.textContent = "확인하는 중…";
        let out;
        try { out = await loginTry(id, pw, two.hidden ? null : form.password2.value); }
        catch (err) { out = { msg: "확인하지 못했습니다(" + String((err && err.message) || err) + ")." }; }
        btn.disabled = false;
        if (out.first) { two.hidden = false; form.password2.focus(); }
        if (!out.key) { msg.textContent = out.msg; return; }
        const old = pass();
        if (old && old !== out.key && !confirm("이 기기에는 이미 다른 동기화 키가 들어 있습니다.\n바꾸면 예전 키로 올린 필기는 이 로그인으로 열리지 않습니다. 바꿀까요?")) { msg.textContent = "바꾸지 않았습니다."; return; }
        msg.textContent = out.created ? "로그인을 만들었습니다 — 이 기기의 필기를 올립니다." : "맞습니다 — 이 기기에 키를 넣고 필기를 맞춥니다.";
        await applyKey(out.key);
        form.password.value = ""; form.password2.value = ""; two.hidden = true;
        setTimeout(() => el.classList.add("hidden"), 1200);
      });
    }
    el.querySelector(".ink-login-m").textContent = pass() ? "이 기기에는 이미 키가 들어 있습니다. 다른 로그인으로 바꿀 때만 넣으세요." : "";
    el.classList.toggle("gate", gate);
    el.querySelector("[data-a=cancel]").textContent = gate ? "로그인 없이 쓰기(이 기기에만 저장)" : "닫기";
    el.classList.remove("hidden");
    if (!gate) el.querySelector("input[name=username]").focus();
  }

  /* 배치 — 종이를 화면에 맞춘다. 덩이의 자리(왼쪽 · 위)를 다시 재고, 보이는 조각만 다시 그린다.
     가로로 넓은 화면(아이패드 가로)에서 문항은 「나란히」 — 왼쪽에 문항 · 보기 · 해설, 오른쪽에 여백 — 로 놓고,
     문항 + 보기가 한 화면에 담기도록 배율을 낮춘다(3판 — 「문제 전체가 화면에 담겨야」).
     획은 덩이 왼쪽 위에서 잰 좌표라, 세로로 쌓든 나란히 놓든 같은 덩이의 같은 자리에 그려진다. */
  const GAP = 20, MIN_S = 0.62;
  function layout(resetTiles) {
    const st = UI.st || {}, cw = UI.scroll.clientWidth, ch = UI.scroll.clientHeight;
    const paper = UI.content.querySelector('[data-b="p"]');
    if (paper) paper.style.minHeight = UI.rec.doc.ph + "px";
    const keepTop = UI.scroll.scrollTop / (UI.s || 1);
    UI.fitW = cw; UI.fitH = ch;
    const wide = st.kind === "q" && cw >= 900 && cw > ch * 1.15;
    const side = wide && UI.tool.side;
    UI.wide = wide;
    UI.content.classList.toggle("side", side);
    UI.el.querySelector("[data-a=side]").hidden = !wide;
    // 정리본 두 단(2026-11-15 「한 내용이 한 쪽에」) — 절(덩이)의 폭은 한 단일 때와 같고(764), 단 사이를 56 으로 띄워 둘째 단의 덩이가
    // 정확히 820 오른쪽에 온다. 덩이는 단 사이에서 쪼개지지 않는다(CSS break-inside) — 획은 덩이 왼쪽 위 기준이라 어느 쪽으로 보든 같은 자리.
    const canCols = st.kind === "concept" && cw >= 700;
    const cols = canCols && UI.tool.cols;
    UI.content.classList.toggle("cols", cols);
    UI.el.querySelector("[data-a=cols]").hidden = !canCols;
    const SW = side ? 2 * W + GAP : cols ? 2 * W : W;
    if (SW !== UI.SW) { UI.SW = SW; resetTiles = true; }
    UI.sheet.style.width = SW + "px";
    let base = Math.min((cw - 12) / SW, 1.5);
    const qb = UI.content.querySelector('[data-b="q"]'), ob = UI.content.querySelector('[data-b="o"]');
    if (st.kind === "q" && qb && ob) {                            // 문항 + 보기가 한 화면에 담기는 배율
      const sH = (ch - 16) / (qb.offsetHeight + ob.offsetHeight + 8);
      if (side) base = Math.min(base, Math.max(sH, MIN_S));
      else if (sH < base && sH >= base * 0.72) base = sH;
    }
    UI.zoom = Math.max(ZMIN, Math.min(ZMAX, UI.zoom));
    const s = Math.max(0.25, Math.min(S_MAX, base * UI.zoom));
    if (Math.abs(s - UI.s) > 1e-4) resetTiles = true;
    UI.s = s;
    // 조각은 화면 px 로 크기가 고정이라(TPX) 배율이 곧 선명도다 — 확대하면 조각이 덮는 종이 넓이가 줄고 화소 밀도는 그만큼 오른다.
    UI.q = UI.s * (window.devicePixelRatio || 1);
    UI.TL = TPX / UI.s;                                           // 조각 한 변(종이 px)
    UI.step = Math.max(0.2, 1.6 / UI.q);                          // 획을 이 길이(종이 px)로 잘게 나눠 그린다 ≈ 화면 1.6 화소
    // 종이만 transform 으로 맞춘다. 필기 층(캔버스)은 종이 **밖**(형제)에 화면 px 로 둔다 — 캔버스가 transform 안에 있으면 Safari 가
    // 종이를 통째로 한 장의 그림(저해상도)으로 굳힌 뒤 늘려서 글자가 흐려진다(2026-11-15 「PDF 를 필기 앱으로 열었을 때만큼 선명하게」).
    UI.sheet.style.transform = `scale(${UI.s})`;
    UI.geo = {}; UI.first = "";
    const c0 = UI.content.getBoundingClientRect(), art = UI.content.querySelector(".ink-cn article"), a0 = art ? art.getBoundingClientRect().left : c0.left;
    UI.content.querySelectorAll("[data-b]").forEach((b) => {
      const k = b.getAttribute("data-b"), r = b.getBoundingClientRect(), blk = b.classList.contains("ink-block"), left = (r.left - c0.left) / UI.s;
      // x = 획의 기준점 · hx = 실제 왼쪽(어느 덩이에 쓰는지 고를 때). 종이의 큰 덩이(문항 · 보기 · 해설 · 여백)는 둘이 같고,
      // 정리본의 절은 기준점이 단의 왼쪽 끝(첫 단 0 · 둘째 단 820)이다 — 한 단일 때 쓴 필기와 같은 좌표.
      UI.geo[k] = { x: blk ? left : Math.max(0, Math.round((r.left - a0) / UI.s)), hx: left, tol: blk ? 4 : 28, y: (r.top - c0.top) / UI.s, w: r.width / UI.s, h: r.height / UI.s };
      if (!UI.first) UI.first = k;
    });
    UI.sheetH = UI.content.offsetHeight;
    UI.fit.style.width = Math.ceil(SW * UI.s) + "px";
    UI.fit.style.height = Math.ceil(UI.sheetH * UI.s) + "px";
    UI.layer.style.width = SW * UI.s + "px";
    UI.layer.style.height = UI.sheetH * UI.s + "px";
    if (resetTiles) { dropTiles(); UI.scroll.scrollTop = keepTop * UI.s; } else UI.tiles.forEach((t) => { t.stale = true; });
    sizeLive();
    ensureTiles();
  }
  const ZMIN = 0.5, ZMAX = 6, S_MAX = 4;
  // 배율을 바꾸되 종이의 (lx, ly) 가 화면의 (cx, cy) 에 그대로 있게 한다(두 손가락 가운데 · 단추는 화면 위쪽 1/3).
  function zoomTo(z, lx, ly, cx, cy) {
    UI.zoom = Math.max(ZMIN, Math.min(ZMAX, z));
    layout(true);
    const fr = UI.fit.getBoundingClientRect();
    UI.scroll.scrollLeft += fr.left + lx * UI.s - cx;
    UI.scroll.scrollTop += fr.top + ly * UI.s - cy;
    ensureTiles();
  }
  function killTile(t) { t.c.width = t.c.height = 0; t.c.remove(); }
  function dropTiles() { UI.tiles.forEach(killTile); UI.tiles.clear(); }
  // 보이는 곳(위아래로 한 줄 더)에만 조각을 둔다. 조각 = 화면 TPX 정사각, 화소는 TPX × 기기 배율 — 확대 배율과 무관하게 같은 메모리.
  function ensureTiles() {
    if (!UI.rec || UI.pinch) return;
    const TL = UI.TL, s = UI.s, fr = UI.fit.getBoundingClientRect(), sr = UI.scroll.getBoundingClientRect();
    const vx0 = (sr.left - fr.left) / s, vy0 = (sr.top - fr.top) / s, vx1 = vx0 + sr.width / s, vy1 = vy0 + sr.height / s;
    const x0 = Math.max(0, Math.floor(vx0 / TL)), x1 = Math.min(Math.ceil(UI.SW / TL) - 1, Math.floor(vx1 / TL));
    const y0 = Math.max(0, Math.floor(vy0 / TL) - 1), y1 = Math.min(Math.ceil(UI.sheetH / TL) - 1, Math.floor(vy1 / TL) + 1);
    UI.tiles.forEach((t, k) => { if (t.ix < x0 || t.ix > x1 || t.iy < y0 || t.iy > y1) { killTile(t); UI.tiles.delete(k); } });
    for (let iy = y0; iy <= y1; iy++) for (let ix = x0; ix <= x1; ix++) {
      const key = ix + "," + iy;
      let t = UI.tiles.get(key);
      if (!t) {
        const c = document.createElement("canvas");
        c.className = "ink-tile";
        c.style.left = ix * TPX + "px"; c.style.top = iy * TPX + "px"; c.style.width = c.style.height = TPX + "px";
        c.width = c.height = Math.max(1, Math.round(TPX * UI.q / s));
        UI.layer.appendChild(c);
        t = { c, ix, iy, k: c.width / TL, stale: true };
        UI.tiles.set(key, t);
      }
      if (t.stale) paintTile(t);
    }
  }
  const NOWHERE = { x: 0, y: 0, w: W, h: 0 };
  const org = (b) => UI.geo[b] || UI.geo[UI.first] || NOWHERE;                     // 이름이 사라진 덩이의 필기는 맨 위 덩이로
  const veiled = (sid) => UI.hideOld && !UI.mine[sid];                              // 푸는 중 — 전에 쓴 필기는 채점 뒤에
  function hiddenBlock(b) {
    if (b !== "e") return false;
    const d = UI.content.querySelector("details.ink-ex");
    return !d || !d.open;
  }
  // 조각의 그리기 판 — 종이 좌표로 그리면 되게 변환을 걸어 둔다(조각 밖은 저절로 잘린다)
  function tileCtx(t) {
    const ctx = t.c.getContext("2d");
    ctx.setTransform(t.k, 0, 0, t.k, -t.ix * UI.TL * t.k, -t.iy * UI.TL * t.k);
    return ctx;
  }
  function paintTile(t) {
    const ctx = tileCtx(t), TL = UI.TL, X0 = t.ix * TL, Y0 = t.iy * TL;
    t.stale = false;
    ctx.clearRect(X0 - 1, Y0 - 1, TL + 2, TL + 2);
    Object.keys(UI.rt).forEach((sid) => {
      const st = UI.rt[sid];
      if (hiddenBlock(st.b) || veiled(sid)) return;
      const o = org(st.b), m = st.w + 12;
      if (o.y + st.y1 + m < Y0 || o.y + st.y0 - m > Y0 + TL || o.x + st.x1 + m < X0 || o.x + st.x0 - m > X0 + TL) return;
      drawStroke(ctx, st, o.x, o.y);
    });
  }
  function staleRect(x0, y0, x1, y1) {
    const TL = UI.TL;
    UI.tiles.forEach((t) => { if (t.ix * TL <= x1 && (t.ix + 1) * TL >= x0 && t.iy * TL <= y1 && (t.iy + 1) * TL >= y0) t.stale = true; });
  }

  /* 획 그리기 — 「펜으로 쓴 것처럼」(3판).
     점과 점을 직선으로 잇지 않는다: 이웃한 두 점의 가운데에서 가운데로, 그 사이 점을 당김점으로 하는 곡선을 잇고(모서리가 서지 않는다),
     그 곡선을 화면 1.6 화소 길이로 잘게 나눠 굵기를 조금씩 바꿔 가며 그린다(구슬 꿴 듯한 마디가 없다).
     굵기 = 기본은 **고른 굵기**(직선으로 그을 때와 같은 선 — 써 본 뒤 「굵기가 달라지는 것보다 이게 낫다」). 「힘 · 빠르기에 따라」를 고르면
     압력(펜슬) 또는 빠르기(손가락 · 마우스 — 빠르면 가늘다)를 앞 점과 섞은 값. 쓰는 동안과 다시 그릴 때가 같은 식이다. */
  const penW = (w, p) => w * (0.4 + 1.2 * p);
  function widthsOf(pts, w) {
    const n = pts.length / 3, ws = new Array(n);
    for (let i = 0; i < n; i++) ws[i] = i ? ws[i - 1] * 0.55 + penW(w, pts[i * 3 + 2]) * 0.45 : penW(w, pts[2]);
    return ws;
  }
  function piece(ctx, ax, ay, cx, cy, bx, by, wa, wb) {
    const len = Math.hypot(cx - ax, cy - ay) + Math.hypot(bx - cx, by - cy);
    const k = Math.max(1, Math.min(96, Math.ceil(len / UI.step)));
    let px = ax, py = ay;
    for (let j = 1; j <= k; j++) {
      const t = j / k, u = 1 - t;
      const x = u * u * ax + 2 * u * t * cx + t * t * bx, y = u * u * ay + 2 * u * t * cy + t * t * by;
      ctx.lineWidth = wa + (wb - wa) * (t - 0.5 / k);
      ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(x, y); ctx.stroke();
      px = x; py = y;
    }
  }
  function hlPath(ctx, p, dx, dy) {                               // 형광펜 — 굵기가 고르니 한 번에 그려 이음매가 겹쳐 보이지 않게
    const n = p.length / 3;
    ctx.beginPath(); ctx.moveTo(p[0] + dx, p[1] + dy);
    for (let i = 1; i < n - 1; i++) ctx.quadraticCurveTo(p[i * 3] + dx, p[i * 3 + 1] + dy, (p[i * 3] + p[i * 3 + 3]) / 2 + dx, (p[i * 3 + 1] + p[i * 3 + 4]) / 2 + dy);
    ctx.lineTo(p[(n - 1) * 3] + dx, p[(n - 1) * 3 + 1] + dy);
    ctx.stroke();
  }
  function drawStroke(ctx, st, dx, dy) {
    const p = st.pts, n = p.length / 3;
    ctx.strokeStyle = ctx.fillStyle = st.c;
    ctx.lineJoin = "round";
    if (st.t === 1) {
      ctx.globalAlpha = 0.32; ctx.lineCap = "butt"; ctx.lineWidth = st.w;
      if (n === 1) { ctx.fillRect(p[0] + dx - st.w / 2, p[1] + dy - st.w / 2, st.w, st.w); } else hlPath(ctx, p, dx, dy);
      ctx.globalAlpha = 1;
      return;
    }
    ctx.globalAlpha = 1; ctx.lineCap = "round";
    const ws = st.ws;
    if (n === 1) { ctx.beginPath(); ctx.arc(p[0] + dx, p[1] + dy, Math.max(0.7, penW(st.w, p[2]) * 0.55), 0, 6.3); ctx.fill(); return; }
    let ax = p[0] + dx, ay = p[1] + dy, wa = ws[0];
    for (let i = 1; i < n - 1; i++) {
      const mx = (p[i * 3] + p[i * 3 + 3]) / 2 + dx, my = (p[i * 3 + 1] + p[i * 3 + 4]) / 2 + dy, wm = (ws[i] + ws[i + 1]) / 2;
      piece(ctx, ax, ay, p[i * 3] + dx, p[i * 3 + 1] + dy, mx, my, wa, wm);
      ax = mx; ay = my; wa = wm;
    }
    const lx = p[(n - 1) * 3] + dx, ly = p[(n - 1) * 3 + 1] + dy;
    piece(ctx, ax, ay, (ax + lx) / 2, (ay + ly) / 2, lx, ly, wa, n === 2 ? ws[1] : ws[n - 1]);
  }
  function runtime(sid, s) {
    const pts = unpack(s.d);
    let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
    for (let i = 0; i < pts.length; i += 3) {
      x0 = Math.min(x0, pts[i]); x1 = Math.max(x1, pts[i]); y0 = Math.min(y0, pts[i + 1]); y1 = Math.max(y1, pts[i + 1]);
    }
    const w = s.w || WIDTHS[2], t = s.t ? 1 : 0;
    return { id: sid, c: s.c || COLORS[0], w, t, b: s.b || "p", pts, x0, x1, y0, y1, ws: t ? null : widthsOf(pts, w) };
  }
  function rebuildRuntime() {
    UI.rt = {};
    Object.keys(UI.rec.doc.s).forEach((sid) => { UI.rt[sid] = runtime(sid, UI.rec.doc.s[sid]); });
  }
  function staleFor(st) {
    const o = org(st.b), m = (st.w || 16) + 12;
    staleRect(o.x + st.x0 - m, o.y + st.y0 - m, o.x + st.x1 + m, o.y + st.y1 + m);
  }

  /* 쓰는 중에만 쓰는 덧층 — 형광펜(한 획을 통째로 다시 그려야 고르다) · 직선 미리보기 · 펜 끝의 마지막 반 마디.
     화면 크기 한 장이고, 종이 좌표로 그릴 수 있게 변환을 걸어 둔다. */
  function sizeLive() {
    const c = UI.live, d = window.devicePixelRatio || 1;
    const w = Math.round(UI.el.clientWidth * d), h = Math.round(UI.el.clientHeight * d);
    if (c.width !== w || c.height !== h) { c.width = w; c.height = h; }
  }
  function liveCtx() {
    const c = UI.live, d = window.devicePixelRatio || 1, ctx = c.getContext("2d");
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, c.width, c.height);
    const lr = UI.layer.getBoundingClientRect(), er = UI.el.getBoundingClientRect(), sr = UI.scroll.getBoundingClientRect();
    ctx.save();
    ctx.beginPath(); ctx.rect((sr.left - er.left) * d, (sr.top - er.top) * d, sr.width * d, sr.height * d); ctx.clip();   // 도구 막대 위로 번지지 않게
    const s = lr.width / UI.SW;
    ctx.setTransform(d * s, 0, 0, d * s, d * (lr.left - er.left), d * (lr.top - er.top));
    return ctx;
  }
  function clearLive() { const c = UI.live, ctx = c.getContext("2d"); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, c.width, c.height); }

  /* 입력 — 펜 · 마우스는 쓰고, 손가락은 넘긴다(손가락 쓰기를 켜면 한 손가락 = 쓰기 · 두 손가락 = 넘기기). */
  function pt(e) {
    const r = UI.layer.getBoundingClientRect(), s = r.width / UI.SW;
    return [(e.clientX - r.left) / s, (e.clientY - r.top) / s];
  }
  function blockAt(x, y) {
    let best = "", by = -1;
    Object.keys(UI.geo).forEach((b) => {
      const o = UI.geo[b];
      if (hiddenBlock(b) || y < o.y || o.y <= by || x < o.hx - o.tol || x > o.hx + o.w + o.tol) return;
      by = o.y; best = b;
    });
    return best || (UI.geo.p ? "p" : UI.first);
  }
  // 손가락 · 마우스에는 압력이 없다 — 빠르기로 흉내 낸다(빠르면 가늘게), 앞 값과 섞어 튀지 않게
  function pressureOf(e, a, x, y) {
    if (UI.tool.even) return 0.5;                                // 고른 굵기 — 직선으로 그을 때와 같은 선
    if (e.pointerType === "pen" && e.pressure > 0) return e.pressure;
    if (!a) return 0.5;
    const n = a.pts.length, dt = Math.max(1, (e.timeStamp || 0) - a.lt), v = Math.hypot(x - a.pts[n - 3], y - a.pts[n - 2]) / dt;
    return a.pts[n - 1] * 0.7 + Math.max(0.22, Math.min(0.72, 0.72 - v * 0.35)) * 0.3;
  }
  function bindInput() {
    const L = UI.layer;
    // 펜슬이 화면을 끌지 않게(iPadOS 는 펜슬로도 스크롤한다) · 쓰는 동안 손바닥이 화면을 밀지 않게
    L.addEventListener("touchstart", (e) => {
      const stylus = [].some.call(e.changedTouches, (t) => t.touchType === "stylus");
      if (stylus || UI.tool.finger || UI.act || Date.now() - UI.lastPen < 500) e.preventDefault();
    }, { passive: false });
    L.addEventListener("pointerdown", (e) => {
      closePalette();
      if (e.pointerType === "touch" && !UI.tool.finger) return;
      if (e.pointerType === "mouse" && e.button !== 0) return;
      if (UI.act) {                                              // 손가락 쓰기 중 둘째 손가락 → 쓰던 획을 버리고 넘기기로
        if (e.pointerType === "touch" && UI.act.type === "touch") { cancelStroke(); UI.act = { pan: true, id: e.pointerId, y: e.clientY, x: e.clientX }; }
        return;
      }
      e.preventDefault();
      try { L.setPointerCapture(e.pointerId); } catch (_) { /* 무시 */ }
      const p = pt(e), b = blockAt(p[0], p[1]), o = org(b), st = liveStyle();
      const pr = !UI.tool.even && e.pointerType === "pen" && e.pressure > 0 ? e.pressure : 0.5;
      UI.act = { id: e.pointerId, type: e.pointerType, b, ox: o.x, oy: o.y, t0: Date.now(), lt: e.timeStamp || 0, cx: e.clientX, cy: e.clientY, moved: false,
                 st, pts: [p[0] - o.x, p[1] - o.y, pr], ws: [penW(st.w, pr)], mx: p[0], my: p[1], mw: penW(st.w, pr),
                 erase: UI.tool.kind === "erase", line: !!UI.tool.line, travel: 0, hx: p[0], hy: p[1], hold: 0 };
      if (e.pointerType === "pen") UI.lastPen = Date.now();
      if (UI.act.erase) { eraseAt(p); drawEraser(p); }
    });
    L.addEventListener("pointermove", (e) => {
      const a = UI.act;
      if (!a) { if (UI.tool.kind === "erase" && e.pointerType !== "touch") drawEraser(pt(e)); return; }   // 띄워서 움직일 때도 범위를 보인다
      if (e.pointerId !== a.id) return;
      e.preventDefault();
      if (a.pan) { if (UI.pinch) return; UI.scroll.scrollTop += a.y - e.clientY; UI.scroll.scrollLeft += a.x - e.clientX; a.y = e.clientY; a.x = e.clientX; return; }
      if (Math.abs(e.clientX - a.cx) + Math.abs(e.clientY - a.cy) > 4) a.moved = true;
      const evs = e.getCoalescedEvents ? e.getCoalescedEvents() : [];
      (evs.length ? evs : [e]).forEach((ev) => {
        const p = pt(ev);
        if (a.erase) return eraseAt(p);
        if (a.line) { a.ex = p[0] - a.ox; a.ey = p[1] - a.oy; return; }
        const n = a.pts.length, lx = a.pts[n - 3], ly = a.pts[n - 2], x = p[0] - a.ox, y = p[1] - a.oy;
        const d = Math.hypot(x - lx, y - ly);
        if (d < 0.35) return;
        const pr = pressureOf(ev, a, x, y);
        a.lt = ev.timeStamp || a.lt; a.travel += d;
        a.pts.push(x, y, pr);
        a.ws.push(a.ws[a.ws.length - 1] * 0.55 + penW(a.st.w, pr) * 0.45);
        const k = a.pts.length / 3;
        if (!a.st.t && k >= 3) {                                   // 가운데 → 가운데, 앞 점이 당김점
          const mx = (lx + x) / 2 + a.ox, my = (ly + y) / 2 + a.oy, mw = (a.ws[k - 2] + a.ws[k - 1]) / 2;
          inkPiece(a.st, a.mx, a.my, lx + a.ox, ly + a.oy, mx, my, a.mw, mw);
          a.mx = mx; a.my = my; a.mw = mw;
        }
        // 멈춰 있으면 직선으로 — 2.5 넘게 움직일 때마다 시계를 다시 건다
        if (Math.hypot(p[0] - a.hx, p[1] - a.hy) > 2.5) {
          a.hx = p[0]; a.hy = p[1];
          clearTimeout(a.hold); a.hold = setTimeout(() => holdToLine(a), 480);
        }
      });
      if (a.erase) drawEraser(pt(e)); else drawLive(a);
      if (e.pointerType === "pen") UI.lastPen = Date.now();
    });
    const end = (e) => {
      const a = UI.act;
      if (!a || e.pointerId !== a.id) return;
      UI.act = null;
      clearTimeout(a.hold);
      clearLive();
      if (a.pan || a.erase) { if (a.erase) flushErase(); return; }
      if (e.type === "pointercancel") { ensureStale(a); return; }
      if (!a.moved && Date.now() - a.t0 < 500) {                 // 톡 — 아래가 누르는 것(해설 펼치기 등)이면 그것을 누른다
        L.style.pointerEvents = "none";
        const under = document.elementFromPoint(e.clientX, e.clientY);
        L.style.pointerEvents = "";
        const hit = under && under.closest && under.closest(TAPPABLE);
        if (hit && UI.content.contains(hit)) { ensureStale(a); UI.tapAt = Date.now(); hit.click(); return; }
      }
      if (a.line && a.ex != null) {                               // 직선 — 처음과 끝 두 점만 남긴다
        const z = snapLine(a);
        a.pts = [a.pts[0], a.pts[1], 0.5, z[0], z[1], 0.5];
        return commitStroke(a, true);
      }
      const k = a.pts.length / 3;
      if (a.st.t) return commitStroke(a, true);                   // 형광펜은 덧층에만 그렸다 → 조각에 옮겨 그린다
      if (k === 1) return commitStroke(a, true);
      const lx = a.pts[(k - 1) * 3] + a.ox, ly = a.pts[(k - 1) * 3 + 1] + a.oy;
      inkPiece(a.st, a.mx, a.my, (a.mx + lx) / 2, (a.my + ly) / 2, lx, ly, a.mw, k === 2 ? a.ws[1] : a.ws[k - 1]);
      commitStroke(a, false);                                     // 쓰는 동안 그린 것이 곧 마지막 모양 — 다시 그리지 않는다
    };
    L.addEventListener("pointerleave", () => { if (!UI.act) clearLive(); });
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
  const TAPPABLE = "[data-pick], details.ink-ex > summary, [data-note-act], a[data-paper]";      // 종이에서 누를 수 있는 것은 이것뿐(정리본 안 단추는 누르지 않는다)
  function liveStyle() {
    const t = UI.tool;
    return t.kind === "hl" ? { c: t.hlColor, w: 16, t: 1 } : { c: t.color, w: t.width, t: 0 };
  }
  // 펜 획의 한 마디를 걸친 조각 캔버스마다 그린다(종이 좌표)
  function inkPiece(st, ax, ay, cx, cy, bx, by, wa, wb) {
    const pad = Math.max(wa, wb) + 1, TL = UI.TL;
    const x0 = Math.min(ax, cx, bx) - pad, x1 = Math.max(ax, cx, bx) + pad, y0 = Math.min(ay, cy, by) - pad, y1 = Math.max(ay, cy, by) + pad;
    UI.tiles.forEach((t) => {
      if (t.ix * TL > x1 || (t.ix + 1) * TL < x0 || t.iy * TL > y1 || (t.iy + 1) * TL < y0) return;
      const ctx = tileCtx(t);
      ctx.globalAlpha = 1; ctx.strokeStyle = st.c; ctx.lineCap = "round"; ctx.lineJoin = "round";
      piece(ctx, ax, ay, cx, cy, bx, by, wa, wb);
    });
  }
  /* 두 손가락 확대 · 축소(2026-11-15 「축소 · 확대를 하면 좋겠다」). 오므리고 벌리는 동안은 종이를 통째로 늘여 보이고(빠르다),
     손을 떼면 그 배율로 다시 배치해 글자와 필기를 선명하게 그린다. 두 손가락을 같이 끌면 넘기기도 된다. 펜을 쓰는 중 · 쓴 직후에는
     무시한다(손바닥). 마우스 · 트랙패드는 Ctrl + 휠. */
  function bindZoom() {
    const sc = UI.scroll;
    let gz = null, wheelT = 0, wz = null;
    const two = (e) => {
      const a = e.touches[0], b = e.touches[1];
      return { d: Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY) || 1, x: (a.clientX + b.clientX) / 2, y: (a.clientY + b.clientY) / 2 };
    };
    sc.addEventListener("touchstart", (e) => {
      if (e.touches.length !== 2 || !UI.rec || gz) return;
      if ([].some.call(e.touches, (t) => t.touchType === "stylus") || (UI.act && UI.act.type === "pen") || Date.now() - UI.lastPen < 700) return;
      const m = two(e), fr = UI.fit.getBoundingClientRect();
      gz = UI.pinch = { d0: m.d, z0: UI.zoom, lx: (m.x - fr.left) / UI.s, ly: (m.y - fr.top) / UI.s, x0: m.x, y0: m.y, x: m.x, y: m.y, k: 1 };
      UI.fit.style.transformOrigin = (m.x - fr.left) + "px " + (m.y - fr.top) + "px";
      if (e.cancelable) e.preventDefault();
    }, { passive: false });
    sc.addEventListener("touchmove", (e) => {
      if (!gz || e.touches.length < 2) return;
      if (e.cancelable) e.preventDefault();
      const m = two(e);
      gz.k = Math.max(ZMIN / gz.z0, Math.min(ZMAX / gz.z0, m.d / gz.d0));
      gz.x = m.x; gz.y = m.y;
      UI.fit.style.transform = `translate(${m.x - gz.x0}px, ${m.y - gz.y0}px) scale(${gz.k})`;
    }, { passive: false });
    const done = (e) => {
      if (!gz || e.touches.length >= 2) return;
      const p = gz;
      gz = UI.pinch = null;
      UI.fit.style.transform = ""; UI.fit.style.transformOrigin = "";
      zoomTo(p.z0 * p.k, p.lx, p.ly, p.x, p.y);
    };
    sc.addEventListener("touchend", done);
    sc.addEventListener("touchcancel", done);
    sc.addEventListener("wheel", (e) => {
      if (!e.ctrlKey || !UI.rec) return;
      e.preventDefault();
      const fr = UI.fit.getBoundingClientRect();
      if (!wz) wz = { z: UI.zoom, lx: (e.clientX - fr.left) / UI.s, ly: (e.clientY - fr.top) / UI.s };
      wz.z = Math.max(ZMIN, Math.min(ZMAX, wz.z * Math.exp(-e.deltaY * 0.01)));
      wz.x = e.clientX; wz.y = e.clientY;
      cancelAnimationFrame(wheelT);
      wheelT = requestAnimationFrame(() => { const p = wz; wz = null; zoomTo(p.z, p.lx, p.ly, p.x, p.y); });
    }, { passive: false });
  }
  // 수평 · 수직에 가까우면(약 4도) 딱 맞춘다
  function snapLine(a) {
    let dx = a.ex - a.pts[0], dy = a.ey - a.pts[1];
    if (Math.abs(dy) < Math.abs(dx) * 0.07) dy = 0; else if (Math.abs(dx) < Math.abs(dy) * 0.07) dx = 0;
    return [a.pts[0] + dx, a.pts[1] + dy];
  }
  function holdToLine(a) {
    if (UI.act !== a || a.line || a.erase || a.travel < 24) return;
    const n = a.pts.length;
    a.line = true; a.ex = a.pts[n - 3]; a.ey = a.pts[n - 2];
    ensureStale(a);                                               // 지금까지 그린 굽은 선을 지운다
    drawLive(a);
    status("직선으로 폈습니다");
  }
  function drawLive(a) {
    const ctx = liveCtx(), st = a.st;
    ctx.strokeStyle = st.c; ctx.lineJoin = "round";
    if (a.line) {
      if (a.ex == null) { ctx.restore(); return; }
      const z = snapLine(a);
      ctx.globalAlpha = st.t ? 0.32 : 1; ctx.lineCap = st.t ? "butt" : "round"; ctx.lineWidth = st.t ? st.w : penW(st.w, 0.5);
      ctx.beginPath(); ctx.moveTo(a.pts[0] + a.ox, a.pts[1] + a.oy); ctx.lineTo(z[0] + a.ox, z[1] + a.oy); ctx.stroke();
    } else if (st.t) {
      ctx.globalAlpha = 0.32; ctx.lineCap = "butt"; ctx.lineWidth = st.w;
      if (a.pts.length > 3) hlPath(ctx, a.pts, a.ox, a.oy);
    } else {                                                      // 펜 끝 — 마지막 가운데 점에서 지금 점까지(다음 점이 오면 조각에 제대로 그려진다)
      const n = a.pts.length;
      ctx.globalAlpha = 1; ctx.lineCap = "round"; ctx.lineWidth = a.ws[a.ws.length - 1];
      ctx.beginPath(); ctx.moveTo(a.mx, a.my); ctx.lineTo(a.pts[n - 3] + a.ox, a.pts[n - 2] + a.oy); ctx.stroke();
    }
    ctx.restore();
  }
  function ensureStale(a) {                                       // 버린 획의 흔적을 지운다
    let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
    for (let i = 0; i < a.pts.length; i += 3) {
      x0 = Math.min(x0, a.pts[i]); x1 = Math.max(x1, a.pts[i]); y0 = Math.min(y0, a.pts[i + 1]); y1 = Math.max(y1, a.pts[i + 1]);
    }
    if (a.ex != null) { x0 = Math.min(x0, a.ex); x1 = Math.max(x1, a.ex); y0 = Math.min(y0, a.ey); y1 = Math.max(y1, a.ey); }
    staleFor({ b: a.b, w: a.st.w, x0, x1, y0, y1 }); ensureTiles();
  }
  function cancelStroke() { if (UI.act && UI.act.pts) { clearTimeout(UI.act.hold); clearLive(); ensureStale(UI.act); } }
  function newId() { return device().slice(-8) + "-" + Date.now().toString(36) + "-" + Math.floor(Math.random() * 46656).toString(36); }
  function commitStroke(a, repaint) {
    const st = a.st, sid = newId();
    UI.rec.doc.s[sid] = { c: st.c, w: st.w, t: st.t, b: a.b, d: pack(a.pts) };
    UI.rt[sid] = runtime(sid, UI.rec.doc.s[sid]);
    UI.mine[sid] = 1;
    UI.undo.push({ add: sid });
    if (repaint) staleFor(UI.rt[sid]);
    // 여백 끝 가까이까지 썼으면 종이를 늘인다
    const pg = UI.geo.p;
    if (a.b === "p" && pg && UI.rt[sid].y1 > pg.h - 160) { UI.rec.doc.ph = Math.max(UI.rec.doc.ph, Math.round(pg.h)) + PAPER_STEP; layout(false); }
    else if (repaint) ensureTiles();
    touched(); paintBar();
  }
  // 지우개 — 지나간 길(앞 점 → 지금 점)을 촘촘히 나눠, 획의 **선분**까지의 거리로 판정한다(획의 점만 보면 빨리 그은 획을 놓친다).
  function segDist(px, py, ax, ay, bx, by) {
    const dx = bx - ax, dy = by - ay, L = dx * dx + dy * dy;
    const t = L ? Math.max(0, Math.min(1, ((px - ax) * dx + (py - ay) * dy) / L)) : 0;
    return Math.hypot(px - ax - t * dx, py - ay - t * dy);
  }
  const ERASE_R = 9;                                              // 지우개 반지름(종이 좌표) — 화면에 보이는 원과 같은 값
  function drawEraser(p) {
    const ctx = liveCtx();
    ctx.beginPath(); ctx.arc(p[0], p[1], ERASE_R, 0, 6.3);
    ctx.fillStyle = "rgba(120,130,145,.18)"; ctx.fill();
    ctx.lineWidth = 1 / (UI.s || 1); ctx.strokeStyle = "rgba(60,70,85,.8)"; ctx.stroke();
    ctx.restore();
  }
  function eraseAt(p) {
    const R = ERASE_R, from = UI.erasePrev || p;
    UI.erasePrev = p;
    const steps = Math.max(1, Math.ceil(Math.hypot(p[0] - from[0], p[1] - from[1]) / (R / 2)));
    for (let k = 1; k <= steps; k++) {
      const ex = from[0] + (p[0] - from[0]) * k / steps, ey = from[1] + (p[1] - from[1]) * k / steps;
      Object.keys(UI.rt).forEach((sid) => {
        const st = UI.rt[sid];
        if (hiddenBlock(st.b) || veiled(sid)) return;
        const o = org(st.b), x = ex - o.x, y = ey - o.y, r = R + st.w / 2;
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
    ensureSnap();
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
    const res = await syncRec(rec, () => {
      if (UI.rec !== rec) return;
      rebuildRuntime();
      ensureSnap();
      // 다른 기기가 필기본을 새 판으로 옮겼으면 종이의 글부터 다시 그린다
      if (UI.st.kind === "concept" && ((rec.doc.n && rec.doc.n.at) || "") !== UI.st.snapAt) return renderSheet(false);
      layout(false); UI.tiles.forEach((t) => { t.stale = true; }); ensureTiles();
    });
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
    UI.st = { exam, id, kind: isC ? "concept" : "q", q, w, solve: !!opts.solve && !!q, chosen, quiz: !!opts.quiz,
      live: isC ? liveConcept(id) : null, old: false, list: isC && Array.isArray(opts.list) ? opts.list : null };
    if (ensureSnap()) saveRec(UI.rec);
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
      const cid = b.getAttribute("data-ink-concept");
      b.textContent = conceptLabel(cid);
      b.classList.toggle("has", hasCopy(cid));
    });
    const sh = document.getElementById("inkShelf");
    if (sh && !sh.classList.contains("hidden")) renderShelf();
  }
  async function close() {
    if (!UI.el || UI.el.classList.contains("hidden")) return;
    await leave();
    dropTiles();
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

  /* 필기 모음 — 필기가 있는 것 전부(이 기기 색인 + 다른 기기에서 올린 것).
     2026-11-15 2차(「한꺼번에 있으면 구분하기 힘들다」): 종류(KMLE · USMLE · 정리본 · 논문)로 먼저 나누고 그 안에서 분야별로 묶는다.
     KMLE · USMLE 는 **틀린 문항**(지금 오답노트에 있는 것)과 **맞힌 문항**(그 밖)을 따로 본다.
     논문 칸은 펜 필기가 아니라 논문 화면에서 적은 메모다(이 기기에 저장된 것 — papers-app.js 의 medkos_paper_notes).
     영상 · 변형 문항 칸은 필기가 있을 때만 보인다. */
  const KIND_NAME = { kmle: "KMLE", usmle: "USMLE", imaging: "영상", variant: "변형", concept: "정리본", paper: "논문" };
  const TABS = ["kmle", "usmle", "concept", "paper", "imaging", "variant"], ALWAYS = 4;      // 앞의 넷은 비어 있어도 보인다
  const ALLV = { tab: "", sub: "wrong" };
  function paperNotes() {
    try {
      const o = JSON.parse(localStorage.getItem("medkos_paper_notes") || "{}") || {};
      return Object.keys(o).filter((k) => o[k] && o[k].text).map((k) => ({ id: k, text: String(o[k].text), updated: String(o[k].updated || "") }));
    } catch (e) { return []; }
  }
  // 논문 제목 · 분야는 papers.js(2.5 MB)에 있다 — 논문 칸을 열 때만 읽는다
  function needPapers(done) {
    if (Array.isArray(window.PAPERS) || needPapers.failed) return done();
    if (needPapers.busy) return;
    needPapers.busy = true;
    const s = document.createElement("script");
    s.src = "papers.js";
    s.onload = () => { needPapers.busy = false; done(); };
    s.onerror = () => { needPapers.busy = false; needPapers.failed = true; done(); };
    document.head.appendChild(s);
  }
  const fieldName = (t) => BOOKS[t] || t || "기타";                // 분야 이름 — 학습서의 책 이름과 같게
  function allItems() {
    const idx = loadIdx(), items = {};
    Object.keys(idx).forEach((k) => { items[k] = { n: idx[k] }; });
    EXAMS.forEach((ex) => Object.keys(NET.remote[ex] || {}).forEach((f) => {
      const k = keyOf(ex, unfid(ex, f));
      (items[k] = items[k] || { n: 0 }).remote = true;
    }));
    return Object.keys(items).map((k) => {
      const i = k.indexOf(":"), ex = k.slice(0, i), id = k.slice(i + 1);
      if (ex === "concept") {
        const c = liveConcept(id);
        return { ex, id, n: items[k].n, title: c ? c.title : id, group: fieldName(c && c.topic), wrong: false };
      }
      const q = findQuestion(id);
      return { ex, id, n: items[k].n, title: q ? (q.question || q.vignette || "").trim().slice(0, 90) : "(문항 은행에 없음)",
               group: fieldName(q && (q.subject || q.topic)), wrong: !!wrongEntry(ex, id) };
    });
  }
  function showAll() {
    let el = document.getElementById("inkList");
    if (!el) {
      el = document.createElement("div");
      el.id = "inkList"; el.className = "ink-list hidden";
      el.innerHTML = `<section class="card"><h2>필기 모음 <span id="inkListCount" class="muted"></span></h2>
        <div class="row"><button data-a="back">← 돌아가기</button><span id="inkTabs"></span></div>
        <div class="row" id="inkSubs"></div><div id="inkListBody"></div></section>`;
      document.body.appendChild(el);
      el.addEventListener("click", (e) => {
        const b = e.target.closest("button");
        if (!b) return;
        if (b.getAttribute("data-a") === "back") return el.classList.add("hidden");
        if (b.hasAttribute("data-tab")) { ALLV.tab = b.getAttribute("data-tab"); ALLV.sub = "wrong"; ALLV.picked = false; return renderAll(); }
        if (b.hasAttribute("data-sub")) { ALLV.sub = b.getAttribute("data-sub"); ALLV.picked = true; return renderAll(); }
        if (b.hasAttribute("data-open")) open(b.getAttribute("data-ex"), b.getAttribute("data-open"));
      });
    }
    document.body.appendChild(el);                                // 학습서 목록 위에 뜨게 맨 위 층으로
    el.classList.remove("hidden");
    renderAll();
    EXAMS.forEach((ex) => {
      const before = JSON.stringify(NET.remote[ex] || {});
      refreshRemote(ex).then((files) => { if (JSON.stringify(files) !== before && !el.classList.contains("hidden")) renderAll(); });
    });
  }
  function renderAll() {
    const el = document.getElementById("inkList");
    if (!el) return;
    const items = allItems(), notes = paperNotes();
    const count = (t) => (t === "paper" ? notes.length : items.filter((x) => x.ex === t).length);
    const tabs = TABS.filter((t, i) => i < ALWAYS || count(t));
    if (tabs.indexOf(ALLV.tab) < 0) ALLV.tab = tabs.filter(count)[0] || tabs[0];
    const tab = ALLV.tab, chip = (attr, v, text, on) => `<button type="button" class="chip${on ? " on" : ""}" ${attr}="${v}">${esc(text)}</button>`;
    document.getElementById("inkListCount").textContent = `(${items.length + notes.length}개)`;
    document.getElementById("inkTabs").innerHTML = tabs.map((t) => chip("data-tab", t, `${KIND_NAME[t]} ${count(t)}`, t === tab)).join("");
    let rows = items.filter((x) => x.ex === tab), subs = "";
    if (tab === "kmle" || tab === "usmle") {
      const w = rows.filter((x) => x.wrong).length, r = rows.length - w;
      if (!ALLV.picked) ALLV.sub = !w && r ? "right" : "wrong";   // 고르지 않았으면 필기가 있는 쪽을 먼저
      subs = chip("data-sub", "wrong", `틀린 문항 ${w}`, ALLV.sub === "wrong") + chip("data-sub", "right", `맞힌 문항 ${r}`, ALLV.sub === "right")
        + `<span class="muted small">틀린 문항 = 지금 오답노트에 있는 문항</span>`;
      rows = rows.filter((x) => x.wrong === (ALLV.sub === "wrong"));
    }
    document.getElementById("inkSubs").innerHTML = subs;
    const body = document.getElementById("inkListBody");
    const grouped = (list, rowHtml) => {
      const by = {};
      list.forEach((x) => { (by[x.group] = by[x.group] || []).push(x); });
      return Object.keys(by).sort((a, b) => a.localeCompare(b, "ko")).map((gname) =>
        `<details open><summary>${esc(gname)} <span class="muted small">${by[gname].length}개</span></summary>${by[gname].map(rowHtml).join("")}</details>`).join("");
    };
    if (tab === "paper") {
      if (!notes.length) { body.innerHTML = `<p class="muted">논문에 적은 메모가 없습니다. 논문 화면에서 「💡 내 생각 / 아이디어」에 적으면 여기 모입니다(이 기기에 저장된 메모).</p>`; return; }
      if (!Array.isArray(window.PAPERS) && !needPapers.failed) {
        body.innerHTML = `<p class="muted">논문 목록을 불러오는 중…</p>`;
        return needPapers(() => { if (!el.classList.contains("hidden") && ALLV.tab === "paper") renderAll(); });
      }
      const byId = {};
      (window.PAPERS || []).forEach((p) => { byId[p.id] = p; });
      const list = notes.map((nt) => { const p = byId[nt.id] || {}; return Object.assign({ p, group: fieldName(p.topic) }, nt); })
        .sort((a, b) => b.updated.localeCompare(a.updated));
      body.innerHTML = grouped(list, (x) => `<div class="w"><div class="wmeta"><b>${esc(x.p.title || x.id)}</b></div>
          <div class="whead muted">${esc([x.p.journal, x.p.pubdate].filter(Boolean).join(" · "))}</div>
          <div class="ink-memo">${esc(x.text.length > 300 ? x.text.slice(0, 300) + "…" : x.text)}</div>
          <a class="ink-open-btn has" href="papers.html?id=${encodeURIComponent(x.id)}">📄 논문에서 열기</a></div>`);
      return;
    }
    rows.sort((a, b) => (a.id < b.id ? 1 : -1));
    body.innerHTML = rows.length ? grouped(rows, (x) => `<div class="w"><div class="whead">${x.ex === "concept" ? "" : "#" + esc(x.id)}</div>
        <div class="wmeta">${esc(x.title)}</div>
        <button data-open="${esc(x.id)}" data-ex="${esc(x.ex)}" class="ink-open-btn has">✍ 열기${x.n ? ` (${x.n}획)` : " ☁"}</button></div>`)
      : `<p class="muted">${tab === "concept" ? "필기한 정리본이 없습니다. 「📖 학습서 필기」에서 정리본을 열어 쓰면 여기 모입니다."
        : (tab === "kmle" || tab === "usmle") && items.some((x) => x.ex === tab) ? "이쪽에는 필기한 문항이 없습니다."
        : "필기한 문항이 없습니다. 오답노트의 「✍ 필기」, 문항 화면의 「✍ 펜으로 풀기」에서 쓰면 여기 모입니다."}</p>`;
  }
  // 개념 정리본 머리에 필기 단추(learn.js 의 renderConcept 가 부른다 — 필기장 안에서 그릴 때는 부르지 않는다)
  function conceptButton(box, cid) {
    const head = box.querySelector(".cn-h");
    if (!head || head.querySelector("[data-ink-concept]")) return;
    const b = document.createElement("button");
    b.type = "button"; b.className = "small ink-open-btn"; b.setAttribute("data-ink-concept", cid);
    b.textContent = conceptLabel(cid);
    b.classList.toggle("has", hasCopy(cid));
    b.onclick = () => open("concept", cid);
    head.appendChild(b);
  }
  const hasCopy = (cid) => !!loadIdx()[keyOf("concept", cid)];
  function conceptLabel(cid) {
    const n = loadIdx()[keyOf("concept", cid)] || 0, sx = loadSnapIdx()[cid], live = liveConcept(cid);
    return "✍ 이 정리본에 필기" + (n ? ` (${n}획)` : "") + (n && sx != null && live && sx !== sigOf(live) ? " · 고쳐짐" : "");
  }

  /* 학습서 필기(2026-11-15) — 과별 학습서의 단위(개념 정리본)를 책처럼 과목별로 늘어놓고, 눌러서 그 위에 쓴다.
     종이는 늘 최신 정리본이고 필기는 그 위에 남는다(「내 필기본」 구분 없음 — 여러 번 볼 것이라 필기 유무로 나눌 까닭이 없다).
     필기한 뒤에 고쳐진 정리본에만 「고쳐짐」을 붙인다. PDF 에 직접 쓰지 않는 까닭: 학습서 PDF 는 매일 다시 만들어져 쪽이 밀리고,
     드라이브 쪽 파일을 고치면 「필기 보호」로 새 판이 안 올라온다. 과목 → 책 이름은 pipelines/books_config.yaml 의 books 와 같아야 한다. */
  const BOOKS = {"Internal Medicine": "내과 총론", "Cardiology": "순환기내과", "Pulmonology": "호흡기내과", "Gastroenterology": "소화기내과", "Nephrology": "신장내과", "Endocrinology": "내분비내과", "Hematology": "혈액종양내과", "Hematology-Oncology": "혈액종양내과", "Infectious Disease": "감염내과", "Rheumatology": "류마티스내과", "Allergy": "알레르기내과", "Neurology": "신경과", "Psychiatry": "정신건강의학과", "Pediatrics": "소아청소년과", "Obstetrics & Gynecology": "산부인과", "Obstetrics and Gynecology": "산부인과", "General Surgery": "외과", "Surgery": "외과", "Orthopedics": "정형외과", "Dermatology": "피부과", "Ophthalmology": "안과", "Emergency Medicine": "응급의학과", "Otorhinolaryngology": "이비인후과", "ENT": "이비인후과", "Urology": "비뇨의학과", "Preventive Medicine": "예방의학", "Epidemiology": "예방의학", "Biochemistry": "기초의학", "Physiology": "기초의학", "Pathology": "기초의학", "Pharmacology": "기초의학", "Microbiology": "기초의학", "Immunology": "기초의학"};
  const SHELF = { open: {}, q: "" };
  function shelfRows() {
    const all = window.MEDKOS_CONCEPTS || {}, idx = loadIdx(), sx = loadSnapIdx(), rem = NET.remote.concept || {};
    return Object.keys(all).map((id) => {
      const c = all[id], n = idx[keyOf("concept", id)] || 0;
      return { id, c, n, cloud: !n && rem[id] != null, stale: n > 0 && sx[id] != null && sx[id] !== sigOf(c), book: BOOKS[c.topic] || c.topic || "기타" };
    });
  }
  function showShelf() {
    let el = document.getElementById("inkShelf");
    if (!el) {
      el = document.createElement("div");
      el.id = "inkShelf"; el.className = "ink-list ink-shelf hidden";
      el.innerHTML = `<section class="card"><h2>학습서 필기 <span id="inkShelfCount" class="muted"></span></h2>
        <p class="muted small">정리본은 늘 최신판으로 열리고, 필기는 그 위에 그대로 남습니다. 필기한 뒤에 고쳐진 정리본에는 「고쳐짐」이 붙고,
          열면 무엇이 바뀌었는지 알려 줍니다.</p>
        <div class="row"><button data-a="back">← 돌아가기</button>
          <button data-a="all" title="필기가 있는 문항 · 정리본 전부">✍ 필기 모음</button>
          <input id="inkShelfQ" type="search" placeholder="제목으로 찾기" autocomplete="off" /></div>
        <div id="inkShelfBody"></div></section>`;
      document.body.appendChild(el);
      el.addEventListener("click", (e) => {
        const b = e.target.closest("button");
        if (!b) return;
        if (b.getAttribute("data-a") === "back") return el.classList.add("hidden");
        if (b.getAttribute("data-a") === "all") return showAll();
        if (b.hasAttribute("data-open")) {
          const grp = b.closest("details");
          const list = [].map.call((grp || el).querySelectorAll("button[data-open]"), (x) => x.getAttribute("data-open"));
          open("concept", b.getAttribute("data-open"), { list });
        }
      });
      el.addEventListener("toggle", (e) => { const d = e.target; if (d && d.hasAttribute && d.hasAttribute("data-book")) SHELF.open[d.getAttribute("data-book")] = d.open; }, true);
      el.querySelector("#inkShelfQ").addEventListener("input", (e) => { SHELF.q = e.target.value.trim().toLowerCase(); renderShelf(); });
    }
    el.classList.remove("hidden");
    renderShelf();
    const before = JSON.stringify(NET.remote.concept || {});
    refreshRemote("concept").then((files) => { if (JSON.stringify(files) !== before && !el.classList.contains("hidden")) renderShelf(); });
  }
  function renderShelf() {
    const rows = shelfRows();
    document.getElementById("inkShelfCount").textContent = `(정리본 ${rows.length}개)`;
    const show = rows.filter((r) => !SHELF.q || (r.c.title + " " + (r.c.condition || "") + " " + r.book).toLowerCase().indexOf(SHELF.q) >= 0);
    const by = {};
    show.forEach((r) => { (by[r.book] = by[r.book] || []).push(r); });
    const names = Object.keys(by).sort((a, b) => a.localeCompare(b, "ko"));
    document.getElementById("inkShelfBody").innerHTML = names.length ? names.map((bk) => {
      const rs = by[bk].sort((a, b) => String(a.c.title).localeCompare(String(b.c.title), "ko"));
      const s = rs.filter((r) => r.stale).length;
      return `<details data-book="${esc(bk)}"${SHELF.q || SHELF.open[bk] ? " open" : ""}><summary>${esc(bk)} <span class="muted small">${rs.length}개`
        + (s ? ` · 고쳐짐 ${s}` : "") + `</span></summary>`
        + rs.map((r) => `<div class="w"><div class="wmeta"><b>${esc(r.c.title)}</b>${r.stale ? `<span class="ink-badge">고쳐짐</span>` : ""}</div>
          <div class="whead muted">${esc(r.c.objectiveKind || "")} · ${esc(verText(r.c.version || 1, r.c.updated))}</div>
          <button data-open="${esc(r.id)}" class="ink-open-btn${r.n || r.cloud ? " has" : ""}">✍ 열기${r.n ? ` (${r.n}획)` : r.cloud ? " ☁" : ""}</button></div>`).join("")
        + `</details>`;
    }).join("") : `<p class="muted">${SHELF.q ? "조건에 맞는 정리본이 없습니다." : "정리본을 불러오지 못했습니다."}</p>`;
  }
  // 문항 화면의 「✍ 펜으로 풀기」 · 첫 화면의 「✍ 필기 모음」 — 앱 껍데기(index.html)를 건드리지 않고 여기서 끼운다.
  function addButtons() {
    const quit = document.getElementById("quitBtn"), vw = document.getElementById("viewWrongBtn");
    if (quit && !document.getElementById("inkSolveBtn")) {
      const b = document.createElement("button");
      b.id = "inkSolveBtn"; b.textContent = "✍ 펜으로 풀기"; b.onclick = openFromQuiz;
      quit.parentNode.insertBefore(b, quit);
    }
    const link = document.getElementById("syncLinkBtn");          // 첫 화면 「동기화 설정」에도 로그인 단추
    if (link && !document.getElementById("inkLoginBtn")) {
      const b = document.createElement("button");
      b.id = "inkLoginBtn"; b.type = "button"; b.className = "small"; b.textContent = "🔑 로그인"; b.onclick = () => openLogin();
      link.parentNode.insertBefore(b, link);
      const o = document.createElement("button");
      o.id = "inkLogoutBtn"; o.type = "button"; o.className = "small"; o.textContent = "로그아웃"; o.onclick = logout;
      link.parentNode.insertBefore(o, link);
    }
    // 메뉴 줄 맨 위의 「📖 학습서 필기」(2026-11-15) — 이 화면에서는 새로 읽지 않고 바로 연다. 「✍ 필기 모음」은 그 안의 단추다
    // (사용자 「학습서 필기도 맨 위로 · 들어간 다음에 필기 모음」 — 첫 화면 단추 줄에는 필기 단추를 두지 않는다).
    const nav = document.getElementById("navShelf");
    if (nav && !nav.getAttribute("data-bound")) {
      nav.setAttribute("data-bound", "1");
      nav.addEventListener("click", (e) => { e.preventDefault(); showShelf(); });
    }
  }
  addButtons();
  gateIfNeeded();
  try {                                                          // 다른 화면의 메뉴 줄에서 넘어왔다(ink = 예전 주소)
    const view = new URLSearchParams(location.search).get("view");
    if (view === "shelf" || view === "ink") showShelf();
    if (view === "ink") showAll();
  } catch (e) { /* 주소를 못 읽으면 그냥 둔다 */ }

  window.addEventListener("online", () => { flushAll(); });
  setTimeout(flushAll, 5000);

  return Object.assign(core, { open, close, decorate, flushAll, showAll, showShelf, conceptButton, openFromQuiz, openLogin, loginTry, _net: NET });      // _net = 시험용(서버 유무 판정을 되돌릴 때)
})();
if (typeof module !== "undefined" && module.exports) module.exports = MEDKOS_INK;
