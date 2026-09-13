/* MedKOS PWA 부트스트랩 — 모든 페이지에서 로드.
   - service worker 등록(오프라인·캐시)
   - Android Chrome 의 설치 프롬프트를 받아 「📲 앱 설치」 버튼으로 노출
   - 서비스워커가 새 문항 번들을 받아오면 「새 자료 · 새로고침」 토스트
   file:// 로 열었을 때는 아무것도 하지 않는다(로컬 미리보기 호환). */
(function () {
  "use strict";
  if (location.protocol === "file:" || !("serviceWorker" in navigator)) return;

  var deferredPrompt = null;

  function toast(text, actionLabel, onAction) {
    var old = document.getElementById("pwaToast");
    if (old) old.remove();
    var el = document.createElement("div");
    el.id = "pwaToast";
    el.className = "pwa-toast";
    el.innerHTML = '<span></span>';
    el.firstChild.textContent = text;
    if (actionLabel) {
      var b = document.createElement("button");
      b.textContent = actionLabel;
      b.onclick = function () { el.remove(); onAction && onAction(); };
      el.appendChild(b);
    }
    var x = document.createElement("button");
    x.className = "x"; x.textContent = "✕"; x.setAttribute("aria-label", "닫기");
    x.onclick = function () { el.remove(); };
    el.appendChild(x);
    document.body.appendChild(el);
  }

  function showInstallButton() {
    if (document.getElementById("pwaInstall")) return;
    var b = document.createElement("button");
    b.id = "pwaInstall";
    b.className = "pwa-install";
    b.textContent = "📲 앱으로 설치";
    b.onclick = function () {
      if (!deferredPrompt) return;
      deferredPrompt.prompt();
      deferredPrompt.userChoice.then(function () { deferredPrompt = null; b.remove(); });
    };
    document.body.appendChild(b);
  }

  window.addEventListener("beforeinstallprompt", function (e) {
    e.preventDefault();
    deferredPrompt = e;
    showInstallButton();
  });
  window.addEventListener("appinstalled", function () {
    var b = document.getElementById("pwaInstall");
    if (b) b.remove();
    toast("홈 화면에 MedKOS 가 설치되었습니다.");
  });

  var reloading = false;
  navigator.serviceWorker.addEventListener("message", function (e) {
    if (e.data && e.data.type === "DATA_UPDATED") {
      toast("새 문항 자료가 도착했습니다.", "새로고침", function () { location.reload(); });
    }
  });
  navigator.serviceWorker.addEventListener("controllerchange", function () {
    if (reloading) return;
    reloading = true;
  });

  // iPad/iPhone: beforeinstallprompt 가 없다. Safari 공유 → 홈 화면에 추가 로만 설치되므로 한 번 안내한다.
  function iosHint() {
    var ua = navigator.userAgent || "";
    var isIOS = /iPad|iPhone|iPod/.test(ua) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
    var standalone = window.matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
    if (!isIOS || standalone) return;
    try { if (localStorage.getItem("medkos_ios_hint") === "1") return; } catch (e) { /* ignore */ }
    var isSafari = /Safari/.test(ua) && !/CriOS|FxiOS|EdgiOS/.test(ua);
    toast(isSafari
      ? "아이패드: 하단(또는 상단) 공유 버튼 ▸ 「홈 화면에 추가」를 누르면 앱처럼 설치됩니다."
      : "아이패드: Safari 로 이 주소를 열고 공유 ▸ 「홈 화면에 추가」를 누르면 앱처럼 설치됩니다.",
      "알겠어요", function () { try { localStorage.setItem("medkos_ios_hint", "1"); } catch (e) { /* ignore */ } });
  }

  window.addEventListener("load", function () {
    navigator.serviceWorker.register("./sw.js").catch(function (err) {
      console.warn("[pwa] service worker 등록 실패:", err);
    });
    setTimeout(iosHint, 1200);
  });
})();
