/* MedKOS 대화형 웹 퀴즈 — 순수 JS, 의존성 없음
   - 문항: window.KMLE_QUESTIONS (questions.js), window.USMLE_QUESTIONS (questions_usmle.js)
   - 오답: localStorage("wrong_<exam>")에 문항 id 기준으로 시험별 분리 저장
   - USMLE는 Step 1(기초의학)/Step 2(임상) 필터를 지원 */
"use strict";

// KMLE 덱 = content/kmle(MedKOS SoT) + 레거시 quiz.py 번들. 둘 다 있으면 합친다.
const KMLE = [].concat(
  Array.isArray(window.KMLE_CONTENT_QUESTIONS) ? window.KMLE_CONTENT_QUESTIONS : [],
  Array.isArray(window.KMLE_QUESTIONS) ? window.KMLE_QUESTIONS : []
);
const USMLE = Array.isArray(window.USMLE_QUESTIONS) ? window.USMLE_QUESTIONS : [];
const CIRCLED = ["①", "②", "③", "④", "⑤"];
const ALPHA = ["A", "B", "C", "D", "E"];

const $ = (id) => document.getElementById(id);
const show = (el) => el.classList.remove("hidden");
const hide = (el) => el.classList.add("hidden");

/* ---------- 시험 컨텍스트 ---------- */
function exam() { return $("exam").value; }             // "kmle" | "usmle"
function isUsmle() { return exam() === "usmle"; }
function allQuestions() { return isUsmle() ? USMLE : KMLE; }
function label(i) { return (isUsmle() ? ALPHA : CIRCLED)[i] || String(i + 1); }
function storeKey() { return "wrong_" + exam(); }

/* USMLE에서 선택된 Step 으로 필터한 기준 문항 목록 */
function baseList() {
  let list = allQuestions().slice();
  if (isUsmle()) {
    const step = $("step").value;
    if (step && step !== "__ALL__") list = list.filter((q) => q.step === step);
  }
  return list;
}

/* ---------- 오답노트 저장소(시험별) ---------- */
function loadWrong() {
  try { return JSON.parse(localStorage.getItem(storeKey())) || {}; }
  catch (e) { return {}; }
}
function saveWrong(map) { localStorage.setItem(storeKey(), JSON.stringify(map)); }
// 한국시간(KST=UTC+9) 기준 '오늘'. 콘텐츠 date도 KST로 스탬프하므로 '오늘의 문항'이
// 한국 날짜와 일치한다(UTC로 하면 새벽 생성분이 하루 밀려 안 잡힘).
function todayStr() { return new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10); }

function recordWrong(q, chosenIdx) {
  const map = loadWrong();
  map[q.id] = {
    id: q.id, exam: exam(), subject: q.subject, step: q.step || "", type: q.type,
    question: q.question,
    chosen: chosenIdx, chosenText: q.options[chosenIdx],
    answer: q.answer - 1, answerText: q.options[q.answer - 1],
    coreNote: q.explanationText ? "" : (q.explanation && q.explanation["임상핵심"]) || "",
    differ: q.explanationText ? "" : (q.explanation && q.explanation["오답감별"]) || "",
    source: q.source || "", date: todayStr(),
  };
  saveWrong(map);
}
function removeWrong(id) { const m = loadWrong(); delete m[id]; saveWrong(m); }
function wrongIds() { return new Set(Object.keys(loadWrong())); }

/* ---------- 퀴즈 상태 ---------- */
let deck = [];
let pos = 0;
let correctCnt = 0;
let sessionWrong = [];

function isToday(q) { return q.created === todayStr(); }

function buildDeck() {
  const mode = $("mode").value;
  const base = baseList();
  let list;
  if (mode === "today") {
    const subj = $("subject").value;
    list = base.filter(isToday);
    if (subj && subj !== "__ALL__") list = list.filter((q) => q.subject === subj);
  } else if (mode === "review") {
    const ids = wrongIds();
    list = base.filter((q) => ids.has(q.id));
  } else {
    const subj = $("subject").value;
    list = subj === "__ALL__" ? base : base.filter((q) => q.subject === subj);
  }
  if ($("shuffle").checked) {
    for (let i = list.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [list[i], list[j]] = [list[j], list[i]];
    }
  }
  return list;
}

function startQuiz() {
  deck = buildDeck();
  if (deck.length === 0) {
    const mode = $("mode").value;
    const msg = mode === "today"
      ? "오늘 생성된 문항이 아직 없습니다."
      : mode === "review"
      ? "이 시험의 오답노트에 쌓인 문항이 없습니다. 먼저 전체 문항을 풀어보세요."
      : "조건에 맞는 문항이 없습니다.";
    alert(msg);
    return;
  }
  pos = 0; correctCnt = 0; sessionWrong = [];
  hide($("setup")); hide($("result")); hide($("wrongbook"));
  show($("quiz"));
  renderQuestion();
}

function renderQuestion() {
  const q = deck[pos];
  $("progress").textContent = `${pos + 1} / ${deck.length}`;
  $("typeTag").textContent = q.step ? `${q.step} · ${q.type || ""}` : (q.type || "");
  $("subjTag").textContent = q.subject;
  $("vignette").textContent = q.vignette.trim();
  $("clindata").innerHTML = dataBox(q);
  $("question").textContent = "Q. " + q.question.trim();

  const box = $("options");
  box.innerHTML = "";
  q.options.forEach((opt, i) => {
    const b = document.createElement("button");
    b.className = "opt";
    b.innerHTML = `<span class="num">${label(i)}</span>${escapeHtml(opt)}`;
    b.onclick = () => grade(i, b);
    box.appendChild(b);
  });

  const ex = $("explanation");
  ex.classList.add("hidden");
  ex.innerHTML = "";
  hide($("nextBtn"));
}

function grade(chosenIdx, btn) {
  const q = deck[pos];
  const correctIdx = q.answer - 1;
  const buttons = Array.from($("options").children);
  buttons.forEach((b, i) => {
    b.disabled = true;
    if (i === correctIdx) b.classList.add("correct");
    if (i === chosenIdx && chosenIdx !== correctIdx) b.classList.add("wrong");
  });

  const ok = chosenIdx === correctIdx;
  if (ok) {
    correctCnt++;
  } else {
    recordWrong(q, chosenIdx);
    sessionWrong.push(q);
  }
  renderExplanation(q, chosenIdx, ok);
  show($("nextBtn"));
  updateWrongCount();
}

function renderExplanation(q, chosenIdx, ok) {
  const el = $("explanation");
  const verdict = ok
    ? `<div class="verdict ok">✅ 정답입니다! 정답: ${label(q.answer - 1)}</div>`
    : `<div class="verdict bad">❌ 오답입니다. 당신의 선택: ${label(chosenIdx)} / 정답: ${label(q.answer - 1)}
       <div class="muted">↳ 이 오답은 오답노트에 자동 저장되었습니다.</div></div>`;

  let bodyHtml;
  if (q.explanationItems && q.explanationItems.length) {
    // 구조화 해설(항목별 박스) + (있으면) 부록 결정표 박스.
    bodyHtml = renderExplItems(q.explanationItems) + renderAppendix(q.appendix);
  } else if (q.explanationText) {
    bodyHtml = `<pre class="expl-text">${escapeHtml(q.explanationText)}</pre>` + renderAppendix(q.appendix);
  } else {
    const ex = q.explanation || {};
    const rows = [];
    ["진단", "정답근거", "오답감별", "임상핵심"].forEach((k) => {
      if (ex[k]) rows.push(`<div class="expl-item"><span class="k">${k}</span>${fmtExplValue(ex[k])}</div>`);
    });
    const src = q.source ? `<div class="src">출처: ${escapeHtml(q.source)}</div>` : "";
    bodyHtml = rows.join("") + src + renderAppendix(q.appendix);
  }
  el.innerHTML = verdict + bodyHtml;
  el.classList.remove("hidden");
}

// 해설 값에서 보기 반박 (A)…(B)… 은 각 줄로 분리해 가독성을 높인다.
function fmtExplValue(v) {
  let s = escapeHtml(v);
  if ((s.match(/\([A-E]\)/g) || []).length >= 2) {
    s = s.replace(/\s*(?=\([A-E]\)\s)/g, "\n").replace(/^\n+/, "");
    return `<span class="optlines">${s}</span>`;
  }
  return s;
}

// 구조화 해설: `- **키**: 값` 항목들을 각각 간격을 둔 박스로 렌더한다.
function renderExplItems(items) {
  return items.map((it) =>
    `<div class="expl-item"><span class="k">${escapeHtml(it.k)}</span>${fmtExplValue(it.v)}</div>`
  ).join("");
}

// 구조화 임상 자료(활력징후·검사소견)를 문제 상단 박스로 렌더한다.
function dataBox(q) {
  const vit = Array.isArray(q.vitals) ? q.vitals : [];
  const labs = Array.isArray(q.labs) ? q.labs : [];
  if (!vit.length && !labs.length) return "";
  let html = '<div class="databox">';
  if (vit.length) {
    html += '<div class="db-h">활력징후</div><div class="db-vitals">'
      + vit.map((v) => `<span class="vchip"><b>${escapeHtml(v.name)}</b> ${escapeHtml(v.value)}</span>`).join("")
      + "</div>";
  }
  if (labs.length) {
    html += '<div class="db-h">검사 소견</div>'
      + '<table class="db-labs"><thead><tr><th>항목</th><th>값</th><th>참고치</th></tr></thead><tbody>'
      + labs.map((l) => `<tr><td>${escapeHtml(l.name)}</td><td>${escapeHtml(l.value)}</td><td class="ref">${escapeHtml(l.ref || "")}</td></tr>`).join("")
      + "</tbody></table>";
  }
  return html + "</div>";
}

function renderAppendix(ap) {
  if (!ap) return "";
  const parts = [];
  if (ap["가이드라인"]) {
    parts.push(`<div class="item"><span class="k">가이드라인</span></div><pre class="guide-table">${escapeHtml(ap["가이드라인"].trim())}</pre>`);
  }
  if (ap["최신지견"]) {
    parts.push(`<div class="item"><span class="k">최신지견</span>${escapeHtml(ap["최신지견"])}</div>`);
  }
  if (Array.isArray(ap["참고문헌"]) && ap["참고문헌"].length) {
    const refs = ap["참고문헌"].map((r) => `<li>${escapeHtml(r)}</li>`).join("");
    parts.push(`<div class="item"><span class="k">참고문헌</span></div><ul class="refs">${refs}</ul>`);
  }
  if (parts.length === 0) return "";
  return `<div class="appendix"><div class="appendix-head">부록 — 함께 알아두면 좋은 내용</div>${parts.join("")}</div>`;
}

function nextQuestion() {
  pos++;
  if (pos >= deck.length) { finish(); return; }
  renderQuestion();
}

function finish() {
  hide($("quiz"));
  show($("result"));
  const graded = correctCnt + sessionWrong.length;
  const rate = graded ? Math.round((correctCnt / graded) * 100) : 0;
  $("score").textContent = `채점 ${graded}문항 · 정답 ${correctCnt} · 오답 ${sessionWrong.length} · 정답률 ${rate}%`;
  const wl = $("wrongList");
  if (sessionWrong.length === 0) {
    wl.innerHTML = `<p class="muted">이번 세션 오답이 없습니다. 👏</p>`;
  } else {
    wl.innerHTML = `<h3>이번 세션 오답 (오답노트에 저장됨)</h3>` +
      sessionWrong.map((q) => `<div class="w">
        <div class="whead">[${q.subject}] #${q.id}</div>
        <div class="wmeta">${escapeHtml(q.question)}</div>
        <div class="ans">정답 ${label(q.answer - 1)} ${escapeHtml(q.options[q.answer - 1])}</div>
      </div>`).join("");
  }
}

/* ---------- 오답노트 화면 ---------- */
function renderWrongbook() {
  hide($("setup")); hide($("quiz")); hide($("result"));
  show($("wrongbook"));
  const map = loadWrong();
  const items = Object.values(map);
  $("wbCount").textContent = `(${exam().toUpperCase()} · ${items.length}개)`;
  const list = $("wbList");
  if (items.length === 0) { list.innerHTML = `<p class="muted">저장된 오답이 없습니다.</p>`; return; }
  const bySub = {};
  items.forEach((w) => { (bySub[w.subject] = bySub[w.subject] || []).push(w); });
  list.innerHTML = Object.keys(bySub).map((sub) => {
    const rows = bySub[sub].map((w) => `<div class="w">
      <div class="whead">#${w.id} <span class="muted">${w.step ? w.step + " · " : ""}${w.type || ""} · ${w.date}</span></div>
      <div class="wmeta">${escapeHtml(w.question)}</div>
      <div class="mine">내 선택 ${label(w.chosen)} ${escapeHtml(w.chosenText)}</div>
      <div class="ans">정답 ${label(w.answer)} ${escapeHtml(w.answerText)}</div>
      ${w.coreNote ? `<div class="wmeta">핵심: ${escapeHtml(w.coreNote)}</div>` : ""}
      <button data-del="${w.id}">이 오답 삭제</button>
    </div>`).join("");
    return `<h3>${sub} (${bySub[sub].length})</h3>` + rows;
  }).join("");
  list.querySelectorAll("button[data-del]").forEach((b) => {
    b.onclick = () => { removeWrong(b.getAttribute("data-del")); renderWrongbook(); updateWrongCount(); };
  });
}

/* ---------- 내보내기 ---------- */
function download(filename, text, mime) {
  const blob = new Blob([text], { type: (mime || "text/plain") + ";charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click();
  document.body.removeChild(a); URL.revokeObjectURL(url);
}

function exportMarkdown() {
  const items = Object.values(loadWrong());
  if (items.length === 0) { alert("저장된 오답이 없습니다."); return; }
  const bySub = {};
  items.forEach((w) => { (bySub[w.subject] = bySub[w.subject] || []).push(w); });
  let md = `# ${exam().toUpperCase()} 오답노트 (웹 퀴즈 내보내기 · ${todayStr()})\n\n총 ${items.length}개\n`;
  Object.keys(bySub).forEach((sub) => {
    md += `\n## ${sub} (${bySub[sub].length})\n`;
    bySub[sub].forEach((w, i) => {
      md += `\n### ${i + 1}. #${w.id} ${w.step ? w.step + " · " : ""}${w.type || ""}\n\n`;
      md += `| 항목 | 내용 |\n|------|------|\n`;
      md += `| 기록일 | ${w.date} |\n`;
      md += `| 문항 | ${w.question} |\n`;
      md += `| 내가 고른 답 | ${label(w.chosen)} ${w.chosenText} |\n`;
      md += `| 정답 | ${label(w.answer)} ${w.answerText} |\n`;
      if (w.coreNote) md += `| 핵심 정리 | ${w.coreNote} |\n`;
      md += `| 출처 | ${w.source} |\n`;
      md += `| 틀린 이유(직접 작성) |  |\n`;
      md += `| 복습 예정일(직접 작성) |  |\n`;
    });
  });
  download(`오답노트_${exam()}_${todayStr()}.md`, md, "text/markdown");
}

function exportCsv() {
  const items = Object.values(loadWrong());
  if (items.length === 0) { alert("저장된 오답이 없습니다."); return; }
  const esc = (s) => `"${String(s == null ? "" : s).replace(/"/g, '""')}"`;
  const head = ["id", "시험", "step", "과목", "유형", "기록일", "문항", "내가고른답", "정답", "출처"];
  const rows = items.map((w) => [
    w.id, (w.exam || exam()).toUpperCase(), w.step || "", w.subject, w.type, w.date, w.question,
    label(w.chosen) + " " + w.chosenText,
    label(w.answer) + " " + w.answerText,
    w.source,
  ].map(esc).join(","));
  download(`오답노트_${exam()}_${todayStr()}.csv`, "﻿" + head.join(",") + "\n" + rows.join("\n"), "text/csv");
}

/* ---------- 유틸 ---------- */
function escapeHtml(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
function updateWrongCount() {
  const n = Object.keys(loadWrong()).length;
  $("wrongCount").textContent = n ? `현재 ${exam().toUpperCase()} 오답노트에 ${n}개 저장됨` : "";
}

function populateSubjects(list) {
  const sel = $("subject");
  sel.innerHTML = "";
  const optAll = document.createElement("option");
  optAll.value = "__ALL__";
  optAll.textContent = `전체 (${list.length})`;
  sel.appendChild(optAll);
  const seen = [];
  list.forEach((q) => { if (!seen.includes(q.subject)) seen.push(q.subject); });
  seen.forEach((s) => {
    const cnt = list.filter((q) => q.subject === s).length;
    const o = document.createElement("option");
    o.value = s; o.textContent = `${s} (${cnt})`;
    sel.appendChild(o);
  });
}

function onModeChange() {
  const mode = $("mode").value;
  const base = baseList();
  $("subjectRow").style.display = mode === "review" ? "none" : "";
  if (mode === "today") populateSubjects(base.filter(isToday));
  else if (mode === "all") populateSubjects(base);
  const todayN = base.filter(isToday).length;
  const wrongN = Object.keys(loadWrong()).length;
  const stepTxt = isUsmle() && $("step").value !== "__ALL__" ? ` [${$("step").value}]` : "";
  const hint = {
    today: `오늘(${todayStr()}) 생성된 문항 ${todayN}개를 풉니다.`,
    all: `${exam().toUpperCase()}${stepTxt} 누적 ${base.length}개 전체(또는 선택 과목)를 풉니다.`,
    review: `${exam().toUpperCase()} 오답노트에 쌓인 ${wrongN}개만 다시 풉니다.`,
  }[mode];
  $("modeHint").textContent = hint || "";
}

function onExamChange() {
  const usmle = isUsmle();
  $("stepRow").style.display = usmle ? "" : "none";
  // USMLE도 '오늘의 문항'을 지원한다(레코드에 created=생성일 포함). 옵션 항상 활성화.
  const todayOpt = $("mode").querySelector('option[value="today"]');
  if (todayOpt) todayOpt.disabled = false;
  onModeChange();
  updateWrongCount();
}

/* ---------- 초기화 ---------- */
function init() {
  if (KMLE.length === 0 && USMLE.length === 0) {
    document.body.insertAdjacentHTML("beforeend",
      '<p style="max-width:820px;margin:16px auto;color:#ffb4b4">문항 데이터를 불러오지 못했습니다. questions.js / questions_usmle.js를 확인하세요.</p>');
    return;
  }
  $("exam").onchange = onExamChange;
  $("step").onchange = onModeChange;
  $("mode").onchange = onModeChange;
  onExamChange();

  $("startBtn").onclick = startQuiz;
  $("viewWrongBtn").onclick = renderWrongbook;
  $("nextBtn").onclick = nextQuestion;
  $("quitBtn").onclick = finish;
  $("restartBtn").onclick = () => { hide($("result")); show($("setup")); onModeChange(); updateWrongCount(); };
  $("reviewBtn").onclick = () => { $("mode").value = "review"; hide($("result")); startQuiz(); };
  $("backBtn").onclick = () => { hide($("wrongbook")); show($("setup")); onModeChange(); updateWrongCount(); };
  $("exportMdBtn").onclick = exportMarkdown;
  $("exportCsvBtn").onclick = exportCsv;
  $("clearBtn").onclick = () => {
    if (confirm(`${exam().toUpperCase()} 오답노트를 모두 비웁니다. 계속할까요?`)) { localStorage.removeItem(storeKey()); renderWrongbook(); updateWrongCount(); }
  };
  updateWrongCount();
}

document.addEventListener("DOMContentLoaded", init);
