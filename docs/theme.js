/* theme.js — 밝은 화면(기본 · Daylight Clinical Paper) / 어두운 화면 (2026-11-23 vNext Phase 1)
   <head> 에서 style.css 보다 먼저 읽는다 — 첫 그림 전에 html[data-theme] 를 걸어 깜빡임이 없다.
   저장: localStorage.medkos_theme = "light" | "dark"(없으면 밝은 화면 — 기기의 다크 모드를 따라가지 않는다).
   메뉴 줄(.nav) 끝에 단추를 하나 넣는다. 색은 전부 style.css 의 변수가 정한다 — 여기서는 속성만 바꾼다. */
(function () {
  "use strict";
  var KEY = "medkos_theme";
  var BAR = { light: "#f3f6fa", dark: "#0f1620" };      // 브라우저 주소줄 색(style.css --bg 와 같게)

  function saved() {
    try { return localStorage.getItem(KEY) === "dark" ? "dark" : "light"; } catch (e) { return "light"; }
  }
  function apply(t) {
    document.documentElement.setAttribute("data-theme", t);
    var m = document.querySelector('meta[name="theme-color"]');
    if (m) m.setAttribute("content", BAR[t]);
    var b = document.getElementById("themeToggle");
    if (b) {
      b.textContent = t === "dark" ? "밝은 화면" : "어두운 화면";
      b.setAttribute("aria-pressed", String(t === "dark"));
      b.title = t === "dark" ? "밝은 화면으로 바꾸기" : "어두운 화면으로 바꾸기";
    }
  }
  function set(t) {
    t = t === "dark" ? "dark" : "light";
    try { localStorage.setItem(KEY, t); } catch (e) { /* 저장 못 해도 이번 화면에는 건다 */ }
    apply(t);
  }
  function mount() {
    // 맨 위 불투명 띠 — iPadOS 26 홈 화면 앱이 상태 막대를 흐리게 덧씌우지 않고 이 색으로 반듯하게 채우게 한다(style.css .edge-band)
    if (document.body && !document.getElementById("edgeBand")) {
      var band = document.createElement("div");
      band.id = "edgeBand"; band.className = "edge-band"; band.setAttribute("aria-hidden", "true");
      document.body.insertBefore(band, document.body.firstChild);
    }
    var nav = document.querySelector(".nav");
    if (nav && !document.getElementById("themeToggle")) {
      var b = document.createElement("button");
      b.type = "button"; b.id = "themeToggle"; b.className = "theme-toggle";
      b.onclick = function () { set(saved() === "dark" ? "light" : "dark"); };
      nav.appendChild(b);
    }
    apply(saved());
  }

  apply(saved());
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount); else mount();
  window.addEventListener("storage", function (e) { if (e.key === KEY) apply(saved()); });   // 다른 탭에서 바꾸면 따라간다
  window.MEDKOS_THEME = { get: saved, set: set };
})();
