/* MedKOS 오답노트 필기 — 펜슬로 쓰고, 기기끼리 맞춘다 (2026-11-15)

   왜: 오답노트는 자동으로 쌓이지만 「왜 틀렸나」를 손으로 풀어 쓰는 자리가 없었다(글 메모 한 줄뿐).
   오답 하나마다 필기장을 연다 — 위에 문항 · 내 답 · 정답 · 해설(접힘), 아래에 줄 여백. 그 위 어디에든 쓴다.

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
  function emptyDoc() { return { v: 1, ph: PAPER0, s: {}, g: {}, u: "" }; }
  function normDoc(d) {
    const o = d && typeof d === "object" ? d : {};
    return {
      v: 1, ph: Math.max(PAPER0, Math.min(60000, Number(o.ph) || PAPER0)),
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
    return { v: 1, ph: Math.max(a.ph, b.ph), s, g, u: a.u > b.u ? a.u : b.u };
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
    const r = await fetch(`${NET.url}?exam=${encodeURIComponent(exam)}&id=${encodeURIComponent(id)}`, { headers: headers() });
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
          body: JSON.stringify({ exam: rec.exam, id: rec.id, sha: rec.sha, env: await seal(rec.doc, pass()), device: device() }),
        });
        if (noServer(r.status)) { NET.available = false; return "local"; }
        if (r.status === 409) continue;                                   // 다른 기기가 먼저 올렸다 → 다시 받아 합친다
        if (!r.ok) throw new Error(r.status === 401 ? "동기화 키가 맞지 않습니다" : "올리기 실패 " + r.status);
        const out = await r.json();
        rec.sha = out.sha || rec.sha;
        rec.dirty = JSON.stringify(rec.doc) !== sent;                     // 올리는 사이에 더 썼으면 아직 남았다
        await saveRec(rec);
        (NET.remote[rec.exam] = NET.remote[rec.exam] || {})[rec.id] = rec.sha;
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
    tool: loadTool(), undo: [], saveT: null, pushT: null, raf: 0, lastPen: 0, act: null, dirtyTiles: null,
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
    const lists = ["KMLE", "USMLE", "IMAGING"].map(g).filter(Array.isArray);
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
  function sheetHtml(exam, id, q, w) {
    const lab = labels(q, w);
    const head = `<div class="ink-h">#${esc(id)}<span>${esc((q && q.subject) || (w && w.subject) || "")}${w && w.date ? " · 틀린 날 " + esc(w.date) : ""}</span></div>`;
    let qb = head, ob = "", eb = "";
    if (q) {
      const fig = g("figureHtml"), data = g("dataBox");
      qb += (q.vignette || "").trim() ? `<div class="ink-vig">${esc(q.vignette.trim())}</div>` : "";
      try { qb += (typeof fig === "function" ? fig(q) : "") + (typeof data === "function" ? data(q) : ""); } catch (e) { /* 그림 없이 */ }
      qb += (q.question || "").trim() ? `<div class="ink-q">Q. ${esc(q.question.trim())}</div>` : "";
      ob = (q.options || []).map((o, i) => {
        const mine = w && w.chosen === i, ans = q.answer - 1 === i;
        return `<div class="ink-opt${ans ? " ans" : ""}${mine && !ans ? " mine" : ""}"><span class="num">${lab[i] || i + 1}</span><span class="t">${esc(o)}</span>`
          + `${ans ? '<span class="tg">정답</span>' : ""}${mine ? '<span class="tg">내 선택</span>' : ""}</div>`;
      }).join("");
      eb = explHtml(q);
    } else if (w) {                                   // 문항 은행에서 빠진 옛 오답 — 오답노트에 남은 것만 보인다
      qb += `<div class="ink-q">Q. ${esc(w.question || "")}</div>`;
      ob = `<div class="ink-opt mine"><span class="num">${lab[w.chosen] || ""}</span><span class="t">${esc(w.chosenText || "")}</span><span class="tg">내 선택</span></div>`
        + `<div class="ink-opt ans"><span class="num">${lab[w.answer] || ""}</span><span class="t">${esc(w.answerText || "")}</span><span class="tg">정답</span></div>`;
      eb = w.coreNote ? `<div class="expl-item"><span class="k">핵심</span>${esc(w.coreNote)}</div>` : "";
    }
    if (w && w.note) ob += `<div class="ink-memo">✍ ${esc(w.note)}</div>`;
    return `<div class="ink-block" data-b="q">${qb}</div><div class="ink-block" data-b="o">${ob}</div>`
      + (eb ? `<details class="ink-block ink-ex" data-b="e"><summary>해설 펼치기</summary><div class="ink-exb explanation">${eb}</div></details>` : "")
      + `<div class="ink-block ink-paper" data-b="p"><span class="ink-ph">여기부터 내 필기 — 왜 틀렸나 · 다음에 볼 단서</span></div>`;
  }

  function build() {
    if (UI.el) return;
    const el = document.createElement("div");
    el.id = "inkOverlay"; el.className = "ink-ov hidden";
    el.innerHTML = `<div class="ink-bar">
        <button data-a="close" class="ink-x">← 오답노트</button>
        <span class="ink-tools">
          ${COLORS.map((c) => `<button data-a="color" data-c="${c}" class="ink-dot" style="--c:${c}" aria-label="펜 색"></button>`).join("")}
          <button data-a="width" title="굵기">굵기</button>
          <button data-a="hl">형광펜</button>
          <button data-a="erase">지우개</button>
          <button data-a="undo">↶</button>
          <button data-a="finger" title="손가락으로도 쓰기 — 켜면 두 손가락으로 넘긴다">☝ 손가락 쓰기</button>
          <button data-a="zout" aria-label="작게">−</button><button data-a="zin" aria-label="크게">＋</button>
          <button data-a="more">여백 ＋</button>
        </span>
        <span class="ink-st" id="inkStatus"></span>
      </div>
      <div class="ink-scroll"><div class="ink-fit"><div class="ink-sheet"><div class="ink-content"></div><div class="ink-layer"></div></div></div></div>`;
    document.body.appendChild(el);
    UI.el = el;
    UI.scroll = el.querySelector(".ink-scroll"); UI.fit = el.querySelector(".ink-fit"); UI.sheet = el.querySelector(".ink-sheet");
    UI.content = el.querySelector(".ink-content"); UI.layer = el.querySelector(".ink-layer");
    el.querySelector(".ink-bar").addEventListener("click", onBar);
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
    UI.tops = {};
    UI.content.querySelectorAll(".ink-block").forEach((b) => { UI.tops[b.getAttribute("data-b")] = b.offsetTop; });
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
  function hiddenBlock(b) {
    if (!(b in UI.tops)) return true;
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
      if (hiddenBlock(st.b)) return;
      const top = UI.tops[st.b];
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
    if (!(st.b in UI.tops)) return;
    const top = UI.tops[st.b];
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
        const hit = under && under.closest && under.closest("summary,a,button");
        if (hit && UI.content.contains(hit)) { ensureStale(a); hit.click(); return; }
      }
      commitStroke(a);
    };
    L.addEventListener("pointerup", end);
    L.addEventListener("pointercancel", end);
  }
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
        if (hiddenBlock(st.b)) return;
        const x = ex, y = ey - UI.tops[st.b], r = R + st.w / 2;
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
    else { const sid = newId(); UI.rec.doc.s[sid] = op.del; UI.rt[sid] = runtime(sid, op.del); staleFor(UI.rt[sid]); }   // 묘비가 있으니 새 id 로 되살린다
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

  async function open(exam, id) {
    build();
    const q = findQuestion(id), w = wrongEntry(exam, id);
    UI.rec = await loadRec(exam, id);
    UI.undo = []; UI.zoom = 1;
    UI.content.innerHTML = sheetHtml(exam, id, q, w);
    UI.content.querySelectorAll("img").forEach((im) => im.addEventListener("load", () => layout(false)));
    const d = UI.content.querySelector("details.ink-ex");
    if (d) d.addEventListener("toggle", () => { d.querySelector("summary").textContent = d.open ? "해설 접기" : "해설 펼치기"; layout(false); UI.tiles.forEach((t) => { t.stale = true; }); ensureTiles(); });
    UI.el.classList.remove("hidden"); document.body.classList.add("ink-open");
    UI.scroll.scrollTop = 0;
    rebuildRuntime(); paintBar(); layout(true);
    status(countStrokes(UI.rec.doc) ? "기기에 저장된 필기" : "");
    pushNow();                                                    // 열면서 서버 것과 맞춘다(다른 기기에서 쓴 것 받기)
  }
  async function close() {
    if (!UI.rec) return;
    await flushLocal();
    const rec = UI.rec;
    const relist = () => { const l = document.getElementById("wbList"); if (l && !UI.rec) decorate(l); };
    pushNow(rec).then(() => { relist(); if (rec.dirty) flushAll(); });
    UI.rec = null; UI.act = null;
    UI.tiles.forEach(dropTile);
    UI.el.classList.add("hidden"); document.body.classList.remove("ink-open");
    const list = document.getElementById("wbList");
    if (list) decorate(list);
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
      const n = idx[keyOf(ex, id)] || 0, remote = (NET.remote[ex] || {})[id];
      b.textContent = n ? `✍ 필기 (${n}획)` : remote ? "✍ 필기 ☁" : "✍ 필기";
      b.classList.toggle("has", !!(n || remote));
      exams[ex] = true;
    });
    Object.keys(exams).forEach((ex) => {
      const before = JSON.stringify(NET.remote[ex] || {});
      refreshRemote(ex).then((files) => { if (JSON.stringify(files) !== before && document.body.contains(list)) decorate(list); });
    });
  }

  window.addEventListener("online", () => { flushAll(); });
  setTimeout(flushAll, 5000);

  return Object.assign(core, { open, close, decorate, flushAll, _net: NET });      // _net = 시험용(서버 유무 판정을 되돌릴 때)
})();
if (typeof module !== "undefined" && module.exports) module.exports = MEDKOS_INK;
