/* MedKOS 동기화 키 — 기기 연결 링크(2026-09-23)

   왜: 동기화 키는 기기·브라우저·주소마다 따로 저장된다(localStorage). 설정 칸에 손으로 넣어야만 했고,
   넣지 않은 기기의 오답·학습 기록은 조용히 그 기기 안에만 쌓였다(2026-09-23 실측: 저장소 오답 KMLE 21개 · USMLE 0개).
   이제 키가 있는 기기에서 「다른 기기 연결 링크」를 만들어 보내고, 새 기기에서 그 링크를 한 번 열면 키가 저장된다.

   - 링크 형식: https://my-github-test.pages.dev/#k=<키>
     키는 # 뒤(fragment)에 있어 서버·로그로 가지 않는다. 읽은 즉시 주소창에서 지운다(history.replaceState).
   - 키를 받기 전의 오답·학습 기록도 버리지 않는다 — 기기에 남아 있다가 키가 들어오는 순간 전부 합쳐 올라간다
     (서버는 합집합 병합: functions/api/wrong.js · learning.js).
   - 순수 함수는 pipelines/test_sync_key.py 가 node 로 시험한다. DOM 을 건드리지 않는다. */
var MEDKOS_SYNC = (function () {
  "use strict";
  const STORE = "medkos_sync_key";
  const NAMES = ["k", "sync"];                         // #k=… (기본) · #sync=… (별칭)
  const HOME = "https://my-github-test.pages.dev/";   // 동기화 서버가 있는 주소 — 새 기기는 여기로 연결한다

  function parts(hash) {
    return String(hash || "").replace(/^#/, "").split("&").filter(Boolean);
  }
  // "#k=abc&x=1" → "abc". 없거나 깨졌으면 "".
  function parseHash(hash) {
    for (const p of parts(hash)) {
      const i = p.indexOf("=");
      if (i < 0 || NAMES.indexOf(p.slice(0, i)) < 0) continue;
      try { return decodeURIComponent(p.slice(i + 1)).trim(); } catch (e) { return ""; }
    }
    return "";
  }
  // 키 부분만 뺀 나머지 fragment("#x=1" 또는 "").
  function stripHash(hash) {
    const rest = parts(hash).filter((p) => NAMES.indexOf(p.split("=")[0]) < 0);
    return rest.length ? "#" + rest.join("&") : "";
  }
  function linkFor(key, base) {
    return (base || HOME) + "#k=" + encodeURIComponent(String(key || "").trim());
  }
  function get(store) {
    try { return ((store || localStorage).getItem(STORE) || "").trim(); } catch (e) { return ""; }
  }
  function set(value, store) {
    try {
      const s = store || localStorage;
      const v = String(value || "").trim();
      if (v) s.setItem(STORE, v); else s.removeItem(STORE);
      return true;
    } catch (e) { return false; }
  }
  // 주소의 #k= 를 저장하고 주소창에서 지운다. 반환: 새로 저장한 키("" = 없음).
  function capture(loc, hist, store) {
    const key = parseHash(loc && loc.hash);
    if (!key) return "";
    if (!set(key, store)) return "";
    try {
      if (hist && hist.replaceState) hist.replaceState(null, "", loc.pathname + loc.search + stripHash(loc.hash));
    } catch (e) { /* 주소를 못 지워도 키는 저장됐다 */ }
    return key;
  }

  const captured = typeof location !== "undefined" && typeof history !== "undefined"
    ? capture(location, history) : "";
  return { STORE, HOME, parseHash, stripHash, linkFor, get, set, capture, captured };
})();
