/* 동기화 서버 주소 — 같은 주소면 상대경로, 옛 GitHub Pages 주소면 Cloudflare 주소(2026-09-22). */
var API_BASE = window.MEDKOS_API_BASE = /\.github\.io$/.test(location.hostname) ? "https://my-github-test.pages.dev/" : "";
/* MedKOS 오답 뒤 학습 흐름 — 순수 JS, 의존성 없음 (app.js 의 $·escapeHtml·label·sanitizeHtml·openZoom 을 쓴다)

   흐름(강요하지 않음 — 훑고 넘어가도, 깊게 봐도, 저장만 하고 계속 풀어도 된다):
     채점 → 오답 확인(내 답/정답 · 결정적 차이 · 학습 목표) → 선택한 오답과 정답 비교
     → 개념 정리본 → 임상 판단 도식(이 사례 경로 · 갈림 지점) → 인출 확인 → 변형 문제 → 복습 기록

   원칙
   - 답을 내기 전에는 아무것도 보이지 않는다(app.js 의 grade 뒤에만 불린다).
   - 학습 기록은 **덧붙이기만** 한다(medkos_learning_events). 고치거나 지우지 않는다 — 상태는 기록에서 계산한다.
   - 열람은 학습의 증거가 아니다. 해설 열람 · 정리본 읽음 · 이해 표시 · 이후 적용 성공을 따로 센다.
     「재확인 완료」는 **다음 날 이후** 같은 목표의 다른 문항·변형 문제를 맞혔을 때만.
   - 우선순위는 반복 오답과 후속 확인 실패로 정한다. 「다시 풀 날」(schedule — 2026-09-23 사용자 채택)은 틀린 날 +1일·+7일이
     기본값이지만 **최적이라는 근거로 정한 값이 아니다**(2026-09-18 지시) — 개념 복습 화면에서 바꿀 수 있다.
   - 콘텐츠는 미리 만들어 검토한다 — 여기서 생성하지 않는다(브라우저에 API 키 없음).
   - 콘텐츠의 글자는 escape 하거나 허용 태그만 남기고(sanitizeHtml), 도식은 createElementNS+textContent 로 그린다.
     스크립트·속성·외부 리소스가 끼어들 길을 만들지 않는다. 링크는 https 만.
   - 정리본·도식·문항 필드가 없어도 흐름이 멈추지 않는다(있는 것만 보여 준다). */
"use strict";

const LEARN = (() => {
  const KEY = "medkos_learning_events";
  const CONCEPTS = (window.MEDKOS_CONCEPTS && typeof window.MEDKOS_CONCEPTS === "object") ? window.MEDKOS_CONCEPTS : {};
  const STATUS = { need: "복습 필요", doing: "복습 중", done: "재확인 완료" };
  // 틀린 이유(선택). 학습자가 고르는 것이고, 앱이 「무엇을 모른다」고 단정하지 않는다.
  const REASONS = [
    ["missed_clue", "결정적 단서를 놓쳤다"],
    ["misread_clue", "단서의 의미를 다르게 해석했다"],
    ["two_options", "두 보기 사이에서 망설였다"],
    ["priority", "순서·우선순위가 헷갈렸다"],
    ["criteria", "기준·수치를 다르게 기억했다"],
    ["misread_q", "질문을 다르게 읽었다"],
    ["unsure", "확신 없이 골랐다"],
  ];
  const FLAGS = [
    ["guessed", "찍었다"],
    ["not_understood", "해설이 이해되지 않았다"],
    ["confused", "반복해서 헷갈린다"],
    ["want_note", "정리본으로 보고 싶다"],
  ];
  const KIND_LABEL = { start: "시작", step: "평가·처치", decision: "판단", info: "추가 정보 필요", alert: "위험·이 도식 범위 밖", end: "결론" };
  const STATE_MARK = { path: "★ 이 사례", normal: "★ 정상·음성 확인", abnormal: "★ 이상 소견", unknown: "? 문항에 정보 없음", not_done: "○ 미시행" };

  /* ---------- 기록(덧붙이기만) ---------- */
  function load() {
    try { const a = JSON.parse(localStorage.getItem(KEY) || "[]"); return Array.isArray(a) ? a : []; }
    catch (e) { return []; }
  }
  function save(list) {
    try { localStorage.setItem(KEY, JSON.stringify(list)); return true; }
    catch (e) { return false; }
  }
  function device() { return (typeof SYNC === "object" && SYNC.device) || "web"; }
  function add(ev) {
    const list = load();
    const e = Object.assign({}, ev, {
      eid: `${device()}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`,
      t: new Date().toISOString(), day: kstDay(), device: device(),
    });
    list.push(e);
    save(list);
    scheduleLearnSync();
    return e;
  }
  // 다른 기기·내보낸 파일과 합칠 때: eid 합집합(기존 기록은 그대로)
  function mergeEvents(incoming) {
    const list = load();
    const seen = new Set(list.map((e) => e.eid));
    let n = 0;
    (Array.isArray(incoming) ? incoming : []).forEach((e) => {
      if (e && typeof e === "object" && typeof e.eid === "string" && !seen.has(e.eid) && typeof e.kind === "string") {
        list.push(e); seen.add(e.eid); n++;
      }
    });
    list.sort((a, b) => String(a.t).localeCompare(String(b.t)));
    save(list);
    return n;
  }
  function kstDay(t) { return new Date((t ? Date.parse(t) : Date.now()) + 9 * 3600 * 1000).toISOString().slice(0, 10); }

  /* ---------- 문항·정리본 조회 ---------- */
  let BY_ID = null;
  function qById(id) {
    if (!BY_ID) {
      BY_ID = {};
      [KMLE, USMLE, IMAGING].forEach((arr) => arr.forEach((q) => { if (q && q.id && !BY_ID[q.id]) BY_ID[q.id] = q; }));
    }
    return BY_ID[id] || null;
  }
  function concept(id) { return id && CONCEPTS[id] ? CONCEPTS[id] : null; }
  // 그 정리본에서 내가 틀린 문항(도식 경로가 있는 것만, 최근에 틀린 것부터 넷까지) — 필기장이 도식에 「내가 틀린 사례」로 그린다.
  // 학습 기록의 오답이 먼저이고, 기록이 생기기 전의 오답(오답노트에만 있다)이 뒤에 온다.
  function wrongCases(cid) {
    const seen = {}, out = [];
    const take = (qid) => {
      if (!qid || seen[qid]) return;
      seen[qid] = 1;
      const q = qById(qid);
      if (q && q.objective === cid && (q.casePath || []).length) out.push(q);
    };
    load().filter((e) => e && e.kind === "answer" && !e.ok && e.qid).sort((a, b) => String(b.t).localeCompare(String(a.t))).forEach((e) => take(e.qid));
    try { if (typeof wrongIds === "function") Array.from(wrongIds()).sort().reverse().forEach(take); } catch (e) { /* 오답노트를 못 읽으면 기록만 쓴다 */ }
    return out.slice(0, 4);
  }
  function keyOf(q) { return q && q.objective ? q.objective : "q:" + (q && q.id); }
  function letterOf(i) { return "ABCDE"[i] || ""; }

  /* ---------- 상태 계산(기록에서만) ---------- */
  function states() {
    const ev = load();
    const S = {};
    const get = (key) => (S[key] = S[key] || {
      key, objective: key.startsWith("q:") ? null : key, qids: new Set(), wrongs: 0, wrongQids: new Set(),
      lastWrongT: "", lastWrongDay: "", followFails: 0, followOk: 0, applied: false, appliedT: "",
      viewedExpl: false, viewedNote: false, understood: false, later: false, flags: {}, reasons: {}, chosen: [],
      checksOk: 0, checksMiss: 0, memo: "", lastT: "", active: false,
    });
    ev.forEach((e) => {
      // 기록의 objective 는 푼 순간의 값이다 — 정리본이 나중에 생긴 문항은 지금의 목표로 모은다(learning_log.py 와 같은 규칙)
      const key = e.objective || (e.qid ? ((qById(e.qid) || {}).objective || "q:" + e.qid) : null);
      if (!key) return;
      const s = get(key);
      s.lastT = e.t > s.lastT ? e.t : s.lastT;
      if (e.qid && e.mode !== "variant") s.qids.add(e.qid);
      if (e.kind === "answer") {
        if (!e.ok) {
          s.wrongs++; s.wrongQids.add(e.qid); s.lastWrongT = e.t; s.lastWrongDay = e.day || kstDay(e.t);
          s.applied = false; s.active = false;          // 상태는 마지막 오답 뒤의 활동만 본다
          if (e.chosenText) s.chosen.push({ qid: e.qid, text: e.chosenText, answer: e.answerText || "", day: e.day });
          if (s.wrongs > 1 || e.mode === "variant") s.followFails++;
        } else if (s.wrongs) {
          const later = (e.day || kstDay(e.t)) > s.lastWrongDay;
          const other = e.mode === "variant" || !s.wrongQids.has(e.qid);
          if (later && other) { s.applied = true; s.appliedT = e.t; } else { s.followOk++; s.active = true; }
        }
      } else if (e.kind === "view") {
        if (e.what === "explanation") s.viewedExpl = true;
        if (e.what === "note") s.viewedNote = true;
      } else if (e.kind === "check") {
        if (e.result === "ok") { s.checksOk++; if (s.wrongs) s.followOk++; } else { s.checksMiss++; s.followFails++; }
        s.active = true;
      } else if (e.kind === "understood") { s.understood = true; s.active = true; }
      else if (e.kind === "later") s.later = true;
      else if (e.kind === "flag") s.flags[e.flag] = !!e.on;
      else if (e.kind === "reason") { (e.reasons || []).forEach((r) => { s.reasons[r] = (s.reasons[r] || 0) + 1; }); }
      else if (e.kind === "memo") s.memo = String(e.text || "");
    });
    Object.values(S).forEach((s) => {
      const flagged = Object.values(s.flags).some(Boolean);
      if (!s.wrongs && !flagged && !s.later) { s.status = null; return; }
      if (s.applied) s.status = "done";
      else if (s.active) s.status = "doing";   // 마지막 오답 뒤 능동적 후속 활동(인출 확인·변형 문제·이해 표시). 열람만으로는 바뀌지 않는다
      else s.status = "need";
      s.priority = s.wrongs * 2 + s.followFails * 2 + (s.flags.confused ? 2 : 0) + (s.flags.not_understood ? 1 : 0)
        + (s.flags.guessed ? 1 : 0) + (s.status === "done" ? -10 : 0);
    });
    return S;
  }
  /* ---------- 다시 풀 날(learning_log.py 의 schedule() 과 같은 규칙 — test_learning_books.py 가 같은 픽스처로 본다) ----------
     틀리면 그날이 기준일·0단계. 기준일 + 간격[단계] 일 이후에 같은 목표 문항(변형 포함)을 맞히면 한 단계 올라가고 그날이 새 기준일.
     예정일 전에 맞힌 것은 연습(단계 그대로). 마지막 단계를 넘기면 예정 끝. 다시 틀리면 0단계. */
  const STEPS_KEY = "medkos_review_steps";
  const DEFAULT_STEPS = [1, 7];
  function parseSteps(v) {
    const parts = Array.isArray(v) ? v : String(v == null ? "" : v).replace(/\s/g, "").split(",");
    const out = [];
    for (const x of parts) {
      if (!/^\d+$/.test(String(x))) return DEFAULT_STEPS.slice();
      const n = parseInt(String(x), 10);
      if (n < 1 || n > 365) return DEFAULT_STEPS.slice();
      out.push(n);
    }
    return out.length ? out.slice(0, 6) : DEFAULT_STEPS.slice();
  }
  function reviewSteps() { try { return parseSteps(localStorage.getItem(STEPS_KEY)); } catch (e) { return DEFAULT_STEPS.slice(); } }
  function setReviewSteps(v) { const s = parseSteps(v); try { localStorage.setItem(STEPS_KEY, s.join(",")); } catch (e) { /* 저장 불가 — 이번 화면만 */ } return s; }
  function addDays(day, n) {
    const d = new Date(String(day) + "T00:00:00Z");
    if (isNaN(d.getTime())) return "";
    d.setUTCDate(d.getUTCDate() + n);
    return d.toISOString().slice(0, 10);
  }
  function schedule(steps) {
    const st = steps ? parseSteps(steps) : reviewSteps();
    const out = {};
    load().slice().sort((a, b) => String(a.t).localeCompare(String(b.t)) || String(a.eid).localeCompare(String(b.eid))).forEach((e) => {
      if (e.kind !== "answer") return;
      const key = e.objective || (e.qid ? ((qById(e.qid) || {}).objective || "q:" + e.qid) : null);
      if (!key) return;
      const day = e.day || kstDay(e.t);
      const r = out[key];
      if (!e.ok) out[key] = { stage: 0, total: st.length, anchor: day, due: addDays(day, st[0]) };
      else if (r && r.due && day >= r.due) {
        r.stage++; r.anchor = day;
        r.due = r.stage < st.length ? addDays(day, st[r.stage]) : "";
      }
    });
    return out;
  }
  function dueKeys() {
    const today = kstDay();
    const sc = schedule();
    return Object.keys(sc).filter((k) => sc[k].due && sc[k].due <= today);
  }
  // 다시 풀 문항 고르기: ① 틀린 문항에서 나온 변형(안 푼 것) ② 같은 목표의 다른 변형 ③ 같은 목표의 안 푼 다른 문항 ④ 틀린 문항 그대로
  function pickRetest(key) {
    const s = states()[key];
    if (!s) return null;
    const done = new Set(load().filter((e) => e.kind === "answer").map((e) => e.qid));
    const c = concept(s.objective);
    const vs = (c && c.variants) || [];
    const fresh = vs.filter((v) => !done.has(v.id));
    const own = fresh.find((v) => v.of && s.wrongQids.has(v.of));
    if (own) return { type: "variant", c, v: own };
    if (fresh.length) return { type: "variant", c, v: fresh[0] };
    if (s.objective) {
      for (const arr of [KMLE, USMLE, IMAGING]) {
        const q = arr.find((x) => x && x.objective === s.objective && !done.has(x.id) && !s.wrongQids.has(x.id));
        if (q) return { type: "q", id: q.id };
      }
    }
    const first = Array.from(s.wrongQids).find((id) => id && id.indexOf("#") < 0);
    return first ? { type: "q", id: first } : null;
  }

  function phaseFor(key) {
    const s = states()[key];
    return s && s.lastWrongDay && kstDay() > s.lastWrongDay ? "delayed" : "immediate";
  }

  /* ---------- 채점 훅 ---------- */
  function onAnswer(q, chosenIdx, ok) {
    const ci = q.answer - 1;
    add({ kind: "answer", qid: q.id, qver: q.qversion || 1, exam: q.exam || q.src || (typeof exam === "function" ? exam() : ""),
      objective: q.objective || null, chosen: letterOf(chosenIdx), correct: letterOf(ci), ok,
      chosenText: q.options[chosenIdx] || "", answerText: q.options[ci] || "", mode: "deck" });
    add({ kind: "view", what: "explanation", qid: q.id, objective: q.objective || null });
  }

  // 퀴즈 덱에서 푼 변형 문제(app.js 변형 덱) — 개념 복습 화면의 변형 풀기(renderVariant)와 같은 기록을 남긴다
  function onVariantAnswer(q, chosenIdx, ok) {
    const ci = q.answer - 1;
    add({ kind: "answer", mode: "variant", qid: q.id, objective: q.objective, chosen: letterOf(chosenIdx), correct: letterOf(ci), ok,
      chosenText: q.options[chosenIdx] || "", answerText: q.options[ci] || "", phase: phaseFor(q.objective) });
  }

  /* ---------- 오답 화면 첫 부분 ---------- */
  function wrongPanelHtml(q, chosenIdx) {
    const ci = q.answer - 1;
    const L = String(letterOf(chosenIdx));
    const dist = (q.distractors && q.distractors[L]) || null;
    const d = q.design || {};
    const c = concept(q.objective);
    const diff = (dist && dist.discriminator) || d.discriminator || "";
    const goal = c ? c.objective : (d.decision || "");
    let h = `<section class="learn" data-learn="1">`
      + `<div class="learn-h">오답 확인</div>`
      + `<div class="learn-ab"><div class="mine"><span class="k">내 답</span>${label(chosenIdx, q)} ${escapeHtml(q.options[chosenIdx])}</div>`
      + `<div class="ans"><span class="k">정답</span>${label(ci, q)} ${escapeHtml(q.options[ci])}</div></div>`;
    if (diff) h += `<div class="learn-row"><span class="k">결정적 차이</span>${escapeHtml(diff)}</div>`;
    if (goal) h += `<div class="learn-row"><span class="k">학습 목표</span>${escapeHtml(goal)}</div>`;
    const sc = schedule()[keyOf(q)];
    if (sc && sc.due) h += `<div class="learn-row"><span class="k">다시 풀 날</span>${escapeHtml(sc.due)} — 개념 복습 ▸ 「오늘 다시 풀 것」에 나옵니다(가능하면 변형 문항으로)</div>`;
    if (dist) h += distCard(q, chosenIdx, dist, true);
    const others = q.distractors ? Object.keys(q.distractors).filter((k) => k !== L) : [];
    if (others.length) {
      h += `<details class="learn-others"><summary>다른 오답 보기와의 비교 (${others.length})</summary>`
        + others.map((k) => distCard(q, "ABCDE".indexOf(k), q.distractors[k], false)).join("") + `</details>`;
    }
    h += `<div class="learn-reasons"><div class="learn-sub">왜 이 답을 골랐는지 떠오르면 표시해 두세요 (선택)</div>`
      + REASONS.map(([k, t]) => `<button type="button" class="chip" data-reason="${k}" aria-pressed="false">${escapeHtml(t)}</button>`).join("")
      + `</div>`;
    h += `<div class="learn-actions">`
      + (c ? `<button type="button" class="primary" data-open-concept="${escapeHtml(c.id)}">개념 정리본 · 판단 도식 열기</button>`
           : (q.objective ? `<span class="muted">이 문항의 개념 정리본은 아직 준비 중입니다(목표 ${escapeHtml(q.objective)}).</span>` : ""))
      + `<button type="button" data-later="1">나중에 복습 — 저장하고 계속</button></div>`
      + `<div class="learn-concept" hidden></div></section>`;
    return h;
  }
  function distCard(q, idx, dist, open) {
    const row = (k, v) => (v ? `<div class="dc-row"><span class="k">${k}</span>${escapeHtml(v)}</div>` : "");
    return `<div class="distcard${open ? " chosen" : ""}"><div class="dc-h">${open ? "선택한 " : ""}${label(idx, q)} ${escapeHtml(q.options[idx] || "")} ↔ 정답 ${label(q.answer - 1, q)}</div>`
      + row("왜 끌리는가", dist.tempting) + row("왜 정답이 먼저인가", dist.answer_first)
      + row("가르는 소견", dist.discriminator)
      + (dist.when_right ? row("이 보기가 맞는 경우", dist.when_right) : "") + `</div>`;
  }
  // 맞힌 문항에도 표시(찍었다·정리본 원함 등)를 남길 수 있게
  function flagRowHtml(q) {
    return `<div class="learn-flags" data-flags="1"><span class="learn-sub">표시(선택):</span>`
      + FLAGS.map(([k, t]) => `<button type="button" class="chip" data-flag="${k}" aria-pressed="false">${escapeHtml(t)}</button>`).join("")
      + (concept(q.objective) ? ` <button type="button" class="small" data-open-concept="${escapeHtml(q.objective)}">개념 정리본</button>` : "")
      + `<div class="learn-concept" hidden></div></div>`;
  }

  function bind(root, q, chosenIdx) {
    if (!root) return;
    const key = keyOf(q);
    const S = states()[key] || { flags: {} };
    root.querySelectorAll("button[data-flag]").forEach((b) => {
      const f = b.getAttribute("data-flag");
      setPressed(b, !!S.flags[f]);
      b.onclick = () => {
        const on = b.getAttribute("aria-pressed") !== "true";
        setPressed(b, on);
        add({ kind: "flag", flag: f, on, qid: q.id, objective: q.objective || null });
      };
    });
    const picked = new Set();
    root.querySelectorAll("button[data-reason]").forEach((b) => {
      b.onclick = () => {
        const r = b.getAttribute("data-reason");
        if (picked.has(r)) picked.delete(r); else picked.add(r);
        setPressed(b, picked.has(r));
        add({ kind: "reason", qid: q.id, objective: q.objective || null, reasons: Array.from(picked) });
      };
    });
    root.querySelectorAll("button[data-later]").forEach((b) => {
      b.onclick = () => {
        add({ kind: "later", qid: q.id, objective: q.objective || null });
        b.textContent = "✓ 복습 목록에 저장됨"; b.disabled = true;
        const nb = $("nextBtn"); if (nb) nb.focus();
      };
    });
    root.querySelectorAll("button[data-open-concept]").forEach((b) => {
      b.onclick = () => {
        const box = b.closest("[data-learn],[data-flags]").querySelector(".learn-concept");
        if (!box) return;
        if (!box.hidden) { box.hidden = true; return; }
        renderConcept(box, b.getAttribute("data-open-concept"), q, chosenIdx);
        box.hidden = false;
        box.scrollIntoView({ block: "start", behavior: "smooth" });
      };
    });
  }
  function setPressed(b, on) { b.setAttribute("aria-pressed", on ? "true" : "false"); b.classList.toggle("on", on); }

  /* ---------- 개념 정리본 ---------- */
  // over = 필기장(ink.js)이 넘기는 「내 필기본」의 고정 사본 — 원본이 고쳐진 뒤에도 내가 쓴 판을 그대로 그린다.
  // opts.form — 1 = 판형 12 전의 모양. 필기장(ink.js)이 그 모양일 때 써 둔 필기가 글자와 어긋나지 않게 고른다. 기본은 2(판형 12 · 2026-11-23).
  function renderConcept(box, cid, q, chosenIdx, over, opts) {
    const c = over || concept(cid);
    if (!c) { box.innerHTML = `<p class="muted">개념 정리본을 찾지 못했습니다(${escapeHtml(cid)}).</p>`; return; }
    add({ kind: "view", what: "note", objective: cid, qid: q ? q.id : null });
    const L = q && chosenIdx != null && chosenIdx !== q.answer - 1 ? letterOf(chosenIdx) : "";
    const dist = L && q.distractors ? q.distractors[L] : null;
    const splitNode = dist && dist.split ? dist.split : "";
    const f2 = !(opts && opts.form === 1) && Array.isArray(c.slots);      // 옛 사본(떠 둔 판)에는 slots 가 없다 — 옛 모양으로 그린다
    const rev = c.reviewStatus === "reviewed"
      ? `<span class="badge-ok">내용 검토 완료</span>`
      : `<span class="badge-warn">의학적 내용 검토 전 — 형식 검사만 통과</span>`;
    // 「시험 쟁점」이 해당 없음 한 줄이면 절을 세우지 않고 머리의 배지로 줄인다
    const clean = f2 && c.issues && c.issues.none ? ` · <span class="badge-plain" title="${escapeHtml(c.issues.ref || "")}">Harrison 대조 · 충돌 없음</span>` : "";
    let h = `<article class="concept${f2 ? " f2" : ""}"><div class="cn-h"><div class="cn-title">${escapeHtml(c.title)}</div>`
      + `<div class="cn-meta">${escapeHtml(c.objectiveKind)} · v${escapeHtml(String(c.version || 1))} · ${escapeHtml(c.updated)} · ${rev}${clean}</div>`
      + `<div class="cn-goal"><span class="k">학습 목표</span>${escapeHtml(c.objective)}</div>${f2 ? headExtrasHtml(c) : ""}</div>`;
    if (f2 && c.slots.length) h += slotsHtml(c);
    else if (c.summary && c.summary.length) {
      h += `<div class="cn-sum"><div class="cn-sec">빠른 요약</div><ul>${c.summary.map((s) => `<li>${escapeHtml(s)}</li>`).join("")}</ul></div>`;
    }
    h += figuresHtml(c);
    // 필기장처럼 「이 사례」가 없는 화면에서는 내가 틀린 문항(opts.cases — 최근 것부터)의 경로를 도식에 진하게 그린다(2026-11-23).
    // 여럿이면 제목 줄의 칩으로 바꿔 본다. 칩은 제목 줄 안에 두어 도식의 자리가 밀리지 않는다.
    const cases = !q && opts && Array.isArray(opts.cases) ? opts.cases.filter((x) => x && x.objective === c.id && (x.casePath || []).length) : [];
    const dq = q || cases[0] || null;
    box._cases = cases;
    const chips = cases.length ? `<span class="dia-cases">` + cases.map((x, i) =>
      `<span class="dia-case${i === 0 ? " on" : ""}" role="button" tabindex="0" data-case="${i}">내가 틀린 사례${cases.length > 1 ? " " + (i + 1) : ""}</span>`).join("") + `</span>` : "";
    h += `<div class="cn-dia" data-bk="임상 판단 도식"><div class="cn-sec">임상 판단 도식${q ? " — 이 사례의 경로" : ""}${chips}</div>`
      + `<div class="dia-legend">★ 이 사례가 지난 곳 · ◆ ${L ? "선택한 " + escapeHtml(label(chosenIdx, q)) + " 보기와 " : "오답과 "}갈리는 곳 · ? 문항에 정보 없음 · ○ 미시행 · 굵은 실선 = 이 사례 경로</div>`
      + `<div class="dia-box" role="img" aria-label="${escapeHtml(c.diagramTitle || c.title)}"></div>`
      + `<div class="dia-hint muted">탭하면 크게 · 두 손가락으로 확대</div>`
      + (dist && splitNode ? `<div class="learn-row split"><span class="k">◆ ${escapeHtml(label(chosenIdx, q))} 보기와 갈리는 곳</span>${escapeHtml(nodeText(c, splitNode))} — ${escapeHtml(dist.discriminator || "")}</div>` : "")
      + ((c.diagramNotes || []).length ? `<div class="dia-notes"><div class="cn-sec small">도식에 담기지 않은 조건·예외</div><ul>${c.diagramNotes.map((x) => `<li>${sanitizeHtml(x)}</li>`).join("")}</ul></div>` : "")
      + `<details class="dia-text"><summary>도식을 글로 보기</summary>${stepsHtml(c, dq, splitNode, L ? label(chosenIdx, q) : "")}</details></div>`;
    (c.sections || []).forEach((s) => {
      if (f2 && s.issue && c.issues) return;                      // 시험 쟁점은 아래에서 카드로(해당 없음이면 머리의 배지로)
      const body = sanitizeHtml(s.html);
      h += s.deep
        ? `<details class="cn-deep"><summary>${escapeHtml(s.title)} (심화)</summary><div class="cn-body">${body}</div></details>`
        : `<details class="cn-part"><summary>${escapeHtml(s.title)}</summary><div class="cn-body">${body}</div></details>`;
    });
    (c.tables || []).forEach((tb) => {
      h += `<details class="cn-part"><summary>${escapeHtml(tb.title)}</summary><div class="cn-body"><table><thead><tr>`
        + tb.columns.map((x) => `<th>${escapeHtml(x)}</th>`).join("") + `</tr></thead><tbody>`
        + tb.rows.map((r) => `<tr>${r.map((x) => `<td>${sanitizeHtml(x)}</td>`).join("")}</tr>`).join("")
        + `</tbody></table>${tb.note ? `<p class="small">${sanitizeHtml(tb.note)}</p>` : ""}</div></details>`;
    });
    if (f2) h += checklistsHtml(c);
    if ((c.pitfalls || []).length) {
      h += f2
        // 혼동 ↔ 기준을 나란히 — 「무엇과 헷갈리나」를 왼쪽에서 읽고 「그래서 기준은」을 오른쪽에서 읽는다
        ? `<details class="cn-part" open><summary>혼동하기 쉬운 점 (${c.pitfalls.length})</summary><div class="pit2">`
          + c.pitfalls.map((pf) => `<div class="pc"><div class="pc-a"><span class="pc-k">혼동</span>${escapeHtml(pf.contrast)}</div>`
            + `<div class="pc-b"><span class="pc-k">기준</span>${sanitizeHtml(pf.point)}${pf.cites ? ` ${sanitizeHtml(pf.cites)}` : ""}`
            + (pf.exception ? `<div class="pc-x"><span class="pc-k">예외</span>${sanitizeHtml(pf.exception)}</div>` : "") + `</div></div>`).join("") + `</div></details>`
        : `<details class="cn-part" open><summary>혼동하기 쉬운 점 (${c.pitfalls.length})</summary><ul class="pit">`
          + c.pitfalls.map((pf) => `<li><b>${escapeHtml(pf.contrast)}</b> — ${sanitizeHtml(pf.point)}`
            + (pf.exception ? ` <span class="muted">예외: ${sanitizeHtml(pf.exception)}</span>` : "")
            + (pf.cites ? ` ${sanitizeHtml(pf.cites)}` : "") + `</li>`).join("") + `</ul></details>`;
    }
    if (c.criteria && c.criteria.length) {
      h += `<details class="cn-part"><summary>기준·권고 (${c.criteria.length})</summary>` + c.criteria.map((cr) => criterionHtml(c, cr)).join("") + `</details>`;
    }
    if (f2) h += issuesHtml(c);
    h += checksHtml(c, f2) + variantsHtml(c) + (f2 ? supportsHtml(c) : "") + selfHtml(c) + papersHtml(c) + sourcesHtml(c) + `</article>`;
    box.innerHTML = h;
    drawDiagram(box.querySelector(".dia-box"), c, dq, splitNode, L ? label(chosenIdx, q) : "", box.querySelector(".dia-text"));
    bindConcept(box, c);
    // 필기 단추(ink.js) — 필기장 안에서 다시 그릴 때는 달지 않는다
    if (!box.closest(".ink-sheet") && typeof MEDKOS_INK === "object" && MEDKOS_INK.conceptButton) MEDKOS_INK.conceptButton(box, c.id);
  }
  /* ---------- 판형 12(2026-11-23 vNext Phase 3) — 한눈에 칸 · 같은 질환 · 기초 뿌리 · 시험 쟁점 카드 ----------
     풀이는 내보낼 때 한다(pipelines/note_parts.py — PDF 학습서와 같은 함수). 여기서는 그리기만 한다. 한 가지 톤 · 글자 라벨만(이모티콘 없음).
     종이(필기장) 안에서는 단추가 숨으므로 누르는 것은 <a data-goto> · <a data-root> 로 둔다 — 필기장이 톡을 받아 넘긴다. */
  const titleOf = (id) => { const x = concept(id); return x ? x.title : id; };
  function headExtrasHtml(c) {
    let h = "";
    if (c.series && c.series.length > 1) {
      h += `<div class="cn-series"><span class="k">같은 질환</span>` + c.series.map((s) => (s.id === c.id
        ? `<b class="here">${escapeHtml(s.kind || "이 단원")}</b>`
        : `<a href="#" data-goto="${escapeHtml(s.id)}" title="${escapeHtml(s.title)}">${escapeHtml(s.kind || s.title)}</a>`)).join(`<span class="sep">→</span>`) + `</div>`;
    }
    const ep = c.examPoints || {};
    if (ep.kmle) h += `<div class="cn-exam"><span class="k">KMLE 포인트</span>${sanitizeHtml(ep.kmle)}</div>`;
    if (ep.usmle) h += `<div class="cn-exam"><span class="k">USMLE 포인트</span>${sanitizeHtml(ep.usmle)}</div>`;
    if (c.roots && c.roots.length) {
      h += `<div class="cn-roots"><span class="k">기초 뿌리</span>` + c.roots.map((r) =>
        `<a href="#" data-root="${escapeHtml(r)}">${escapeHtml(titleOf(r))}</a>`).join(`<span class="sep">·</span>`) + `</div>`;
    }
    return h;
  }
  // 칸 안의 줄(2026-11-23 「약제 같은 부분이 다 한 줄이라 읽기 어렵다」) — 한 줄에 이어 쓴 나열을 덩이마다 줄을 바꿔 보인다.
  // 어디서 나눌지는 내보낼 때 정한다(note_parts.slot_groups — PDF 와 같다). 나눌 것이 없으면 글 그대로.
  function slotLinesHtml(s) {
    const gs = s.groups || [];
    const n = gs.reduce((a, g) => a + g.items.length + (g.lead ? 1 : 0), 0);
    if (n <= 1) return sanitizeHtml(s.html);
    return gs.map((g) => (g.lead ? `<div class="sl-lead">${sanitizeHtml(g.lead)}</div>` : "")
      + `<ul class="sl${g.lead ? " sub" : ""}">${g.items.map((x) => `<li>${sanitizeHtml(x)}</li>`).join("")}</ul>`).join("");
  }
  function slotsHtml(c) {
    const main = c.slots.filter((s) => s.kind !== "more"), more = c.slots.filter((s) => s.kind === "more");
    return `<div class="cn-sum"><div class="cn-sec">한눈에</div><div class="slots">`
      + main.map((s) => `<div class="slot k-${escapeHtml(s.kind)}"><div class="slot-k">${escapeHtml(s.label)}</div><div class="slot-t">${slotLinesHtml(s)}</div></div>`).join("")
      + `</div>` + (more.length ? `<ul class="slot-more">${more.map((s) => `<li>${slotLinesHtml(s)}</li>`).join("")}</ul>` : "") + `</div>`;
  }
  function checklistsHtml(c) {
    if (!c.checklists || !c.checklists.length) return "";
    return `<div class="cn-cl"><div class="cn-sec">점수 · 기준 체크리스트</div>` + c.checklists.map((k) =>
      `<div class="cl"><div class="cl-h">${escapeHtml(k.name)}</div><ul class="cl-i">`
      + k.items.map((it) => `<li><span class="cl-box"></span><span class="cl-t">${sanitizeHtml(it.label)}</span>${it.points ? `<span class="cl-p">${escapeHtml(it.points)}</span>` : ""}</li>`).join("")
      + `</ul>${k.cut ? `<div class="cl-c"><span class="pc-k">판정</span>${sanitizeHtml(k.cut)}</div>` : ""}${k.note ? `<div class="muted small">${sanitizeHtml(k.note)}</div>` : ""}</div>`).join("") + `</div>`;
  }
  function issuesHtml(c) {
    const z = c.issues;
    if (!z || z.none || !z.items.length) return "";
    const row = (k, v, cls) => (v ? `<div class="${cls}"><span class="pc-k">${k}</span>${sanitizeHtml(v)}</div>` : "");
    return `<div class="cn-issues"><div class="cn-sec">시험 쟁점</div>` + z.items.map((it) => {
      const four = it.exam || it.other || it.why || it.onexam;
      if (!four) return `<div class="iz iz-note">${sanitizeHtml(it.body)}</div>`;
      return `<div class="iz"><div class="iz-h"><span class="iz-id">${escapeHtml(it.id)}</span>${escapeHtml([it.kind, it.title].filter(Boolean).join(" · "))}</div>`
        + (it.body ? `<div class="iz-b">${sanitizeHtml(it.body)}</div>` : "")
        + `<div class="iz-2">${row("시험 기준", it.exam, "iz-a")}${row("다른 기준", it.other, "iz-o")}</div>`
        + row("왜 다른가", it.why, "iz-w") + row("시험에서는", it.onexam, "iz-s") + `</div>`;
    }).join("") + `</div>`;
  }
  // 기초 정리본 — 이 기전이 받치는 임상 단원(역방향 링크 모음)
  function supportsHtml(c) {
    if (c.layer !== "basic" || !c.rootSupports || !c.rootSupports.length) return "";
    return `<div class="cn-supports"><div class="cn-sec">이 기전이 받치는 임상 단원</div><ul>`
      + c.rootSupports.map((id) => `<li><a href="#" data-goto="${escapeHtml(id)}">${escapeHtml(titleOf(id))}</a></li>`).join("") + `</ul></div>`;
  }
  // 정독 확인(회독 수) — 학습 기록에 「읽음」을 하나 더한다. 정리본의 review_status(내용 검토)와는 다른 것이고,
  // 복습 상태 계산(states)에는 들어가지 않는다(열람은 학습 증거가 아니다 — 규칙은 learning_log.py 와 같다).
  function readCount(cid) { return load().filter((e) => e && e.kind === "view" && e.what === "read" && e.objective === cid).length; }
  function markRead(cid) { add({ kind: "view", what: "read", objective: cid }); return readCount(cid); }
  // 필기장(ink.js)의 「★ 정리본에 넣기」 — 맞힌 문항에도 표시를 남긴다. 규칙은 바꾸지 않고 기록만 더한다.
  function flagsOf(q) { const S = states()[keyOf(q)]; return (S && S.flags) || {}; }
  function setFlag(q, f, on) { return add({ kind: "flag", flag: f, on: !!on, qid: q.id, objective: q.objective || null }); }
  /* ---------- 그림(2026-09-27) — 확실한 라벨만. 소견은 먼저 떠올려 보고 연다(인출) ----------
     src 는 export 가 docs/ 아래 상대경로만 넘긴다. 글은 모두 escape, 링크는 https 만. */
  const BASIS = { dataset_expert: "전문가 판정 데이터셋 라벨", published_figure: "동료 심사 논문의 그림 설명" };
  function figuresHtml(c) {
    const figs = (c.figures || []).filter((f) => f && /^assets\/figures\/[\w.-]+$/.test(f.src || ""));
    if (!figs.length) return "";
    return `<div class="cn-figs"><div class="cn-sec">그림으로 보는 소견 — 먼저 무엇이 보이는지 떠올려 보세요</div>`
      + figs.map((f, i) => {
        const link = (u, t) => (/^https:\/\//.test(u || "") ? ` <a href="${escapeHtml(u)}" target="_blank" rel="noopener noreferrer">${t}</a>` : "");
        return `<figure class="cn-fig" data-fig="${i}"><img src="${escapeHtml(f.src)}" alt="${escapeHtml(f.shows)}" loading="lazy" />`
          + `<figcaption><button type="button" class="small" data-fig-open="${i}">소견 보기</button>`
          + `<div class="fig-ans" hidden><div class="fig-shows">${escapeHtml(f.shows)}</div>`
          + (f.look && f.look.length ? `<ul class="fig-look">${f.look.map((x) => `<li>${escapeHtml(x)}</li>`).join("")}</ul>` : "")
          + `<div class="fig-label"><span class="k">데이터 라벨</span>${escapeHtml(f.label)}</div>`
          + `<div class="muted small">라벨 근거: ${escapeHtml(BASIS[f.basis] || f.basis)} — ${escapeHtml(f.reference)}`
          + (f.paper ? ` · ${escapeHtml(f.paper)}${f.citedBy ? ` (피인용 ${escapeHtml(String(f.citedBy))}회)` : ""}${link(f.doiUrl, "논문")}` : "")
          + `<br>「보는 곳」 설명은 모델이 쓴 것으로 검토 전입니다.${f.marked ? " " + escapeHtml(f.marked) : ""}</div></div>`
          + `<div class="muted small fig-credit">${escapeHtml(f.credit)} · ${escapeHtml(f.license)}${link(f.url, "원본")}</div>`
          + `</figcaption></figure>`;
      }).join("") + `</div>`;
  }
  function nodeText(c, id) {
    const n = (c.geo && c.geo.nodes || []).find((x) => x.id === id);
    return n ? n.lines.join(" ") : id;
  }
  function criterionHtml(c, cr) {
    const src = (c.sources || []).find((s) => s.id === cr.source);
    const ex = Array.isArray(cr.exams) ? cr.exams.map((e) => e.toUpperCase()).join("·") : "";
    return `<div class="crit"><div class="crit-h">${escapeHtml(cr.name)} <span class="muted">${escapeHtml(cr.kind)}</span></div>`
      + `<div class="dc-row"><span class="k">대상</span>${escapeHtml(cr.population)}</div>`
      + `<div class="dc-row"><span class="k">내용</span>${escapeHtml(cr.statement)}</div>`
      + (cr.exceptions ? `<div class="dc-row"><span class="k">예외</span>${escapeHtml(cr.exceptions)}</div>` : "")
      + `<div class="dc-row muted">${escapeHtml(cr.basis === "past_exam" ? "기출 근거" : "현행 권고")}${ex ? " · " + escapeHtml(ex) : ""}`
      + (src ? ` · ${escapeHtml(src.org)} ${escapeHtml(src.year)} · 확인 ${escapeHtml(src.checkedAt)}` : "") + `</div></div>`;
  }
  function stepsHtml(c, q, splitNode, splitLabel) {
    const visit = {};
    ((q && q.objective === c.id && q.casePath) || []).forEach((v) => { visit[v.node] = v; });
    if (!c.steps || !c.steps.length) return `<p class="muted">이 정리본에는 도식이 없습니다.</p>`;
    return `<ol class="steps">` + c.steps.map((s) => {
      const v = visit[s.id];
      const marks = [s.kind];
      if (v) marks.push(STATE_MARK[v.state] || STATE_MARK.path);
      if (splitNode === s.id) marks.push(`◆ ${splitLabel} 보기와 갈림`);
      return `<li value="${s.num}"><span class="st-mark">${escapeHtml(marks.join(" · "))}</span> ${escapeHtml(s.text)}`
        + (v && v.note ? `<div class="st-note">이 사례: ${escapeHtml(v.note)}</div>` : "")
        + (s.branches.length ? `<ul>${s.branches.map((b) => `<li>${escapeHtml(b.label)} → ${b.to}번</li>`).join("")}</ul>` : "")
        + `</li>`;
    }).join("") + `</ol>`;
  }

  /* 도식: 파이프라인이 계산한 배치(geo)를 createElementNS + textContent 로 그린다(innerHTML 없음). */
  function drawDiagram(box, c, q, splitNode, splitLabel, textDetails) {
    const fail = (msg) => {
      box.textContent = msg;
      box.classList.add("dia-fail");
      if (textDetails) textDetails.open = true;       // 도식이 없거나 실패하면 글 대체본을 펼친다
    };
    try {
      const g = c.geo;
      if (!g || !Array.isArray(g.nodes) || !g.nodes.length) { fail("도식을 그릴 수 없어 아래 글로 보여 드립니다."); return; }
      const NS = "http://www.w3.org/2000/svg";
      const el = (tag, attrs, text) => {
        const n = document.createElementNS(NS, tag);
        Object.keys(attrs || {}).forEach((k) => n.setAttribute(k, String(attrs[k])));
        if (text != null) n.textContent = String(text);
        return n;
      };
      const states = {};
      const seq = [];
      ((q && q.objective === c.id && q.casePath) || []).forEach((v) => { states[v.node] = v.state || "path"; seq.push(v.node); });
      const pathEdges = new Set(seq.slice(1).map((n, i) => seq[i] + ">" + n));
      const svg = el("svg", { xmlns: NS, viewBox: `0 0 ${g.w} ${g.h}`, width: g.w, height: g.h, class: "dia-svg",
        "font-family": "NanumGothic, 'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif" });
      svg.appendChild(el("rect", { width: "100%", height: "100%", class: "d-bg" }));
      const defs = el("defs");
      [["ah", "d-arrow"], ["ahp", "d-arrow-path"]].forEach(([id, cls]) => {
        const m = el("marker", { id: id + "-" + c.id.replace(/[^a-z0-9]/gi, ""), viewBox: "0 0 10 10", refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: "auto" });
        m.appendChild(el("path", { d: "M0,0 L10,5 L0,10 z", class: cls }));
        defs.appendChild(m);
      });
      svg.appendChild(defs);
      const mid = c.id.replace(/[^a-z0-9]/gi, "");
      g.edges.forEach((e) => {
        const on = pathEdges.has(e.from + ">" + e.to);
        svg.appendChild(el("polyline", { points: e.points.map((p) => p.join(",")).join(" "), fill: "none",
          class: on ? "d-edge on" : (seq.length ? "d-edge off" : "d-edge"), "marker-end": `url(#${on ? "ahp" : "ah"}-${mid})` }));
      });
      // 사례가 있으면 그 사례가 지나지 않은 곳(노드 · 글 · 선 · 갈래 이름)은 흐리게 한다 — 이 사례의 경로만 진하게 남는다(2026-11-23)
      const has = seq.length > 0;
      g.nodes.forEach((n) => {
        const st = states[n.id];
        const split = n.id === splitNode;
        const dim = has && !st && !split, toff = dim ? " t-off" : "";
        const rx = n.kind === "start" || n.kind === "end" ? 14 : 4;
        svg.appendChild(el("rect", { x: n.x, y: n.y, width: n.w, height: n.h, rx,
          class: `d-node k-${n.kind}${st ? " st st-" + st : ""}${split ? " split" : ""}${dim ? " off" : ""}` }));
        const marks = [n.kindLabel || KIND_LABEL[n.kind] || ""];
        if (st) marks.push(STATE_MARK[st] || STATE_MARK.path);
        if (split) marks.push(`◆ ${splitLabel} 보기와 갈림`);
        svg.appendChild(el("text", { x: n.x + 10, y: n.y + 16, "font-size": 10, class: "d-sub" + (st || split ? " b" : "") + toff }, marks.join(" · ")));
        n.lines.forEach((ln, k) => svg.appendChild(el("text", { x: n.x + 10, y: n.y + 8 + 16 + 17 * k + 13, "font-size": 13,
          class: "d-txt" + (n.kind === "decision" || n.kind === "end" || st ? " b" : "") + toff }, ln)));
      });
      g.edges.forEach((e) => {
        const lab = e.label;
        if (!lab) return;
        const dim = has && !pathEdges.has(e.from + ">" + e.to);
        svg.appendChild(el("rect", { x: lab.x, y: lab.y, width: lab.w, height: lab.h, rx: 3, class: "d-lab" + (dim ? " off" : "") }));
        lab.lines.forEach((ln, k) => svg.appendChild(el("text", { x: lab.x + lab.w / 2, y: lab.y + 13 + 13 * k, "font-size": 11, "text-anchor": "middle",
          class: "d-txt" + (dim ? " t-off" : " b") }, ln)));
      });
      box.textContent = "";
      box.appendChild(svg);
      box.onclick = () => {
        try {
          // 확대 창은 <img> 라 페이지 CSS 가 안 먹는다 — 색을 박아 넣은 복사본을 만든다
          const clone = svg.cloneNode(true);
          const style = el("style", {}, zoomCss(box));
          clone.insertBefore(style, clone.firstChild);
          const blob = new Blob([new XMLSerializer().serializeToString(clone)], { type: "image/svg+xml" });
          openZoom(URL.createObjectURL(blob), c.diagramTitle || c.title);
        } catch (err) { /* 확대 실패는 무시 — 글 대체본이 있다 */ }
      };
    } catch (err) {
      fail("도식을 그리는 중 문제가 생겨 아래 글로 보여 드립니다.");
    }
  }
  // 확대 창은 <img> 라 페이지 CSS(변수 포함)가 안 먹는다 — 도식 상자에 걸린 지금 테마의 색을 읽어 박아 넣는다
  // (필기 종이 안이면 앱이 어두워도 밝은 색이 나온다). 색 이름은 style.css 맨 위 「임상 판단 도식」 변수.
  function zoomCss(box) {
    const cs = getComputedStyle(box);
    const v = (n, d) => (cs.getPropertyValue(n) || "").trim() || d;
    const bg = v("--d-bg", "#ffffff"), edge = v("--d-edge", "#7b8aa0"), on = v("--d-on", "#1d57a8"), stroke = v("--d-stroke", "#94a3b8");
    return `.d-bg{fill:${bg}}.d-edge{stroke:${edge};stroke-width:1.4}.d-edge.off{stroke-dasharray:5 4}`
      + `.d-edge.on{stroke:${on};stroke-width:3.2}.d-arrow{fill:${edge}}.d-arrow-path{fill:${on}}`
      + `.d-node{fill:${v("--d-node", "#ffffff")};stroke:${stroke};stroke-width:1.2}.k-decision{fill:${v("--d-decision", "#e9f0fa")}}`
      + `.k-info{fill:${v("--d-info", "#f8fafc")}}.k-alert{fill:${v("--d-alert", "#f1f4f8")}}.k-end{fill:${v("--d-end", "#f4f7fb")}}`
      + `.d-node.st{stroke:${on};stroke-width:3}.st-unknown,.st-not_done{stroke-dasharray:6 3}.d-node.split{stroke:${v("--d-split", "#d92d20")};stroke-width:3}`
      + `.d-sub{fill:${v("--d-sub", "#5c6c82")}}.d-txt{fill:${v("--d-txt", "#182334")}}.b{font-weight:700}.d-lab{fill:${bg};stroke:${stroke};stroke-width:.6}`
      // 이 사례의 경로만 진하게 — style.css 의 같은 규칙과 맞춘다(규칙의 순서도: 채움 → 정보 없음은 흰 바탕 → 흐리게)
      + `.d-node.st{fill:${v("--d-on-soft", "#d6e6fb")}}.d-node.st-unknown,.d-node.st-not_done{fill:${v("--d-node", "#ffffff")}}`
      + `.d-node.off,.t-off,.d-edge.off,.d-lab.off{opacity:.42}`;
  }

  /* ---------- 인출 확인 · 변형 문제 · 자기 표시 ---------- */
  // 판형 12 — 단원 끝의 「30초 구술 체크」. 종이(필기장) 안에서는 단추가 숨으므로 답을 가림막(.tape) 아래에 두고 톡 쳐서 연다.
  /* 30초 퀴즈(2026-11-23 사용자 「말로 확인하는 것보다 간단한 퀴즈로」) — 구술 체크의 질문마다 보기 넷을 만든다. 정답은 그 질문의 답,
     오답은 같은 정리본의 다른 질문의 답이고, 셋이 안 되면(질문이 서넛뿐인 정리본이 많다) 같은 과의 다른 정리본 답에서 길이가 비슷한 것으로
     채운다. 새 콘텐츠를 쓰지 않는다 — 그래서 보기가 어색한 문항이 섞일 수 있다(사용자가 알고 고른 방식).
     보기와 그 순서는 정리본 id · 질문 번호 · 글자로 **정해진다**(무작위가 아니다) — 종이 위에 써 둔 필기가 보기 자리와 어긋나지 않게. */
  function qzHash(s) {
    let h = 2166136261;
    for (let x = 0; x < s.length; x++) { h ^= s.charCodeAt(x); h = Math.imul(h, 16777619); }
    return h >>> 0;
  }
  function quizOptions(c, i) {
    const ans = String(c.checks[i].a), key = String(c.id) + "#" + i, own = [], seen = {};
    seen[ans] = 1;
    c.checks.forEach((k, j) => { const t = String(k.a); if (j !== i && !seen[t]) { seen[t] = 1; own.push({ t, s: qzHash(key + t) }); } });
    let pool = own.sort((a, b) => a.s - b.s).slice(0, 3);
    if (pool.length < 3) {
      const far = (t) => (Math.abs(t.length - ans.length) > Math.max(12, ans.length * 0.6) ? 1 : 0);      // 길이로 답이 드러나지 않게 비슷한 길이 먼저
      const ext = [];
      Object.keys(CONCEPTS).forEach((id) => {
        const o = CONCEPTS[id];
        if (id === c.id || !c.topic || o.topic !== c.topic) return;
        (o.checks || []).forEach((k) => { const t = String(k.a); if (!seen[t]) { seen[t] = 1; ext.push({ t, far: far(t), s: qzHash(key + t) }); } });
      });
      ext.sort((a, b) => a.far - b.far || a.s - b.s);
      pool = pool.concat(ext.slice(0, 3 - pool.length));
    }
    const opts = pool.map((x) => ({ t: x.t, ok: false }));
    opts.splice(qzHash(key + "@") % (opts.length + 1), 0, { t: ans, ok: true });
    return opts;
  }
  const QZ_NUM = ["①", "②", "③", "④"];
  // 절의 이름표(data-bk) — 필기장은 절 제목으로 필기를 붙들어 둔다. 제목을 바꿔도 전에 쓴 필기가 이 절에 남도록 옛 이름을 그대로 준다.
  const CHECKS_KEY = "30초 구술 체크 — 소리 내어 답해 보고 ";
  function quizHtml(c) {
    return `<div class="cn-checks" data-bk="${CHECKS_KEY}"><div class="cn-sec">30초 퀴즈 — 맞는 답을 톡 쳐서 고르세요<span class="qz-score" data-qz-score></span></div>`
      + c.checks.map((k, i) => `<div class="qz" data-qz-i="${i}"><div class="qz-q">Q${i + 1}. ${escapeHtml(k.q)}</div><div class="qz-opts">`
        + quizOptions(c, i).map((o, j) => `<div class="qz-opt" role="button" tabindex="0" data-qz="${i}:${j}"><span class="n">${QZ_NUM[j]}</span><span>${escapeHtml(o.t)}</span></div>`).join("")
        + `</div></div>`).join("")
      + `</div>`;
  }
  function checksHtml(c, f2) {
    if (!c.checks || !c.checks.length) return "";
    if (f2 && c.checks.length >= 2) return quizHtml(c);
    return `<div class="cn-checks"><div class="cn-sec">${f2 ? "30초 구술 체크 — 소리 내어 답해 보고 여세요" : "인출 확인 — 먼저 떠올려 보고 답을 여세요"}</div>`
      + c.checks.map((k, i) => `<div class="ck" data-ck="${i}"><div class="ck-q">Q${i + 1}. ${escapeHtml(k.q)}</div>`
        + (f2 ? `<div class="ck-tape"><span class="tape" data-tape="1">${escapeHtml(k.a)}</span></div>` : "")
        + `<button type="button" class="small" data-ck-open="${i}">답 보기</button>`
        + `<div class="ck-a" hidden>${escapeHtml(k.a)}<div class="ck-self">떠올린 답이 <button type="button" class="small" data-ck-res="ok">맞았다</button>`
        + `<button type="button" class="small" data-ck-res="miss">달랐다</button></div></div></div>`).join("")
      + `</div>`;
  }
  function variantsHtml(c) {
    if (!c.variants || !c.variants.length) return "";
    return `<div class="cn-var"><div class="cn-sec">변형 문제 — 같은 목표, 다른 맥락</div>`
      + `<p class="muted small">바로 풀면 「즉시 확인」, 다음 날 이후 풀면 「지연된 적용 확인」으로 기록됩니다. 재확인 완료는 지연된 확인에서만 나옵니다.</p>`
      + c.variants.map((v, i) => `<div class="var" data-var="${i}"><button type="button" data-var-open="${i}">변형 ${i + 1} 풀기</button><div class="var-body" hidden></div></div>`).join("")
      + `</div>`;
  }
  function selfHtml(c) {
    const S = states()[c.id] || { flags: {}, memo: "" };
    return `<div class="cn-self"><div class="cn-sec">내 기록</div>`
      + `<div class="learn-flags">` + FLAGS.map(([k, t]) => `<button type="button" class="chip${S.flags[k] ? " on" : ""}" data-cflag="${k}" aria-pressed="${S.flags[k] ? "true" : "false"}">${escapeHtml(t)}</button>`).join("") + `</div>`
      + `<button type="button" class="small" data-understood="1">${S.understood ? "✓ 이해했다고 표시함" : "이해했다고 표시"}</button>`
      + `<span class="muted small"> — 스스로 표시한 것이라 「재확인 완료」로 치지 않습니다.</span>`
      + `<label class="muted small" for="memo-${escapeHtml(c.id)}">내 메모(학습서의 「반복 혼동」 옆에 따로 보관)</label>`
      + `<textarea id="memo-${escapeHtml(c.id)}" class="cn-memo" rows="2">${escapeHtml(S.memo)}</textarea>`
      + `<button type="button" class="small" data-memo="1">메모 저장</button></div>`;
  }
  // 관련 논문(2026-11-15) — 스크랩한 논문 가운데 이 정리본의 질환 이름이 제목 · 초록에 나오는 것(pipelines/export_related_web.py).
  // 글자가 겹친다는 사실만 보인다 — 내용을 검토한 추천이 아니다. 누르면 논문 화면이 그 논문만 띄운다.
  function papersHtml(c) {
    const R = typeof MEDKOS_RELATED === "object" && MEDKOS_RELATED ? MEDKOS_RELATED : null;
    const rows = R && R.concepts ? R.concepts[c.id] : null;
    if (!rows || !rows.length) return "";
    return `<details class="cn-part cn-papers"><summary>관련 논문 (${rows.length})</summary><div class="cn-body">`
      + `<p class="muted small">스크랩한 논문 가운데 이 질환 이름이 제목 · 초록에 나오는 것입니다. 글자가 겹친다는 뜻이지 내용을 검토한 추천은 아닙니다.</p><ul class="cn-paperlist">`
      + rows.map((r) => {
        const p = (R.papers || {})[r.id] || {};
        return `<li><a href="papers.html?id=${encodeURIComponent(r.id)}" target="_blank" rel="noopener" data-paper="${escapeHtml(r.id)}">${escapeHtml(p.t || r.id)}</a>`
          + ` <span class="muted small">${escapeHtml([p.j, p.d].filter(Boolean).join(" · "))} · ${r.how === "t" ? "제목" : "초록"}에 「${escapeHtml(r.term)}」</span></li>`;
      }).join("")
      + `</ul></div></details>`;
  }
  function sourcesHtml(c) {
    if (!c.sources || !c.sources.length) return "";
    return `<details class="cn-part"><summary>출처와 확인일</summary><ul class="refs">` + c.sources.map((s) => {
      const link = /^https:\/\//.test(s.url) ? ` <a href="${escapeHtml(s.url)}" target="_blank" rel="noopener noreferrer">원문</a>` : "";
      return `<li>${escapeHtml(s.org)}. ${escapeHtml(s.title)}. ${escapeHtml(s.citation || s.year)}${link}`
        + `<div class="muted small">${escapeHtml({ text: "본문 대조", abstract: "초록만 대조 †", citation: "서지만 확인 †" }[s.verified] || "서지만 확인 †")} ${escapeHtml(s.checkedAt)} — ${escapeHtml(s.checked)}</div></li>`;
    }).join("") + `</ul></details>`;
  }
  function bindConcept(box, c) {
    // 같은 질환 · 기초 뿌리 · 받치는 임상 단원 — 그 정리본을 필기장으로 연다. 종이 안에서는 필기장(ink.js)이 톡을 받아 처리한다.
    if (!box.closest(".ink-sheet")) {
      box.querySelectorAll("a[data-goto], a[data-root]").forEach((a) => {
        a.onclick = (e) => {
          e.preventDefault();
          const id = a.getAttribute("data-goto") || a.getAttribute("data-root");
          if (typeof MEDKOS_INK === "object" && MEDKOS_INK.open && concept(id)) MEDKOS_INK.open("concept", id);
        };
      });
    }
    box.querySelectorAll("button[data-fig-open]").forEach((b) => {
      b.onclick = () => { const a = b.parentNode.querySelector(".fig-ans"); a.hidden = !a.hidden; b.textContent = a.hidden ? "소견 보기" : "소견 닫기"; };
    });
    box.querySelectorAll(".cn-fig img").forEach((img) => {
      img.onclick = () => { if (typeof openZoom === "function") openZoom(img.getAttribute("src"), img.getAttribute("alt")); };
    });
    // 30초 퀴즈 — 보기를 톡 치면 바로 채점한다(한 질문에 한 번). 결과는 인출 확인 기록(check)으로 남는다. 종이 안에서는 필기장이 톡을 넘겨 준다.
    box.querySelectorAll(".qz-opt").forEach((el) => {
      el.onclick = () => {
        const wrap = el.closest(".qz");
        if (!wrap || wrap.classList.contains("done")) return;
        const ij = el.getAttribute("data-qz").split(":").map(Number), opts = quizOptions(c, ij[0]);
        const ok = !!(opts[ij[1]] && opts[ij[1]].ok);
        wrap.classList.add("done");
        el.classList.add(ok ? "ok" : "no", "pick");
        if (!ok) { const right = wrap.querySelectorAll(".qz-opt")[opts.findIndex((o) => o.ok)]; if (right) right.classList.add("ok"); }
        add({ kind: "check", objective: c.id, idx: ij[0], result: ok ? "ok" : "miss", phase: phaseFor(c.id) });
        const sc = box.querySelector("[data-qz-score]"), all = box.querySelectorAll(".qz").length, done = box.querySelectorAll(".qz.done").length;
        if (sc) sc.textContent = `맞힘 ${box.querySelectorAll(".qz-opt.pick.ok").length} / ${done}` + (done === all ? " · 다 풀었습니다" : "");
      };
    });
    // 도식의 「내가 틀린 사례」 칩 — 그 사례의 경로로 도식을 다시 그린다(도식의 크기는 그대로라 종이가 밀리지 않는다)
    box.querySelectorAll("[data-case]").forEach((ch) => {
      ch.onclick = () => {
        const cases = box._cases || [], i = Number(ch.getAttribute("data-case")), q = cases[i];
        if (!q) return;
        box.querySelectorAll("[data-case]").forEach((x) => x.classList.toggle("on", x === ch));
        const det = box.querySelector(".dia-text");
        drawDiagram(box.querySelector(".dia-box"), c, q, "", "", det);
        if (det) { const ol = det.querySelector(".steps"); if (ol) ol.outerHTML = stepsHtml(c, q, "", ""); }
      };
    });
    box.querySelectorAll("button[data-ck-open]").forEach((b) => {
      b.onclick = () => { const a = b.parentNode.querySelector(".ck-a"); a.hidden = false; b.hidden = true; };
    });
    box.querySelectorAll("button[data-ck-res]").forEach((b) => {
      b.onclick = () => {
        const i = Number(b.closest("[data-ck]").getAttribute("data-ck"));
        add({ kind: "check", objective: c.id, idx: i, result: b.getAttribute("data-ck-res"), phase: phaseFor(c.id) });
        b.parentNode.textContent = b.getAttribute("data-ck-res") === "ok" ? "✓ 기록했습니다" : "✓ 기록했습니다 — 복습 우선순위에 반영됩니다";
      };
    });
    box.querySelectorAll("button[data-var-open]").forEach((b) => {
      b.onclick = () => {
        const i = Number(b.getAttribute("data-var-open"));
        const body = b.parentNode.querySelector(".var-body");
        renderVariant(body, c, c.variants[i]);
        body.hidden = false; b.hidden = true;
      };
    });
    box.querySelectorAll("button[data-cflag]").forEach((b) => {
      b.onclick = () => {
        const on = b.getAttribute("aria-pressed") !== "true";
        setPressed(b, on);
        add({ kind: "flag", flag: b.getAttribute("data-cflag"), on, objective: c.id });
      };
    });
    box.querySelectorAll("button[data-understood]").forEach((b) => {
      b.onclick = () => { add({ kind: "understood", objective: c.id }); b.textContent = "✓ 이해했다고 표시함"; };
    });
    box.querySelectorAll("button[data-memo]").forEach((b) => {
      b.onclick = () => {
        const ta = box.querySelector(".cn-memo");
        add({ kind: "memo", objective: c.id, text: String(ta.value || "").slice(0, 2000) });
        b.textContent = "✓ 저장됨";
      };
    });
  }
  function renderVariant(body, c, v) {
    const phase = phaseFor(c.id);
    body.innerHTML = `<div class="var-ctx muted small">${escapeHtml(v.context || "")}</div><p class="vignette">${escapeHtml(v.stem)}</p>`
      + `<div class="var-opts">${v.options.map((o, i) => `<button type="button" class="opt" data-vopt="${i}"><span class="num">${ALPHA[i]}</span>${escapeHtml(o)}</button>`).join("")}</div>`
      + `<div class="var-res" hidden></div>`;
    body.querySelectorAll("button[data-vopt]").forEach((b) => {
      b.onclick = () => {
        const i = Number(b.getAttribute("data-vopt"));
        const ok = i === v.answer - 1;
        body.querySelectorAll("button[data-vopt]").forEach((x, k) => {
          x.disabled = true;
          if (k === v.answer - 1) x.classList.add("correct");
          if (k === i && !ok) x.classList.add("wrong");
        });
        add({ kind: "answer", mode: "variant", qid: v.id, objective: c.id, chosen: letterOf(i), correct: letterOf(v.answer - 1), ok,
          chosenText: v.options[i], answerText: v.options[v.answer - 1], phase });
        const res = body.querySelector(".var-res");
        res.innerHTML = `<div class="verdict ${ok ? "ok" : "bad"}">${ok ? "맞았습니다" : "다릅니다"} · 정답 ${ALPHA[v.answer - 1]}</div>`
          + `<div class="expl-item">${escapeHtml(v.explanation)}</div>`
          + (v.changed ? `<div class="learn-row"><span class="k">${v.flip ? "바뀐 단서 → 답이 바뀜" : "바뀐 겉모습 → 답은 그대로"}</span>${escapeHtml(v.changed)}</div>` : "")
          + `<div class="muted small">${phase === "delayed" ? "지연된 적용 확인으로 기록했습니다." : "즉시 확인으로 기록했습니다 — 다음 날 이후 다시 확인하면 재확인 완료가 될 수 있습니다."}</div>`;
        res.hidden = false;
      };
    });
  }

  /* ---------- 개념 복습 목록 ---------- */
  function renderReviewList(container, filter) {
    const S = states();
    const rows = Object.values(S).filter((s) => s.status && (!filter || filter === "all" || s.status === filter))
      .sort((a, b) => (b.priority - a.priority) || String(b.lastT).localeCompare(String(a.lastT)));
    const counts = { need: 0, doing: 0, done: 0 };
    Object.values(S).forEach((s) => { if (s.status) counts[s.status]++; });
    let h = `<div class="rv-filter">` + [["all", "전체"], ["need", STATUS.need], ["doing", STATUS.doing], ["done", STATUS.done]].map(([k, t]) =>
      `<button type="button" class="chip${(filter || "all") === k ? " on" : ""}" data-rvf="${k}">${t}${k !== "all" ? " " + counts[k] : ""}</button>`).join("") + `</div>`;
    h += dueHtml();
    h += `<p class="muted small">아래 목록 순서는 반복 오답·후속 확인 실패가 많은 것부터입니다. 재확인 완료도 지우지 않고 남깁니다.</p>`;
    if (!rows.length) h += `<p class="muted">아직 기록이 없습니다. 문항을 풀고 오답이 생기면 여기에 모입니다.</p>`;
    h += rows.map((s) => {
      const c = concept(s.objective);
      const q = !c && s.key.startsWith("q:") ? qById(s.key.slice(2)) : null;
      const title = c ? c.title : q ? `[${q.subject}] ${q.question}` : s.key;
      const ev = [s.viewedExpl && "해설 열람", s.viewedNote && "정리본 읽음", s.understood && "이해 표시", s.applied && "이후 적용 성공"].filter(Boolean);
      return `<div class="rv" data-key="${escapeHtml(s.key)}"><div class="rv-h"><span class="rv-st st-${s.status}">${STATUS[s.status]}</span> ${escapeHtml(title)}</div>`
        + `<div class="muted small">오답 ${s.wrongs} · 후속 확인 실패 ${s.followFails} · 인출 확인 ${s.checksOk}/${s.checksOk + s.checksMiss}`
        + (s.lastWrongDay ? ` · 마지막 오답 ${escapeHtml(s.lastWrongDay)}` : "") + (ev.length ? ` · ${ev.join(" · ")}` : "") + `</div>`
        + (c ? `<button type="button" class="small" data-rv-open="${escapeHtml(c.id)}">정리본·변형 문제</button>` : (s.objective ? `<span class="muted small">정리본 준비 중</span>` : ""))
        + Array.from(s.qids).slice(0, 6).map((id) => `<button type="button" class="small" data-rv-q="${escapeHtml(id)}">문항 ${escapeHtml(id)}</button>`).join("")
        + `<div class="learn-concept" hidden></div></div>`;
    }).join("");
    container.innerHTML = h;
    container.querySelectorAll("button[data-rvf]").forEach((b) => { b.onclick = () => renderReviewList(container, b.getAttribute("data-rvf")); });
    container.querySelectorAll("button[data-rt]").forEach((b) => {
      b.onclick = () => {
        const p = pickRetest(b.getAttribute("data-rt"));
        const body = b.parentNode.querySelector(".rt-body");
        if (!p) { body.textContent = "다시 풀 문항을 찾지 못했습니다(문항이 덱에서 빠졌을 수 있습니다)."; body.hidden = false; return; }
        if (p.type === "q") { openSingleQuestion(p.id); return; }
        renderVariant(body, p.c, p.v);
        body.hidden = false; b.hidden = true;
      };
    });
    const sb = container.querySelector("button[data-steps-save]");
    if (sb) sb.onclick = () => {
      const s = setReviewSteps(container.querySelector("#rvSteps").value);
      renderReviewList(container, filter);
      const note = container.querySelector(".rt-steps-note");
      if (note) note.textContent = `저장했습니다 — ${s.join("일 · ")}일`;
    };
    container.querySelectorAll("button[data-rv-open]").forEach((b) => {
      b.onclick = () => {
        const box = b.parentNode.querySelector(".learn-concept");
        if (!box.hidden) { box.hidden = true; return; }
        renderConcept(box, b.getAttribute("data-rv-open"), null, null);
        box.hidden = false;
      };
    });
    container.querySelectorAll("button[data-rv-q]").forEach((b) => { b.onclick = () => openSingleQuestion(b.getAttribute("data-rv-q")); });
  }

  function dueHtml() {
    const sc = schedule();
    const today = kstDay();
    const S = states();
    const title = (key) => {
      const c = concept(S[key] && S[key].objective);
      const q = !c && key.startsWith("q:") ? qById(key.slice(2)) : null;
      return c ? c.title : q ? `[${q.subject}] ${q.question}` : key;
    };
    const keys = Object.keys(sc).filter((k) => sc[k].due);
    const due = keys.filter((k) => sc[k].due <= today)
      .sort((a, b) => sc[a].due.localeCompare(sc[b].due) || ((S[b] || {}).priority || 0) - ((S[a] || {}).priority || 0));
    const later = keys.filter((k) => sc[k].due > today).sort((a, b) => sc[a].due.localeCompare(sc[b].due));
    const steps = reviewSteps();
    let h = `<div class="rt"><div class="cn-sec">오늘 다시 풀 것 ${due.length}</div>`;
    h += due.length ? due.map((k) => `<div class="rv"><div class="rv-h">${escapeHtml(title(k))}</div>`
        + `<div class="muted small">예정일 ${escapeHtml(sc[k].due)} · ${sc[k].stage + 1}/${sc[k].total}단계</div>`
        + `<button type="button" class="small primary" data-rt="${escapeHtml(k)}">다시 풀기</button><div class="rt-body" hidden></div></div>`).join("")
      : `<p class="muted small">오늘 예정된 문항이 없습니다.</p>`;
    if (later.length) {
      h += `<details class="learn-others"><summary>앞으로 예정 ${later.length}</summary>`
        + later.map((k) => `<div class="muted small">${escapeHtml(sc[k].due)} · ${escapeHtml(title(k))}</div>`).join("") + `</details>`;
    }
    h += `<div class="rt-steps muted small"><label for="rvSteps">다시 풀 간격(일, 쉼표로)</label> `
      + `<input id="rvSteps" value="${escapeHtml(steps.join(","))}" size="10" inputmode="numeric" /> `
      + `<button type="button" class="small" data-steps-save="1">저장</button> <span class="rt-steps-note"></span><br>`
      + `틀린 날부터 첫 간격 뒤에 다시 풀고, 맞히면 다음 간격으로 넘어갑니다. 예정일 전에 푼 것은 연습으로 칩니다. `
      + `기본 1일·7일은 출발점일 뿐 최적이라고 검증된 값이 아닙니다 — 자신에게 맞게 바꾸세요.</div></div>`;
    return h;
  }

  /* ---------- 내보내기·가져오기(드라이브 수신함 · 기기 이동용) ---------- */
  function exportJson() {
    const body = { format: "medkos-learning-events/1", exported: new Date().toISOString(), device: device(), events: load() };
    download(`medkos_학습기록_${device()}_${kstDay()}.json`, JSON.stringify(body, null, 1), "application/json");
  }
  function importJson(file, done) {
    const r = new FileReader();
    r.onload = () => {
      try {
        const data = JSON.parse(String(r.result || "{}"));
        done(mergeEvents(Array.isArray(data) ? data : data.events));
      } catch (e) { done(-1); }
    };
    r.readAsText(file);
  }

  /* ---------- 동기화(/api/learning — 있으면) ---------- */
  // 옛 주소(GitHub Pages)에는 동기화 서버가 없다 — 그 주소에서 연 앱(예: 예전에 설치한 아이패드 홈 화면 앱)은
  // Cloudflare 주소의 /api 를 직접 부른다(서버 쪽 functions/api/_middleware.js 가 그 출처만 CORS 허용, 2026-09-22).
  // 2026-09-22: 예전에는 첫 전송이 한 번만 실패해도(잠깐 오프라인·서버 일시 오류) 그 세션 내내 다시 보내지 않았다.
  // 핸드폰 앱은 하루 종일 백그라운드에 살아 있어서 그날 기록이 통째로 저장소에 안 올라갔다.
  // 이제 「함수가 없는 호스트」(404·405·501·JSON 아님)만 포기하고, 나머지 실패는 간격을 늘려 다시 시도하며
  // 앱으로 돌아올 때·온라인이 될 때·「지금 동기화」를 누를 때도 보낸다. 서버는 eid 합집합이라 여러 번 보내도 안전하다.
  let syncTimer = null;
  const LSYNC = { url: API_BASE + "api/learning", available: null, busy: false, fails: 0, lastOk: "", lastError: "", needsKey: false };
  function scheduleLearnSync(delay) {
    if (LSYNC.available === false) return;
    clearTimeout(syncTimer);
    syncTimer = setTimeout(() => syncLearning(true), delay == null ? 2500 : delay);
  }
  async function syncLearning(quiet) {
    if (LSYNC.busy || LSYNC.available === false || typeof fetch !== "function") return LSYNC;
    LSYNC.busy = true;
    try {
      const headers = Object.assign({ "content-type": "application/json" }, typeof syncHeaders === "function" ? syncHeaders() : {});
      const r = await fetch(LSYNC.url, { method: "POST", headers, body: JSON.stringify({ device: device(), events: load() }) });
      if (r.status === 404 || r.status === 405 || r.status === 501) { LSYNC.available = false; return LSYNC; }  // 함수 없는 호스트
      // 키 없음·틀림은 다시 보내도 같다 — 재시도하지 않고 표시만 한다. 키가 바뀌면 app.js 가 syncLearning 을 다시 부른다(2026-09-23).
      if (r.status === 401) { LSYNC.needsKey = true; LSYNC.lastError = "동기화 키 필요"; return LSYNC; }
      if (!r.ok) throw new Error("HTTP " + r.status);
      if (!/json/.test(r.headers.get("content-type") || "")) { LSYNC.available = false; return LSYNC; }
      LSYNC.available = true; LSYNC.fails = 0; LSYNC.lastError = ""; LSYNC.needsKey = false;
      LSYNC.lastOk = new Date().toTimeString().slice(0, 5);
      const data = await r.json();
      if (data && Array.isArray(data.events)) mergeEvents(data.events);
    } catch (e) {
      LSYNC.fails += 1;
      LSYNC.lastError = String((e && e.message) || e);
      scheduleLearnSync(Math.min(10 * 60 * 1000, 20000 * Math.pow(2, LSYNC.fails - 1)));   // 20초·40초·80초 … 최대 10분
    } finally { LSYNC.busy = false; }
    return LSYNC;
  }
  function learnSyncState() { return { available: LSYNC.available, fails: LSYNC.fails, lastOk: LSYNC.lastOk, lastError: LSYNC.lastError, needsKey: LSYNC.needsKey, count: load().length }; }
  if (typeof document !== "undefined") {
    document.addEventListener("visibilitychange", () => { if (!document.hidden) scheduleLearnSync(500); });
    window.addEventListener("online", () => scheduleLearnSync(500));
  }

  return { onAnswer, onVariantAnswer, wrongPanelHtml, flagRowHtml, bind, renderConcept, renderReviewList, exportJson, importJson,
    syncLearning, learnSyncState, states, schedule, dueKeys, pickRetest, reviewSteps, load, concept, STATUS, flagsOf, setFlag,
    readCount, markRead, wrongCases, quizOptions };
})();
