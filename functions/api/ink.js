/* Cloudflare Pages Function — 오답노트 필기 동기화 (/api/ink)   (2026-11-15)
 *
 * 왜: 문항 · 개념 정리본에 쓴 손필기(아이패드 펜슬)는 그 기기 브라우저에만 남는다. 이 함수가 필기를 저장소의
 * **별도 가지 `ink-data`** 에 `state/ink_sync/<exam>/<문항 id>.json` 으로 커밋해 기기끼리 같은 필기를 보게 한다.
 *
 * 무엇을 저장하나: **암호문만.** 저장소가 공개라서 필기는 기기에서 동기화 키로 잠근 뒤(AES-GCM · docs/ink.js) 올라온다.
 * 이 함수는 봉투(envelope)를 열지 못하고, 모양 · 크기만 검사해 그대로 둔다. 그래서 병합도 기기가 한다 —
 * 기기는 받은 sha 를 같이 보내고, 그사이 다른 기기가 고쳤으면 409 를 돌려받아 다시 받아 합친 뒤 재시도한다.
 *
 * 왜 별도 가지인가: ① main 에 커밋하면 루틴들의 푸시가 「main 이 움직였다」로 자주 거절된다 ② main 푸시마다 도는
 * 배포 · 워크플로를 깨우지 않는다 ③ 암호문은 git 이 압축하지 못해 main 을 받는 쪽이 무거워진다.
 * 가지는 첫 저장 때 부모 없는 커밋으로 만든다(README 한 장). 커밋 글머리 `[CF-Pages-Skip]` = Cloudflare Pages 미리보기 빌드 생략.
 *
 * 환경변수는 /api/wrong 과 같다(GITHUB_TOKEN 필수 · GITHUB_REPO · SYNC_KEY) + INK_BRANCH(선택, 기본 "ink-data").
 *
 * 프로토콜(JSON):
 *   GET  /api/ink?exam=kmle            → { exam, files: { "<id>": "<sha>" } }      가지 · 폴더가 없으면 files = {}
 *   GET  /api/ink?exam=kmle&id=<id>    → { exam, id, sha, env }                    없으면 404
 *   POST /api/ink { exam, id, sha|null, env, device }
 *        → 200 { exam, id, sha }  |  409 { conflict: true }(sha 가 낡음 — 다시 받아 합쳐서 재시도)
 * env(봉투) = { v:1, alg:"A256GCM", z:0|1, iv:"<base64>", ct:"<base64>", n:<획 수>, updated:"<iso>" } */

const EXAMS = new Set(["kmle", "usmle", "imaging", "variant", "concept", "meta"]);   // 문항 넷 + 개념 정리본 + meta(로그인 확인용 암호문 login-check)
const ID_RE = /^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$/;
const B64_RE = /^[A-Za-z0-9+/]+={0,2}$/;
const MAX_BODY = 1536 * 1024;                       // 봉투 한 장 상한(GitHub contents API 여유 안)
const SKIP = "[CF-Pages-Skip] ";

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}
function repoOf(env) { return env.GITHUB_REPO || "ehdbddl06001-ui/my-github-test"; }
function branchOf(env) { return env.INK_BRANCH || "ink-data"; }
function dirPath(exam) { return `state/ink_sync/${exam}`; }
function filePath(exam, id) { return `${dirPath(exam)}/${id}.json`; }

function ghHeaders(env) {
  return {
    authorization: `Bearer ${env.GITHUB_TOKEN}`,
    accept: "application/vnd.github+json",
    "user-agent": "medkos-ink-sync",
    "x-github-api-version": "2022-11-28",
    "content-type": "application/json",
  };
}
function authorized(request, env) {
  if (!env.SYNC_KEY) return true;
  return request.headers.get("x-sync-key") === env.SYNC_KEY;
}
function b64encode(str) { return btoa(unescape(encodeURIComponent(str))); }
function b64decode(b64) { return decodeURIComponent(escape(atob(String(b64 || "").replace(/\n/g, "")))); }

/* 봉투 모양 검사 — 열지는 못하지만 「암호문이 아닌 것」이 저장소에 들어가지 않게 한다. 통과하면 저장할 필드만 추린 사본. */
export function cleanEnvelope(env) {
  if (!env || typeof env !== "object") return null;
  if (env.v !== 1 || env.alg !== "A256GCM") return null;
  if (typeof env.iv !== "string" || !B64_RE.test(env.iv) || env.iv.length > 32) return null;
  if (typeof env.ct !== "string" || !B64_RE.test(env.ct) || env.ct.length < 24) return null;
  return {
    v: 1, alg: "A256GCM", z: env.z ? 1 : 0, iv: env.iv, ct: env.ct,
    n: Number.isFinite(env.n) ? Math.max(0, Math.floor(env.n)) : 0,
    updated: typeof env.updated === "string" ? env.updated.slice(0, 40) : "",
  };
}
export function validTarget(exam, id) { return EXAMS.has(exam) && ID_RE.test(String(id || "")); }

async function gh(env, method, path, body) {
  const r = await fetch(`https://api.github.com/repos/${repoOf(env)}/${path}`, {
    method, headers: ghHeaders(env), body: body ? JSON.stringify(body) : undefined,
  });
  let data = null;
  try { data = await r.json(); } catch (e) { data = null; }
  return { status: r.status, ok: r.ok, data };
}

/* 가지가 없으면 부모 없는 커밋(README 한 장)으로 만든다. 이미 있으면(422) 그대로 둔다. */
async function ensureBranch(env) {
  const br = branchOf(env);
  const ref = await gh(env, "GET", `git/ref/heads/${encodeURIComponent(br)}`);
  if (ref.ok) return true;
  if (ref.status !== 404) throw new Error(`가지 확인 실패 ${ref.status}`);
  const readme = "# MedKOS 오답노트 필기(동기화 자료)\n\n"
    + "이 가지에는 `/api/ink` 가 올리는 필기 **암호문**만 있다(`state/ink_sync/<exam>/<문항 id>.json`).\n"
    + "기기의 동기화 키로만 열 수 있다. 손으로 고치지 않는다 · main 에 병합하지 않는다.\n";
  const tree = await gh(env, "POST", "git/trees", { tree: [{ path: "README.md", mode: "100644", type: "blob", content: readme }] });
  if (!tree.ok) throw new Error(`가지 만들기 실패(tree ${tree.status})`);
  const commit = await gh(env, "POST", "git/commits", { message: SKIP + "필기 동기화 가지 시작", tree: tree.data.sha, parents: [] });
  if (!commit.ok) throw new Error(`가지 만들기 실패(commit ${commit.status})`);
  const made = await gh(env, "POST", "git/refs", { ref: `refs/heads/${br}`, sha: commit.data.sha });
  if (!made.ok && made.status !== 422) throw new Error(`가지 만들기 실패(ref ${made.status})`);
  return true;
}

export async function onRequestGet({ request, env }) {
  if (!env.GITHUB_TOKEN) return json({ error: "GITHUB_TOKEN 이 설정되지 않았습니다." }, 503);
  if (!authorized(request, env)) return json({ error: "X-Sync-Key 불일치" }, 401);
  const p = new URL(request.url).searchParams;
  const exam = p.get("exam") || "", id = p.get("id") || "";
  if (!EXAMS.has(exam)) return json({ error: "exam 은 kmle|usmle|imaging|variant|concept" }, 400);
  const br = encodeURIComponent(branchOf(env));
  try {
    if (!id) {                                                    // 목록 — 어느 문항에 필기가 있고 어느 판인지
      const r = await gh(env, "GET", `contents/${dirPath(exam)}?ref=${br}`);
      if (r.status === 404) return json({ exam, files: {} });
      if (!r.ok || !Array.isArray(r.data)) return json({ error: `목록 실패 ${r.status}` }, 502);
      const files = {};
      r.data.forEach((f) => { if (f && f.type === "file" && /\.json$/.test(f.name)) files[f.name.slice(0, -5)] = f.sha; });
      return json({ exam, files });
    }
    if (!ID_RE.test(id)) return json({ error: "id 형식" }, 400);
    const r = await gh(env, "GET", `contents/${filePath(exam, id)}?ref=${br}`);
    if (r.status === 404) return json({ error: "없음" }, 404);
    if (!r.ok) return json({ error: `읽기 실패 ${r.status}` }, 502);
    let envl = null;
    try { envl = cleanEnvelope(JSON.parse(b64decode(r.data.content))); } catch (e) { envl = null; }
    if (!envl) return json({ error: "저장본이 깨졌습니다" }, 502);
    return json({ exam, id, sha: r.data.sha, env: envl });
  } catch (e) {
    return json({ error: String(e.message || e) }, 502);
  }
}

export async function onRequestPost({ request, env }) {
  if (!env.GITHUB_TOKEN) return json({ error: "GITHUB_TOKEN 이 설정되지 않았습니다." }, 503);
  if (!authorized(request, env)) return json({ error: "X-Sync-Key 불일치" }, 401);
  if (Number(request.headers.get("content-length") || 0) > MAX_BODY) return json({ error: "본문이 너무 큽니다" }, 413);
  let text;
  try { text = await request.text(); } catch (e) { return json({ error: "본문 필요" }, 400); }
  if (text.length > MAX_BODY) return json({ error: "본문이 너무 큽니다" }, 413);
  let body;
  try { body = JSON.parse(text); } catch (e) { return json({ error: "JSON 본문 필요" }, 400); }
  const exam = body && body.exam, id = body && body.id;
  if (!validTarget(exam, id)) return json({ error: "exam · id 형식" }, 400);
  const envl = cleanEnvelope(body.env);
  if (!envl) return json({ error: "봉투 형식(암호문만 받습니다)" }, 400);
  const device = String(body.device || "web").replace(/[^A-Za-z0-9._-]/g, "").slice(0, 24) || "web";
  const payload = {
    message: `${SKIP}필기 동기화: ${exam}/${id} (${envl.n}획 · ${device})`,
    content: b64encode(JSON.stringify(envl)),
    branch: branchOf(env),
  };
  if (body.sha) payload.sha = String(body.sha);
  try {
    let r = await gh(env, "PUT", `contents/${filePath(exam, id)}`, payload);
    if (r.status === 404) {                                       // 가지가 아직 없다 → 만들고 한 번 더
      await ensureBranch(env);
      r = await gh(env, "PUT", `contents/${filePath(exam, id)}`, payload);
    }
    // 409 = sha 가 낡음 · 422 = sha 없이 이미 있는 파일을 쓰려 함 → 둘 다 「다른 기기가 먼저 썼다」
    if (r.status === 409 || r.status === 422) return json({ conflict: true }, 409);
    if (!r.ok) return json({ error: `쓰기 실패 ${r.status}` }, 502);
    return json({ exam, id, sha: r.data && r.data.content && r.data.content.sha });
  } catch (e) {
    return json({ error: String(e.message || e) }, 502);
  }
}
