// 통합검색 · 대시보드 — content/ 에서 생성된 window.MEDKOS_INDEX 를 브라우저에서 검색한다.
// CLI(pipelines/search.py)는 같은 색인을 SQLite FTS5 로 조회한다. 원본은 content/**/*.md 하나.
(function () {
  "use strict";
  var IDX = window.MEDKOS_INDEX || { docs: [], stats: {} };
  var DOCS = (IDX.docs || []).slice();
  var STATS = IDX.stats || {};

  var $ = function (id) { return document.getElementById(id); };
  var qEl = $("q"), typeEl = $("typeFilter"), topicEl = $("topicFilter");
  var resultsEl = $("results"), countEl = $("count");

  var TYPE_LABEL = {
    kmle: "KMLE", usmle: "USMLE", paper: "논문",
    basic: "기초의학", disease: "질환", drug: "약물"
  };

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function blobUrl(path) {
    if (!IDX.repo) return null;
    return "https://github.com/" + IDX.repo + "/blob/" + (IDX.branch || "main") + "/" + path;
  }

  // ── 대시보드 ───────────────────────────────────────────────
  function renderDashboard() {
    $("dashTotal").textContent = "· 총 " + (STATS.total || DOCS.length) + "개 문서";

    var byType = STATS.byType || {};
    var maxType = Math.max.apply(null, Object.keys(byType).map(function (k) { return byType[k]; }).concat([1]));
    var typesHtml = Object.keys(byType).sort(function (a, b) { return byType[b] - byType[a]; })
      .map(function (t) {
        var n = byType[t], pct = Math.round((n / maxType) * 100);
        return '<button class="dash-type" data-type="' + esc(t) + '" title="이 타입만 보기">'
          + '<span class="dt-label">' + esc(TYPE_LABEL[t] || t) + "</span>"
          + '<span class="dt-bar"><span style="width:' + pct + '%"></span></span>'
          + '<span class="dt-n">' + n + "</span></button>";
      }).join("");
    $("dashTypes").innerHTML = typesHtml;

    var byTopic = STATS.byTopic || {};
    var topicsHtml = Object.keys(byTopic).slice(0, 14).map(function (t) {
      return '<button class="chip" data-topic="' + esc(t) + '">' + esc(t)
        + ' <span class="chip-n">' + byTopic[t] + "</span></button>";
    }).join("");
    $("dashTopics").innerHTML = topicsHtml || '<span class="muted">주제 없음</span>';

    var conf = STATS.byConfidence || {};
    var confStr = Object.keys(conf).sort().map(function (c) { return c + " " + conf[c]; }).join(" · ");
    $("dashMeta").textContent = "신뢰도: " + (confStr || "-")
      + "  ·  태그 " + (STATS.tagCount || 0) + "종  ·  색인 생성 " + (IDX.generated || "-");

    // 대시보드 → 검색 필터 연동
    Array.prototype.forEach.call(document.querySelectorAll(".dash-type"), function (b) {
      b.addEventListener("click", function () { typeEl.value = b.getAttribute("data-type"); render(); scrollToResults(); });
    });
    Array.prototype.forEach.call(document.querySelectorAll(".chip"), function (b) {
      b.addEventListener("click", function () { topicEl.value = b.getAttribute("data-topic"); render(); scrollToResults(); });
    });
  }

  function scrollToResults() { countEl.scrollIntoView({ behavior: "smooth", block: "center" }); }

  // ── 필터 채우기 ────────────────────────────────────────────
  function fillFilters() {
    var byType = STATS.byType || {};
    Object.keys(byType).sort().forEach(function (t) {
      var o = document.createElement("option");
      o.value = t; o.textContent = (TYPE_LABEL[t] || t) + " (" + byType[t] + ")";
      typeEl.appendChild(o);
    });
    var byTopic = STATS.byTopic || {};
    Object.keys(byTopic).sort().forEach(function (t) {
      var o = document.createElement("option");
      o.value = t; o.textContent = t + " (" + byTopic[t] + ")";
      topicEl.appendChild(o);
    });
  }

  // ── 검색/렌더 ──────────────────────────────────────────────
  function highlight(text, terms) {
    var out = esc(text);
    terms.forEach(function (term) {
      if (!term) return;
      var re = new RegExp("(" + term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig");
      out = out.replace(re, "<mark>$1</mark>");
    });
    return out;
  }

  function card(d, terms) {
    var tag = TYPE_LABEL[d.type] || d.type;
    var conf = d.confidence
      ? '<span class="pill conf-' + esc(d.confidence) + '">' + esc(d.confidence) + "</span>" : "";
    var sub = d.subtopic ? " / " + esc(d.subtopic) : "";
    var tags = (d.tags || []).slice(0, 6).map(function (t) {
      return '<span class="tag">' + esc(t) + "</span>";
    }).join(" ");
    var url = blobUrl(d.path);
    var link = url ? '<a class="plink" href="' + url + '" target="_blank" rel="noopener">원본 열기 →</a>' : "";
    var snippet = d.snippet ? highlight(d.snippet, terms) : "";

    return '<article class="paper">'
      + '<div class="ptop"><span class="pill">' + esc(tag) + "</span>"
      + '<span class="rid">' + esc(d.id) + "</span>" + conf + "</div>"
      + '<div class="ptitle">' + highlight(d.topic || "?", terms) + sub + "</div>"
      + (snippet ? '<div class="rsnip">' + snippet + (d.snippet.length >= 240 ? "…" : "") + "</div>" : "")
      + (tags ? '<div class="rtags">' + tags + "</div>" : "")
      + '<div class="rmeta">' + esc(d.date || "") + (d.source ? " · " + esc(d.source) : "") + "</div>"
      + (link ? '<div style="margin-top:6px">' + link + "</div>" : "")
      + "</article>";
  }

  function render() {
    var q = (qEl.value || "").trim().toLowerCase();
    var terms = q ? q.split(/\s+/) : [];
    var type = typeEl.value, topic = topicEl.value;

    var out = DOCS.filter(function (d) {
      if (type !== "__ALL__" && d.type !== type) return false;
      if (topic !== "__ALL__" && d.topic !== topic) return false;
      if (!terms.length) return true;
      var hay = (d.text || "").toLowerCase();
      return terms.every(function (t) { return hay.indexOf(t) !== -1; });
    });

    countEl.textContent = out.length + "건"
      + (q ? ' · "' + esc(q) + '"' : "")
      + (type !== "__ALL__" ? " · " + (TYPE_LABEL[type] || type) : "")
      + (topic !== "__ALL__" ? " · " + topic : "");

    if (!out.length) {
      resultsEl.innerHTML = '<p class="empty">일치하는 문서가 없습니다.</p>';
      return;
    }
    resultsEl.innerHTML = out.slice(0, 200).map(function (d) { return card(d, terms); }).join("");
    if (out.length > 200) {
      resultsEl.innerHTML += '<p class="muted" style="text-align:center">상위 200건만 표시 — 검색어로 좁혀주세요.</p>';
    }
  }

  var t;
  qEl.addEventListener("input", function () { clearTimeout(t); t = setTimeout(render, 150); });
  typeEl.addEventListener("change", render);
  topicEl.addEventListener("change", render);

  renderDashboard();
  fillFilters();
  render();
})();
