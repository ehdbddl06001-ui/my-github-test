/* MedKOS 오답 뒤 학습 흐름 — 순수 JS, 의존성 없음 (app.js 의 $·escapeHtml·label·sanitizeHtml·openZoom 을 쓴다)

   흐름(강요하지 않음 — 훑고 넘어가도, 깊게 봐도, 저장만 하고 계속 풀어도 된다):
     채점 → 오답 확인(내 답/정답 · 결정적 차이 · 학습 목표) → 선택한 오답과 정답 비교
     → 개념 정리본 → 임상 판단 도식(이 사례 경로 · 갈림 지점) → 인출 확인 → 변형 문제 → 복습 기록

   원칙
   - 답을 내기 전에는 아무것도 보이지 않는다(app.js 의 grade 뒤에만 불린다).
   - 학습 기록은 **덧붙이기만** 한다(medkos_learning_events). 고치거나 지우지 않는다 — 상태는 기록에서 계산한다.
   - 열람은 학습의 증거가 아니다. 해설 열람 · 정리본 읽음 · 이해 표시 · 이후 적용 성공을 따로 센다.
     「재확인 완료」는 **다음 날 이후** 같은 목표의 다른 문항·변형 문제를 맞혔을 때만.
   - 정해진 「최적 간격」을 두지 않는다. 우선순위는 반복 오답과 후속 확인 실패로만 정한다.
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
      const key = e.objective || (e.qid ? "q:" + e.qid : null);
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
  function phaseFor(key) {
    const s = states()[key];
    return s && s.lastWrongDay && kstDay() > s.lastWrongDay ? "delayed" : "immediate";
  }

  /* ---------- 채점 훅 ---------- */
  function onAnswer(q, chosenIdx, ok) {
    const ci = q.answer - 1;
    add({ kind: "answer", qid: q.id, qver: q.qversion || 1, exam: q.exam || (typeof exam === "function" ? exam() : ""),
      objective: q.objective || null, chosen: letterOf(chosenIdx), correct: letterOf(ci), ok,
      chosenText: q.options[chosenIdx] || "", answerText: q.options[ci] || "", mode: "deck" });
    add({ kind: "view", what: "explanation", qid: q.id, objective: q.objective || null });
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
  function renderConcept(box, cid, q, chosenIdx) {
    const c = concept(cid);
    if (!c) { box.innerHTML = `<p class="muted">개념 정리본을 찾지 못했습니다(${escapeHtml(cid)}).</p>`; return; }
    add({ kind: "view", what: "note", objective: cid, qid: q ? q.id : null });
    const L = q && chosenIdx != null && chosenIdx !== q.answer - 1 ? letterOf(chosenIdx) : "";
    const dist = L && q.distractors ? q.distractors[L] : null;
    const splitNode = dist && dist.split ? dist.split : "";
    const rev = c.reviewStatus === "reviewed"
      ? `<span class="badge-ok">내용 검토 완료</span>`
      : `<span class="badge-warn">의학적 내용 검토 전 — 형식 검사만 통과</span>`;
    let h = `<article class="concept"><div class="cn-h"><div class="cn-title">${escapeHtml(c.title)}</div>`
      + `<div class="cn-meta">${escapeHtml(c.objectiveKind)} · v${escapeHtml(String(c.version || 1))} · ${escapeHtml(c.updated)} · ${rev}</div>`
      + `<div class="cn-goal"><span class="k">학습 목표</span>${escapeHtml(c.objective)}</div></div>`;
    if (c.summary && c.summary.length) {
      h += `<div class="cn-sum"><div class="cn-sec">빠른 요약</div><ul>${c.summary.map((s) => `<li>${escapeHtml(s)}</li>`).join("")}</ul></div>`;
    }
    h += `<div class="cn-dia"><div class="cn-sec">임상 판단 도식${q ? " — 이 사례의 경로" : ""}</div>`
      + `<div class="dia-legend">★ 이 사례가 지난 곳 · ◆ ${L ? "선택한 " + escapeHtml(label(chosenIdx, q)) + " 보기와 " : "오답과 "}갈리는 곳 · ? 문항에 정보 없음 · ○ 미시행 · 굵은 실선 = 이 사례 경로</div>`
      + `<div class="dia-box" role="img" aria-label="${escapeHtml(c.diagramTitle || c.title)}"></div>`
      + `<div class="dia-hint muted">탭하면 크게 · 두 손가락으로 확대</div>`
      + (dist && splitNode ? `<div class="learn-row split"><span class="k">◆ ${escapeHtml(label(chosenIdx, q))} 보기와 갈리는 곳</span>${escapeHtml(nodeText(c, splitNode))} — ${escapeHtml(dist.discriminator || "")}</div>` : "")
      + `<details class="dia-text"><summary>도식을 글로 보기</summary>${stepsHtml(c, q, splitNode, L ? label(chosenIdx, q) : "")}</details></div>`;
    (c.sections || []).forEach((s) => {
      const body = sanitizeHtml(s.html);
      h += s.deep
        ? `<details class="cn-deep"><summary>${escapeHtml(s.title)} (심화)</summary><div class="cn-body">${body}</div></details>`
        : `<details class="cn-part"><summary>${escapeHtml(s.title)}</summary><div class="cn-body">${body}</div></details>`;
    });
    if (c.criteria && c.criteria.length) {
      h += `<details class="cn-part"><summary>기준·권고 (${c.criteria.length})</summary>` + c.criteria.map((cr) => criterionHtml(c, cr)).join("") + `</details>`;
    }
    h += checksHtml(c) + variantsHtml(c) + selfHtml(c) + sourcesHtml(c) + `</article>`;
    box.innerHTML = h;
    drawDiagram(box.querySelector(".dia-box"), c, q, splitNode, L ? label(chosenIdx, q) : "", box.querySelector(".dia-text"));
    bindConcept(box, c);
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
      g.nodes.forEach((n) => {
        const st = states[n.id];
        const split = n.id === splitNode;
        const rx = n.kind === "start" || n.kind === "end" ? 14 : 4;
        svg.appendChild(el("rect", { x: n.x, y: n.y, width: n.w, height: n.h, rx,
          class: `d-node k-${n.kind}${st ? " st st-" + st : ""}${split ? " split" : ""}` }));
        const marks = [n.kindLabel || KIND_LABEL[n.kind] || ""];
        if (st) marks.push(STATE_MARK[st] || STATE_MARK.path);
        if (split) marks.push(`◆ ${splitLabel} 보기와 갈림`);
        svg.appendChild(el("text", { x: n.x + 10, y: n.y + 16, "font-size": 10, class: "d-sub" + (st || split ? " b" : "") }, marks.join(" · ")));
        n.lines.forEach((ln, k) => svg.appendChild(el("text", { x: n.x + 10, y: n.y + 8 + 16 + 17 * k + 13, "font-size": 13,
          class: "d-txt" + (n.kind === "decision" || n.kind === "end" ? " b" : "") }, ln)));
      });
      g.edges.forEach((e) => {
        const lab = e.label;
        if (!lab) return;
        svg.appendChild(el("rect", { x: lab.x, y: lab.y, width: lab.w, height: lab.h, rx: 3, class: "d-lab" }));
        lab.lines.forEach((ln, k) => svg.appendChild(el("text", { x: lab.x + lab.w / 2, y: lab.y + 13 + 13 * k, "font-size": 11, "text-anchor": "middle", class: "d-txt" }, ln)));
      });
      box.textContent = "";
      box.appendChild(svg);
      box.onclick = () => {
        try {
          // 확대 창은 <img> 라 페이지 CSS 가 안 먹는다 — 색을 박아 넣은 복사본을 만든다
          const clone = svg.cloneNode(true);
          const style = el("style", {}, ZOOM_CSS);
          clone.insertBefore(style, clone.firstChild);
          const blob = new Blob([new XMLSerializer().serializeToString(clone)], { type: "image/svg+xml" });
          openZoom(URL.createObjectURL(blob), c.diagramTitle || c.title);
        } catch (err) { /* 확대 실패는 무시 — 글 대체본이 있다 */ }
      };
    } catch (err) {
      fail("도식을 그리는 중 문제가 생겨 아래 글로 보여 드립니다.");
    }
  }
  const ZOOM_CSS = ".d-bg{fill:#0e1826}.d-edge{stroke:#7f8fa6;stroke-width:1.4}.d-edge.off{stroke-dasharray:5 4}"
    + ".d-edge.on{stroke:#7cb8ff;stroke-width:3.2}.d-arrow{fill:#7f8fa6}.d-arrow-path{fill:#7cb8ff}"
    + ".d-node{fill:#16212f;stroke:#7f8fa6;stroke-width:1.2}.k-decision{fill:#2a2412}.k-info{fill:#141f36}.k-alert{fill:#321417}.k-end{fill:#11281c}"
    + ".d-node.st{stroke:#7cb8ff;stroke-width:3}.st-unknown,.st-not_done{stroke-dasharray:6 3}.d-node.split{stroke:#ff8a80;stroke-width:3}"
    + ".d-sub{fill:#a9b6c6}.d-txt{fill:#e6edf5}.b{font-weight:700}.d-lab{fill:#0e1826;stroke:#7f8fa6;stroke-width:.6}";

  /* ---------- 인출 확인 · 변형 문제 · 자기 표시 ---------- */
  function checksHtml(c) {
    if (!c.checks || !c.checks.length) return "";
    return `<div class="cn-checks"><div class="cn-sec">인출 확인 — 먼저 떠올려 보고 답을 여세요</div>`
      + c.checks.map((k, i) => `<div class="ck" data-ck="${i}"><div class="ck-q">Q${i + 1}. ${escapeHtml(k.q)}</div>`
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
  function sourcesHtml(c) {
    if (!c.sources || !c.sources.length) return "";
    return `<details class="cn-part"><summary>출처와 확인일</summary><ul class="refs">` + c.sources.map((s) => {
      const link = /^https:\/\//.test(s.url) ? ` <a href="${escapeHtml(s.url)}" target="_blank" rel="noopener noreferrer">원문</a>` : "";
      return `<li>${escapeHtml(s.org)}. ${escapeHtml(s.title)}. ${escapeHtml(s.citation || s.year)}${link}`
        + `<div class="muted small">확인 ${escapeHtml(s.checkedAt)} — ${escapeHtml(s.checked)}</div></li>`;
    }).join("") + `</ul></details>`;
  }
  function bindConcept(box, c) {
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
        res.innerHTML = `<div class="verdict ${ok ? "ok" : "bad"}">${ok ? "✅ 맞았습니다" : "❌ 다릅니다"} · 정답 ${ALPHA[v.answer - 1]}</div>`
          + `<div class="expl-item">${escapeHtml(v.explanation)}</div>`
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
    h += `<p class="muted small">순서는 반복 오답·후속 확인 실패가 많은 것부터입니다. 정해진 복습 간격은 두지 않습니다. 재확인 완료도 지우지 않고 남깁니다.</p>`;
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
  let syncTimer = null;
  const LSYNC = { url: "api/learning", available: null, busy: false };
  function scheduleLearnSync() {
    if (LSYNC.available === false) return;
    clearTimeout(syncTimer);
    syncTimer = setTimeout(() => syncLearning(true), 2500);
  }
  async function syncLearning(quiet) {
    if (LSYNC.busy || LSYNC.available === false || typeof fetch !== "function") return;
    LSYNC.busy = true;
    try {
      const headers = Object.assign({ "content-type": "application/json" }, typeof syncHeaders === "function" ? syncHeaders() : {});
      const r = await fetch(LSYNC.url, { method: "POST", headers, body: JSON.stringify({ device: device(), events: load() }) });
      // 함수가 없는 호스트(GitHub Pages 405 · 정적 서버 501 · 404)나 서버 오류면 이 세션은 로컬 기록만 쓴다
      if (!r.ok || !/json/.test(r.headers.get("content-type") || "")) { LSYNC.available = false; return; }
      LSYNC.available = true;
      const data = await r.json();
      if (data && Array.isArray(data.events)) mergeEvents(data.events);
    } catch (e) { LSYNC.available = false; /* 오프라인·함수 없음 → 로컬 기록만(다음 방문에 다시 확인) */ }
    finally { LSYNC.busy = false; }
  }

  return { onAnswer, wrongPanelHtml, flagRowHtml, bind, renderConcept, renderReviewList, exportJson, importJson,
    syncLearning, states, load, concept, STATUS };
})();
