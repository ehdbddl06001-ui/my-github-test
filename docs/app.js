/* MedKOS 대화형 웹 퀴즈 — 순수 JS, 의존성 없음 (PWA 겸용)
   - 문항: window.KMLE_QUESTIONS (questions.js) + window.KMLE_CONTENT_QUESTIONS (questions_kmle_content.js),
           window.USMLE_QUESTIONS (questions_usmle.js),
           window.IMAGING_QUESTIONS (questions_imaging.js — 오픈데이터 실제 영상 문항, 국시형/USMLE형 혼합)
   - 오답: localStorage("wrong_<exam>")에 문항 id 기준으로 시험별 분리 저장
           + 삭제 묘비(wrong_removed_<exam>)로 기기 간 동기화 시 삭제가 되살아나지 않게 한다
   - 동기화: 같은 출처의 /api/wrong (Cloudflare Pages Function) 이 있으면 GitHub 저장소와 합친다.
             GitHub Pages 처럼 함수가 없는 호스트에서는 404 → 조용히 로컬 모드.
   - USMLE는 Step 1(기초의학)/Step 2(임상) 필터, 영상은 국시형/USMLE형 필터를 지원 */
"use strict";

// 각 문항에 출처 덱(src)을 박아 둔다 — '최신 세트'는 출처별 최신 날짜를 합쳐서 만든다.
function tagSrc(list, src) { list.forEach((q) => { if (!q.src) q.src = src; }); return list; }
const IMAGING = tagSrc(Array.isArray(window.IMAGING_QUESTIONS) ? window.IMAGING_QUESTIONS : [], "imaging");
// KMLE 덱 = content/kmle(MedKOS SoT) + 레거시 quiz.py 번들 + 영상 세트의 국시형 문항(그날 만든 문항을 한 자리에서).
const KMLE = [].concat(
  tagSrc(Array.isArray(window.KMLE_CONTENT_QUESTIONS) ? window.KMLE_CONTENT_QUESTIONS : [], "kmle"),
  tagSrc(Array.isArray(window.KMLE_QUESTIONS) ? window.KMLE_QUESTIONS : [], "kmle"),
  IMAGING.filter((q) => q.style === "kmle_style")
);
// USMLE 덱 = content/usmle + 영상 세트의 USMLE형 문항(step="Step 2" 로 임상 필터 통과).
const USMLE = [].concat(
  tagSrc(Array.isArray(window.USMLE_QUESTIONS) ? window.USMLE_QUESTIONS : [], "usmle"),
  IMAGING.filter((q) => q.style === "usmle_style")
);
const CIRCLED = ["①", "②", "③", "④", "⑤"];
const ALPHA = ["A", "B", "C", "D", "E"];
const EXAM_NAME = { kmle: "KMLE", usmle: "USMLE", imaging: "영상" };

const $ = (id) => document.getElementById(id);
const show = (el) => el.classList.remove("hidden");
const hide = (el) => el.classList.add("hidden");

/* ---------- 시험 컨텍스트 ---------- */
function exam() { return $("exam").value; }             // "kmle" | "usmle" | "imaging"
function isUsmle() { return exam() === "usmle"; }
function isImaging() { return exam() === "imaging"; }
function examName(e) { return EXAM_NAME[e || exam()] || String(e || exam()).toUpperCase(); }
function allQuestions() { return isUsmle() ? USMLE : isImaging() ? IMAGING : KMLE; }
// 보기 글머리: USMLE 와 영상 덱의 USMLE형은 A~E, 나머지(국시)는 ①~⑤.
function labelsFor(q) {
  const alpha = isUsmle() || (q && q.style === "usmle_style") || (q && q.exam === "usmle");
  return alpha ? ALPHA : CIRCLED;
}
function label(i, q) { return labelsFor(q || deck[pos])[i] || String(i + 1); }
function storeKey(e) { return "wrong_" + (e || exam()); }
function removedKey(e) { return "wrong_removed_" + (e || exam()); }
// 영상 세트 문항은 어느 덱에서 풀었든 오답을 wrong_imaging 에 모은다(같은 문항이 두 곳에 갈라지지 않게).
function wrongExamOf(q) { return q && q.exam === "imaging" ? "imaging" : exam(); }

/* 선택된 Step(USMLE)·형식(영상)으로 필터한 기준 문항 목록 */
function baseList() {
  let list = allQuestions().slice();
  if (isUsmle()) {
    const step = $("step").value;
    if (step && step !== "__ALL__") list = list.filter((q) => q.step === step);
  }
  if (isImaging()) {
    const st = $("style").value;
    if (st && st !== "__ALL__") list = list.filter((q) => q.style === st);
    // 기본은 영상이 붙은 문항만. 세트의 텍스트 문항은 KMLE/USMLE 덱(그날 세트)에서 함께 풀린다.
    if ($("imgOnly") && $("imgOnly").checked) list = list.filter((q) => q.figureImg && q.figureImg.src);
  }
  return list;
}

/* ---------- 오답노트 저장소(시험별) ---------- */
function loadWrong(e) {
  try { return JSON.parse(localStorage.getItem(storeKey(e))) || {}; }
  catch (err) { return {}; }
}
function saveWrong(map, e) { localStorage.setItem(storeKey(e), JSON.stringify(map)); }
function loadRemoved(e) {
  try { return JSON.parse(localStorage.getItem(removedKey(e))) || {}; }
  catch (err) { return {}; }
}
function saveRemoved(map, e) { localStorage.setItem(removedKey(e), JSON.stringify(map)); }
// 한국시간(KST=UTC+9) 기준 '오늘'. 콘텐츠 date도 KST로 스탬프하므로 '오늘의 문항'이
// 한국 날짜와 일치한다(UTC로 하면 새벽 생성분이 하루 밀려 안 잡힘).
function todayStr() { return new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10); }
function nowIso() { return new Date().toISOString(); }

function recordWrong(q, chosenIdx) {
  const we = wrongExamOf(q);
  const map = loadWrong(we);
  const prev = map[q.id] || {};
  map[q.id] = {
    id: q.id, exam: we, subject: q.subject, step: q.step || "", type: q.type,
    style: q.style || "", modality: q.modality || "",
    question: q.question,
    chosen: chosenIdx, chosenText: q.options[chosenIdx],
    answer: q.answer - 1, answerText: q.options[q.answer - 1],
    coreNote: q.explanationText ? "" : (q.explanation && q.explanation["임상핵심"]) || "",
    differ: q.explanationText ? "" : (q.explanation && q.explanation["오답감별"]) || "",
    source: q.source || "", date: todayStr(), device: SYNC.device,
    note: prev.note || "",
  };
  saveWrong(map, we);
  const rm = loadRemoved(we);
  if (rm[q.id]) { delete rm[q.id]; saveRemoved(rm, we); }   // 다시 틀렸으면 묘비 철회
  scheduleSync();
}
function removeWrong(id) {
  const m = loadWrong(); delete m[id]; saveWrong(m);
  const rm = loadRemoved(); rm[id] = nowIso(); saveRemoved(rm);
  scheduleSync();
}
function setWrongNote(id, note) {
  const m = loadWrong();
  if (!m[id]) return;
  m[id].note = note;
  m[id].date = todayStr();      // 메모를 고친 기기의 값이 병합에서 이기도록 기록일 갱신
  saveWrong(m);
  scheduleSync();
}
// 이 덱의 오답 id 집합 — 덱 자체의 오답 + (영상 문항이 섞인 덱이면) 영상 오답까지.
function wrongIds() {
  const ids = new Set(Object.keys(loadWrong()));
  if (!isImaging()) Object.keys(loadWrong("imaging")).forEach((id) => ids.add(id));
  return ids;
}

/* ---------- 오답 동기화(/api/wrong) ---------- */
const SYNC = {
  url: "api/wrong",
  available: null,          // null=미확인, true/false
  timer: null,
  busy: false,
  device: deviceId(),
  lastError: "",
};
function deviceId() {
  try {
    let id = localStorage.getItem("medkos_device");
    if (!id) {
      const kind = /Android/i.test(navigator.userAgent) ? "android"
        : /iPhone|iPad/i.test(navigator.userAgent) ? "ios" : "pc";
      id = kind + "-" + Math.random().toString(36).slice(2, 8);
      localStorage.setItem("medkos_device", id);
    }
    return id;
  } catch (e) { return "web"; }
}
function syncKey() { try { return localStorage.getItem("medkos_sync_key") || ""; } catch (e) { return ""; } }
function syncHeaders() {
  const h = { "content-type": "application/json" };
  const k = syncKey();
  if (k) h["x-sync-key"] = k;
  return h;
}
function setSyncStatus(text, cls) {
  const el = $("syncStatus");
  if (!el) return;
  el.textContent = text;
  el.className = "muted sync " + (cls || "");
}
function scheduleSync() {
  if (SYNC.available === false || location.protocol === "file:") return;
  clearTimeout(SYNC.timer);
  SYNC.timer = setTimeout(() => syncAll(true), 2500);
}
// 현재 덱과 영상 오답을 함께 동기화한다(영상 문항은 어느 덱에서 풀어도 wrong_imaging 에 쌓이므로).
async function syncAll(quiet) {
  const list = isImaging() ? ["imaging"] : [exam(), "imaging"];
  for (const e of list) {
    await syncNow(e, quiet || e !== exam());
    if (SYNC.available === false) break;
  }
}
async function syncNow(e, quiet) {
  if (location.protocol === "file:") { setSyncStatus("로컬 파일로 열림 — 동기화 없음"); return; }
  if (SYNC.busy) return;
  SYNC.busy = true;
  if (!quiet) setSyncStatus("☁ 동기화 중…");
  try {
    const res = await fetch(SYNC.url, {
      method: "POST", headers: syncHeaders(),
      body: JSON.stringify({ exam: e, device: SYNC.device, items: loadWrong(e), removed: loadRemoved(e) }),
    });
    if (res.status === 404 || res.status === 405 || res.status === 501) {   // 정적 호스트(GitHub Pages·http.server)
      SYNC.available = false;
      setSyncStatus("이 주소에는 동기화 서버가 없습니다 — 오답은 이 기기에만 저장됩니다.");
      return;
    }
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      SYNC.available = res.status !== 503;
      SYNC.lastError = data.error || ("HTTP " + res.status);
      setSyncStatus("동기화 실패: " + SYNC.lastError, "bad");
      return;
    }
    SYNC.available = true;
    saveWrong(data.items || {}, e);
    saveRemoved(data.removed || {}, e);
    const n = Object.keys(data.items || {}).length;
    const t = new Date().toTimeString().slice(0, 5);
    setSyncStatus(`☁ ${examName(e)} 오답 ${n}개 동기화됨 · ${t}` + (data.committed ? " (저장소에 커밋)" : ""), "ok");
    updateWrongCount();
    if (!$("wrongbook").classList.contains("hidden")) renderWrongbook();
  } catch (err) {
    SYNC.lastError = String((err && err.message) || err);
    setSyncStatus("동기화 연결 실패(오프라인?) — 나중에 다시 시도합니다.", "bad");
  } finally {
    SYNC.busy = false;
  }
}

/* ---------- 퀴즈 상태 ---------- */
let deck = [];
let pos = 0;
let correctCnt = 0;
let sessionWrong = [];
let answers = [];   // 위치별 선택(idx). null=미답 → 뒤로가기·이어풀기 지원

const PROG_KEY = "medkos_quiz_progress";

function latestCreated(list) {
  return list.reduce((mx, q) => (q.created && q.created > mx ? q.created : mx), "");
}
function minCreated(list) {
  return list.reduce((mn, q) => (q.created && (!mn || q.created < mn) ? q.created : mn), "");
}
// '최신 세트' 대상 날짜 = 가장 최근 생성일. 날짜(오늘) 판단을 하지 않으므로, 새 세트가
// 나오기 전까지(예: 다음 생성까지 며칠간) 최근 세트가 계속 노출된다.
function latestSetDate(list) { return latestCreated(list); }
// 최신 세트 = 출처(src)별 최신 날짜의 합집합. KMLE 세트가 어제, 영상 세트가 오늘이면 둘 다 뜬다
// (영상 세트만 새로 나왔다고 어제 KMLE 세트가 사라지지 않게).
function latestSet(list) {
  const by = {};
  list.forEach((q) => { const s = q.src || "x"; if (q.created && (!by[s] || q.created > by[s])) by[s] = q.created; });
  return list.filter((q) => q.created && q.created === by[q.src || "x"]);
}
function latestLabelOf(list) {
  const dates = [...new Set(latestSet(list).map((q) => q.created))].sort();
  return dates.length > 1 ? `${dates[0]}~${dates[dates.length - 1]}` : (dates[0] || "");
}

// 기간(range) 모드 입력값 — 없으면 전체 범위(min~max)로 폴백.
function rangeBounds(base) {
  const lo = $("rangeFrom") && $("rangeFrom").value ? $("rangeFrom").value : minCreated(base);
  const hi = $("rangeTo") && $("rangeTo").value ? $("rangeTo").value : latestCreated(base);
  return { lo, hi };
}
function inRange(q, lo, hi) {
  if (!q.created) return false;
  if (lo && q.created < lo) return false;
  if (hi && q.created > hi) return false;
  return true;
}

function buildDeck() {
  const mode = $("mode").value;
  const base = baseList();
  let list;
  if (mode === "latest") {
    const subj = $("subject").value;
    list = latestSet(base);
    if (subj && subj !== "__ALL__") list = list.filter((q) => q.subject === subj);
  } else if (mode === "range") {
    const subj = $("subject").value;
    const { lo, hi } = rangeBounds(base);
    list = base.filter((q) => inRange(q, lo, hi));
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
    const msg = mode === "latest"
      ? "아직 생성된 문항이 없습니다."
      : mode === "range"
      ? "선택한 기간에 생성된 문항이 없습니다. 날짜 범위를 조정해 보세요."
      : mode === "review"
      ? "이 시험의 오답노트에 쌓인 문항이 없습니다. 먼저 전체 문항을 풀어보세요."
      : "조건에 맞는 문항이 없습니다.";
    alert(msg);
    return;
  }
  pos = 0; correctCnt = 0; sessionWrong = []; answers = [];
  hide($("setup")); hide($("result")); hide($("wrongbook"));
  show($("quiz"));
  renderQuestion();
  saveProgress();
  window.scrollTo(0, 0);
}

function figureHtml(q) {
  if (q.figureImg && q.figureImg.src) {
    const cap = q.figureImg.caption ? escapeHtml(q.figureImg.caption) + " · " : "";
    return `<figure class="imgfig"><img src="${escapeHtml(q.figureImg.src)}" alt="${escapeHtml(q.figureImg.alt || "임상 영상")}" loading="lazy" data-zoom="1" />
      <figcaption>${cap}<span class="zoomhint">탭하면 크게 · 두 손가락으로 확대</span></figcaption></figure>`;
  }
  if (q.figureSvg) return `<div class="figbox">${q.figureSvg}</div>`;
  return "";
}

function renderQuestion() {
  const q = deck[pos];
  $("progress").textContent = `${pos + 1} / ${deck.length}`;
  let tag;
  if (q.exam === "imaging") {
    tag = ["🩻 영상 세트", q.styleLabel || "", q.modality || q.type || "", q.difficultyLabel ? "난이도 " + q.difficultyLabel : ""].filter(Boolean).join(" · ");
  } else {
    tag = q.step ? `${q.step} · ${q.type || ""}` : (q.type || "");
  }
  $("typeTag").textContent = q.created ? `${tag}  ·  ${q.created}` : tag;
  $("subjTag").textContent = q.subject;
  $("vignette").textContent = (q.vignette || "").trim();
  $("vignette").classList.toggle("hidden", !(q.vignette || "").trim());
  $("clindata").innerHTML = figureHtml(q) + dataBox(q);
  $("clindata").querySelectorAll("img[data-zoom]").forEach((img) => {
    img.onclick = () => openZoom(img.getAttribute("src"), img.getAttribute("alt"));
  });
  $("question").textContent = "Q. " + (q.question || "").trim();

  const box = $("options");
  box.innerHTML = "";
  q.options.forEach((opt, i) => {
    const b = document.createElement("button");
    b.className = "opt";
    b.innerHTML = `<span class="num">${label(i, q)}</span>${escapeHtml(opt)}`;
    b.onclick = () => grade(i, b);
    box.appendChild(b);
  });

  const ex = $("explanation");
  ex.classList.add("hidden");
  ex.innerHTML = "";
  hide($("nextBtn"));
  $("prevBtn").classList.toggle("hidden", pos === 0);
  // 이미 답한 문항이면 채점 상태로 복원(뒤로가기·이어풀기 시)
  if (answers[pos] != null) showGraded(answers[pos]);
}

// 채점 결과 표시(정답/오답 표시 + 해설 + 다음 버튼). grade·복원에서 공용.
function showGraded(chosenIdx) {
  const q = deck[pos];
  const correctIdx = q.answer - 1;
  Array.from($("options").children).forEach((b, i) => {
    b.disabled = true;
    if (i === correctIdx) b.classList.add("correct");
    if (i === chosenIdx && chosenIdx !== correctIdx) b.classList.add("wrong");
  });
  renderExplanation(q, chosenIdx, chosenIdx === correctIdx);
  const nb = $("nextBtn");
  nb.textContent = pos >= deck.length - 1 ? "결과 보기 →" : "다음 문항 →";
  show(nb);
}

function grade(chosenIdx, btn) {
  if (answers[pos] != null) return;   // 이미 답한 문항(뒤로 왔다 온 경우) 재채점 방지
  answers[pos] = chosenIdx;
  const q = deck[pos];
  const ok = chosenIdx === q.answer - 1;
  if (ok) {
    correctCnt++;
  } else {
    recordWrong(q, chosenIdx);
    sessionWrong.push(q);
  }
  showGraded(chosenIdx);
  updateWrongCount();
  saveProgress();
}

function attributionHtml(q) {
  const a = q.attribution;
  if (!a || !(a.dataset || a.license || a.text)) return "";
  const link = a.url ? ` · <a href="${escapeHtml(a.url)}" target="_blank" rel="noopener">원본</a>` : "";
  const lic = a.license_url ? `<a href="${escapeHtml(a.license_url)}" target="_blank" rel="noopener">${escapeHtml(a.license)}</a>` : escapeHtml(a.license);
  const body = a.text ? escapeHtml(a.text) : `${escapeHtml(a.dataset)} · ${lic}`;
  return `<div class="src">영상 출처: ${body}${link}${a.asset_id ? ` · <span class="muted">${escapeHtml(a.asset_id)}</span>` : ""}</div>`;
}

function renderExplanation(q, chosenIdx, ok) {
  const el = $("explanation");
  const verdict = ok
    ? `<div class="verdict ok">✅ 정답입니다! 정답: ${label(q.answer - 1, q)}</div>`
    : `<div class="verdict bad">❌ 오답입니다. 당신의 선택: ${label(chosenIdx, q)} / 정답: ${label(q.answer - 1, q)}
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
  el.innerHTML = verdict + bodyHtml + attributionHtml(q);
  el.classList.remove("hidden");
}

// 해설의 '오답감별' 값을 보기(A~E·①~⑤)별로 각 줄에 나눠 가독성을 높인다.
function fmtExplValue(v) {
  let s = escapeHtml(v);
  if (s.indexOf("\n") >= 0) {
    return `<span class="optlines">${s.replace(/^\n+/, "")}</span>`;
  }
  const markers = s.match(/(?:\([A-E]\)|(?:^|\s)[A-E](?=\s+\S)|[①②③④⑤])/g) || [];
  if (markers.length >= 3) {
    s = s.replace(/\s+(?=(?:\([A-E]\)|[A-E]\s+\S|[①②③④⑤]))/g, "\n").replace(/^\n+/, "");
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
  if (pos >= deck.length - 1) { finish(); return; }
  pos++;
  renderQuestion();
  saveProgress();
  window.scrollTo(0, 0);
}

function prevQuestion() {
  if (pos > 0) { pos--; renderQuestion(); saveProgress(); window.scrollTo(0, 0); }
}

// 나가기 = 진행 저장 후 설정으로(나중에 '이어서 풀기'로 복귀). 완료(finish)와 구분.
function pauseQuiz() {
  saveProgress();
  hide($("quiz"));
  show($("setup"));
  refreshResume();
}

/* ---------- 영상 확대(핀치·드래그·더블탭) ---------- */
const ZOOM = { scale: 1, x: 0, y: 0, pointers: new Map(), startDist: 0, startScale: 1, last: null, lastTap: 0 };
function zoomEl() {
  let z = $("zoom");
  if (z) return z;
  z = document.createElement("div");
  z.id = "zoom";
  z.className = "zoom hidden";
  z.innerHTML = '<img alt="" draggable="false" /><button class="zclose" aria-label="닫기">✕</button>'
    + '<div class="zhint">두 손가락으로 확대 · 드래그로 이동 · 두 번 탭 = 2배/원래대로</div>';
  document.body.appendChild(z);
  const img = z.querySelector("img");
  z.querySelector(".zclose").onclick = closeZoom;
  z.addEventListener("click", (e) => { if (e.target === z) closeZoom(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeZoom(); });
  z.addEventListener("wheel", (e) => {
    e.preventDefault();
    setZoomScale(ZOOM.scale * (e.deltaY < 0 ? 1.15 : 1 / 1.15));
  }, { passive: false });
  z.addEventListener("pointerdown", (e) => {
    z.setPointerCapture(e.pointerId);
    ZOOM.pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (ZOOM.pointers.size === 2) {
      const [a, b] = [...ZOOM.pointers.values()];
      ZOOM.startDist = Math.hypot(a.x - b.x, a.y - b.y);
      ZOOM.startScale = ZOOM.scale;
    } else if (ZOOM.pointers.size === 1) {
      ZOOM.last = { x: e.clientX, y: e.clientY };
      const now = Date.now();
      if (now - ZOOM.lastTap < 300 && e.target === img) {
        setZoomScale(ZOOM.scale > 1.5 ? 1 : 2.2);
      }
      ZOOM.lastTap = now;
    }
  });
  z.addEventListener("pointermove", (e) => {
    if (!ZOOM.pointers.has(e.pointerId)) return;
    ZOOM.pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (ZOOM.pointers.size === 2) {
      const [a, b] = [...ZOOM.pointers.values()];
      const d = Math.hypot(a.x - b.x, a.y - b.y);
      if (ZOOM.startDist) setZoomScale(ZOOM.startScale * (d / ZOOM.startDist));
    } else if (ZOOM.pointers.size === 1 && ZOOM.last) {
      ZOOM.x += e.clientX - ZOOM.last.x;
      ZOOM.y += e.clientY - ZOOM.last.y;
      ZOOM.last = { x: e.clientX, y: e.clientY };
      applyZoom();
    }
  });
  const up = (e) => { ZOOM.pointers.delete(e.pointerId); if (ZOOM.pointers.size < 2) ZOOM.startDist = 0; if (!ZOOM.pointers.size) ZOOM.last = null; };
  z.addEventListener("pointerup", up);
  z.addEventListener("pointercancel", up);
  return z;
}
function setZoomScale(s) { ZOOM.scale = Math.min(8, Math.max(1, s)); applyZoom(); }
function applyZoom() {
  const img = zoomEl().querySelector("img");
  if (ZOOM.scale === 1) { ZOOM.x = 0; ZOOM.y = 0; }
  img.style.transform = `translate(${ZOOM.x}px, ${ZOOM.y}px) scale(${ZOOM.scale})`;
}
function openZoom(src, alt) {
  const z = zoomEl();
  const img = z.querySelector("img");
  img.src = src; img.alt = alt || "";
  ZOOM.scale = 1; ZOOM.x = 0; ZOOM.y = 0; applyZoom();
  show(z);
  document.body.classList.add("noscroll");
}
function closeZoom() {
  const z = $("zoom");
  if (!z) return;
  hide(z);
  document.body.classList.remove("noscroll");
}

// ── 진행 저장/복원(localStorage) ─────────────────────────────
function saveProgress() {
  try {
    localStorage.setItem(PROG_KEY, JSON.stringify({
      exam: exam(), mode: $("mode").value, subject: $("subject").value,
      step: $("step").value, style: $("style").value, ids: deck.map((q) => q.id), answers, pos,
    }));
  } catch (e) { /* 저장 실패는 무시 */ }
}
function loadProgress() {
  try { return JSON.parse(localStorage.getItem(PROG_KEY) || "null"); }
  catch (e) { return null; }
}
function clearProgress() { localStorage.removeItem(PROG_KEY); refreshResume(); }

function refreshResume() {
  const p = loadProgress();
  const btn = $("resumeBtn");
  if (!btn) return;
  if (p && p.ids && p.ids.length && (p.pos || 0) < p.ids.length) {
    btn.classList.remove("hidden");
    btn.textContent = `이어서 풀기 (${(p.pos || 0) + 1}/${p.ids.length} · ${examName(p.exam)})`;
  } else {
    btn.classList.add("hidden");
  }
}

function resumeQuiz() {
  const p = loadProgress();
  if (!p || !p.ids) return;
  if (p.exam) { $("exam").value = p.exam; onExamChange(); }
  if (p.step) $("step").value = p.step;
  if (p.style) $("style").value = p.style;
  if (p.mode) $("mode").value = p.mode;
  onModeChange();
  if (p.subject && [...$("subject").options].some((o) => o.value === p.subject)) {
    $("subject").value = p.subject;
  }
  const byId = {};
  allQuestions().forEach((q) => { byId[q.id] = q; });
  deck = p.ids.map((id) => byId[id]).filter(Boolean);
  if (!deck.length) { clearProgress(); return; }
  answers = (p.answers || []).slice(0, deck.length);
  pos = Math.min(p.pos || 0, deck.length - 1);
  correctCnt = 0; sessionWrong = [];
  answers.forEach((a, i) => {
    if (a == null) return;
    if (a === deck[i].answer - 1) correctCnt++; else sessionWrong.push(deck[i]);
  });
  hide($("setup")); hide($("result")); hide($("wrongbook"));
  show($("quiz"));
  renderQuestion();
}

function finish() {
  clearProgress();
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
        <div class="whead">[${escapeHtml(q.subject)}] #${q.id}</div>
        <div class="wmeta">${escapeHtml(q.question)}</div>
        <div class="ans">정답 ${label(q.answer - 1, q)} ${escapeHtml(q.options[q.answer - 1])}</div>
      </div>`).join("");
  }
  window.scrollTo(0, 0);
}

/* ---------- 오답노트 화면 ---------- */
function renderWrongbook() {
  hide($("setup")); hide($("quiz")); hide($("result"));
  show($("wrongbook"));
  const map = loadWrong();
  const items = Object.values(map);
  $("wbCount").textContent = `(${examName()} · ${items.length}개)`;
  const list = $("wbList");
  if (items.length === 0) { list.innerHTML = `<p class="muted">저장된 오답이 없습니다.</p>`; return; }
  const bySub = {};
  items.forEach((w) => { (bySub[w.subject] = bySub[w.subject] || []).push(w); });
  list.innerHTML = Object.keys(bySub).map((sub) => {
    const rows = bySub[sub].map((w) => `<div class="w">
      <div class="whead">#${escapeHtml(w.id)} <span class="muted">${w.step ? w.step + " · " : ""}${w.style === "usmle_style" ? "USMLE형 · " : w.style === "kmle_style" ? "국시형 · " : ""}${escapeHtml(w.type || "")} · ${w.date}${w.device && w.device !== SYNC.device ? " · " + escapeHtml(w.device) : ""}</span></div>
      <div class="wmeta">${escapeHtml(w.question)}</div>
      <div class="mine">내 선택 ${label(w.chosen, w)} ${escapeHtml(w.chosenText)}</div>
      <div class="ans">정답 ${label(w.answer, w)} ${escapeHtml(w.answerText)}</div>
      ${w.coreNote ? `<div class="wmeta">핵심: ${escapeHtml(w.coreNote)}</div>` : ""}
      ${w.note ? `<div class="wnote">✍ ${escapeHtml(w.note)}</div>` : ""}
      <button data-note="${escapeHtml(w.id)}">${w.note ? "메모 수정" : "틀린 이유 메모"}</button>
      <button data-del="${escapeHtml(w.id)}">이 오답 삭제</button>
    </div>`).join("");
    return `<h3>${escapeHtml(sub)} (${bySub[sub].length})</h3>` + rows;
  }).join("");
  list.querySelectorAll("button[data-del]").forEach((b) => {
    b.onclick = () => { removeWrong(b.getAttribute("data-del")); renderWrongbook(); updateWrongCount(); };
  });
  list.querySelectorAll("button[data-note]").forEach((b) => {
    b.onclick = () => {
      const id = b.getAttribute("data-note");
      const cur = (loadWrong()[id] || {}).note || "";
      const v = prompt("틀린 이유 / 기억할 것 (비우면 삭제)", cur);
      if (v === null) return;
      setWrongNote(id, v.trim());
      renderWrongbook();
    };
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
  let md = `# ${examName()} 오답노트 (웹 퀴즈 내보내기 · ${todayStr()})\n\n총 ${items.length}개\n`;
  Object.keys(bySub).forEach((sub) => {
    md += `\n## ${sub} (${bySub[sub].length})\n`;
    bySub[sub].forEach((w, i) => {
      md += `\n### ${i + 1}. #${w.id} ${w.step ? w.step + " · " : ""}${w.type || ""}\n\n`;
      md += `| 항목 | 내용 |\n|------|------|\n`;
      md += `| 기록일 | ${w.date} |\n`;
      md += `| 문항 | ${w.question} |\n`;
      md += `| 내가 고른 답 | ${label(w.chosen, w)} ${w.chosenText} |\n`;
      md += `| 정답 | ${label(w.answer, w)} ${w.answerText} |\n`;
      if (w.coreNote) md += `| 핵심 정리 | ${w.coreNote} |\n`;
      md += `| 출처 | ${w.source} |\n`;
      md += `| 틀린 이유(직접 작성) | ${w.note || ""} |\n`;
      md += `| 복습 예정일(직접 작성) |  |\n`;
    });
  });
  download(`오답노트_${exam()}_${todayStr()}.md`, md, "text/markdown");
}

function exportCsv() {
  const items = Object.values(loadWrong());
  if (items.length === 0) { alert("저장된 오답이 없습니다."); return; }
  const esc = (s) => `"${String(s == null ? "" : s).replace(/"/g, '""')}"`;
  const head = ["id", "시험", "step", "과목", "유형", "기록일", "문항", "내가고른답", "정답", "출처", "메모"];
  const rows = items.map((w) => [
    w.id, examName(w.exam || exam()), w.step || "", w.subject, w.type, w.date, w.question,
    label(w.chosen, w) + " " + w.chosenText,
    label(w.answer, w) + " " + w.answerText,
    w.source, w.note || "",
  ].map(esc).join(","));
  download(`오답노트_${exam()}_${todayStr()}.csv`, "﻿" + head.join(",") + "\n" + rows.join("\n"), "text/csv");
}

/* ---------- 유틸 ---------- */
function escapeHtml(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
function updateWrongCount() {
  const n = Object.keys(loadWrong()).length;
  $("wrongCount").textContent = n ? `현재 ${examName()} 오답노트에 ${n}개 저장됨` : "";
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

// 기간 입력의 선택 가능 범위(min/max)를 갱신하고, 비어있거나 force면 전체범위로 채운다.
function setRangeDefaults(base, force) {
  const f = $("rangeFrom"), t = $("rangeTo");
  if (!f || !t) return;
  const lo = minCreated(base), hi = latestCreated(base);
  f.min = lo; f.max = hi; t.min = lo; t.max = hi;
  if (force || !f.value) f.value = lo;
  if (force || !t.value) t.value = hi;
}

function onModeChange() {
  const mode = $("mode").value;
  const base = baseList();
  $("subjectRow").style.display = mode === "review" ? "none" : "";
  $("rangeRow").style.display = mode === "range" ? "" : "none";

  const fd = latestLabelOf(base);
  if (mode === "latest") {
    populateSubjects(latestSet(base));
  } else if (mode === "range") {
    setRangeDefaults(base, false);
    const { lo, hi } = rangeBounds(base);
    populateSubjects(base.filter((q) => inRange(q, lo, hi)));
  } else if (mode === "all") {
    populateSubjects(base);
  }

  const wrongN = Object.keys(loadWrong()).length;
  const stepTxt = isUsmle() && $("step").value !== "__ALL__" ? ` [${$("step").value}]` : "";
  const latestN = latestSet(base).length;
  const latestImg = latestSet(base).filter((q) => q.exam === "imaging").length;
  let rangeHint = "날짜 범위를 고르세요.";
  if (mode === "range") {
    const { lo, hi } = rangeBounds(base);
    const n = base.filter((q) => inRange(q, lo, hi)).length;
    rangeHint = `${lo} ~ ${hi} 사이에 만든 ${n}개를 풉니다.`;
  }
  const latestLabel = isImaging() ? `오늘의 영상 세트(${fd})` : `최신 세트(${fd})`;
  const imgNote = !isImaging() && latestImg ? ` 이 중 ${latestImg}개는 그날 영상 세트에서 온 문항입니다.` : "";
  const hint = {
    latest: `${latestLabel} ${latestN}개를 풉니다.${imgNote} 새 세트가 나오면 자동으로 그 세트로 바뀝니다.`,
    range: rangeHint,
    all: `${examName()}${stepTxt} 누적 ${base.length}개 전체(또는 선택 과목)를 풉니다.`,
    review: `${examName()} 오답노트에 쌓인 ${wrongN}개만 다시 풉니다.`,
  }[mode];
  $("modeHint").textContent = hint || "";
}

function onExamChange() {
  const usmle = isUsmle(), imaging = isImaging();
  $("stepRow").style.display = usmle ? "" : "none";
  $("styleRow").style.display = imaging ? "" : "none";
  // 시험이 바뀌면 사용 가능한 날짜 범위도 달라지므로 기간 입력을 새 전체범위로 리셋한다.
  setRangeDefaults(baseList(), true);
  onModeChange();
  updateWrongCount();
  if (SYNC.available !== false) syncAll(true);
}

// 홈 화면 바로가기(manifest shortcuts)·링크의 ?exam=imaging&mode=latest 를 초기 상태에 반영.
function applyQueryParams() {
  const p = new URLSearchParams(location.search);
  const e = p.get("exam");
  if (e && [...$("exam").options].some((o) => o.value === e)) $("exam").value = e;
  const m = p.get("mode");
  if (m && [...$("mode").options].some((o) => o.value === m)) $("mode").value = m;
  return p.get("start") === "1";
}

/* ---------- 초기화 ---------- */
function init() {
  if (KMLE.length === 0 && USMLE.length === 0 && IMAGING.length === 0) {
    document.body.insertAdjacentHTML("beforeend",
      '<p style="max-width:820px;margin:16px auto;color:#ffb4b4">문항 데이터를 불러오지 못했습니다. questions.js / questions_usmle.js / questions_imaging.js 를 확인하세요.</p>');
    return;
  }
  if (IMAGING.length === 0) {
    const o = [...$("exam").options].find((x) => x.value === "imaging");
    if (o) o.textContent = "🩻 영상 (아직 문항 없음)";
  }
  const autoStart = applyQueryParams();
  $("exam").onchange = onExamChange;
  $("step").onchange = onModeChange;
  $("style").onchange = onModeChange;
  if ($("imgOnly")) $("imgOnly").onchange = onModeChange;
  $("mode").onchange = onModeChange;
  if ($("rangeFrom")) $("rangeFrom").onchange = onModeChange;
  if ($("rangeTo")) $("rangeTo").onchange = onModeChange;
  onExamChange();

  $("startBtn").onclick = startQuiz;
  $("resumeBtn").onclick = resumeQuiz;
  $("viewWrongBtn").onclick = renderWrongbook;
  $("nextBtn").onclick = nextQuestion;
  $("prevBtn").onclick = prevQuestion;
  $("quitBtn").onclick = pauseQuiz;
  $("restartBtn").onclick = () => { hide($("result")); show($("setup")); onModeChange(); updateWrongCount(); refreshResume(); };
  refreshResume();
  $("reviewBtn").onclick = () => { $("mode").value = "review"; hide($("result")); startQuiz(); };
  $("backBtn").onclick = () => { hide($("wrongbook")); show($("setup")); onModeChange(); updateWrongCount(); };
  $("exportMdBtn").onclick = exportMarkdown;
  $("exportCsvBtn").onclick = exportCsv;
  $("clearBtn").onclick = () => {
    if (confirm(`${examName()} 오답노트를 모두 비웁니다. 계속할까요?`)) {
      const rm = loadRemoved(); const t = nowIso();
      Object.keys(loadWrong()).forEach((id) => { rm[id] = t; });
      saveRemoved(rm);
      localStorage.removeItem(storeKey());
      renderWrongbook(); updateWrongCount(); scheduleSync();
    }
  };
  if ($("syncBtn")) $("syncBtn").onclick = () => syncAll(false);
  if ($("syncKey")) {
    $("syncKey").value = syncKey();
    $("syncKey").onchange = () => {
      try { localStorage.setItem("medkos_sync_key", $("syncKey").value.trim()); } catch (e) { /* ignore */ }
      SYNC.available = null;
      syncNow(exam(), false);
    };
  }
  updateWrongCount();
  window.addEventListener("online", () => { if (SYNC.available !== false) syncAll(true); });
  if (autoStart) startQuiz();
}

document.addEventListener("DOMContentLoaded", init);
