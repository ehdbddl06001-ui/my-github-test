// 논문 스크랩 피드 — content/papers 의 .md 에서 생성된 window.PAPERS 를 렌더링한다.
// 검색·주제 필터·초록 펼치기 + 논문별 '내 생각/아이디어' 메모(localStorage).
// 메모는 이 브라우저에만 남는다. .json 으로 내보내 pipelines/apply_notes.py 로 카드의
// ## My Ideas 에 반영하면 GitHub·Google Drive에 영구 저장되고 모든 기기에 뜬다.
(function () {
  "use strict";
  var PAPERS = (window.PAPERS || []).slice();
  var NOTE_KEY = "medkos_paper_notes";

  var $ = function (id) { return document.getElementById(id); };
  var listEl = $("list"), countEl = $("count");
  var searchEl = $("search"), topicEl = $("topicFilter"), notesOnlyEl = $("notesOnly");
  var landmarkOnlyEl = $("landmarkOnly"), sortByEl = $("sortBy");

  // ── 노트 저장소(localStorage) ────────────────────────────────
  function loadNotes() {
    try { return JSON.parse(localStorage.getItem(NOTE_KEY) || "{}"); }
    catch (e) { return {}; }
  }
  function saveNote(id, text) {
    var all = loadNotes();
    if (text && text.trim()) all[id] = { text: text, updated: new Date().toISOString() };
    else delete all[id];
    localStorage.setItem(NOTE_KEY, JSON.stringify(all));
  }
  var NOTES = loadNotes();

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
    var hasNote = !!(NOTES[p.id] && NOTES[p.id].text);
    var noteBadge = hasNote ? '<span class="pill notebadge">📝 내 노트</span>' : "";
    var dateBadge = p.date ? '<span class="pill datepill">🗓 ' + esc(p.date) + "</span>" : "";
    // 랜드마크(고인용) 배지 — 인용수를 함께 보여 '왜 꼭 봐야 하는지'를 한눈에.
    var landmarkBadge = p.landmark
      ? '<span class="pill landmark">⭐ 꼭 봐야 함' + (p.citations != null ? " · 인용 " + esc(p.citations) : "") + "</span>"
      : "";

    // 초록·요약 섹션 + 카드에 이미 저장된 My Ideas
    var body = section("왜 꼭 봐야 하는가", p.whyMustRead)
      + section("Abstract", p.abstract) + section("Summary", p.summary)
      + section("Clinical Impact", p.clinicalImpact) + section("My Ideas (저장됨)", p.myIdeas);

    // 내 생각 에디터 (localStorage 초안)
    var draft = hasNote ? NOTES[p.id].text : "";
    var editor =
      '<div class="sec noteedit">'
      + '<h4>💡 내 생각 / 아이디어</h4>'
      + '<textarea class="noteinput" data-id="' + esc(p.id) + '" rows="3" '
      + 'placeholder="이 논문에 대한 생각·의문·후속 아이디어를 적어두세요…">' + esc(draft) + "</textarea>"
      + '<div class="noterow">'
      + '<span class="notestatus muted" data-status="' + esc(p.id) + '"></span>'
      + '<button class="notecopy" data-id="' + esc(p.id) + '">📋 복사</button>'
      + "</div></div>";

    var details = "<details><summary>초록·요약·내 생각</summary>" + body + editor + "</details>";
    var link = p.url
      ? '<a class="plink" href="' + esc(p.url) + '" target="_blank" rel="noopener">PubMed 원문 →</a>' : "";

    return '<article class="paper">'
      + '<div class="ptop"><span class="pill">' + esc(p.topic || "?") + "</span>" + landmarkBadge + dateBadge + conf + noteBadge + "</div>"
      + '<div class="ptitle">' + esc(p.title) + "</div>"
      + (meta.length ? '<div class="pmeta">' + meta.join(" · ") + "</div>" : "")
      + (authors ? '<div class="pauthors">' + esc(authors) + "</div>" : "")
      + details
      + (link ? '<div style="margin-top:8px">' + link + "</div>" : "")
      + "</article>";
  }

  // 스크랩 날짜(p.date, 최신순 정렬됨)별로 그룹 헤더를 끼워 "어디까지 봤는지" 경계를 만든다.
  function groupedHTML(rows) {
    var counts = {};
    rows.forEach(function (p) { var d = p.date || ""; counts[d] = (counts[d] || 0) + 1; });
    var html = "", last = null;
    rows.forEach(function (p) {
      var d = p.date || "";
      if (d !== last) {
        html += '<div class="datehead">'
          + '<span class="dhdate">📅 ' + esc(d || "날짜 미상") + "</span>"
          + '<span class="dhcount">' + counts[d] + "편</span>"
          + '<span class="dhline"></span></div>';
        last = d;
      }
      html += card(p);
    });
    return html;
  }

  var debounceT;
  function bindNoteEditors() {
    Array.prototype.forEach.call(document.querySelectorAll(".noteinput"), function (ta) {
      ta.addEventListener("input", function () {
        var id = ta.getAttribute("data-id");
        clearTimeout(debounceT);
        debounceT = setTimeout(function () {
          saveNote(id, ta.value);
          NOTES = loadNotes();
          var s = document.querySelector('[data-status="' + id + '"]');
          if (s) {
            var t = new Date();
            s.textContent = "저장됨 " + t.toTimeString().slice(0, 5);
          }
        }, 350);
      });
    });
    Array.prototype.forEach.call(document.querySelectorAll(".notecopy"), function (btn) {
      btn.addEventListener("click", function () {
        var id = btn.getAttribute("data-id");
        var ta = document.querySelector('.noteinput[data-id="' + id + '"]');
        if (ta && navigator.clipboard) {
          navigator.clipboard.writeText(ta.value).then(function () {
            btn.textContent = "복사됨 ✓";
            setTimeout(function () { btn.textContent = "📋 복사"; }, 1200);
          });
        }
      });
    });
  }

  function render() {
    var q = (searchEl.value || "").trim().toLowerCase();
    var topic = topicEl.value;
    var notesOnly = notesOnlyEl.checked;
    var landmarkOnly = landmarkOnlyEl.checked;
    var sortBy = sortByEl.value;
    var rows = PAPERS.filter(function (p) {
      if (topic !== "__ALL__" && p.topic !== topic) return false;
      if (landmarkOnly && !p.landmark) return false;
      if (notesOnly && !(NOTES[p.id] && NOTES[p.id].text)) return false;
      if (!q) return true;
      var hay = [p.title, p.journal, p.abstract, p.summary, (p.authors || []).join(" ")]
        .join(" ").toLowerCase();
      return hay.indexOf(q) !== -1;
    });
    // 인용순 정렬: 인용 많은 논문부터(값 없으면 뒤로). 최신순은 window.PAPERS 기본 순서.
    if (sortBy === "citations") {
      rows = rows.slice().sort(function (a, b) {
        return (b.citations || 0) - (a.citations || 0);
      });
    }

    if (!PAPERS.length) {
      listEl.innerHTML = '<div class="empty">아직 스크랩된 논문이 없습니다.<br>'
        + 'GitHub Actions의 <code>scrape-papers</code> 워크플로를 실행하면 채워집니다.</div>';
      countEl.textContent = "";
      return;
    }
    var noteN = Object.keys(NOTES).length;
    countEl.textContent = "총 " + PAPERS.length + "편 중 " + rows.length + "편 표시"
      + (noteN ? " · 내 노트 " + noteN + "개" : "");
    listEl.innerHTML = rows.length
      ? (sortBy === "citations" ? rows.map(card).join("") : groupedHTML(rows))
      : '<div class="empty">조건에 맞는 논문이 없습니다.</div>';
    bindNoteEditors();
  }

  // ── 노트 내보내기 ────────────────────────────────────────────
  function download(name, text, type) {
    var blob = new Blob([text], { type: type || "text/plain;charset=utf-8" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 500);
  }
  function paperById(id) {
    for (var i = 0; i < PAPERS.length; i++) if (PAPERS[i].id === id) return PAPERS[i];
    return null;
  }
  $("exportNotesJson").addEventListener("click", function () {
    var n = loadNotes();
    if (!Object.keys(n).length) { alert("내보낼 노트가 없습니다."); return; }
    download("medkos-notes.json", JSON.stringify(n, null, 2), "application/json");
  });
  $("exportNotesMd").addEventListener("click", function () {
    var n = loadNotes(); var ids = Object.keys(n);
    if (!ids.length) { alert("내보낼 노트가 없습니다."); return; }
    var out = ["# 내 논문 노트 (" + new Date().toISOString().slice(0, 10) + ")\n"];
    ids.forEach(function (id) {
      var p = paperById(id) || {};
      out.push("## " + (p.title || id));
      var meta = [p.journal, p.pmid ? "PMID " + p.pmid : "", p.url].filter(Boolean).join(" · ");
      if (meta) out.push("_" + meta + "_\n");
      out.push(n[id].text + "\n");
    });
    download("medkos-notes.md", out.join("\n"), "text/markdown;charset=utf-8");
  });

  searchEl.addEventListener("input", render);
  topicEl.addEventListener("change", render);
  notesOnlyEl.addEventListener("change", render);
  landmarkOnlyEl.addEventListener("change", render);
  sortByEl.addEventListener("change", render);
  render();
})();
