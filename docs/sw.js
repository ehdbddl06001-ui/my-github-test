/* MedKOS PWA service worker
   - 앱 껍데기(html/css/js)는 network-first: 새 배포가 바로 반영되고, 오프라인이면 캐시.
   - 문항 번들(questions*.js, search-index.js 등 큰 데이터)도 network-first(시간 제한 있음):
     v3 까지는 stale-while-revalidate 라 「이번 방문」은 지난 방문 때 캐시한 번들을 보여 주고 새 번들은
     다음 방문에야 나왔다(2026-09-15 실측: 핸드폰은 하루 두 번 열어 보이고, 노트북은 하루 한 번 열어
     늘 하루 전 세트가 보임). 지금은 네트워크가 되면 최신 번들을 바로 쓰고, 느리거나 오프라인이면 캐시.
     서버가 ETag/304 로 답하므로 바뀌지 않은 번들은 실제로 다시 받지 않는다.
   - 영상·아이콘(assets/, icons/)은 cache-first: 내용이 바뀌지 않는 파일이다.
   - /api/ (Cloudflare Pages Functions, 오답 동기화)는 캐시하지 않는다.
   경로는 전부 상대경로라 GitHub Pages(/my-github-test/)와 Cloudflare Pages(/) 어디서든 같다. */
"use strict";

const VERSION = "medkos-v15";
const DATA_TIMEOUT_MS = 8000;   // 이 시간 안에 네트워크 응답이 없으면 캐시로 먼저 보여 준다
const SHELL = [
  "./", "./index.html", "./style.css", "./app.js", "./learn.js", "./synckey.js", "./pwa.js", "./manifest.webmanifest",
  "./papers.html", "./papers-app.js", "./ailab.html", "./ailab-app.js",
  "./anatomy.html", "./anatomy.css", "./anatomy-app.js",
  "./search.html", "./search-app.js", "./whatsnew.html", "./whatsnew-app.js",
  "./icons/icon-192.png", "./icons/icon-512.png",
];
const DATA_RE = /\/(questions[^/]*\.js|search-index\.js|papers\.js|ailab\.js|anatomy-data\.js|diagrams-data\.js|concepts\.js)$/;
const IMMUTABLE_RE = /\/(assets|icons)\//;

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(VERSION)
      .then((c) => Promise.allSettled(SHELL.map((u) => c.add(u))))   // 하나 실패해도 설치는 진행
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("message", (e) => {
  if (e.data && e.data.type === "SKIP_WAITING") self.skipWaiting();
});

async function notifyClients(msg) {
  const list = await self.clients.matchAll({ includeUncontrolled: true, type: "window" });
  list.forEach((c) => c.postMessage(msg));
}

async function networkFirst(req) {
  const cache = await caches.open(VERSION);
  try {
    const res = await fetch(req);
    if (res && res.ok) cache.put(req, res.clone());
    return res;
  } catch (err) {
    const hit = await cache.match(req, { ignoreSearch: true });
    if (hit) return hit;
    if (req.mode === "navigate") {
      const idx = await cache.match("./index.html");
      if (idx) return idx;
    }
    throw err;
  }
}

async function cacheFirst(req) {
  const cache = await caches.open(VERSION);
  const hit = await cache.match(req);
  if (hit) return hit;
  const res = await fetch(req);
  if (res && res.ok) cache.put(req, res.clone());
  return res;
}

/* 문항 번들: network-first + 시간 제한.
   네트워크가 제때 답하면 그 응답(최신)을 쓰고 캐시를 갱신한다. 시간 안에 못 오거나 실패하면 캐시를 준다.
   시간 초과 뒤 늦게 도착한 응답도 캐시에 넣고, 캐시와 달라졌으면 페이지에 알려 「새 자료」 토스트를 띄운다. */
async function networkFirstData(req) {
  const cache = await caches.open(VERSION);
  const hit = await cache.match(req);
  let timer = null;
  const update = fetch(req).then(async (res) => {
    if (!res || !res.ok) return null;
    const fresh = res.clone();
    if (hit) {
      const a = hit.headers.get("etag") || hit.headers.get("content-length");
      const b = fresh.headers.get("etag") || fresh.headers.get("content-length");
      if (a !== b) notifyClients({ type: "DATA_UPDATED", url: req.url });
    }
    await cache.put(req, fresh);
    return res;
  }).catch(() => null);
  if (!hit) return (await update) || Response.error();
  const timeout = new Promise((resolve) => { timer = setTimeout(() => resolve(null), DATA_TIMEOUT_MS); });
  const res = await Promise.race([update, timeout]);
  if (timer) clearTimeout(timer);
  return res || hit;
}

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname.includes("/api/")) return;              // 오답 동기화 API — 캐시 금지
  if (DATA_RE.test(url.pathname)) { e.respondWith(networkFirstData(req)); return; }
  if (IMMUTABLE_RE.test(url.pathname)) { e.respondWith(cacheFirst(req)); return; }
  e.respondWith(networkFirst(req));
});
