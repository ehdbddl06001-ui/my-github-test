/* AI랩 페이지 — docs/ailab.js(window.AILAB)만 읽는 순수 정적 스크립트.
   marked(마크다운)·mermaid(도식)는 CDN에서 선택적으로 불러오고, 실패하면
   텍스트로 우아하게 폴백한다(오프라인·CSP에서도 최소 동작). */
(function () {
  var DATA = window.AILAB || { datasets: [], cards: [], weekly: {}, modalityLabels: {} };
  var ACC_KO = { open: "🟢 바로", registration: "🟡 가입", credentialed: "🔴 심사" };

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  // ── CDN 로더(선택) ────────────────────────────────────────────────
  function loadScript(src) {
    return new Promise(function (res) {
      var s = document.createElement("script");
      s.src = src; s.onload = function () { res(true); };
      s.onerror = function () { res(false); };
      document.head.appendChild(s);
    });
  }

  var mdReady = loadScript("https://cdn.jsdelivr.net/npm/marked/marked.min.js");
  var mermaidReady = loadScript("https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js")
    .then(function (ok) {
      if (ok && window.mermaid) {
        window.mermaid.initialize({ startOnLoad: false, securityLevel: "strict" });
      }
      return ok;
    });

  // 마크다운 → HTML (marked 있으면 사용, 없으면 escape+<pre>)
  function renderMarkdown(container, text) {
    mdReady.then(function (ok) {
      if (ok && window.marked) {
        container.innerHTML = window.marked.parse(text);
        upgradeMermaid(container);
      } else {
        container.innerHTML = "<pre>" + esc(text) + "</pre>";
      }
    });
  }

  // ```mermaid 코드블록을 다이어그램으로 승격
  function upgradeMermaid(root) {
    var blocks = root.querySelectorAll("code.language-mermaid");
    if (!blocks.length) return;
    mermaidReady.then(function (ok) {
      if (!ok || !window.mermaid) return; // 폴백: 코드 그대로 둔다
      blocks.forEach(function (code, i) {
        var div = el("div", "mermaid");
        div.textContent = code.textContent;
        var pre = code.closest("pre") || code;
        pre.parentNode.replaceChild(div, pre);
      });
      try { window.mermaid.run({ nodes: root.querySelectorAll(".mermaid") }); } catch (e) {}
    });
  }

  // ── 주차별 진도 목록(모든 주차 + 각 주차의 카드로 바로 이동) ──────
  var CHIP_KO = {
    weekly: "📖 실습카드", deepdive: "🔬 심화", log: "🧪 로그",
    concept: "📘 개념", project: "🔬 프로젝트", mentor: "🗣 논의", roadmap: "🗺 로드맵",
  };
  function chipFor(card) {
    var label = CHIP_KO[card.kind] || card.kind;
    if (card.kind === "log" && card.split) label += "(" + card.split + ")";
    var b = el("button", "wk-chip", esc(label));
    b.title = esc((card.topic || "") + (card.subtopic ? " — " + card.subtopic : ""));
    b.addEventListener("click", function () { openCard(card.id); });
    return b;
  }
  function renderProgressList(host) {
    var cur = DATA.curriculum || [];
    if (!cur.length) return;
    var done = (DATA.progress || {}).done || {};
    var curWeek = (DATA.weekly && DATA.weekly.week) || (DATA.progress || {}).week;

    var wrap = el("div", "wk-list");
    wrap.appendChild(el("h3", "wk-list-h", "📚 주차별 진도 <span class='muted'>(카드 클릭 → 바로 열림)</span>"));

    cur.forEach(function (t) {
      var w = t.week, key = String(w);
      var isDone = key in done, isCur = key === String(curWeek);
      var row = el("div", "wk-row" + (isCur ? " wk-cur" : "") + (isDone ? " wk-done" : ""));

      var status = isDone ? "✅" : (isCur ? "👉" : "·");
      var score = "";
      if (isDone && done[key] && done[key].value != null) {
        score = ' <span class="wk-score">' + esc(done[key].metric || "") + " " + esc(done[key].value) + "</span>";
      }
      row.appendChild(el("div", "wk-head",
        '<span class="wk-num">' + status + " " + esc(w) + "주</span> " +
        '<span class="wk-goal">' + esc(t.goal) + "</span>" +
        '<span class="muted wk-arch"> · ' + esc(t.arch) + "</span>" + score));

      var wkCards = (DATA.cards || []).filter(function (c) { return String(c.week) === key; });
      var rank = { weekly: 0, deepdive: 1, log: 2 };
      wkCards.sort(function (a, b) {
        return (rank[a.kind] == null ? 9 : rank[a.kind]) - (rank[b.kind] == null ? 9 : rank[b.kind]);
      });
      var chips = el("div", "wk-chips");
      if (wkCards.length) {
        wkCards.forEach(function (c) { chips.appendChild(chipFor(c)); });
      } else {
        chips.appendChild(el("span", "muted wk-empty", isCur ? "학습 카드 준비 중 (/ai-weekly)" : "카드 없음"));
      }
      row.appendChild(chips);
      wrap.appendChild(row);
    });
    host.appendChild(wrap);
  }

  // ── 이번 주 배너 + 주차별 진도 ────────────────────────────────────
  function renderWeekly() {
    var w = DATA.weekly || {};
    var host = document.getElementById("weekly");
    if (!host) return;
    if (!w.goal) {
      // 현재 주차 정보가 없어도 주차별 목록은 보여준다.
      host.innerHTML = "";
      renderProgressList(host);
      return;
    }
    host.innerHTML =
      '<h2>🗓 실습 진도 <span class="muted">(' + esc(w.week) + '주차 / 총 ' + esc(w.total || 12) + '주' +
      (w.done ? ' · ✅완료' : '') + ')</span></h2>' +
      '<div class="goal">🎯 ' + esc(w.goal) + '</div>' +
      '<p style="margin:6px 0"><span class="badgep">모델 ' + esc(w.arch) + '</span>' +
      '<span class="badgep">양식 ' + esc(DATA.modalityLabels[w.modality] || w.modality) + '</span>' +
      '<span class="acc acc-' + esc(w.access) + '">' + (ACC_KO[w.access] || w.access) + '</span></p>' +
      '<p class="muted" style="margin:4px 0">💡 ' + esc(w.why) + '</p>' +
      (w.metric ? '<p style="margin:4px 0">🚦 통과 기준: <b>' + esc(w.metric) + ' ≥ ' + esc(w.target) + '</b>' +
        (w.deliverable ? ' <span class="muted">· ' + esc(w.deliverable) + '</span>' : '') + '</p>' : '') +
      '<p style="margin:6px 0">📦 ' + esc(w.dataset_name) +
      (w.dataset_url ? ' · <a href="' + esc(w.dataset_url) + '" target="_blank" rel="noopener">데이터 열기 ↗</a>' : "") +
      '</p>';

    // 이 주차에 해당하는 학습 카드로 바로 이동(설명이 카드에 있으니 클릭 한 번으로 연결)
    var match = (DATA.cards || []).filter(function (c) {
      return c.kind === "weekly" && String(c.week) === String(w.week);
    })[0] || (DATA.cards || []).filter(function (c) {
      return c.kind === "weekly" && c.dataset === w.dataset_key;
    })[0];
    if (match) {
      var btn = el("button", "jump-btn", "📖 이 주차 학습 카드 열기 →");
      btn.addEventListener("click", function () { openCard(match.id); });
      host.appendChild(btn);
    } else {
      var hint = el("p", "muted");
      hint.style.marginTop = "8px";
      hint.innerHTML = "이 주차 학습 카드는 아직 없습니다. <code>/ai-weekly</code>로 생성하세요.";
      host.appendChild(hint);
    }

    // 현재 주차 배너 아래에 12주 전체 진도 목록(완료 주차의 카드로 바로 이동)
    renderProgressList(host);
  }

  // ── 오픈 데이터 카탈로그 ─────────────────────────────────────────
  function renderDatasets() {
    var host = document.getElementById("datasets");
    var q = (document.getElementById("dsSearch").value || "").toLowerCase();
    var mod = document.getElementById("modFilter").value;
    var openOnly = document.getElementById("openOnly").checked;
    host.innerHTML = "";

    var rows = (DATA.datasets || []).filter(function (d) {
      if (mod !== "__ALL__" && d.modality !== mod) return false;
      if (openOnly && d.access !== "open") return false;
      if (q) {
        var hay = (d.name + " " + d.task + " " + d.note + " " + d.key).toLowerCase();
        if (hay.indexOf(q) < 0) return false;
      }
      return true;
    });

    if (!rows.length) { host.appendChild(el("p", "muted", "조건에 맞는 데이터셋이 없습니다.")); return; }

    var groups = {};
    rows.forEach(function (d) { (groups[d.modality] = groups[d.modality] || []).push(d); });
    Object.keys(groups).forEach(function (m) {
      var g = el("div", "ds-group");
      g.appendChild(el("h3", null, "📁 " + esc(DATA.modalityLabels[m] || m) + " <span class='muted'>(" + m + ")</span>"));
      groups[m].forEach(function (d) {
        var card = el("div", "ds");
        card.innerHTML =
          '<div class="ds-top">' +
          '<span class="name">' + esc(d.name) + '</span>' +
          '<span class="acc acc-' + esc(d.access) + '">' + (ACC_KO[d.access] || d.access) + '</span>' +
          (d.colab_ready ? '<span class="colab-ok">· Colab OK</span>' : "") +
          '</div>' +
          '<div class="meta">' + esc(d.task) + ' · ' + esc(d.records || "") + ' · ' + esc(d.license || "") + '</div>' +
          '<div class="meta">' + esc(d.note || "") + '</div>' +
          '<div><a href="' + esc(d.url) + '" target="_blank" rel="noopener">접근 링크 ↗</a></div>';
        g.appendChild(card);
      });
      host.appendChild(g);
    });
  }

  // ── 학습 카드 ────────────────────────────────────────────────────
  var SECTION_ICON = {
    // 프로젝트/개념 카드
    "Overview": "📌 개요", "Architecture": "🧩 구조(도식)", "Data": "📊 데이터",
    "Code walkthrough": "💻 코드", "Instructions": "📖 지시어 해설",
    "Exercises": "🏃 실습 과제", "Resources": "🔗 자료", "My notes": "📝 내 노트",
    "Gate": "🚦 완료 게이트",
    // 멘토(논의) 노트
    "심화 학습": "🔬 심화 학습", "코드 보완": "🛠 코드 보완",
    "새 기능 아이디어": "💡 새 기능 아이디어", "다음 주 추천": "➡️ 다음 주 추천",
    "내 답변": "🗣 내 답변",
  };

  var cardKind = "__ALL__";

  function renderCards() {
    var host = document.getElementById("cards");
    host.innerHTML = "";
    var list = (DATA.cards || []).filter(function (c) {
      return cardKind === "__ALL__" || c.kind === cardKind;
    });
    if (!list.length) { host.appendChild(el("p", "muted", "해당 종류의 카드가 없습니다.")); return; }
    list.forEach(function (c) {
      var det = el("details", "ai-card card");
      det.id = "card-" + c.id;
      det.dataset.kind = c.kind || "";
      var links = [];
      if (c.projectUrl) links.push('<a href="' + esc(c.projectUrl) + '" target="_blank" rel="noopener">원본 프로젝트 ↗</a>');
      if (c.colabUrl) links.push('<a href="' + esc(c.colabUrl) + '" target="_blank" rel="noopener">▶ Colab 열기</a>');
      if (c.datasetUrl) links.push('<a href="' + esc(c.datasetUrl) + '" target="_blank" rel="noopener">데이터 ↗</a>');
      if (c.notebook) links.push('<a href="https://github.com/' + esc(DATA.repo) + '/blob/' + esc(DATA.branch) + '/' + esc(c.notebook) + '" target="_blank" rel="noopener">노트북</a>');

      var chips = [];
      if (c.framework) chips.push('<span class="badgep">' + esc(c.framework) + '</span>');
      if (c.arch) chips.push('<span class="badgep">' + esc(c.arch) + '</span>');
      if (c.modality) chips.push('<span class="badgep">' + esc(DATA.modalityLabels[c.modality] || c.modality) + '</span>');
      if (c.level) chips.push('<span class="badgep">' + esc(c.level) + '</span>');

      var summary = el("summary");
      summary.innerHTML =
        '<span class="kind">' + esc(c.kind || "card") + '</span> ' +
        '<span class="title">' + esc(c.topic) + (c.subtopic ? ' — ' + esc(c.subtopic) : "") + '</span>' +
        '<div class="sub2">' + chips.join(" ") + '</div>' +
        '<div class="links" style="margin-top:6px">' + links.join(" ") + '</div>';
      det.appendChild(summary);

      var body = el("div", "cardbody");
      det.appendChild(body);
      // 펼칠 때 한 번만 렌더(무거운 마크다운/mermaid 지연 로드)
      det.addEventListener("toggle", function () {
        if (det.open && !body.dataset.done) {
          body.dataset.done = "1";
          // 섹션은 저작(삽입) 순서 그대로 렌더 — 화이트리스트 없이 어떤 섹션이든 표시
          Object.keys(c.sections || {}).forEach(function (name) {
            var text = c.sections[name];
            if (!text) return;
            var sec = el("div", "sec");
            sec.appendChild(el("h4", null, SECTION_ICON[name] || name));
            var content = el("div");
            sec.appendChild(content);
            renderMarkdown(content, text);
            body.appendChild(sec);
          });
        }
      });
      host.appendChild(det);
    });
  }

  // ── 필터 옵션 채우기 + 이벤트 ────────────────────────────────────
  function initFilters() {
    var sel = document.getElementById("modFilter");
    var mods = {};
    (DATA.datasets || []).forEach(function (d) { mods[d.modality] = 1; });
    Object.keys(mods).forEach(function (m) {
      var o = el("option"); o.value = m;
      o.textContent = (DATA.modalityLabels[m] || m) + " (" + m + ")";
      sel.appendChild(o);
    });
    document.getElementById("dsSearch").addEventListener("input", renderDatasets);
    sel.addEventListener("change", renderDatasets);
    document.getElementById("openOnly").addEventListener("change", renderDatasets);
  }

  // ── 서브탭 전환(실습 진도 · 오픈 데이터 · 학습 카드) ──────────────
  function switchTab(name) {
    ["progress", "data", "cards"].forEach(function (p) {
      var panel = document.getElementById("panel-" + p);
      if (panel) panel.hidden = (p !== name);
    });
    Array.prototype.forEach.call(document.querySelectorAll("#subtabs button"), function (b) {
      b.classList.toggle("active", b.dataset.panel === name);
    });
  }
  function initTabs() {
    Array.prototype.forEach.call(document.querySelectorAll("#subtabs button"), function (b) {
      b.addEventListener("click", function () { switchTab(b.dataset.panel); });
    });
  }

  // ── 학습 카드 종류 필터 ─────────────────────────────────────────
  var KIND_KO = { mentor: "🗣 논의", roadmap: "🗺 로드맵", deepdive: "🔬 심화", concept: "📘 개념", project: "🔬 프로젝트", weekly: "🗓 주간", log: "🧪 로그" };
  function initKindFilter() {
    var host = document.getElementById("kindFilter");
    if (!host) return;
    var kinds = ["__ALL__"];
    (DATA.cards || []).forEach(function (c) { if (kinds.indexOf(c.kind) < 0) kinds.push(c.kind); });
    kinds.forEach(function (k) {
      var b = el("button", k === "__ALL__" ? "active" : null, k === "__ALL__" ? "전체" : (KIND_KO[k] || k));
      b.addEventListener("click", function () {
        cardKind = k;
        Array.prototype.forEach.call(host.children, function (x) { x.classList.remove("active"); });
        b.classList.add("active");
        renderCards();
      });
      host.appendChild(b);
    });
  }

  // ── 카드로 점프(실습 진도 배너 → 해당 학습 카드 열기) ────────────
  function openCard(cardId) {
    cardKind = "__ALL__";
    var host = document.getElementById("kindFilter");
    if (host) Array.prototype.forEach.call(host.children, function (x, i) { x.classList.toggle("active", i === 0); });
    renderCards();
    switchTab("cards");
    var det = document.getElementById("card-" + cardId);
    if (!det) return;
    det.open = true;
    det.scrollIntoView({ behavior: "smooth", block: "start" });
    det.classList.add("flash");
    setTimeout(function () { det.classList.remove("flash"); }, 1500);
  }
  window.__ailabOpenCard = openCard;  // 인라인 onclick에서 호출

  renderWeekly();
  initFilters();
  initTabs();
  initKindFilter();
  renderDatasets();
  renderCards();
})();
