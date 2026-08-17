// 새 자료 화면 — window.MEDKOS_INDEX(search-index.js)를 만든 날짜순으로 보여준다.
// 별도 번들을 만들지 않는 이유: 검색 색인이 이미 content/ 전체를 date 내림차순으로
// 담고 있어, 새 파이프라인을 붙이면 같은 사실이 두 곳에 생겨 어긋난다.
(function () {
  "use strict";
  var DATA = window.MEDKOS_INDEX || {};
  var DOCS = (DATA.docs || []).filter(function (d) { return d.date; });
  // 도해·트리는 content 카드가 아니라 자산 파일이라 검색 색인에 없다 → 별도 매니페스트를
  // 같은 타임라인에 합친다(라벨판만 — 퀴즈판까지 넣으면 목록이 두 배가 된다).
  (function () {
    var DG = window.MEDKOS_DIAGRAMS || {};
    (DG.items || []).forEach(function (it) {
      if (it.variant === "quiz") return;
      DOCS.push({
        id: it.base, type: "diagram", date: it.date,
        unit: it.unit || (it.session ? it.session + "회차" : ""),
        topic: "",                       // 회차는 unit 배지가 보여준다(오른쪽 중복 제거)
        subtopic: it.title + " — " + it.kindLabel,
        tags: [it.kind], path: "docs/assets/anatomy/" + it.file,
        _href: "anatomy.html#diagrams"
      });
    });
    DOCS.sort(function (a, b) { return a.date < b.date ? 1 : a.date > b.date ? -1 : 0; });
  })();
  var SEEN_KEY = "medkos_whatsnew_seen";   // 마지막으로 "여기까지 봤음" 누른 날짜
  var unitSel = "";                        // 회차 배지로 좁힌 상태("6회차")

  var TYPE_LABEL = {
    anatomy: "해부학", kmle: "KMLE", usmle: "USMLE", paper: "논문",
    ailab: "AI랩", basic: "기초의학", disease: "질환", drug: "약물", diagram: "도해"
  };
  var TYPE_HREF = {
    anatomy: "anatomy.html", kmle: "index.html", usmle: "index.html",
    paper: "papers.html", ailab: "ailab.html", diagram: "anatomy.html#diagrams"
  };
  var REPO = DATA.repo || "";
  var BRANCH = DATA.branch || "main";

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
  function setSeen(v) {
    try { localStorage.setItem(SEEN_KEY, v); } catch (e) { /* 무시 */ }
  }
  function ghUrl(path) {
    if (!REPO) return "";
    return "https://github.com/" + REPO + "/blob/" + BRANCH + "/" + path;
  }
  function weekday(iso) {
    var d = new Date(iso + "T00:00:00+09:00");
    return ["일", "월", "화", "수", "목", "금", "토"][d.getDay()];
  }

  function isNew(d) {
    var s = seenDate();
    return s ? d.date > s : daysAgo(d.date) <= 7;
  }

  function fillTypes() {
    var sel = $("typeFilter");
    var counts = {};
    DOCS.forEach(function (d) { counts[d.type] = (counts[d.type] || 0) + 1; });
    Object.keys(counts).sort(function (a, b) { return counts[b] - counts[a]; })
      .forEach(function (t) {
        var o = document.createElement("option");
        o.value = t;
        o.textContent = (TYPE_LABEL[t] || t) + " (" + counts[t] + ")";
        sel.appendChild(o);
      });
  }

  function filtered() {
    var t = $("typeFilter").value;
    var range = parseInt($("rangeFilter").value, 10);
    var q = ($("q").value || "").trim().toLowerCase();
    return DOCS.filter(function (d) {
      if (t !== "__ALL__" && d.type !== t) return false;
      if (range > 0 && daysAgo(d.date) > range) return false;
      // 회차 배지 필터는 정확일치다 — 부분일치면 '1회차'가 '11회차'까지 끌고 온다.
      if (unitSel && (d.unit || "").split(" · ")[0] !== unitSel) return false;
      if (q) {
        var hay = (d.subtopic + " " + d.topic + " " + (d.unit || "") + " "
                   + (d.tags || []).join(" ") + " " + d.id).toLowerCase();
        if (hay.indexOf(q) < 0) return false;
      }
      return true;
    });
  }

  function card(d) {
    var href = TYPE_HREF[d.type] || "search.html";
    var gh = ghUrl(d.path);
    // 날짜순으로 늘어놓으면 해부 자료는 소속을 잃는다 → '2회차 · 등'을 제목 앞에.
    var unit = d.unit
      ? '<button class="wn-unit" data-unit="' + esc(d.unit.split(" · ")[0]) + '"'
        + ' title="이 회차만 보기">' + esc(d.unit) + "</button>" : "";
    return '<li class="wn-item' + (isNew(d) ? " is-new" : "") + '">' +
      '<span class="wn-type wn-' + esc(d.type) + '">' + esc(TYPE_LABEL[d.type] || d.type) + "</span>" +
      unit +
      '<span class="wn-title">' + esc(d.subtopic || d.topic || d.id) + "</span>" +
      (d.topic && d.subtopic ? '<span class="wn-topic">' + esc(d.topic) + "</span>" : "") +
      '<span class="wn-links">' +
        '<a href="' + href + '">열기</a>' +
        (gh ? ' · <a href="' + gh + '" target="_blank" rel="noopener">원본</a>' : "") +
      "</span></li>";
  }

  function render() {
    var rows = filtered();
    var byDate = {};
    var order = [];
    rows.forEach(function (d) {
      if (!byDate[d.date]) { byDate[d.date] = []; order.push(d.date); }
      byDate[d.date].push(d);
    });
    var html = order.map(function (date) {
      var items = byDate[date];
      var n = items.filter(isNew).length;
      return '<div class="card wn-day">' +
        '<h3 class="wn-date">' + esc(date) + " (" + weekday(date) + ")" +
          '<span class="muted"> · ' + items.length + "건</span>" +
          (n ? ' <span class="wn-badge">NEW ' + n + "</span>" : "") +
        "</h3><ul class=\"wn-list\">" + items.map(card).join("") + "</ul></div>";
    }).join("");
    $("timeline").innerHTML = html || '<div class="card muted">조건에 맞는 자료가 없습니다.</div>';
    $("count").innerHTML = esc(rows.length + "건 · " + order.length + "일")
      + (unitSel ? ' <button class="wn-unit wn-unitclear" title="회차 필터 해제">'
                   + esc(unitSel) + " ✕</button>" : "");
    var clear = $("count").querySelector(".wn-unitclear");
    if (clear) clear.addEventListener("click", function () { unitSel = ""; render(); });
    Array.prototype.forEach.call($("timeline").querySelectorAll(".wn-unit"), function (b) {
      b.addEventListener("click", function () {
        unitSel = b.getAttribute("data-unit");
        render();
      });
    });

    var newTotal = DOCS.filter(isNew).length;
    var badge = $("newBadge");
    if (newTotal) { badge.textContent = "NEW " + newTotal; badge.hidden = false; }
    else { badge.hidden = true; }
  }

  function init() {
    if (!DOCS.length) {
      $("timeline").innerHTML = '<div class="card muted">색인이 비어 있습니다. ' +
        "<code>python pipelines/export_search_web.py</code> 로 재생성하세요.</div>";
      return;
    }
    fillTypes();
    ["typeFilter", "rangeFilter"].forEach(function (id) {
      $(id).addEventListener("change", render);
    });
    $("q").addEventListener("input", render);
    $("markSeen").addEventListener("click", function () {
      setSeen(DOCS[0].date);   // 가장 최근 자료 날짜까지 확인한 것으로 기록
      render();
    });
    var s = seenDate();
    $("meta").textContent = "색인 생성 " + (DATA.generated || "?") +
      " · 총 " + DOCS.length + "건" +
      (s ? " · 마지막 확인 " + s : " · 마지막 확인 기록 없음(최근 7일을 NEW로 표시)");
    render();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else { init(); }
})();
