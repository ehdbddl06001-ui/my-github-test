/* Cloudflare Pages Function — 학습 기록 동기화 (/api/learning)
 *
 * 왜: 오답 뒤 학습 흐름(docs/learn.js)의 기록은 브라우저 localStorage 에 **덧붙이기만** 한다. 이 함수가 그 기록을
 * GitHub 저장소 `state/learning_sync/events.json` 에 합쳐 두면, 핸드폰·PC 가 같은 복습 목록을 보고
 * 매일 도는 과별 PDF 학습서(.github/workflows/books.yml)가 그 기록으로 단원을 고른다.
 *
 * 병합 규칙: 사건 id(eid) 합집합. **서버는 어떤 기록도 고치거나 지우지 않는다**(기록 덮어쓰기 금지).
 * 설정은 functions/api/wrong.js 와 같다(GITHUB_TOKEN·GITHUB_REPO·GITHUB_BRANCH·SYNC_KEY — Cloudflare 대시보드에만).
 * 토큰은 이 서버 함수 안에서만 쓰이고 브라우저로 나가지 않는다.
 *
 *   POST /api/learning { device, events:[{eid, kind, t, ...}] } → { events:[합친 전체], committed }
 * GitHub Pages 처럼 함수가 없는 호스트에서는 404 → learn.js 는 로컬 기록 + 내보내기(.json)로 남는다. */

const MAX_BODY = 4 * 1024 * 1024;
const PATH = "state/learning_sync/events.json";
const KINDS = new Set(["answer", "view", "check", "understood", "later", "flag", "reason", "memo"]);

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}
function b64encodeUtf8(str) {
  const bytes = new TextEncoder().encode(str);
  let bin = "";
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  return btoa(bin);
}
function b64decodeUtf8(b64) {
  const bin = atob(b64.replace(/\n/g, ""));
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return new TextDecoder().decode(bytes);
}
function ghHeaders(env) {
  return { authorization: `Bearer ${env.GITHUB_TOKEN}`, accept: "application/vnd.github+json",
    "user-agent": "medkos-learning-sync", "x-github-api-version": "2022-11-28" };
}
function repo(env) { return env.GITHUB_REPO || "ehdbddl06001-ui/my-github-test"; }
function branch(env) { return env.GITHUB_BRANCH || "main"; }

async function readState(env) {
  const r = await fetch(`https://api.github.com/repos/${repo(env)}/contents/${PATH}?ref=${encodeURIComponent(branch(env))}`, { headers: ghHeaders(env) });
  if (r.status === 404) return { sha: null, events: [] };
  if (!r.ok) throw new Error(`GitHub 읽기 실패 ${r.status}`);
  const body = await r.json();
  let data = {};
  // 1MB 넘는 파일은 contents API 가 content 를 비워 준다 → download_url 로 읽는다
  if (body.content) data = JSON.parse(b64decodeUtf8(body.content));
  else if (body.download_url) data = await (await fetch(body.download_url, { headers: ghHeaders(env) })).json();
  return { sha: body.sha, events: Array.isArray(data.events) ? data.events : [] };
}

function valid(e) {
  return e && typeof e === "object" && typeof e.eid === "string" && e.eid.length <= 80
    && KINDS.has(e.kind) && typeof e.t === "string" && JSON.stringify(e).length <= 4000;
}

export async function onRequestPost({ request, env }) {
  if (!env.GITHUB_TOKEN) return json({ error: "GITHUB_TOKEN 이 설정되지 않았습니다." }, 503);
  if (env.SYNC_KEY && request.headers.get("x-sync-key") !== env.SYNC_KEY) return json({ error: "X-Sync-Key 불일치" }, 401);
  if (Number(request.headers.get("content-length") || 0) > MAX_BODY) return json({ error: "본문이 너무 큽니다" }, 413);
  let body;
  try { body = await request.json(); } catch (e) { return json({ error: "JSON 본문 필요" }, 400); }
  const incoming = Array.isArray(body && body.events) ? body.events.filter(valid) : [];
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const { sha, events } = await readState(env);
      const seen = new Set(events.map((e) => e.eid));
      const add = incoming.filter((e) => !seen.has(e.eid));
      const merged = events.concat(add).sort((a, b) => String(a.t).localeCompare(String(b.t)));
      if (add.length) {
        const payload = {
          message: `학습 기록 동기화: +${add.length}건 (${String(body.device || "web").slice(0, 40)})`,
          content: b64encodeUtf8(JSON.stringify({ format: "medkos-learning-events/1", updated: new Date().toISOString(), events: merged }, null, 0)),
          branch: branch(env),
        };
        if (sha) payload.sha = sha;
        const r = await fetch(`https://api.github.com/repos/${repo(env)}/contents/${PATH}`,
          { method: "PUT", headers: { ...ghHeaders(env), "content-type": "application/json" }, body: JSON.stringify(payload) });
        if (!r.ok) throw new Error(`GitHub 쓰기 실패 ${r.status}`);
      }
      return json({ events: merged, committed: add.length > 0 });
    } catch (e) {
      if (attempt === 1 || !/409|422/.test(String(e.message))) return json({ error: String(e.message || e) }, 502);
    }
  }
  return json({ error: "동기화 실패" }, 502);
}
