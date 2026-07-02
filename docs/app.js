/* KMLE 대화형 웹 퀴즈 — 순수 JS, 의존성 없음
   - 문항: window.KMLE_QUESTIONS (questions.js, quiz.py --export로 생성)
   - 오답: localStorage("kmle_wrong")에 문항 id 기준으로 저장 */
"use strict";

const CIRCLED = ["①", "②", "③", "④", "⑤"];
const STORE_KEY = "kmle_wrong";
const ALL = Array.isArray(window.KMLE_QUESTIONS) ? window.KMLE_QUESTIONS : [];

const $ = (id) => document.getElementById(id);
const show = (el) => el.classList.remove("hidden");
const hide = (el) => el.classList.add("hidden");

/* ---------- 오답노트 저장소 ---------- */
function loadWrong() {
  try { return JSON.parse(localStorage.getItem(STORE_KEY)) || {}; }
  catch (e) { return {}; }
}
function saveWrong(map) { localStorage.setItem(STORE_KEY, JSON.stringify(map)); }
function todayStr() { return new Date().toISOString().slice(0, 10); }

function recordWrong(q, chosenIdx) {
  const map = loadWrong();
  map[q.id] = {
    id: q.id, subject: q.subject, type: q.type,
    question: q.question,
    chosen: chosenIdx, chosenText: q.options[chosenIdx],
    answer: q.answer - 1, answerText: q.options[q.answer - 1],
    coreNote: (q.explanation && q.explanation["임상핵심"]) || "",
    differ: (q.explanation && q.explanation["오답감별"]) || "",
    source: q.source || "", date: todayStr(),
  };
  saveWrong(map);
}
function removeWrong(id) { const m = loadWrong(); delete m[id]; saveWrong(m); }
function wrongIds() { return new Set(Object.keys(loadWrong())); }

/* ---------- 과목 목록 ---------- */
function subjects() {
  const seen = [];
  ALL.forEach((q) => { if (!seen.includes(q.subject)) seen.push(q.subject); });
  return seen;
}

/* ---------- 퀴즈 상태 ---------- */
let deck = [];
let pos = 0;
let correctCnt = 0;
let sessionWrong = [];

function isToday(q) { return q.created === todayStr(); }

function buildDeck() {
  const mode = $("mode").value;
  let list;
  if (mode === "today") {
    const subj = $("subject").value;
    list = ALL.filter(isToday);
    if (subj && subj !== "__ALL__") list = list.filter((q) => q.subject === subj);
  } else if (mode === "review") {
    const ids = wrongIds();
    list = ALL.filter((q) => ids.has(q.id));
  } else {
    const subj = $("subject").value;
    list = subj === "__ALL__" ? ALL.slice() : ALL.filter((q) => q.subject === subj);
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
      ? "오늘 생성된 문항이 아직 없습니다. (매일 오전 6시 루틴이 새 문항을 추가합니다)"
      : mode === "review"
      ? "오답노트에 쌓인 문항이 없습니다. 먼저 전체 문항을 풀어보세요."
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
  $("typeTag").textContent = q.type || "";
  $("subjTag").textContent = q.subject;
  $("vignette").textContent = q.vignette.trim();
  $("question").textContent = "Q. " + q.question.trim();

  const box = $("options");
  box.innerHTML = "";
  q.options.forEach((opt, i) => {
    const b = document.createElement("button");
    b.className = "opt";
    b.innerHTML = `<span class="num">${CIRCLED[i]}</span>${escapeHtml(opt)}`;
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
  const ex = q.explanation || {};
  const el = $("explanation");
  const verdict = ok
    ? `<div class="verdict ok">✅ 정답입니다! 정답: ${CIRCLED[q.answer - 1]}</div>`
    : `<div class="verdict bad">❌ 오답입니다. 당신의 선택: ${CIRCLED[chosenIdx]} / 정답: ${CIRCLED[q.answer - 1]}
       <div class="muted">↳ 이 오답은 오답노트에 자동 저장되었습니다.</div></div>`;
  const rows = [];
  const keys = ["진단", "정답근거", "오답감별", "임상핵심"];
  keys.forEach((k) => {
    if (ex[k]) rows.push(`<div class="item"><span class="k">${k}</span>${escapeHtml(ex[k])}</div>`);
  });
  const src = q.source ? `<div class="src">출처: ${escapeHtml(q.source)}</div>` : "";
  el.innerHTML = verdict + rows.join("") + src + renderAppendix(q.appendix);
  el.classList.remove("hidden");
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
        <div class="ans">정답 ${CIRCLED[q.answer - 1]} ${escapeHtml(q.options[q.answer - 1])}</div>
      </div>`).join("");
  }
}

/* ---------- 오답노트 화면 ---------- */
function renderWrongbook() {
  hide($("setup")); hide($("quiz")); hide($("result"));
  show($("wrongbook"));
  const map = loadWrong();
  const items = Object.values(map);
  $("wbCount").textContent = `(${items.length}개)`;
  const list = $("wbList");
  if (items.length === 0) { list.innerHTML = `<p class="muted">저장된 오답이 없습니다.</p>`; return; }
  // 과목별 그룹
  const bySub = {};
  items.forEach((w) => { (bySub[w.subject] = bySub[w.subject] || []).push(w); });
  list.innerHTML = Object.keys(bySub).map((sub) => {
    const rows = bySub[sub].map((w) => `<div class="w">
      <div class="whead">#${w.id} <span class="muted">${w.type || ""} · ${w.date}</span></div>
      <div class="wmeta">${escapeHtml(w.question)}</div>
      <div class="mine">내 선택 ${CIRCLED[w.chosen]} ${escapeHtml(w.chosenText)}</div>
      <div class="ans">정답 ${CIRCLED[w.answer]} ${escapeHtml(w.answerText)}</div>
      <div class="wmeta">핵심: ${escapeHtml(w.coreNote)}</div>
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
  let md = `# KMLE 오답노트 (웹 퀴즈 내보내기 · ${todayStr()})\n\n총 ${items.length}개\n`;
  Object.keys(bySub).forEach((sub) => {
    md += `\n## ${sub} (${bySub[sub].length})\n`;
    bySub[sub].forEach((w, i) => {
      md += `\n### ${i + 1}. #${w.id} ${w.type || ""}\n\n`;
      md += `| 항목 | 내용 |\n|------|------|\n`;
      md += `| 기록일 | ${w.date} |\n`;
      md += `| 문항 | ${w.question} |\n`;
      md += `| 내가 고른 답 | ${CIRCLED[w.chosen]} ${w.chosenText} |\n`;
      md += `| 정답 | ${CIRCLED[w.answer]} ${w.answerText} |\n`;
      md += `| 핵심 정리 | ${w.coreNote} |\n`;
      md += `| 감별 포인트 | ${w.differ} |\n`;
      md += `| 출처 | ${w.source} |\n`;
      md += `| 틀린 이유(직접 작성) |  |\n`;
      md += `| 복습 예정일(직접 작성) |  |\n`;
    });
  });
  download(`오답노트_${todayStr()}.md`, md, "text/markdown");
}

function exportCsv() {
  const items = Object.values(loadWrong());
  if (items.length === 0) { alert("저장된 오답이 없습니다."); return; }
  const esc = (s) => `"${String(s == null ? "" : s).replace(/"/g, '""')}"`;
  const head = ["id", "과목", "유형", "기록일", "문항", "내가고른답", "정답", "핵심정리", "감별", "출처"];
  const rows = items.map((w) => [
    w.id, w.subject, w.type, w.date, w.question,
    CIRCLED[w.chosen] + " " + w.chosenText,
    CIRCLED[w.answer] + " " + w.answerText,
    w.coreNote, w.differ, w.source,
  ].map(esc).join(","));
  download(`오답노트_${todayStr()}.csv`, "﻿" + head.join(",") + "\n" + rows.join("\n"), "text/csv");
}

/* ---------- 유틸 ---------- */
function escapeHtml(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
function updateWrongCount() {
  const n = Object.keys(loadWrong()).length;
  $("wrongCount").textContent = n ? `현재 오답노트에 ${n}개 저장됨` : "";
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
  // 과목 필터는 '전체 문항'과 '오늘의 문항'에서 사용(오답 복습에서는 숨김)
  $("subjectRow").style.display = mode === "review" ? "none" : "";
  if (mode === "today") populateSubjects(ALL.filter(isToday));
  else if (mode === "all") populateSubjects(ALL);
  const todayN = ALL.filter(isToday).length;
  const wrongN = Object.keys(loadWrong()).length;
  const hint = {
    today: `오늘(${todayStr()}) 생성된 문항 ${todayN}개를 풉니다. 매일 오전 6시 루틴이 새 문항을 추가합니다.`,
    all: `누적 ${ALL.length}개 전체(또는 선택 과목)를 풉니다. 이미 푼 문제가 다시 나올 수 있습니다.`,
    review: `오답노트에 쌓인 ${wrongN}개만 다시 풉니다.`,
  }[mode];
  $("modeHint").textContent = hint || "";
}

/* ---------- 초기화 ---------- */
function init() {
  if (ALL.length === 0) {
    document.body.insertAdjacentHTML("beforeend",
      '<p style="max-width:820px;margin:16px auto;color:#ffb4b4">문항 데이터를 불러오지 못했습니다. questions.js를 확인하세요.</p>');
    return;
  }
  populateSubjects(ALL);

  $("mode").onchange = onModeChange;
  onModeChange();
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
    if (confirm("오답노트를 모두 비웁니다. 계속할까요?")) { localStorage.removeItem(STORE_KEY); renderWrongbook(); updateWrongCount(); }
  };
  updateWrongCount();
}

document.addEventListener("DOMContentLoaded", init);
