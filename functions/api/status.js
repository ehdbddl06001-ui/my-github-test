/* Cloudflare Pages Function — 동기화 상태 (/api/status), 2026-09-23
 *
 * 왜: 동기화 키가 없거나 틀린 기기는 예전에는 상태 줄 한 칸에 작게 「실패」가 뜰 뿐이었고, 학습 기록 쪽은
 * 아무 표시 없이 재시도만 반복했다. 앱이 켜질 때 이 함수에 한 번 물어 「이 기기의 키가 맞는가」를 알고,
 * 틀리면 첫 화면에 경고를 띄운다(docs/app.js checkSyncAuth).
 *
 *   GET /api/status → { server, keyRequired, keySent, keyOk }
 * 키 값은 절대 돌려주지 않는다 — 「키가 필요한가 / 보낸 키가 맞는가」만 알린다. 데이터도 읽지 않는다. */

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}

export function syncStatus(env, sentKey) {
  const keyRequired = Boolean(env && env.SYNC_KEY);
  const sent = String(sentKey || "");
  return {
    server: Boolean(env && env.GITHUB_TOKEN),
    keyRequired,
    keySent: sent.length > 0,
    keyOk: !keyRequired || sent === env.SYNC_KEY,
  };
}

export async function onRequestGet({ request, env }) {
  return json(syncStatus(env, request.headers.get("x-sync-key")));
}
