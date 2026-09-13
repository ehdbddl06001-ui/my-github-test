/* Cloudflare Pages Function — 오답노트 동기화 (/api/wrong)
 *
 * 왜: 웹 퀴즈의 오답은 브라우저 localStorage 에만 남아 핸드폰과 PC 가 따로 논다. 이 함수가
 * 오답을 GitHub 저장소 `state/wrong_sync/<exam>.json` 에 커밋해 두 기기가 같은 오답노트를
 * 보게 하고, GitHub Actions(wrong-sync.yml)가 그 JSON 을 사람이 읽는 오답노트 .md 로 만든다.
 *
 * 배포: Cloudflare Pages 프로젝트(빌드 출력 = docs/)에 이 저장소를 연결하면 `functions/` 가
 * 자동으로 함수가 된다. 대시보드 ▸ Settings ▸ Environment variables 에 아래를 넣는다.
 *   GITHUB_TOKEN  (Secret, 필수) — 이 저장소 Contents: Read and write 권한의 fine-grained PAT
 *   GITHUB_REPO   (선택) 기본 "ehdbddl06001-ui/my-github-test"
 *   GITHUB_BRANCH (선택) 기본 "main"
 *   SYNC_KEY      (선택) 있으면 요청 헤더 X-Sync-Key 가 같아야 한다(Access 를 안 켰을 때의 최소 잠금)
 * 사이트 전체를 Cloudflare Access 로 잠그면 이 함수도 같이 잠긴다(권장).
 *
 * 프로토콜(같은 출처, JSON):
 *   GET  /api/wrong?exam=kmle            → { exam, items:{id:entry}, removed:{id:iso}, updated }
 *   POST /api/wrong  { exam, device, items, removed }
 *        → 서버가 저장본과 합집합(삭제 시각이 기록 시각보다 뒤면 삭제 우선) → 커밋 → 합친 결과 반환
 * GitHub Pages 처럼 함수가 없는 호스트에서는 404 가 나고, app.js 는 조용히 로컬 모드로 남는다. */

const EXAMS = new Set(["kmle", "usmle", "imaging"]);
const MAX_BODY = 2 * 1024 * 1024;

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}

function b64encodeUtf8(str) {
  const bytes = new TextEncoder().encode(str);
  let bin = "";
  for (let i = 0; i < bytes.length; i += 0x8000) {
    bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  }
  return btoa(bin);
}
function b64decodeUtf8(b64) {
  const bin = atob(b64.replace(/\n/g, ""));
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return new TextDecoder().decode(bytes);
}

function ghHeaders(env) {
  return {
    authorization: `Bearer ${env.GITHUB_TOKEN}`,
    accept: "application/vnd.github+json",
    "user-agent": "medkos-wrong-sync",
    "x-github-api-version": "2022-11-28",
  };
}

function filePath(exam) { return `state/wrong_sync/${exam}.json`; }

async function readState(env, exam) {
  const repo = env.GITHUB_REPO || "ehdbddl06001-ui/my-github-test";
  const branch = env.GITHUB_BRANCH || "main";
  const url = `https://api.github.com/repos/${repo}/contents/${filePath(exam)}?ref=${encodeURIComponent(branch)}`;
  const r = await fetch(url, { headers: ghHeaders(env) });
  if (r.status === 404) return { sha: null, data: { exam, items: {}, removed: {}, updated: "" } };
  if (!r.ok) throw new Error(`GitHub 읽기 실패 ${r.status}: ${await r.text()}`);
  const body = await r.json();
  let data;
  try { data = JSON.parse(b64decodeUtf8(body.content || "")); }
  catch (e) { data = { exam, items: {}, removed: {}, updated: "" }; }
  data.items = data.items || {};
  data.removed = data.removed || {};
  return { sha: body.sha, data };
}

async function writeState(env, exam, data, sha, device) {
  const repo = env.GITHUB_REPO || "ehdbddl06001-ui/my-github-test";
  const branch = env.GITHUB_BRANCH || "main";
  const url = `https://api.github.com/repos/${repo}/contents/${filePath(exam)}`;
  const payload = {
    message: `오답 동기화: ${exam} (${Object.keys(data.items).length}개 · ${device || "web"})`,
    content: b64encodeUtf8(JSON.stringify(data, null, 1)),
    branch,
  };
  if (sha) payload.sha = sha;
  const r = await fetch(url, { method: "PUT", headers: { ...ghHeaders(env), "content-type": "application/json" }, body: JSON.stringify(payload) });
  if (!r.ok) throw new Error(`GitHub 쓰기 실패 ${r.status}: ${await r.text()}`);
  return r.json();
}

/* 합집합 병합. 같은 id 는 date(기록일)가 늦은 쪽, 삭제 시각이 기록일보다 뒤면 삭제가 이긴다. */
function merge(server, client) {
  const items = { ...server.items };
  const removed = { ...server.removed };
  for (const [id, when] of Object.entries(client.removed || {})) {
    if (!removed[id] || removed[id] < when) removed[id] = when;
  }
  for (const [id, entry] of Object.entries(client.items || {})) {
    if (!entry || typeof entry !== "object") continue;
    const cur = items[id];
    if (!cur || String(cur.date || "") <= String(entry.date || "")) items[id] = entry;
  }
  for (const [id, when] of Object.entries(removed)) {
    const it = items[id];
    if (it && String(it.date || "") <= String(when).slice(0, 10)) delete items[id];
  }
  return { items, removed };
}

function authorized(request, env) {
  if (!env.SYNC_KEY) return true;
  return request.headers.get("x-sync-key") === env.SYNC_KEY;
}

export async function onRequestGet({ request, env }) {
  if (!env.GITHUB_TOKEN) return json({ error: "GITHUB_TOKEN 이 설정되지 않았습니다 (Cloudflare Pages ▸ Settings ▸ Environment variables)." }, 503);
  if (!authorized(request, env)) return json({ error: "X-Sync-Key 불일치" }, 401);
  const exam = new URL(request.url).searchParams.get("exam") || "";
  if (!EXAMS.has(exam)) return json({ error: "exam 은 kmle|usmle|imaging" }, 400);
  try {
    const { data } = await readState(env, exam);
    return json(data);
  } catch (e) {
    return json({ error: String(e.message || e) }, 502);
  }
}

export async function onRequestPost({ request, env }) {
  if (!env.GITHUB_TOKEN) return json({ error: "GITHUB_TOKEN 이 설정되지 않았습니다." }, 503);
  if (!authorized(request, env)) return json({ error: "X-Sync-Key 불일치" }, 401);
  const len = Number(request.headers.get("content-length") || 0);
  if (len > MAX_BODY) return json({ error: "본문이 너무 큽니다" }, 413);
  let body;
  try { body = await request.json(); } catch (e) { return json({ error: "JSON 본문 필요" }, 400); }
  const exam = body && body.exam;
  if (!EXAMS.has(exam)) return json({ error: "exam 은 kmle|usmle|imaging" }, 400);

  // 충돌(다른 기기가 방금 커밋) 시 한 번 다시 읽어 재시도한다.
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const { sha, data } = await readState(env, exam);
      const merged = merge(data, body);
      const next = { exam, ...merged, updated: new Date().toISOString() };
      const unchanged = JSON.stringify(merged) === JSON.stringify({ items: data.items, removed: data.removed });
      if (!unchanged) await writeState(env, exam, next, sha, body.device);
      return json({ ...next, committed: !unchanged });
    } catch (e) {
      if (attempt === 1 || !/409|422/.test(String(e.message))) return json({ error: String(e.message || e) }, 502);
    }
  }
  return json({ error: "동기화 실패" }, 502);
}
