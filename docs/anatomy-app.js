// 해부학 학습 화면 — window.MEDKOS_ANATOMY(자동 생성 번들)를 렌더한다.
// 정답·해설은 '정답 보기' 전에는 DOM에 넣지 않는다. 진행 기록은
// localStorage `medkos_anatomy_*` 네임스페이스만 사용(기존 퀴즈 키와 충돌 없음).
(function () {
  "use strict";
  var DATA = window.MEDKOS_ANATOMY || {};
  var CONCEPTS = DATA.concepts || [];
  var QUESTIONS = DATA.questions || [];
  var DAILY = DATA.daily || [];
  var GLOSSARY = DATA.glossary || [];
  var SOURCES = DATA.sources || [];
  var SCHEDULE = DATA.schedule || [];
  var DEADLINES = DATA.deadlines || {};

  var SRS_KEY = "medkos_anatomy_srs";     // {id: {box, due, history[]}}
  var WRONG_KEY = "medkos_anatomy_wrong"; // {id: {n, last}}
  var INTERVALS = [1, 3, 7, 14];

  var REGION_LABEL = {
    "back": "등", "thorax": "가슴", "upper-limb": "팔", "lower-limb": "다리",
    "head": "머리", "neck": "목", "abdomen": "배", "pelvis-perineum": "골반·샅",
    "multi": "여러 부위"
  };
  var STYLE_LABEL = {
    "spotter": "태깅 spotter", "layer-order": "층·순서", "branch-tree": "분지 트리",
    "course-tracing": "주행 추적", "relation": "인접관계", "distinction": "혼동 구별",
    "clinical-application": "임상 응용"
  };

  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function kstToday() {
    return new Intl.DateTimeFormat("sv-SE", { timeZone: "Asia/Seoul" })
      .format(new Date()); // YYYY-MM-DD
  }
  function daysBetween(a, b) {
    return Math.round((new Date(b) - new Date(a)) / 86400000);
  }
  function loadJson(key) {
    try { return JSON.parse(localStorage.getItem(key) || "{}"); } catch (e) { return {}; }
  }
  function saveJson(key, v) { localStorage.setItem(key, JSON.stringify(v)); }

  // ── SRS(1/3/7/14) ──────────────────────────────────────────
  function gradeItem(id, grade) { // grade: know | fuzzy | dontknow
    var srs = loadJson(SRS_KEY);
    var rec = srs[id] || { box: 0, history: [] };
    if (grade === "know") rec.box = Math.min(rec.box + 1, INTERVALS.length - 1);
    else if (grade === "dontknow") rec.box = 0;
    var iv = grade === "dontknow" ? 1 : INTERVALS[rec.box];
    var d = new Date(kstToday()); d.setDate(d.getDate() + iv);
    rec.due = d.toISOString().slice(0, 10);
    rec.history.push({ date: kstToday(), grade: grade });
    if (rec.history.length > 60) rec.history = rec.history.slice(-60);
    srs[id] = rec; saveJson(SRS_KEY, srs);
  }
  function markWrong(id) {
    var w = loadJson(WRONG_KEY);
    w[id] = { n: (w[id] ? w[id].n : 0) + 1, last: kstToday() };
    saveJson(WRONG_KEY, w);
  }
  function dueIds() {
    var srs = loadJson(SRS_KEY), today = kstToday(), out = [];
    Object.keys(srs).forEach(function (id) {
      if (srs[id].due && srs[id].due <= today) out.push(id);
    });
    return out;
  }

  function qById(id) {
    for (var i = 0; i < QUESTIONS.length; i++) if (QUESTIONS[i].id === id) return QUESTIONS[i];
    return null;
  }
  function refsHtml(refs) {
    if (!refs || !refs.length) return "";
    return '<div class="anat-srcref">출처: ' + refs.map(function (r) {
      var loc = r.page ? "p." + r.page : (r.section ? "§" + r.section : "");
      return esc(r.file) + (loc ? " · " + esc(loc) : "");
    }).join(" / ") + "</div>";
  }
  function confBadge(c) {
    var cls = c === "high" ? "conf-high" : (c === "low" ? "conf-low" : "conf-medium");
    return '<span class="conf-badge ' + cls + '">' + esc(c || "?") + "</span>";
  }

  // ── 탭 ────────────────────────────────────────────────────
  var VIEWS = { today: renderToday, region: renderRegion, relation: renderRelation,
                quiz: renderQuizSetup, review: renderReview, diagrams: renderDiagrams,
                sources: renderSources };
  var viewEls = { today: "anatToday", region: "anatRegion", relation: "anatRelation",
                  quiz: "anatQuiz", review: "anatReview", diagrams: "anatDiagrams",
                  sources: "anatSources" };
  document.querySelectorAll(".anat-tab").forEach(function (btn) {
    btn.addEventListener("click", function () { show(btn.dataset.view); });
  });
  function show(view) {
    document.querySelectorAll(".anat-tab").forEach(function (b) {
      var on = b.dataset.view === view;
      b.classList.toggle("active", on);
      b.setAttribute("aria-selected", on ? "true" : "false");
    });
    Object.keys(viewEls).forEach(function (v) {
      $(viewEls[v]).classList.toggle("hidden", v !== view);
    });
    VIEWS[view]();
  }

  // ── 오늘의 학습 ────────────────────────────────────────────
  function todayPlan() {
    var t = kstToday(), best = null;
    DAILY.forEach(function (p) { if (p.date <= t && (!best || p.date > best.date)) best = p; });
    return best;
  }
  function nextSession(t) {
    for (var i = 0; i < SCHEDULE.length; i++) if (SCHEDULE[i].date >= t) return SCHEDULE[i];
    return null;
  }
  function conceptById(id) {
    for (var i = 0; i < CONCEPTS.length; i++) if (CONCEPTS[i].id === id) return CONCEPTS[i];
    return null;
  }
  function say3(concepts) {
    var lines = [];
    concepts.forEach(function (c) {
      if (!c || !c.body) return;
      var m = c.body.split(/##\s*관계 문장[^\n]*\n/);
      if (m.length > 1) {
        m[1].split("\n").forEach(function (ln) {
          var t = ln.replace(/^\d+\.\s*/, "").trim();
          if (t && /^\d+\./.test(ln.trim())) lines.push(t);
        });
      }
    });
    return lines.slice(0, 3);
  }
  function renderToday() {
    var t = kstToday(), plan = todayPlan(), ns = nextSession(t);
    var due = dueIds();
    var d1 = DEADLINES.tagging1 ? daysBetween(t, DEADLINES.tagging1) : null;
    var d2 = DEADLINES.tagging2 ? daysBetween(t, DEADLINES.tagging2) : null;
    var done = DEADLINES.end && t > DEADLINES.end;
    var html = '<h2>오늘의 학습 <span class="muted">' + esc(t) + "</span></h2>";
    html += '<div class="anat-kpis">';
    html += kpi("다음 수업/시험", ns ? esc(ns.date) + (ns.exam ? " 🔴" : "") : "없음");
    if (d1 !== null && d1 >= 0) html += kpi("Tagging 1까지", "D-" + d1);
    if (d2 !== null && d2 >= 0) html += kpi("Tagging 2까지", "D-" + d2);
    html += kpi("오늘 예상", plan && plan.estMinutes ? "약 " + plan.estMinutes + "분" : "—");
    html += kpi("복습 due", due.length + "개", due.length > 0);
    html += "</div>";
    if (ns) html += '<p class="muted">다음: ' + esc(ns.topics.join(", ")) + "</p>";
    if (done) {
      html += '<div class="anat-item"><b>학습 루틴 종료(2026-10-19 Tagging 2 완료).</b>'
        + '<div class="imeta">새 콘텐츠는 더 생성되지 않는다. 복습 큐는 계속 사용할 수 있다.</div></div>';
    }
    if (!plan) {
      html += '<div class="anat-item">아직 생성된 일일 계획이 없다. 매일 05:00 KST 루틴이 '
        + '<code>content/anatomy/daily/</code>에 계획을 만들면 여기 표시된다.</div>';
    } else {
      html += '<h3>계획 (' + esc(plan.date) + " · " + esc(plan.phase) + ")</h3>";
      var cids = [];
      Object.keys(plan.concepts || {}).forEach(function (slot) {
        (plan.concepts[slot] || []).forEach(function (id) { cids.push(id); });
      });
      var todayConcepts = cids.map(conceptById).filter(Boolean);
      todayConcepts.forEach(function (c) { html += conceptCard(c, false); });
      html += '<div class="row"><button class="primary" id="startTodayQuiz">오늘 문항 '
        + (plan.questions || []).length + "개 + 복습 " + due.length + "개 풀기</button></div>";
      var s3 = say3(todayConcepts);
      if (s3.length) {
        html += '<div class="anat-say3"><h3>오늘 반드시 말로 설명할 3개 관계</h3><ol>'
          + s3.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ol></div>";
      }
    }
    $("anatToday").innerHTML = html;
    var btn = $("startTodayQuiz");
    if (btn) btn.addEventListener("click", function () {
      var ids = (plan.questions || []).concat(due);
      var qs = ids.map(qById).filter(Boolean);
      startQuiz(qs.length ? qs : QUESTIONS.slice());
    });
  }
  function kpi(k, v, warn) {
    return '<div class="anat-kpi"><div class="k">' + esc(k) + '</div><div class="v'
      + (warn ? " warn" : "") + '">' + v + "</div></div>";
  }

  // ── 부위별 ────────────────────────────────────────────────
  var curRegion = "pelvis-perineum";
  function renderRegion() {
    var counts = {};
    CONCEPTS.concat(QUESTIONS).forEach(function (x) {
      counts[x.region] = (counts[x.region] || 0) + 1;
    });
    GLOSSARY.forEach(function (g) { counts[g.region] = (counts[g.region] || 0); });
    var html = "<h2>부위별 탐색</h2><div class='anat-chips' role='group' aria-label='부위'>";
    Object.keys(REGION_LABEL).forEach(function (r) {
      if (r === "multi") return;
      html += '<button class="anat-chip' + (r === curRegion ? " active" : "") + '" data-region="'
        + r + '">' + esc(REGION_LABEL[r]) + ' <span class="muted">' + (counts[r] || 0) + "</span></button>";
    });
    html += "</div>";
    var cs = CONCEPTS.filter(function (c) { return c.region === curRegion; });
    var qs = QUESTIONS.filter(function (q) { return q.region === curRegion; });
    var gl = GLOSSARY.filter(function (g) { return g.region === curRegion; });
    html += "<h3>개념 카드 " + cs.length + "</h3>";
    html += cs.length ? cs.map(function (c) { return conceptCard(c, false); }).join("")
      : emptyBox("이 부위의 개념 카드가 아직 없다. 해당 회차 PDF가 인제스트되면 생성된다.");
    html += "<h3>문항 " + qs.length + "</h3>";
    if (qs.length) html += '<div class="row"><button class="primary" data-quizregion="'
      + curRegion + '" id="regionQuizBtn">이 부위 문항 풀기</button></div>';
    else html += emptyBox("이 부위 문항이 아직 없다.");
    html += "<h3>용어 " + gl.length + '개 <span class="muted">(★ = tagging 답 후보)</span></h3>';
    if (gl.length) {
      html += '<div class="anat-chips">' + gl.slice(0, 200).map(function (g) {
        return '<span class="anat-chip">' + (g.priority === "high" ? "★ " : "") + esc(g.ko)
          + (g.en ? ' <span class="muted">' + esc(g.en) + "</span>" : "") + "</span>";
      }).join("") + (gl.length > 200 ? '<span class="muted">… 외 ' + (gl.length - 200) + "개</span>" : "") + "</div>";
    } else html += emptyBox("용어가 아직 없다.");
    $("anatRegion").innerHTML = html;
    document.querySelectorAll("#anatRegion .anat-chip[data-region]").forEach(function (b) {
      b.addEventListener("click", function () { curRegion = b.dataset.region; renderRegion(); });
    });
    var rb = $("regionQuizBtn");
    if (rb) rb.addEventListener("click", function () {
      startQuiz(QUESTIONS.filter(function (q) { return q.region === curRegion; }));
    });
  }
  function emptyBox(msg) { return '<div class="anat-imgbox">' + esc(msg) + "</div>"; }

  // ── 관계 모드 ─────────────────────────────────────────────
  var curStyle = "";
  function renderRelation() {
    var styles = {};
    CONCEPTS.forEach(function (c) { if (c.conceptStyle) styles[c.conceptStyle] = 1; });
    var html = "<h2>관계 모드</h2><p class='muted'>층 · 칸 · 삼각/공간 · 동맥 분지 · 신경 주행 · 인접관계.</p>";
    html += "<div class='anat-chips'>";
    html += '<button class="anat-chip' + (curStyle === "" ? " active" : "") + '" data-style="">전체</button>';
    Object.keys(styles).forEach(function (s) {
      html += '<button class="anat-chip' + (s === curStyle ? " active" : "") + '" data-style="' + s + '">'
        + esc(STYLE_LABEL[s] || s) + "</button>";
    });
    html += "</div>";
    var cs = CONCEPTS.filter(function (c) { return !curStyle || c.conceptStyle === curStyle; });
    html += cs.length ? cs.map(function (c) { return conceptCard(c, true); }).join("")
      : emptyBox("해당 관계 유형의 카드가 아직 없다.");
    $("anatRelation").innerHTML = html;
    document.querySelectorAll("#anatRelation .anat-chip").forEach(function (b) {
      b.addEventListener("click", function () { curStyle = b.dataset.style; renderRelation(); });
    });
  }
  function treeHtml(node, depth) {
    if (!node) return "";
    var name = esc(node.name || "");
    var cls = depth === 0 ? "troot" : (name.indexOf("★") >= 0 ? "thigh" : "");
    var h = "<li" + '><span class="' + cls + '">' + name + "</span>";
    if (node.children && node.children.length) {
      h += "<ul>" + node.children.map(function (c) { return treeHtml(c, depth + 1); }).join("") + "</ul>";
    }
    return h + "</li>";
  }
  function conceptCard(c, withBody) {
    var h = '<article class="anat-item"><div class="ihead"><span class="ititle">'
      + esc(c.title) + "</span><span class='tag'>" + esc(REGION_LABEL[c.region] || c.region)
      + "</span>" + (c.conceptStyle ? '<span class="pill">' + esc(STYLE_LABEL[c.conceptStyle] || c.conceptStyle) + "</span>" : "")
      + confBadge(c.confidence) + "</div>";
    if (c.image) {
      h += '<div class="anat-imgbox"><img src="' + esc(c.image) + '" alt="'
        + esc(c.title) + ' 도해' + (c.imageOrigin === "claude-drawn-svg" ? " (자체 제작 모식도)" : "") + '">'
        + (c.imageOrigin === "claude-drawn-svg"
          ? '<div class="muted" style="font-size:.78rem;margin-top:4px">자체 제작 모식도 — 실제 비율이 아니라 관계·행선지를 보여주는 도식</div>' : "")
        + "</div>";
    }
    if (c.tree) h += '<nav class="anat-tree" aria-label="분지 트리"><ul>' + treeHtml(c.tree, 0) + "</ul></nav>";
    if (withBody || !c.tree) h += '<div class="ibody">' + esc(c.body).slice(0, 2400) + "</div>";
    h += refsHtml(c.refs) + "</article>";
    return h;
  }

  // ── 태깅 퀴즈 ─────────────────────────────────────────────
  var session = null;
  function renderQuizSetup() {
    var html = "<h2>태깅 퀴즈</h2>";
    html += "<div class='row'><label for='quizRegion'>부위</label><select id='quizRegion'>"
      + "<option value=''>전체</option>"
      + Object.keys(REGION_LABEL).filter(function (r) { return r !== "multi"; })
        .map(function (r) { return '<option value="' + r + '">' + esc(REGION_LABEL[r]) + "</option>"; }).join("")
      + "</select></div>";
    html += "<div class='row'><label for='quizStyle'>유형</label><select id='quizStyle'>"
      + "<option value=''>전체</option>"
      + Object.keys(STYLE_LABEL).map(function (s) {
        return '<option value="' + s + '">' + esc(STYLE_LABEL[s]) + "</option>"; }).join("")
      + "</select></div>";
    html += "<div class='row'><button class='primary' id='quizStartBtn'>시작</button>"
      + "<button id='quizWrongBtn'>오답만 풀기</button></div>";
    html += '<p class="muted">이미지 spotter는 검수(publishable) 완료 자산이 있을 때만 나온다. '
      + "지금은 텍스트 기반 spotter(단답)로 대체된다.</p>";
    $("anatQuiz").innerHTML = html;
    $("quizStartBtn").addEventListener("click", function () {
      var r = $("quizRegion").value, s = $("quizStyle").value;
      startQuiz(QUESTIONS.filter(function (q) {
        return (!r || q.region === r) && (!s || q.style === s);
      }));
    });
    $("quizWrongBtn").addEventListener("click", function () {
      var w = loadJson(WRONG_KEY);
      startQuiz(Object.keys(w).map(qById).filter(Boolean));
    });
  }
  function startQuiz(qs) {
    if (!qs || !qs.length) {
      show("quiz");
      $("anatQuiz").innerHTML = "<h2>태깅 퀴즈</h2>" + emptyBox("조건에 맞는 문항이 없다.")
        + '<div class="row"><button id="quizBackBtn">← 설정으로</button></div>';
      $("quizBackBtn").addEventListener("click", renderQuizSetup);
      return;
    }
    session = { qs: qs.slice(), i: 0, right: 0, wrong: [] };
    show("quiz");
    renderQuestion();
  }
  function renderQuestion() {
    var q = session.qs[session.i];
    var html = '<div class="quiz-top"><span class="badge">' + (session.i + 1) + " / "
      + session.qs.length + '</span><span class="tag">' + esc(STYLE_LABEL[q.style] || q.style)
      + '</span><span class="subj">' + esc(REGION_LABEL[q.region] || q.region) + "</span></div>";
    if (q.style === "spotter") {
      html += q.image
        ? '<div class="anat-imgbox"><img src="' + esc(q.image) + '" alt="태깅 문제 이미지(구조물 명칭이 가려져 있음)"></div>'
        : '<div class="anat-imgbox">이미지 없음 — 이 spotter는 아직 공개 검수 전이라 텍스트 설명으로 대체된다.</div>';
    }
    html += '<p class="question">' + esc(q.stem) + "</p><div id='anatOpts'></div>"
      + '<div id="anatAnswerBox"></div><div class="quiz-nav">'
      + '<button id="anatQuit">나가기</button></div>';
    $("anatQuiz").innerHTML = html;
    var opts = $("anatOpts");
    if (q.choices && q.choices.length) {
      q.choices.forEach(function (c, idx) {
        var b = document.createElement("button");
        b.className = "opt"; b.textContent = c;
        b.addEventListener("click", function () { answerMcq(q, idx, c); });
        opts.appendChild(b);
      });
    } else {
      opts.innerHTML = '<div class="anat-shortanswer">'
        + '<input id="anatShort" type="text" autocomplete="off" placeholder="구조물 이름을 말해보고 입력(선택)" aria-label="단답 입력">'
        + '<button class="primary" id="anatReveal">정답 보기</button></div>';
      $("anatReveal").addEventListener("click", function () { revealShort(q); });
      $("anatShort").addEventListener("keydown", function (e) {
        if (e.key === "Enter") revealShort(q);
      });
    }
    $("anatQuit").addEventListener("click", renderQuizSetup);
  }
  function letterOf(choice) { var m = /^([A-Z])\./.exec(choice); return m ? m[1] : choice; }
  function answerMcq(q, idx, choice) {
    var ok = letterOf(choice) === q.answer;
    document.querySelectorAll("#anatOpts .opt").forEach(function (b, i) {
      b.disabled = true;
      if (letterOf(b.textContent) === q.answer) b.classList.add("correct");
      if (i === idx && !ok) b.classList.add("wrong");
    });
    if (!ok) { markWrong(q.id); session.wrong.push(q.id); } else session.right++;
    showAnswer(q, ok ? "정답!" : "오답", ok);
  }
  function revealShort(q) {
    showAnswer(q, "정답 확인 — 스스로 채점하세요", null);
  }
  function showAnswer(q, verdict, ok) {
    // 정답·해설은 이 시점에만 DOM에 들어간다.
    var box = $("anatAnswerBox");
    var h = '<div class="anat-answer"><div class="verdict ' + (ok === false ? "bad" : "ok") + '">'
      + esc(verdict) + "</div><div><b>정답:</b> " + esc(q.answer) + "</div>";
    if (q.explanation) h += '<div class="ibody">' + esc(q.explanation) + "</div>";
    h += refsHtml(q.refs);
    h += '<div class="anat-confbtns" role="group" aria-label="자신감">'
      + '<button class="btn-know" data-g="know">확실 (다음 ' + INTERVALS[Math.min((loadJson(SRS_KEY)[q.id] || { box: 0 }).box + 1, 3)] + "일 뒤)</button>"
      + '<button class="btn-fuzzy" data-g="fuzzy">애매</button>'
      + '<button class="btn-dontknow" data-g="dontknow">모름 (내일 다시)</button></div>'
      + '<div class="quiz-nav"><button class="primary" id="anatNext">다음 →</button></div></div>';
    box.innerHTML = h;
    box.querySelectorAll("[data-g]").forEach(function (b) {
      b.addEventListener("click", function () {
        gradeItem(q.id, b.dataset.g);
        if (b.dataset.g === "dontknow") markWrong(q.id);
        b.parentElement.querySelectorAll("button").forEach(function (x) { x.disabled = true; });
      });
    });
    $("anatNext").addEventListener("click", nextQuestion);
    $("anatNext").focus();
  }
  function nextQuestion() {
    session.i++;
    if (session.i >= session.qs.length) return renderQuizResult();
    renderQuestion();
  }
  function renderQuizResult() {
    var html = "<h2>결과</h2><p class='score'>" + session.right + " / " + session.qs.length
      + " (MCQ 기준)</p>";
    if (session.wrong.length) {
      html += "<h3>오답 " + session.wrong.length + "개</h3>"
        + session.wrong.map(function (id) {
          var q = qById(id);
          return q ? '<div class="anat-item">' + esc(q.stem).slice(0, 120) + "…</div>" : "";
        }).join("");
      html += '<div class="row"><button class="primary" id="retryWrong">오답만 다시</button>'
        + '<button id="backSetup">설정으로</button></div>';
    } else {
      html += '<div class="row"><button id="backSetup">설정으로</button></div>';
    }
    $("anatQuiz").innerHTML = html;
    var r = $("retryWrong");
    if (r) r.addEventListener("click", function () {
      startQuiz(session.wrong.map(qById).filter(Boolean));
    });
    $("backSetup").addEventListener("click", renderQuizSetup);
  }

  // ── 복습 큐 ───────────────────────────────────────────────
  function renderReview() {
    var srs = loadJson(SRS_KEY), today = kstToday();
    var ids = Object.keys(srs);
    var due = ids.filter(function (id) { return srs[id].due && srs[id].due <= today; });
    var later = ids.filter(function (id) { return srs[id].due && srs[id].due > today; })
      .sort(function (a, b) { return srs[a].due < srs[b].due ? -1 : 1; });
    var html = "<h2>복습 큐 <span class='muted'>1 · 3 · 7 · 14일 간격</span></h2>";
    html += '<div class="anat-kpis">' + kpi("오늘 due", due.length + "개", due.length > 0)
      + kpi("예정", later.length + "개") + "</div>";
    if (due.length) {
      html += '<div class="row"><button class="primary" id="reviewStart">due 복습 시작</button></div>';
    } else html += emptyBox("오늘 복습할 항목이 없다. 퀴즈에서 모름/애매로 표시하면 여기 쌓인다.");
    if (later.length) {
      html += "<h3>예정</h3>" + later.slice(0, 30).map(function (id) {
        var q = qById(id);
        return '<div class="anat-item"><span class="muted">' + esc(srs[id].due) + "</span> "
          + esc(q ? q.stem.slice(0, 90) : id) + "</div>";
      }).join("");
    }
    $("anatReview").innerHTML = html;
    var b = $("reviewStart");
    if (b) b.addEventListener("click", function () {
      startQuiz(due.map(qById).filter(Boolean));
    });
  }

  // ── 출처·자료 ─────────────────────────────────────────────
  function renderSources() {
    var st = DATA.answersStats || {};
    var html = "<h2>출처·자료 현황</h2>";
    html += "<p class='muted'>원본은 Google Drive(비공개)에 있고 이 사이트에는 파생 학습"
      + " 데이터만 공개된다. 생성일 " + esc(DATA.generated || "?") + ".</p>";
    html += '<table class="src-table"><thead><tr><th>파일</th><th>폴더</th><th>회차</th>'
      + "<th>상태</th><th>페이지</th></tr></thead><tbody>";
    SOURCES.forEach(function (s) {
      var cls = s.status === "ingested" ? "st-ok"
        : (s.status === "missing_source" ? "st-miss" : "st-warn");
      html += "<tr><td>" + esc(s.name) + "</td><td>" + esc(s.folder || "-") + "</td><td>"
        + (s.session || "-") + '</td><td class="' + cls + '">' + esc(s.status)
        + "</td><td>" + (s.pages || "—") + "</td></tr>";
    });
    html += "</tbody></table>";
    html += "<h3>답-전용 자료(tagging 2차)</h3>";
    html += '<div class="anat-kpis">' + kpi("구조물", (st.total || 0) + "개")
      + kpi("번호 항목(답 후보)", (st.numbered || 0) + "개") + "</div>";
    html += '<p class="muted">번호 항목은 과거 태깅 답 후보로만 기록한다 — 원래 질문·핀'
      + " 위치를 복원하지 않으며, 새 문항은 강의 자료에서 같은 구조가 확인될 때만 만든다.</p>";
    $("anatSources").innerHTML = html;
  }

  // ── 도해·계보 갤러리 ───────────────────────────────────────
  // 자산(SVG)은 content 카드가 아니라 검색 색인에 안 잡힌다 → 별도 매니페스트
  // (diagrams-data.js, pipelines/export_diagrams_web.py)를 읽는다.
  var DG = (window.MEDKOS_DIAGRAMS || {});
  var DGI = DG.items || [];
  var DG_SEEN = "medkos_diagrams_seen";
  var dgState = { kind: "__ALL__", session: "__ALL__", variant: "labeled", q: "" };

  function dgSeen() {
    try { return localStorage.getItem(DG_SEEN) || ""; } catch (e) { return ""; }
  }
  function dgIsNew(it) {
    var sd = dgSeen();
    if (sd) return it.date > sd;
    return Math.round((new Date(kstToday()) - new Date(it.date)) / 86400000) <= 7;
  }
  function dgFiltered() {
    return DGI.filter(function (it) {
      if (dgState.kind !== "__ALL__" && it.kind !== dgState.kind) return false;
      if (dgState.session !== "__ALL__" && String(it.session || "") !== dgState.session) return false;
      if (dgState.variant !== "__ALL__" && it.variant !== dgState.variant) return false;
      if (dgState.q && (it.title + " " + it.file).toLowerCase().indexOf(dgState.q) < 0) return false;
      return true;
    });
  }
  function dgMate(it) {
    var other = it.variant === "labeled" ? "quiz" : "labeled";
    return DGI.filter(function (x) { return x.base === it.base && x.variant === other; })[0];
  }
  function dgTile(it) {
    var mate = dgMate(it);
    return '<figure class="dg-tile' + (dgIsNew(it) ? " is-new" : "") + '">'
      + '<a href="assets/anatomy/' + esc(it.file) + '" target="_blank" rel="noopener">'
      + '<img loading="lazy" src="assets/anatomy/' + esc(it.file) + '" alt="' + esc(it.title) + '" /></a>'
      + "<figcaption>"
      + '<span class="dg-kind dg-' + esc(it.kind) + '">' + esc(it.kindLabel) + "</span>"
      + (it.session ? '<span class="dg-sess">' + it.session + "회차</span>" : "")
      + (it.variant === "quiz" ? '<span class="dg-sess dg-quiz">퀴즈판</span>' : "")
      + '<span class="dg-title">' + esc(it.title) + "</span>"
      + '<span class="dg-links"><a href="assets/anatomy/' + esc(it.file)
      + '" target="_blank" rel="noopener">크게 보기</a>'
      + (mate ? ' · <a href="assets/anatomy/' + esc(mate.file) + '" target="_blank" rel="noopener">'
          + (mate.variant === "quiz" ? "퀴즈판" : "라벨판") + "</a>" : "")
      + "</span></figcaption></figure>";
  }
  function dgPaint() {
    var rows = dgFiltered(), byDate = {}, order = [];
    rows.forEach(function (it) {
      if (!byDate[it.date]) { byDate[it.date] = []; order.push(it.date); }
      byDate[it.date].push(it);
    });
    var html = order.map(function (d) {
      var items = byDate[d], n = items.filter(dgIsNew).length;
      return '<div class="wn-day"><h3 class="wn-date">' + esc(d) + " (" + weekdayKr(d) + ")"
        + '<span class="muted"> · ' + items.length + "장</span>"
        + (n ? ' <span class="wn-badge">NEW ' + n + "</span>" : "")
        + '</h3><div class="dg-grid">' + items.map(dgTile).join("") + "</div></div>";
    }).join("") || '<p class="muted">조건에 맞는 도해가 없습니다.</p>';
    var box = $("dgResults");
    if (box) box.innerHTML = html;
    var cnt = $("dgCount");
    if (cnt) cnt.textContent = rows.length + "장 · " + order.length + "일";
  }
  function weekdayKr(iso) {
    return ["일", "월", "화", "수", "목", "금", "토"][new Date(iso + "T00:00:00+09:00").getDay()];
  }
  function renderDiagrams() {
    if (!DGI.length) {
      $("anatDiagrams").innerHTML = '<p class="muted">도해 목록이 비어 있습니다. '
        + "<code>python pipelines/export_diagrams_web.py</code> 로 생성하세요.</p>";
      return;
    }
    var kinds = [], seenK = {};
    DGI.forEach(function (i) { if (!seenK[i.kind]) { seenK[i.kind] = i.kindLabel; kinds.push(i.kind); } });
    var sess = [];
    DGI.forEach(function (i) { if (i.session && sess.indexOf(i.session) < 0) sess.push(i.session); });
    sess.sort(function (a, b) { return a - b; });
    var nt = DGI.filter(dgIsNew).length;

    $("anatDiagrams").innerHTML =
      "<h2>도해·계보 <span class=\"muted\">만든 날짜순</span>"
      + (nt ? ' <span class="wn-badge">NEW ' + nt + "</span>" : "") + "</h2>"
      + '<p class="muted">직접 그린 도해와 분지 계보 트리. 날짜는 git에 처음 커밋된 날(KST)이다. '
      + "라벨판과 퀴즈판이 짝이라 <b>퀴즈판을 먼저 풀고 라벨판으로 채점</b>한다.</p>"
      + '<div class="filters">'
      + '<select id="dgKind"><option value="__ALL__">전체 종류</option>'
      + kinds.map(function (k) { return '<option value="' + esc(k) + '">' + esc(seenK[k]) + "</option>"; }).join("")
      + "</select>"
      + '<select id="dgSession"><option value="__ALL__">전체 회차</option>'
      + sess.map(function (v) { return '<option value="' + v + '">' + v + "회차</option>"; }).join("")
      + "</select>"
      + '<select id="dgVariant"><option value="labeled">라벨판만 보기</option>'
      + '<option value="quiz">퀴즈판만 보기</option><option value="__ALL__">둘 다</option></select>'
      + '<input type="search" id="dgQ" placeholder="제목으로 좁히기" />'
      + '<button id="dgSeenBtn" type="button" class="wn-btn">여기까지 봤음</button>'
      + '</div><p id="dgCount" class="muted"></p><div id="dgResults"></div>';

    $("dgKind").value = dgState.kind;
    $("dgSession").value = dgState.session;
    $("dgVariant").value = dgState.variant;
    $("dgQ").value = dgState.q;
    $("dgKind").addEventListener("change", function () { dgState.kind = this.value; dgPaint(); });
    $("dgSession").addEventListener("change", function () { dgState.session = this.value; dgPaint(); });
    $("dgVariant").addEventListener("change", function () { dgState.variant = this.value; dgPaint(); });
    $("dgQ").addEventListener("input", function () { dgState.q = this.value.trim().toLowerCase(); dgPaint(); });
    $("dgSeenBtn").addEventListener("click", function () {
      try { localStorage.setItem(DG_SEEN, DGI[0].date); } catch (e) { /* 무시 */ }
      renderDiagrams();
    });
    dgPaint();
  }

  // 초기 화면
  var hash = (location.hash || "").replace("#", "");
  show(VIEWS[hash] ? hash : "today");
})();
