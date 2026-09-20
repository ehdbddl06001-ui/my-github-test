/* Workers 로 배포할 때의 진입점 — 정적 사이트(docs/)와 동기화 API 를 한 Worker 가 맡는다.
 *
 * 왜 있나: Cloudflare 대시보드의 「저장소 가져오기(Workers Builds)」 흐름은 `npx wrangler deploy` 를 실행하므로
 * wrangler 설정과 진입점이 필요하다. Pages 흐름(Connect to Git → 빌드 출력 디렉터리 docs)으로 배포하면
 * 이 파일은 쓰이지 않고 `functions/api/*.js` 가 그대로 Pages Functions 이 된다.
 *
 * 규칙: 함수 본체는 `functions/api/` 한 곳에만 둔다. 여기서는 경로만 이어 준다 — 같은 코드를 두 벌로 만들지 않는다.
 * 정적 자산에 있는 경로는 Worker 를 거치지 않고 바로 서비스되고, 없는 경로(/api/…)만 여기로 온다.
 */
import { onRequestGet as wrongGet, onRequestPost as wrongPost } from "../functions/api/wrong.js";
import { onRequestPost as learningPost } from "../functions/api/learning.js";

const ROUTES = {
  "/api/wrong": { GET: wrongGet, POST: wrongPost },
  "/api/learning": { POST: learningPost },
};

export default {
  async fetch(request, env, ctx) {
    const path = new URL(request.url).pathname.replace(/\/+$/, "") || "/";
    const route = ROUTES[path];
    if (route) {
      const handler = route[request.method];
      if (!handler) {
        return new Response(JSON.stringify({ error: `${request.method} 는 이 경로에서 쓰지 않는다` }), {
          status: 405,
          headers: { "content-type": "application/json; charset=utf-8", allow: Object.keys(route).join(", ") },
        });
      }
      return handler({ request, env, ctx });
    }
    return env.ASSETS.fetch(request);      // 나머지는 docs/ 의 정적 파일
  },
};
