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
    decision: (q.design && q.design.summary) || "",
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
  url: (window.MEDKOS_API_BASE || "") + "api/wrong",   // 옛 GitHub Pages 주소면 Cloudflare 서버로(learn.js)
  available: null,          // null=미확인, true/false
  timer: null,
  busy: false,
  device: deviceId(),
  lastError: "",
  auth: null,               // null=모름 · "ok" · "missing"(서버는 키가 필요한데 이 기기에 없음) · "wrong"(틀린 키)
};
const SYNC_EXAMS = ["kmle", "usmle", "imaging"];
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
// 키는 docs/synckey.js 가 관리한다(#k= 연결 링크로 받은 키 포함).
function syncKey() {
  if (typeof MEDKOS_SYNC === "object") return MEDKOS_SYNC.get();
  try { return localStorage.getItem("medkos_sync_key") || ""; } catch (e) { return ""; }
}
// 이 기기에만 있는 것 — 키가 들어오면 전부 합쳐 올라간다(서버는 합집합).
function localBacklog() {
  let wrong = 0;
  SYNC_EXAMS.forEach((e) => { wrong += Object.keys(loadWrong(e)).length; });
  const events = typeof LEARN === "object" && LEARN.load ? LEARN.load().length : 0;
  return { wrong, events };
}
/* 키가 없거나 틀린 기기는 첫 화면에 크게 알린다(2026-09-23). 예전에는 상태 줄 한 칸의 「실패」뿐이라
   몇 주 동안 오답이 기기 안에만 쌓인 것을 아무도 몰랐다. */
function renderSyncBanner() {
  const el = $("syncNeedKey");
  if (!el) return;
  if (SYNC.auth !== "missing" && SYNC.auth !== "wrong") { el.classList.add("hidden"); return; }
  const b = localBacklog();
  const why = SYNC.auth === "wrong" ? "이 기기에 저장된 동기화 키가 서버와 맞지 않아" : "이 기기에 동기화 키가 없어";
  $("syncNeedKeyText").textContent =
    `${why} 오답 ${b.wrong}개 · 학습 기록 ${b.events}건이 이 기기에만 있습니다. ` +
    "키가 있는 기기의 「동기화 설정 ▸ 다른 기기 연결 링크」를 이 기기에서 열거나, 아래에 키를 넣으세요. " +
    "넣는 즉시 지금까지의 기록이 모두 올라갑니다.";
  el.classList.remove("hidden");
}
function describeAuth() {
  const el = $("syncAuthInfo");
  if (!el) return;
  el.textContent = SYNC.auth === "ok" ? "이 기기: 키 확인됨"
    : SYNC.auth === "missing" ? "이 기기: 키 없음 — 동기화 안 됨"
    : SYNC.auth === "wrong" ? "이 기기: 키 틀림 — 동기화 안 됨"
    : "이 기기: 키 상태 확인 전";
}
// 서버에 「이 기기의 키가 맞는가」만 묻는다(데이터는 읽지 않음). 옛 배포라 /api/status 가 없으면 동기화 응답(401)으로 판단한다.
async function checkSyncAuth() {
  if (location.protocol === "file:" || typeof fetch !== "function") return;
  try {
    const r = await fetch((window.MEDKOS_API_BASE || "") + "api/status", { headers: syncHeaders() });
    if (!r.ok || !/json/.test(r.headers.get("content-type") || "")) return;
    const s = await r.json();
    SYNC.auth = s.keyOk ? "ok" : (s.keySent ? "wrong" : "missing");
  } catch (e) { return; }
  renderSyncBanner(); describeAuth();
}
async function onSyncKeyChange(value) {
  if (typeof MEDKOS_SYNC === "object") MEDKOS_SYNC.set(value);
  else try { localStorage.setItem("medkos_sync_key", String(value || "").trim()); } catch (e) { /* ignore */ }
  SYNC.available = null;
  SYNC.auth = null;
  await checkSyncAuth();
  if (typeof LEARN === "object") await LEARN.syncLearning(false);
  await syncAll(false);
}
async function shareSyncLink() {
  const k = syncKey();
  const out = $("syncLinkOut");
  if (!k) { alert("이 기기에 동기화 키가 없어 링크를 만들 수 없습니다. 키가 있는 기기에서 만드세요."); return; }
  const link = typeof MEDKOS_SYNC === "object" ? MEDKOS_SYNC.linkFor(k) : "";
  if (out) { out.value = link; out.classList.remove("hidden"); out.select(); }
  try {
    if (navigator.share) { await navigator.share({ title: "MedKOS 기기 연결", url: link }); return; }
    if (navigator.clipboard) { await navigator.clipboard.writeText(link); setSyncStatus("☁ 연결 링크를 복사했습니다 — 본인 기기에서만 여세요.", "ok"); }
  } catch (e) { /* 공유 취소 — 아래 칸에서 직접 복사 */ }
}
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
// 상태 줄은 마지막 덱이 아니라 **덱별 개수를 모아** 한 줄로 적는다 — 예전에는 늘 뒤에 도는 영상 결과만 남아
// 「영상 오답 0개」로 보여, KMLE 오답이 안 올라간 것처럼 읽혔다(2026-09-20).
async function syncAll(quiet) {
  // 지금 연 덱만이 아니라 이 기기에 기록이 있는 모든 시험을 보낸다(2026-09-23) — 예전에는 KMLE 덱을 열면
  // USMLE 오답이 올라가지 않아 저장소에 USMLE 오답 파일이 한 번도 생기지 않았다.
  const list = [exam()];
  SYNC_EXAMS.forEach((e) => {
    if (list.indexOf(e) < 0 && (e === "imaging" || Object.keys(loadWrong(e)).length || Object.keys(loadRemoved(e)).length)) list.push(e);
  });
  if (!quiet) setSyncStatus("☁ 동기화 중…");
  const parts = [];
  for (const e of list) {
    const n = await syncNow(e, true);
    if (SYNC.available === false) return;
    if (n === null) return;                       // 실패 — 그 메시지를 그대로 둔다
    parts.push(`${examName(e)} ${n}개`);
  }
  const t = new Date().toTimeString().slice(0, 5);
  // 학습 기록(정리본 큐가 읽는 것)은 따로 전송된다 — 실패 중이면 상태 줄에 드러낸다
  const ls = typeof LEARN === "object" && LEARN.learnSyncState ? LEARN.learnSyncState() : null;
  const learnNote = !ls || ls.available === false ? ""
    : ls.fails ? ` · 학습 기록 전송 실패 ${ls.fails}회(자동 재시도)` : ls.lastOk ? ` · 학습 기록 ${ls.count}건 ${ls.lastOk}` : "";
  setSyncStatus(`☁ 오답 ${parts.join(" · ")} 동기화됨 · ${t}${learnNote}`, ls && ls.fails ? "bad" : "ok");
}
// 반환: 동기화된 오답 수(실패·서버 없음이면 null)
async function syncNow(e, quiet) {
  if (location.protocol === "file:") { setSyncStatus("로컬 파일로 열림 — 동기화 없음"); return null; }
  if (SYNC.busy) return null;
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
      return null;
    }
    const data = await res.json().catch(() => ({}));
    if (res.status === 401) {                     // 키 없음·틀림 — 첫 화면에 크게 알린다
      SYNC.auth = syncKey() ? "wrong" : "missing";
      SYNC.lastError = data.error || "동기화 키 필요";
      setSyncStatus("동기화 안 됨: 이 기기에 맞는 동기화 키가 없습니다(아래 경고 참고)", "bad");
      renderSyncBanner(); describeAuth();
      return null;
    }
    if (!res.ok) {
      SYNC.available = res.status !== 503;
      SYNC.lastError = data.error || ("HTTP " + res.status);
      setSyncStatus("동기화 실패: " + SYNC.lastError, "bad");
      return null;
    }
    SYNC.available = true;
    if (SYNC.auth !== "ok") { SYNC.auth = "ok"; renderSyncBanner(); describeAuth(); }
    saveWrong(data.items || {}, e);
    saveRemoved(data.removed || {}, e);
    const n = Object.keys(data.items || {}).length;
    updateWrongCount();
    if (!$("wrongbook").classList.contains("hidden")) renderWrongbook();
    return n;
  } catch (err) {
    SYNC.lastError = String((err && err.message) || err);
    setSyncStatus("동기화 연결 실패(오프라인?) — 나중에 다시 시도합니다.", "bad");
    return null;
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

/* 문항 머리표. subtopic(q.type)은 정답을 말해 버리는 경우가 많아(예: 「… — Oral Vancomycin」, 2026-09-25 감사)
   풀기 전에는 숨기고 채점 뒤에만 보인다. */
function tagText(q, reveal) {
  let tag;
  if (q.exam === "imaging") {
    tag = ["🩻 영상 세트", q.styleLabel || "", q.modality || (reveal ? q.type : "") || "", q.difficultyLabel ? "난이도 " + q.difficultyLabel : ""].filter(Boolean).join(" · ");
  } else {
    const t = reveal ? (q.type || "") : "";
    tag = q.step ? (t ? `${q.step} · ${t}` : q.step) : (t || (q.exam === "usmle" ? "USMLE" : "국시형"));
  }
  return q.created ? `${tag}  ·  ${q.created}` : tag;
}

function renderQuestion() {
  const q = deck[pos];
  $("progress").textContent = `${pos + 1} / ${deck.length}`;
  $("typeTag").textContent = tagText(q, answers[pos] != null);
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
  if (typeof LEARN === "object") LEARN.onAnswer(q, chosenIdx, ok);   // 덧붙이기만 하는 학습 기록
  updateReviewBadge();
  showGraded(chosenIdx);
  $("typeTag").textContent = tagText(q, true);
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
    // 구조화 해설(항목별 박스) + 정보 선별(있으면) + 부록 결정표 박스.
    bodyHtml = renderExplItems(q.explanationItems) + renderTriage(q) + renderAppendix(q.appendix);
  } else if (q.explanationText) {
    bodyHtml = `<pre class="expl-text">${escapeHtml(q.explanationText)}</pre>` + renderTriage(q) + renderAppendix(q.appendix);
  } else {
    const ex = q.explanation || {};
    const rows = [];
    ["진단", "정답근거", "오답감별", "임상핵심"].forEach((k) => {
      if (ex[k]) rows.push(`<div class="expl-item"><span class="k">${k}</span>${fmtExplValue(ex[k])}</div>`);
    });
    const src = q.source ? `<div class="src">출처: ${escapeHtml(q.source)}</div>` : "";
    bodyHtml = rows.join("") + src + renderTriage(q) + renderAppendix(q.appendix);
  }
  // 오답이면 해설보다 먼저 「오답 확인 → 선택한 오답과 정답 비교 → 정리본」 흐름을, 정답이면 표시(찍었다 등)만 붙인다.
  let learnHtml = "";
  try {
    if (typeof LEARN === "object") learnHtml = ok ? LEARN.flagRowHtml(q) : LEARN.wrongPanelHtml(q, chosenIdx);
  } catch (e) { learnHtml = ""; }             // 학습 흐름 오류가 해설 표시를 막지 않게
  el.innerHTML = ok ? verdict + bodyHtml + attributionHtml(q) + learnHtml
                    : verdict + learnHtml + `<div class="expl-head">해설</div>` + bodyHtml + attributionHtml(q);
  el.classList.remove("hidden");
  try { if (typeof LEARN === "object") LEARN.bind(el, q, chosenIdx); } catch (e) { /* 무시 — 해설은 이미 보인다 */ }
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
  return splitEnums(s);
}

// 한 문단 안에 (1)·(2)… 또는 ①·②… 로 나열한 항목이 있으면 항목마다 줄을 바꾼다(2026-09-19 사용자 요청).
// (1)과 (2)가 함께 있을 때만 — 「127(2):389」 같은 쪽 표기나 「(1C)」 같은 권고 등급은 건드리지 않는다.
// html 은 이미 escape·정화된 글이어야 한다(여기서는 <br>·<span> 만 더한다).
const ENUM_RE = /(^|[\s:;,.—])(\((?:[1-9]|1[0-9])\)|[①-⑳])(?=\s)/g;
function splitEnums(html) {
  const found = new Set();
  String(html).replace(ENUM_RE, (m, pre, mk) => { found.add(mk); return m; });
  if (!((found.has("(1)") && found.has("(2)")) || (found.has("①") && found.has("②")))) return html;
  return String(html).replace(ENUM_RE, (m, pre, mk, off) => {
    const keep = pre.trim();                         // 「:」「;」 같은 앞 문장부호는 줄 끝에 남긴다
    const brk = off === 0 && !keep ? "" : "<br>";
    return `${keep}${brk}<span class="enum">${mk}</span>`;
  });
}
// 깊이 해설(원리·비교): <br> 로 나뉜 덩어리를 문단으로 띄우고, 문단 안의 나열 항목은 줄을 바꾼다.
function deepBodyHtml(raw) {
  return sanitizeHtml(raw).split(/<br\s*\/?>/i).map((s) => s.trim()).filter(Boolean)
    .map((s) => `<p class="dp">${splitEnums(s)}</p>`).join("");
}

// 깊이 해설(정리본 해설지 규칙): 원리·비교는 HTML(<b>·<br>·<table>)을 허용하되 화이트리스트로 정화해 그린다.
const DEEP_KEYS = { "원리": ["prin", "왜 그런가 — 원리"], "비교": ["cmpx", "경계는 어디인가 — 비교"] };
const SAFE_TAGS = new Set(["B", "STRONG", "I", "EM", "U", "BR", "TABLE", "THEAD", "TBODY", "TR", "TH", "TD", "UL", "OL", "LI", "P", "SPAN", "SUB", "SUP"]);
function sanitizeHtml(html) {
  let doc;
  try { doc = new DOMParser().parseFromString("<div>" + String(html || "") + "</div>", "text/html"); }
  catch (e) { return escapeHtml(html); }
  const walk = (node) => {
    let out = "";
    node.childNodes.forEach((n) => {
      if (n.nodeType === 3) { out += escapeHtml(n.nodeValue); return; }
      if (n.nodeType !== 1) return;
      const tag = n.tagName;
      if (!SAFE_TAGS.has(tag)) { out += walk(n); return; }   // 허용 밖 태그는 벗기고 내용만
      const t = tag.toLowerCase();
      out += t === "br" ? "<br>" : `<${t}>${walk(n)}</${t}>`;
    });
    return out;
  };
  return walk(doc.body.firstChild || doc.body);
}

// 구조화 해설: `- **키**: 값` 항목들을 각각 간격을 둔 박스로 렌더한다. 원리·비교는 정리본 해설지와 같은 제목의 박스.
function renderExplItems(items) {
  return items.map((it) => {
    const deep = DEEP_KEYS[it.k];
    if (deep) return `<div class="expl-item deep ${deep[0]}"><div class="k">${deep[1]}</div><div class="deep-body">${deepBodyHtml(it.v)}</div></div>`;
    const key = it.k === "오답 이유" ? "선지별로 틀린 이유 — 정답이 되려면 무엇이 달라져야 하는가" : it.k;
    return `<div class="expl-item"><span class="k">${escapeHtml(key)}</span>${fmtExplValue(it.v)}</div>`;
  }).join("");
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

// 정보를 어떻게 선별했는가 — 문항 frontmatter 의 design(출제 설계·정보 역할)에서 그린다.
// 채점(renderExplanation) 뒤에만 불리므로 답을 내기 전에는 보이지 않는다. 핵심 판단 요약만 펼쳐 두고
// 단서별 분류는 접어 둔다(기본 해설은 빠르게 복습할 분량을 유지). design 이 없는 기존 문항은 아무것도 그리지 않는다.
function renderTriage(q) {
  const d = q && q.design;
  if (!d || typeof d !== "object") return "";
  const li = (arr) => (Array.isArray(arr) ? arr : [])
    .filter((x) => x && x.item)
    .map((x) => `<li><b>${escapeHtml(x.item)}</b>${x.why ? " — " + escapeHtml(x.why) : ""}`
      + (Array.isArray(x.also) && x.also.length ? ` <span class="tg-also">+ ${x.also.map(escapeHtml).join(" · ")}</span>` : "")
      + "</li>").join("");
  const group = (cls, title, arr) => {
    const items = li(arr);
    return items ? `<div class="tg ${cls}"><div class="tg-h">${title}</div><ul>${items}</ul></div>` : "";
  };
  const optLabel = (letter) => {
    const i = "ABCDE".indexOf(String(letter || "").toUpperCase());
    return i >= 0 ? label(i, q) : escapeHtml(letter || "");
  };
  const parts = [
    group("key", "결정적 단서", d.key),
    group("ruleout", "의미 있는 정상·음성 소견", d.ruleOut),
    group("mgmt", "중증도·금기·치료 선택에 영향", d.management),
    group("bg", "비중이 낮은 정보 — 이번 질문에서 결정적이지 않은 이유", d.background),
  ];
  if (Array.isArray(d.rival) && d.rival.length && d.discriminator) {
    parts.push(`<div class="tg rival"><div class="tg-h">가장 헷갈리는 선택지 ${d.rival.map(optLabel).join("·")}</div><p>${escapeHtml(d.discriminator)}</p></div>`);
  }
  if (d.switch && d.switch.choice && d.switch.condition) {
    parts.push(`<div class="tg switch"><div class="tg-h">조건이 바뀌면 — ${optLabel(d.switch.choice)} 가 더 적절해지는 경우</div><p>${escapeHtml(d.switch.condition)}</p></div>`);
  }
  const more = parts.filter(Boolean).join("");
  const target = d.target ? `<span class="tg-target">평가: ${escapeHtml(d.target)}${d.steps ? ` · 판단 ${escapeHtml(String(d.steps))}단계` : ""}</span>` : "";
  const sum = (d.summary ? `<div class="triage-sum"><span class="k">핵심 판단</span>${escapeHtml(d.summary)}</div>` : "")
    + (Array.isArray(d.chain) && d.chain.length
      ? `<div class="triage-chain"><span class="k">판단 사슬 — 어느 단계에서 갈렸는지 짚어 보세요</span><ol>${d.chain.map((c) => `<li>${escapeHtml(c)}</li>`).join("")}</ol></div>`
      : "");
  const review = q.reviewStatus === "reviewed"
    ? '<div class="triage-rev ok">내용 검토 완료</div>'
    : '<div class="triage-rev">의학적 내용 검토 전 문항 — 생성 후 자동 형식 검사만 통과했습니다</div>';
  return `<div class="triage"><div class="triage-head">정보를 어떻게 선별했는가 ${target}</div>${sum}`
    + (more ? `<details class="triage-more"><summary>단서별로 보기</summary>${more}</details>` : "")
    + review + "</div>";
}

// 부록 「가이드라인」 글을 표로 — 원본은 여러 모양으로 쓰여 있다(2026-09-22, 295문항 조사).
//   목록형: 제목 / 「- 항목: 내용」 / 「· 하위」 / 「각주: …」        → 항목 | 내용 표
//   정렬형: 제목 / ───── / 「조건   : 처치」(들여쓴 다음 줄은 이어짐) / 「† ‡ ※」 주석
//   결정표: 「상황 → 진단 → 검사」 줄들                                → 화살표 단계마다 한 칸
//   마크다운 표: 「| 지표 | 정의 |」 + 「|---|」                       → 머리행이 있는 표
// 읽어 내지 못하면 예전처럼 글 그대로(<pre>). 모든 글은 escapeHtml 을 거친다(**굵게**만 허용).
function guideTableHtml(raw) {
  const text = String(raw || "").replace(/\r/g, "").trim();
  if (!text) return "";
  const inline = (t) => escapeHtml(t).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");
  const RULE = /^[─━═\-=_]{3,}\s*$/;
  const NOTE = /^(각주\s*[:：]?|[†‡§¶※*]+)\s*/;
  const PIPE = /^\|.*\|\s*$/;
  const splitKV = (t) => {
    if (/→/.test(t.split(/[:：]/)[0])) return null;                   // 화살표가 콜론보다 먼저면 결정표 줄
    const m = t.match(/^([^:：]{1,28}?)\s*[:：]\s*(.+)$/);
    if (!m) return null;
    const k = m[1].replace(/\s{2,}/g, " ").trim(), v = m[2].trim();
    if (!k || !v || (/\d$/.test(k) && /^\d/.test(v))) return null;     // 1:1 같은 비율은 나누지 않는다
    return [k, v];
  };
  const cellsOf = (row) => row.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim());
  const blocks = [], notes = [];
  const push = (type, row) => {
    const last = blocks[blocks.length - 1];
    if (last && last.type === type) last.rows.push(row); else blocks.push({ type, rows: [row] });
  };
  const lastRow = () => { const b = blocks[blocks.length - 1]; return b && b.type === "kv" ? b.rows[b.rows.length - 1] : null; };
  const lines = text.split("\n");
  let caption = "", i = 0;
  const first = lines[0].trim();
  if (first && !RULE.test(first) && !PIPE.test(first) && !/^[-•·ㆍ]\s/.test(first) && !NOTE.test(first)
      && !splitKV(first) && !/→/.test(first)) { caption = first; i = 1; }
  for (; i < lines.length; i++) {
    const line = lines[i].replace(/\s+$/, "");
    const t = line.trim();
    if (!t || RULE.test(t)) continue;
    if (PIPE.test(t)) {                                              // 마크다운 표
      const cells = cellsOf(t);
      if (cells.every((c) => /^:?-{2,}:?$/.test(c))) {               // |---| 구분선 → 앞 행이 머리행
        const b = blocks[blocks.length - 1];
        if (b && b.type === "md" && b.rows.length === 1) b.head = b.rows.pop();
        continue;
      }
      push("md", cells);
      continue;
    }
    if (NOTE.test(t) && !/^\*\*/.test(t)) { notes.push(t.replace(/^각주\s*[:：]\s*/, "")); continue; }
    const sub = t.match(/^[·ㆍ]\s*(.+)$/);
    if (sub && lastRow()) { lastRow().subs.push(sub[1]); continue; }
    if (/^\s{2,}/.test(line) && lastRow() && !/^[-•]\s/.test(t)) { lastRow().v.push(t); continue; }   // 들여쓴 줄 = 윗줄의 이어짐
    const body = (t.match(/^(?:[-•]|\d+[.)])\s+(.+)$/) || [null, t])[1];
    const kv = splitKV(body);
    if (!kv && (body.match(/→/g) || []).length >= 1) { push("flow", body.split(/\s*→\s*/)); continue; }
    push("kv", kv ? { k: kv[0], v: [kv[1]], subs: [] } : { k: "", v: [body], subs: [] });
  }
  if (!blocks.length) return `<pre class="guide-table">${escapeHtml(text)}</pre>`;
  const subList = (subs) => subs.length ? `<ul>${subs.map((x) => {
    const kv = splitKV(x);
    return `<li>${kv ? `<b>${inline(kv[0])}</b> — ${inline(kv[1])}` : inline(x)}</li>`;
  }).join("")}</ul>` : "";
  const html = blocks.map((b) => {
    if (b.type === "md") {
      const n = Math.max(b.head ? b.head.length : 0, ...b.rows.map((r) => r.length));
      const pad = (r) => r.concat(Array(Math.max(0, n - r.length)).fill(""));
      const head = b.head ? `<thead><tr>${pad(b.head).map((c) => `<th scope="col">${inline(c)}</th>`).join("")}</tr></thead>` : "";
      return `<table class="gt-table gt-grid">${head}<tbody>${b.rows.map((r) =>
        `<tr>${pad(r).map((c, j) => j === 0 ? `<th scope="row">${inline(c)}</th>`
          : `<td${b.head && b.head[j] ? ` data-h="${escapeHtml(b.head[j])}"` : ""}>${inline(c)}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
    }
    if (b.type === "flow") {                                          // 결정표: 단계마다 한 칸, 마지막 칸이 결론
      const n = Math.max(...b.rows.map((r) => r.length));
      return `<table class="gt-table gt-flow"><tbody>${b.rows.map((r) => {
        // 단계가 적은 줄은 가운데를 비워 결론이 늘 마지막 칸에 오게 한다
        const cells = r.length >= n ? r : r.slice(0, -1).concat(Array(n - r.length).fill(""), r.slice(-1));
        return `<tr>${cells.map((c, j) => j === 0 ? `<th scope="row">${inline(c)}</th>`
          : `<td${j === n - 1 ? ' class="gt-end"' : ""}>${c ? `<span class="gt-arrow" aria-hidden="true">→</span>${inline(c)}` : ""}</td>`).join("")}</tr>`;
      }).join("")}</tbody></table>`;
    }
    return `<table class="gt-table"><tbody>${b.rows.map((r) => {
      const val = r.v.map(inline).join("<br>") + subList(r.subs);
      return r.k ? `<tr><th scope="row">${inline(r.k)}</th><td>${val}</td></tr>`
                 : `<tr><td colspan="2" class="gt-wide">${val}</td></tr>`;
    }).join("")}</tbody></table>`;
  }).join("");
  return `<div class="gt">${caption ? `<div class="gt-cap">${inline(caption)}</div>` : ""}${html}`
    + (notes.length ? `<ul class="gt-notes">${notes.map((n) => `<li>${inline(n)}</li>`).join("")}</ul>` : "")
    + "</div>";
}

function renderAppendix(ap) {
  if (!ap) return "";
  const parts = [];
  if (ap["가이드라인"]) {
    parts.push(`<div class="item"><span class="k">가이드라인</span></div>${guideTableHtml(ap["가이드라인"])}`);
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

/* ---------- 단일 문항(학습서 링크 ?q=<id> · 복습 목록) ---------- */
function openSingleQuestion(id) {
  const pools = [["kmle", KMLE], ["usmle", USMLE], ["imaging", IMAGING]];
  for (const [e, arr] of pools) {
    const q = arr.find((x) => x.id === id);
    if (!q) continue;
    if (exam() !== e) { $("exam").value = e; onExamChange(); }
    deck = [q]; pos = 0; correctCnt = 0; sessionWrong = []; answers = [];
    ["setup", "result", "wrongbook", "review"].forEach((s) => { if ($(s)) hide($(s)); });
    show($("quiz"));
    renderQuestion();
    window.scrollTo(0, 0);
    return true;
  }
  alert(`문항 ${id} 을 찾지 못했습니다.`);
  return false;
}

/* ---------- 개념 복습 화면(복습 필요 · 복습 중 · 재확인 완료) ---------- */
// 첫 화면 버튼에 「오늘 다시 풀 것」 수를 붙인다(learn.js schedule — 2026-09-23)
function updateReviewBadge() {
  const b = $("reviewOpenBtn");
  if (!b || typeof LEARN !== "object" || !LEARN.dueKeys) return;
  let n = 0;
  try { n = LEARN.dueKeys().length; } catch (e) { n = 0; }
  b.textContent = n ? `개념 복습 · 오늘 다시 풀 것 ${n}` : "개념 복습";
}
function renderReview(openConcept) {
  ["setup", "quiz", "result", "wrongbook"].forEach((s) => hide($(s)));
  show($("review"));
  if (typeof LEARN !== "object") { $("rvList").textContent = "학습 흐름 스크립트를 불러오지 못했습니다."; return; }
  LEARN.renderReviewList($("rvList"), "all");
  if (openConcept) {
    const box = $("rvConcept");
    LEARN.renderConcept(box, openConcept, null, null);
    box.hidden = false;
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
  return { start: p.get("start") === "1", q: p.get("q") || "", concept: p.get("concept") || "" };
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
  const qp = applyQueryParams();
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
  if ($("syncBtn")) $("syncBtn").onclick = async () => {
    if (typeof LEARN === "object") await LEARN.syncLearning(false);   // 학습 기록(정리본 큐의 원천)도 함께 보낸다
    syncAll(false);
  };
  if ($("syncKey")) {
    $("syncKey").value = syncKey();
    $("syncKey").onchange = () => onSyncKeyChange($("syncKey").value);
  }
  if ($("syncLinkBtn")) $("syncLinkBtn").onclick = shareSyncLink;
  if ($("syncNeedKeyBtn")) $("syncNeedKeyBtn").onclick = () => {
    const d = document.querySelector(".syncopts"); if (d) d.open = true;
    if ($("syncKey")) $("syncKey").focus();
  };
  if (typeof MEDKOS_SYNC === "object" && MEDKOS_SYNC.captured) setSyncStatus("☁ 연결 링크의 동기화 키를 이 기기에 저장했습니다 — 기록을 올립니다…", "ok");
  describeAuth();
  checkSyncAuth();
  updateWrongCount();
  window.addEventListener("online", () => { if (SYNC.available !== false) syncAll(true); });
  // 핸드폰 앱은 닫히지 않고 백그라운드에서 돌아온다 — 돌아올 때마다 한 번 맞춘다(2026-09-22)
  document.addEventListener("visibilitychange", () => { if (!document.hidden && SYNC.available !== false) syncAll(true); });
  if ($("reviewOpenBtn")) $("reviewOpenBtn").onclick = () => renderReview();
  if ($("rvBackBtn")) $("rvBackBtn").onclick = () => { hide($("review")); show($("setup")); onModeChange(); updateReviewBadge(); };
  updateReviewBadge();
  if ($("rvExportBtn")) $("rvExportBtn").onclick = () => LEARN.exportJson();
  if ($("rvImportFile")) $("rvImportFile").onchange = (ev) => {
    const f = ev.target.files && ev.target.files[0];
    if (!f) return;
    LEARN.importJson(f, (n) => { alert(n < 0 ? "읽을 수 없는 파일입니다." : `기록 ${n}건을 합쳤습니다(기존 기록은 그대로).`); renderReview(); });
    ev.target.value = "";
  };
  if (typeof LEARN === "object") LEARN.syncLearning(true);
  if (qp.q) openSingleQuestion(qp.q);
  else if (qp.concept) renderReview(qp.concept);
  else if (qp.start) startQuiz();
}

document.addEventListener("DOMContentLoaded", init);
