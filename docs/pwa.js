/* MedKOS PWA 부트스트랩 — 모든 페이지에서 로드.
   - service worker 등록(오프라인·캐시)
   - 「📲 앱으로 설치」 버튼. Android Chrome 은 beforeinstallprompt 로 바로 설치하고,
     그 신호가 없는 브라우저(아이폰·아이패드 Safari, 카카오톡 등 앱 안 브라우저)는 그 기기의 설치 방법을 안내한다
     — 크롬 말고는 설치 프롬프트 자체가 없어서 「설치가 안 뜬다」로 보이기 때문이다(2026-09-20).
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

  function standalone() {
    return window.matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
  }
  // 이 기기에서 설치가 어떻게 되는지 — 브라우저마다 다르고, 크롬 밖에는 자동 프롬프트가 없다.
  function howToInstall() {
    var ua = navigator.userAgent || "";
    var isIOS = /iPad|iPhone|iPod/.test(ua) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
    if (/KAKAOTALK|NAVER|Instagram|FBAV|FBAN|Line\/|DaumApps|everytimeApp/i.test(ua))
      return "지금은 다른 앱 안의 브라우저로 열려 있어 설치할 수 없습니다. 오른쪽 위 메뉴에서 「다른 브라우저로 열기」(사파리·크롬)를 고른 뒤 다시 눌러 주세요.";
    if (isIOS)
      return /CriOS|FxiOS|EdgiOS/.test(ua)
        ? "아이폰·아이패드는 Safari 에서만 설치됩니다. 이 주소를 Safari 로 연 뒤 공유 버튼 ▸ 「홈 화면에 추가」를 누르세요."
        : "공유 버튼(⬆) ▸ 「홈 화면에 추가」를 누르면 앱처럼 설치됩니다.";
    if (/Android/i.test(ua))
      return "오른쪽 위 메뉴(⋮) ▸ 「앱 설치」 또는 「홈 화면에 추가」를 누르세요. 항목이 없으면 크롬으로 이 주소를 열어 주세요.";
    return "주소창 오른쪽의 설치 아이콘(⊕), 또는 메뉴 ▸ 「앱으로 설치」를 누르세요.";
  }
  function hideForever() {
    try { localStorage.setItem("medkos_install_hint", "1"); } catch (e) { /* ignore */ }
    var b = document.getElementById("pwaInstall");
    if (b) b.remove();
  }
  function showInstallButton() {
    if (document.getElementById("pwaInstall") || standalone()) return;
    try { if (localStorage.getItem("medkos_install_hint") === "1" && !deferredPrompt) return; } catch (e) { /* ignore */ }
    var b = document.createElement("button");
    b.id = "pwaInstall";
    b.className = "pwa-install";
    b.textContent = "📲 앱으로 설치";
    b.onclick = function () {
      if (deferredPrompt) {                       // Android Chrome — 바로 설치 창
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then(function () { deferredPrompt = null; b.remove(); });
        return;
      }
      toast(howToInstall(), "다시 보지 않기", hideForever);   // 그 밖의 브라우저 — 방법을 알려 준다
    };
    document.body.appendChild(b);
  }

  var reloading = false;
  navigator.serviceWorker.addEventListener("message", function (e) {
    if (e.data && e.data.type === "DATA_UPDATED") {
      toast("새 문항 자료가 도착했습니다.", "새로고침", function () { location.reload(); });
    }
  });
  // 새 서비스워커가 이 페이지를 넘겨받으면(sw.js 배포) 한 번만 새로고침해 새 캐시 전략으로 번들을 다시 받는다.
  // 첫 설치(이전 컨트롤러가 없던 경우)는 새로고침하지 않는다 — 이미 네트워크에서 받은 최신 페이지다.
  var hadController = !!navigator.serviceWorker.controller;
  navigator.serviceWorker.addEventListener("controllerchange", function () {
    if (reloading || !hadController) { hadController = true; return; }
    reloading = true;
    location.reload();
  });

  window.addEventListener("load", function () {
    navigator.serviceWorker.register("./sw.js").catch(function (err) {
      console.warn("[pwa] service worker 등록 실패:", err);
    });
    // beforeinstallprompt 는 크롬에서만, 그것도 잠시 뒤에 온다. 안 오면 안내 버튼으로 대신한다.
    setTimeout(showInstallButton, 1500);
  });
})();
