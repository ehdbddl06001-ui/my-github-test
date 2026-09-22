/* /api/* 공통 미들웨어 — 옛 주소(GitHub Pages)에서 연 앱도 이 서버로 동기화할 수 있게 CORS 를 연다.
 *
 * 왜(2026-09-22): 아이패드 홈 화면 앱이 예전 주소 ehdbddl06001-ui.github.io 로 설치돼 있어
 * 「이 주소에는 동기화 서버가 없습니다」가 뜨고 오답·학습 기록이 기기 안에만 쌓였다. 브라우저 저장소는
 * 주소별로 따로라 새 주소로 옮겨 오지도 않는다. 그래서 옛 주소의 앱이 이 서버(pages.dev)의 /api 를
 * 직접 부르게 하고(docs/learn.js 의 API_BASE), 여기서 그 출처 하나만 허용한다.
 * 허용 출처는 아래 목록뿐이다. 동기화 키(SYNC_KEY)를 쓰면 그 검사는 각 함수가 그대로 한다. */
export const ALLOWED_ORIGINS = new Set(["https://ehdbddl06001-ui.github.io"]);

export function corsHeaders(origin) {
  return {
    "access-control-allow-origin": origin,
    "access-control-allow-methods": "GET, POST, OPTIONS",
    "access-control-allow-headers": "content-type, x-sync-key",
    "access-control-max-age": "86400",
    vary: "Origin",
  };
}

export async function onRequest(ctx) {
  const origin = ctx.request.headers.get("origin") || "";
  const allowed = ALLOWED_ORIGINS.has(origin);
  if (ctx.request.method === "OPTIONS") {
    return new Response(null, { status: allowed ? 204 : 403, headers: allowed ? corsHeaders(origin) : {} });
  }
  const res = await ctx.next();
  if (!allowed) return res;
  const out = new Response(res.body, res);
  for (const [k, v] of Object.entries(corsHeaders(origin))) out.headers.set(k, v);
  return out;
}
