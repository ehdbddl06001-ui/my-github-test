// 도해 갤러리 — window.MEDKOS_DIAGRAMS(diagrams-data.js)를 만든 날짜순으로 보여준다.
// content 카드가 아닌 자산(SVG)이라 검색 색인에 안 잡히므로 별도 매니페스트를 쓴다.
(function () {
  "use strict";
  var DATA = window.MEDKOS_DIAGRAMS || {};
  var ITEMS = DATA.items || [];
  var SEEN_KEY = "medkos_diagrams_seen";

  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function kstToday() {
    return new Intl.DateTimeFormat("sv-SE", { timeZone: "Asia/Seoul" }).format(new Date());
  }
  function daysAgo(iso) {
    return Math.round((new Date(kstToday()) - new Date(iso)) / 86400000);
  }
  function seenDate() {
    try { return localStorage.getItem(SEEN_KEY) || ""; } catch (e) { return ""; }
  }
  function weekday(iso) {
    var d = new Date(iso + "T00:00:00+09:00");
    return ["일", "월", "화", "수", "목", "금", "토"][d.getDay()];
  }
  function isNew(it) {
    var s = seenDate();
    return s ? it.date > s : daysAgo(it.date) <= 7;
  }

  function fill(sel, values, label) {
    values.forEach(function (v) {
      var o = document.createElement("option");
      o.value = String(v);
      o.textContent = label(v);
      sel.appendChild(o);
    });
  }

  function filtered() {
    var k = $("kindFilter").value, s = $("sessionFilter").value;
    var v = $("variantFilter").value, q = ($("q").value || "").trim().toLowerCase();
    return ITEMS.filter(function (it) {
      if (k !== "__ALL__" && it.kind !== k) return false;
      if (s !== "__ALL__" && String(it.session || "") !== s) return false;
      if (v !== "__ALL__" && it.variant !== v) return false;
      if (q && (it.title + " " + it.file).toLowerCase().indexOf(q) < 0) return false;
      return true;
    });
  }

  function pairLinks(it) {
    var other = it.variant === "labeled" ? "quiz" : "labeled";
    var mate = ITEMS.filter(function (x) {
      return x.base === it.base && x.variant === other;
    })[0];
    var out = '<a href="assets/anatomy/' + esc(it.file) + '" target="_blank" rel="noopener">크게 보기</a>';
    if (mate) {
      out += ' · <a href="assets/anatomy/' + esc(mate.file) + '" target="_blank" rel="noopener">' +
        (other === "quiz" ? "퀴즈판" : "라벨판") + "</a>";
    }
    return out;
  }

  function tile(it) {
    return '<figure class="dg-tile' + (isNew(it) ? " is-new" : "") + '">' +
      '<a href="assets/anatomy/' + esc(it.file) + '" target="_blank" rel="noopener">' +
      '<img loading="lazy" src="assets/anatomy/' + esc(it.file) + '" alt="' + esc(it.title) + '" /></a>' +
      '<figcaption>' +
        '<span class="dg-kind dg-' + esc(it.kind) + '">' + esc(it.kindLabel) + "</span>" +
        (it.session ? '<span class="dg-sess">' + it.session + "회차</span>" : "") +
        (it.variant === "quiz" ? '<span class="dg-sess dg-quiz">퀴즈판</span>' : "") +
        '<span class="dg-title">' + esc(it.title) + "</span>" +
        '<span class="dg-links">' + pairLinks(it) + "</span>" +
      "</figcaption></figure>";
  }

  function render() {
    var rows = filtered();
    var byDate = {}, order = [];
    rows.forEach(function (it) {
      if (!byDate[it.date]) { byDate[it.date] = []; order.push(it.date); }
      byDate[it.date].push(it);
    });
    $("timeline").innerHTML = order.map(function (d) {
      var items = byDate[d];
      var n = items.filter(isNew).length;
      return '<div class="card wn-day"><h3 class="wn-date">' + esc(d) + " (" + weekday(d) + ")" +
        '<span class="muted"> · ' + items.length + "장</span>" +
        (n ? ' <span class="wn-badge">NEW ' + n + "</span>" : "") +
        '</h3><div class="dg-grid">' + items.map(tile).join("") + "</div></div>";
    }).join("") || '<div class="card muted">조건에 맞는 도해가 없습니다.</div>';
    $("count").textContent = rows.length + "장 · " + order.length + "일";
    var nt = ITEMS.filter(isNew).length;
    var b = $("newBadge");
    if (nt) { b.textContent = "NEW " + nt; b.hidden = false; } else { b.hidden = true; }
  }

  function init() {
    if (!ITEMS.length) {
      $("timeline").innerHTML = '<div class="card muted">도해 목록이 비어 있습니다. ' +
        "<code>python pipelines/export_diagrams_web.py</code> 로 생성하세요.</div>";
      return;
    }
    var kinds = [], seenK = {};
    ITEMS.forEach(function (i) { if (!seenK[i.kind]) { seenK[i.kind] = i.kindLabel; kinds.push(i.kind); } });
    fill($("kindFilter"), kinds, function (k) { return seenK[k]; });
    var sess = [];
    ITEMS.forEach(function (i) { if (i.session && sess.indexOf(i.session) < 0) sess.push(i.session); });
    sess.sort(function (a, b) { return a - b; });
    fill($("sessionFilter"), sess, function (s) { return s + "회차"; });

    ["kindFilter", "sessionFilter", "variantFilter"].forEach(function (id) {
      $(id).addEventListener("change", render);
    });
    $("q").addEventListener("input", render);
    $("markSeen").addEventListener("click", function () {
      try { localStorage.setItem(SEEN_KEY, ITEMS[0].date); } catch (e) { /* 무시 */ }
      render();
    });
    var s = seenDate();
    $("meta").textContent = "목록 생성 " + (DATA.generated || "?") +
      " · 파일 " + DATA.count + "장 · 도해 " + DATA.groups + "종" +
      (s ? " · 마지막 확인 " + s : " · 마지막 확인 기록 없음(최근 7일을 NEW로 표시)");
    render();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else { init(); }
})();
