// 논문 스크랩 피드 — content/papers 의 .md 에서 생성된 window.PAPERS 를 렌더링한다.
// 순수 정적: 검색·주제 필터·초록 펼치기만. 데이터는 papers.js(자동 생성).
(function () {
  "use strict";
  var PAPERS = (window.PAPERS || []).slice();

  var $ = function (id) { return document.getElementById(id); };
  var listEl = $("list"), countEl = $("count");
  var searchEl = $("search"), topicEl = $("topicFilter");

  // 주제 필터 채우기
  var topics = {};
  PAPERS.forEach(function (p) { if (p.topic) topics[p.topic] = (topics[p.topic] || 0) + 1; });
  Object.keys(topics).sort().forEach(function (t) {
    var o = document.createElement("option");
    o.value = t; o.textContent = t + " (" + topics[t] + ")";
    topicEl.appendChild(o);
  });

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function section(title, text) {
    if (!text) return "";
    return '<div class="sec"><h4>' + esc(title) + '</h4><p>' + esc(text) + "</p></div>";
  }

  function card(p) {
    var meta = [];
    if (p.journal) meta.push(esc(p.journal));
    if (p.pubdate) meta.push(esc(p.pubdate));
    if (p.pmid) meta.push("PMID " + esc(p.pmid));
    var conf = p.confidence
      ? '<span class="pill conf-' + esc(p.confidence) + '">' + esc(p.confidence) + "</span>" : "";
    var authors = (p.authors || []).join(", ");

    var details = "";
    var body = section("Abstract", p.abstract) + section("Summary", p.summary)
      + section("Clinical Impact", p.clinicalImpact) + section("My Ideas", p.myIdeas);
    if (body) {
      details = "<details><summary>초록·요약 보기</summary>" + body + "</details>";
    }
    var link = p.url
      ? '<a class="plink" href="' + esc(p.url) + '" target="_blank" rel="noopener">PubMed 원문 →</a>' : "";

    return '<article class="paper">'
      + '<div class="ptop"><span class="pill">' + esc(p.topic || "?") + "</span>" + conf + "</div>"
      + '<div class="ptitle">' + esc(p.title) + "</div>"
      + (meta.length ? '<div class="pmeta">' + meta.join(" · ") + "</div>" : "")
      + (authors ? '<div class="pauthors">' + esc(authors) + "</div>" : "")
      + details
      + (link ? '<div style="margin-top:8px">' + link + "</div>" : "")
      + "</article>";
  }

  function render() {
    var q = (searchEl.value || "").trim().toLowerCase();
    var topic = topicEl.value;
    var rows = PAPERS.filter(function (p) {
      if (topic !== "__ALL__" && p.topic !== topic) return false;
      if (!q) return true;
      var hay = [p.title, p.journal, p.abstract, p.summary, (p.authors || []).join(" ")]
        .join(" ").toLowerCase();
      return hay.indexOf(q) !== -1;
    });

    if (!PAPERS.length) {
      listEl.innerHTML = '<div class="empty">아직 스크랩된 논문이 없습니다.<br>'
        + 'GitHub Actions의 <code>scrape-papers</code> 워크플로를 실행하면 채워집니다.</div>';
      countEl.textContent = "";
      return;
    }
    countEl.textContent = "총 " + PAPERS.length + "편 중 " + rows.length + "편 표시";
    listEl.innerHTML = rows.length
      ? rows.map(card).join("")
      : '<div class="empty">검색 결과가 없습니다.</div>';
  }

  searchEl.addEventListener("input", render);
  topicEl.addEventListener("change", render);
  render();
})();
