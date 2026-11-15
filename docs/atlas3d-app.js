/* MedKOS 3D 아틀라스 — 공개 3D 인체 모형을 페이지 안에서 돌려 보는 화면.
   자료: atlas3d-data.js(window.ATLAS3D — 장면 목록 · 부품 이름 · 층) + assets/atlas3d/models/<장면>.js(window.BP3D)
   뷰어: assets/atlas3d/lib/viewer3d.js (three.js r147). 퀴즈 · 시험 정보는 없다 — 구조를 보는 용도만.
   자료 갱신은 정리본 저장소의 work/anat_atlas/export_medkos.py 가 한다(이 파일은 손으로 고친다). */
(function () {
  'use strict';
  const A = window.ATLAS3D || { scenes: [], areas: [], layers: [], sources: [] };
  const SCENES = A.scenes || [], LAYERS = A.layers || [];
  const BASE = 'assets/atlas3d/', VER = '?b=' + (A.built || '0');
  const $ = (sel, el = document) => el.querySelector(sel);
  const $$ = (sel, el = document) => [...el.querySelectorAll(sel)];
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const store = {
    get(k, d) { try { const v = localStorage.getItem('medkos_atlas3d_' + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem('medkos_atlas3d_' + k, JSON.stringify(v)); } catch (e) { /* 저장 못 해도 화면은 그대로 */ } },
  };
  function norm(s) {
    return String(s || '').toLowerCase()
      .replace(/\barter(y|ies)\b/g, 'a').replace(/\bnerves?\b/g, 'n').replace(/\bveins?\b/g, 'v')
      .replace(/\bmuscles?\b/g, 'm').replace(/\bligaments?\b/g, 'lig').replace(/\bthe\b/g, '')
      .replace(/[\s.,·\-_'’"()\[\]/]/g, '');
  }
  const noSideKo = s => norm(s).replace(/^(오른|왼)/, ''), noSideEn = s => norm(s).replace(/^(right|left)/, '');
  const CLS_KO = { muscle: '근육', artery: '동맥', vein: '정맥', nerve: '신경', ligament: '인대', organ: '장기', bone: '뼈', cartilage: '연골', space: '부위 · 공간', bursa: '윤활주머니 · 힘줄집', lymph: '림프절', other: '기타' };
  const SEARCH_HL = { focus: true, bestView: true, reveal: true, dim: true };
  const sceneById = new Map(SCENES.map(s => [s.id, s]));
  const root = $('#atlas');
  if (!SCENES.length) { root.innerHTML = '<div class="empty">3D 장면 자료(atlas3d-data.js)를 불러오지 못했습니다.</div>'; return; }

  root.innerHTML = `
    <div class="scenepick">
      <div class="chips sp-groups" id="sp-groups"></div>
      <div class="chips" id="s-scenes"></div>
    </div>
    <div class="three-wrap">
      <div class="tcol"><div class="three" id="three"><div class="hud" id="hud">
          <button class="btn sm" id="t-more" aria-expanded="true" title="조작 단추 펴기 · 접기">⚙ 보기 설정</button>
          <button class="btn sm" id="t-drag" aria-pressed="false" title="끌었을 때 돌릴지, 옮길지">끌기: 돌리기</button>
          <button class="btn sm" id="t-nolab" title="화면의 이름표를 모두 지움">이름표 지우기</button>
          <button class="btn sm" id="t-undo" title="마지막으로 숨긴 구조물 하나를 되살림">방금 숨긴 것 되돌리기</button>
          <button class="btn sm" id="t-xray" aria-pressed="true" title="동맥 · 신경이 뼈 · 근육 · 장기 뒤나 속으로 들어간 구간을 옅게 비춰 보여 줌">가려진 혈관 · 신경 비춰 보기</button>
          <button class="btn sm" id="t-dim" aria-pressed="true" title="찾은 구조물만 빛나고 나머지는 옅게 — 빈 곳을 한 번 누르면 원래 색">찾으면 주변 옅게</button>
          <button class="btn sm" id="t-bonesolid" aria-pressed="false" title="뼈를 불투명하게 — 신경 · 혈관이 어느 구멍으로 드나드는지 보임">뼈 불투명 (구멍 보기)</button>
          <span class="skullbase" id="t-skullbase" hidden><button class="btn sm" id="t-sbase" aria-pressed="false" title="머리뼈 벽을 잘라 내고 바닥(구멍)만 — 신경 · 혈관은 자르지 않음">머리뼈바닥만</button>
            <label class="note">자르는 높이 <input type="range" id="t-sbase-h" min="0" max="100" value="40"></label></span>
          <button class="btn sm" id="t-unhide" title="숨긴 구조물을 모두 다시 보이기">숨긴 것 모두 되돌리기</button>
          <span class="hint">두 번 누르기 = 그 구조물 숨기기 · 휠 = 확대 · 위아래는 오른쪽 막대 · ▲▼ · 오른쪽 끌기 = 옮기기</span></div>
        <div class="hbar" title="보는 높이(위 ↔ 아래)"><span>위</span><div class="htrack" id="t-height" role="slider" aria-label="보는 높이" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50" tabindex="0"><i class="hthumb"></i></div><span>아래</span></div>
        <div class="pad" aria-label="화면 이동">
          <button data-pan="0,1" aria-label="위로">▲</button><button data-zoom="0.8" aria-label="확대">+</button>
          <button data-pan="-1,0" aria-label="왼쪽">◀</button><button data-reset aria-label="처음 시점">↺</button><button data-pan="1,0" aria-label="오른쪽">▶</button>
          <button data-pan="0,-1" aria-label="아래로">▼</button><button data-zoom="1.25" aria-label="축소">−</button>
        </div></div>
        <div class="pick" id="pick">구조물을 눌러 보세요.</div></div>
      <div class="panel" id="tpanel">
        <input class="search" id="t-q" type="search" placeholder="구조물 찾기 — 한글 · 영어 (Enter)" autocomplete="off" style="max-width:none">
        <div class="hits" id="t-hits" hidden></div>
        <div class="btnrow"><button class="btn" id="t-reset">시점 처음으로</button><button class="btn" id="t-all">전부 보이기</button></div>
        <p class="sec-title">층별로 벗기기</p><div id="t-layers"></div>
        <p class="sec-title">보이기</p><div id="clsbox" style="display:grid;gap:6px"></div>
        <p class="sec-title">투명도</p>
        <label>근육 <input type="range" id="op-muscle" min="0" max="100" value="100"></label>
        <label>뼈 <input type="range" id="op-bone" min="0" max="100" value="100"></label>
        <label>장기 <input type="range" id="op-organ" min="0" max="100" value="100"></label>
        <label>밝기 <input type="range" id="t-bright" min="40" max="130" value="80" title="화면 밝기 — 옅은 곳이 하얗게 날아가면 낮추세요"></label>
        <p class="attr note" id="t-attr"></p>
      </div>
    </div>
    <details class="at-src"><summary>모형 출처 · 라이선스 (${(A.sources || []).length}곳)</summary>
      <ul>${(A.sources || []).map(s => `<li><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.name)}</a> — ${esc(s.by)} · ${esc(s.lic)}</li>`).join('')}</ul>
      <p>장면마다 쓰인 모형은 장면 이름 옆 꼬리표와 화면 아래 출처 줄에 나옵니다. 고친 내용(부품 고르기 · 단순화 · 한글 이름 붙이기)과 전문은
      <a href="${BASE}ATTRIBUTION.txt">ATTRIBUTION.txt</a>. 한글 이름 가운데 「용어 확인 전」 표시는 표준 용어집과 아직 대조하지 않은 이름입니다.</p></details>`;

  let viewer = null, sceneLoaded = null, pendingHL = null, lastPick = null;
  const pick = html => { $('#pick').innerHTML = html; };
  const curData = () => (window.BP3D || {})[sceneLoaded] || {};

  /* ── 장면 고르기: 부위 묶음 → 장면 ── */
  const sp = { group: store.get('group', null) };
  const groups = () => (A.areas || []).map(a => [a, SCENES.filter(s => s.area === a)]).filter(g => g[1].length);
  function paintPicker() {
    const gs = groups();
    if (!gs.some(([k]) => k === sp.group)) sp.group = (gs.find(([, l]) => l.some(s => s.id === sceneLoaded)) || gs[0])[0];
    $('#sp-groups').innerHTML = gs.map(([k, l]) => `<button class="chip" data-spg="${esc(k)}" aria-pressed="${k === sp.group}">${esc(k)} <span class="k">${l.length}</span></button>`).join('');
    $('#s-scenes').innerHTML = gs.find(([k]) => k === sp.group)[1].map(s =>
      `<button class="chip" data-sc="${esc(s.id)}" title="${esc(s.note || '')}" aria-pressed="${s.id === sceneLoaded}">${esc(s.title)}<span class="srcchip">${esc(s.src)}</span></button>`).join('');
  }
  function followPicker(id) {
    const g = groups().find(([, l]) => l.some(s => s.id === id)); if (g) sp.group = g[0];
    paintPicker();
  }
  $('#sp-groups').addEventListener('click', e => { const g = e.target.closest('[data-spg]'); if (g) { sp.group = g.dataset.spg; store.set('group', sp.group); paintPicker(); } });
  $('#s-scenes').addEventListener('click', e => { const b = e.target.closest('[data-sc]'); if (b) loadScene(b.dataset.sc); });

  /* ── 뷰어 · 장면 불러오기 ── */
  const scriptP = new Map();
  function loadScript(src) {
    if (!scriptP.has(src)) scriptP.set(src, new Promise((res, rej) => {
      const s = document.createElement('script'); s.src = src; s.onload = res;
      s.onerror = () => { scriptP.delete(src); rej(new Error(src)); };
      document.head.appendChild(s);
    }));
    return scriptP.get(src);
  }
  let viewerP = null;
  function ensureViewer() {
    if (!viewerP) viewerP = (async () => {
      await loadScript(BASE + 'lib/vendor/three.min.js');
      await loadScript(BASE + 'lib/vendor/OrbitControls.js');
      await loadScript(BASE + 'lib/viewer3d.js' + VER);
      viewer = window.Viewer3D.createViewer($('#three'), { onPick: onPick3D, onHide: onHide3D, onVisChange: syncPartList, modelsBase: BASE + 'models/' });
      viewer.setBrightness(store.get('bright', 80) / 100);
      viewer.setXray(store.get('xray', true));
      viewer.setDimOnSearch(store.get('dim', true));
      return viewer;
    })().catch(e => { viewerP = null; throw e; });
    return viewerP;
  }
  const sceneFile = id => BASE + 'models/' + id + '.js' + VER;
  let sceneP = null, sceneWant = null;
  function loadScene(id) {
    if (sceneWant === id && sceneP) return sceneP;
    sceneWant = id; sceneP = loadSceneNow(id);
    return sceneP;
  }
  async function loadSceneNow(id) {
    const sc = sceneById.get(id); if (!sc) return;
    followPicker(id);
    $$('#s-scenes .chip').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.sc === id)));
    pick('불러오는 중…');
    try {
      await ensureViewer();
      await loadScript(sceneFile(id));
      if (sceneWant !== id) return;
      await viewer.loadScene(id);
      if (sceneWant !== id) return;
      sceneLoaded = id; store.set('scene', id);
      try { history.replaceState(null, '', '#' + id); } catch (e) { /* file:// 등 */ }
      paintPicker();
      const data = curData();
      $('#t-attr').textContent = data.attr || sc.attr || '';
      renderPartList(data); syncPartList();
      const baseOp = c => { const ps = (data.parts || []).filter(p => p.cls === c && p.vis !== 0); return ps.length ? Math.round(ps.reduce((s, p) => s + (p.op == null ? 1 : p.op), 0) / ps.length * 100) : 100; };
      ['muscle', 'bone', 'organ'].forEach(c => { $('#op-' + c).value = baseOp(c); });
      const bs = $('#t-bonesolid'); bs.setAttribute('aria-pressed', 'false'); bs.dataset.base = baseOp('bone');
      $('#t-skullbase').hidden = !(data.clip && data.clip.axis === 'y' && (data.parts || []).some(p => /occipital|sphenoid/i.test(p.en || '')));
      $('#t-sbase').setAttribute('aria-pressed', 'false');
      pick(`<b>${esc(sc.title)}</b> <span class="note">· 부품 ${sc.n}개</span>${sc.note ? (sc.note.length > 140
        ? `<details class="note" style="margin-top:3px"><summary>이 장면에 든 것 · 없는 것</summary>${esc(sc.note)}</details>`
        : `<div class="note" style="margin-top:3px">${esc(sc.note)}</div>`) : ''}`);
      threeLayer.id = null; threeLayer.k = 0; renderLayers(); setTimeout(syncHeight, 600);
      if (pendingHL) { const h = pendingHL; pendingHL = null; const got = viewer.highlight([h], SEARCH_HL); if (got.length) showPart(got[0]); }
    } catch (e) {
      pick('3D를 불러오지 못했습니다. 연결 상태를 확인한 뒤 장면을 다시 눌러 주세요.');
      sceneP = null; sceneWant = null;
    }
  }
  function open3D(sceneId, partOrSid) { pendingHL = partOrSid || null; if (sceneId === sceneLoaded) { const h = pendingHL; pendingHL = null; if (h) { const got = viewer.highlight([h], SEARCH_HL); if (got.length) showPart(got[0]); } } else loadScene(sceneId); }

  /* ── 구조물 정보 ── */
  const partOf = pid => (curData().parts || []).find(x => x.id === pid) || null;
  function alsoIn(sid, name) {
    const kn = noSideKo(name), seen = new Map();
    SCENES.forEach(sc => {
      if (sc.id === sceneLoaded) return;
      const hit = sc.names.find(n => (sid && n[3] === sid) || (kn && noSideKo(n[0]) === kn));
      if (hit) seen.set(sc.id, { sc, go: (sid && hit[3] === sid) ? sid : hit[2] });
    });
    const list = [...seen.values()];
    if (!list.length) return '<p class="note" style="margin-top:4px">다른 장면에는 없음</p>';
    return `<div class="alsoin"><span class="note">다른 장면에서도 보기 (${list.length})</span><div class="btnrow">${list.map(x => `<button class="btn sm" data-gosc="${esc(x.sc.id)}" data-gopart="${esc(x.go)}">${esc(x.sc.title)}</button>`).join('')}</div></div>`;
  }
  function showPart(pid, borrowedName) {
    const p = partOf(pid) || {};
    lastPick = { partId: pid, ko: p.ko || borrowedName || '', en: p.en || '', cls: p.cls };
    const name = p.ko || borrowedName || p.en || pid;
    const badge = p.kos === 'G' ? ' <span class="badge g" title="표준 용어집과 아직 대조하지 않은 한글 이름">용어 확인 전</span>' : '';
    pick(`<b>${esc(name)}</b>${badge} <span class="note">${esc(p.ko ? p.en : '')}${p.cls ? ' · ' + esc(CLS_KO[p.cls] || p.cls) : ''}</span>
      <div class="btnrow" style="margin-top:4px"><button class="btn sm" data-focus>이곳 중심</button><button class="btn sm" data-only>이것만 보기</button><button class="btn sm" data-hidepart>이것 숨기기</button><button class="btn sm" data-same>같은 종류만</button>
      <label class="toggle" style="font-size:.76rem"><input type="checkbox" id="t-onlybone" checked> 뼈는 같이</label></div>
      ${alsoIn(p.sid, p.ko || p.en)}`);
  }
  function onPick3D(p) { if (p) showPart(p.partId, p.ko || p.en); }
  function onHide3D(p, hidden) { if (hidden) pick(`<b>${esc(p.ko || p.en)}</b> 숨김 <span class="note">· 「방금 숨긴 것 되돌리기」로 되살림 · 보이기 칸 「하나씩」에서도 켜고 끔</span>`); }
  $('#pick').addEventListener('click', e => {
    const g = e.target.closest('[data-gosc]'); if (g) { open3D(g.dataset.gosc, g.dataset.gopart); return; }
    const b = e.target.closest('button'); if (!b || !viewer || !lastPick) return;
    if ('focus' in b.dataset) viewer.focusPart(lastPick.partId);
    else if ('only' in b.dataset) viewer.showOnly([lastPick.partId], $('#t-onlybone') && $('#t-onlybone').checked ? ['bone'] : []);
    else if ('hidepart' in b.dataset) { viewer.hide([lastPick.partId]); syncPartList(); pick(`<b>${esc(lastPick.ko || lastPick.en)}</b> 숨김 · 「숨긴 것 모두 되돌리기」로 다시 보임`); }
    else if ('same' in b.dataset) viewer.showOnly((curData().parts || []).filter(x => x.cls === lastPick.cls).map(x => x.id), []);
  });

  /* ── 찾기: 지금 장면에 있으면 강조, 같은 몸 모형의 다른 장면에 있으면 그 자리에 가져오고, 아니면 장면 목록 ── */
  function findAll(q) {
    const n = noSideKo(q), ne = noSideEn(q); if (!n) return [];
    const out = [];
    SCENES.forEach(sc => sc.names.forEach(([ko, en, pid]) => {
      const k = noSideKo(ko), e = noSideEn(en);
      if ((k && k.includes(n)) || (e && ne && e.includes(ne))) out.push({ sc, pid, name: ko || en, exact: k === n || e === ne });
    }));
    return out;
  }
  async function borrowInto(hits) {
    const cur = sceneById.get(sceneLoaded);
    if (!viewer || !cur || !cur.frame) return false;
    const h0 = hits.find(h => h.sc.id !== cur.id && h.sc.frame === cur.frame); if (!h0) return false;
    try { await loadScript(sceneFile(h0.sc.id)); } catch (e) { return false; }
    const data = (window.BP3D || {})[h0.sc.id]; if (!data) return false;
    const got = viewer.borrow(data, hits.filter(h => h.sc.id === h0.sc.id).map(h => h.pid));
    if (!got.length) return false;
    viewer.highlight(got, SEARCH_HL);
    pick(`<b>${esc(h0.name)}</b> — 이 장면엔 없어서 같은 모형(같은 몸 · 같은 좌표)의 「${esc(h0.sc.title)}」 장면에서 가져와 그 자리에 보여 줍니다. 장면을 바꾸면 사라집니다.${alsoIn(null, h0.name)}`);
    return true;
  }
  function runSearch(q) {
    q = (q || '').trim(); const box = $('#t-hits');
    if (!q) { box.hidden = true; return; }
    let hits = findAll(q);
    if (hits.some(h => h.exact)) hits = hits.filter(h => h.exact);
    if (!hits.length) { box.hidden = true; pick('그 이름의 구조물을 찾지 못했습니다. 한글 · 영어 이름으로 다시 찾아 보세요.'); return; }
    const here = hits.filter(h => h.sc.id === sceneLoaded);
    // 결과 목록 — 이름별로 묶어 어느 장면에 있는지
    const byName = new Map();
    hits.forEach(h => { const k = noSideKo(h.name); if (!byName.has(k)) byName.set(k, { name: h.name.replace(/^(오른|왼)/, ''), list: [] }); const g = byName.get(k); if (!g.list.some(x => x.sc.id === h.sc.id)) g.list.push(h); });
    const rows = [...byName.values()].slice(0, 40);
    box.hidden = false;
    box.innerHTML = `<span class="note">${byName.size}개 이름${byName.size > 40 ? ' 가운데 40개' : ''} · 누르면 그 장면에서 강조</span>` + rows.map(g =>
      g.list.slice(0, 6).map(h => `<button class="btn sm" data-gosc="${esc(h.sc.id)}" data-gopart="${esc(h.pid)}">${esc(g.name)} <span class="note">— ${esc(h.sc.title)}</span></button>`).join('')).join('');
    if (here.length && viewer) {
      const got = viewer.highlight([...new Set(here.map(h => h.pid))], SEARCH_HL);
      if (got.length) { showPart(got[0]); return; }
    }
    borrowInto(hits).then(ok => { if (!ok) pick(`<b>${esc(rows[0].name)}</b> — 이 장면에는 없습니다. 찾기 칸 아래 목록에서 장면을 고르세요.`); });
  }
  let tqEnter = false;   // 같은 글자로 다시 Enter 해도 찾기가 돌게(change 는 글자가 바뀔 때만 생긴다)
  $('#t-q').addEventListener('keydown', e => {
    if (e.key !== 'Enter' || e.isComposing) return;
    tqEnter = true; setTimeout(() => { if (tqEnter) { tqEnter = false; runSearch(e.target.value); } }, 0);
  });
  $('#t-q').addEventListener('change', e => { tqEnter = false; runSearch(e.target.value); });
  $('#t-hits').addEventListener('click', e => { const b = e.target.closest('[data-gosc]'); if (b) open3D(b.dataset.gosc, b.dataset.gopart); });

  /* ── 보이기 칸(분류 · 부품 하나씩) ── */
  const partName = p => p.ko || p.en || p.id;
  function renderPartList(data) {
    const parts = data.parts || [], order = Object.keys(CLS_KO);
    const classes = [...new Set(parts.map(p => p.cls))].sort((a, b) => order.indexOf(a) - order.indexOf(b));
    $('#clsbox').innerHTML = classes.map(c => {
      const ps = parts.filter(p => p.cls === c).sort((x, y) => partName(x).localeCompare(partName(y), 'ko'));
      return `<div class="clsrow"><label><input type="checkbox" checked data-cls="${esc(c)}"> <span class="cls cls-${esc(c)}"></span>${esc(CLS_KO[c] || c)} <span class="note">${ps.length}</span></label>
        <button class="btn sm" data-plist="${esc(c)}" aria-expanded="false">하나씩 ▾</button></div>
        <div class="plist" data-for="${esc(c)}" hidden>${ps.length > 12 ? `<input class="search" data-pfilter placeholder="${esc(CLS_KO[c] || c)} 이름 찾기" autocomplete="off">` : ''}
        ${ps.map(p => `<label data-n="${esc(norm(partName(p)) + ' ' + norm(p.en))}"><input type="checkbox" checked data-part="${esc(p.id)}"> ${esc(partName(p))}</label>`).join('')}</div>`;
    }).join('');
  }
  function syncPartList() {
    if (!viewer) return;
    $$('#clsbox [data-part]').forEach(i => { i.checked = viewer.isVisible(i.dataset.part); });
    $$('#clsbox [data-cls]').forEach(c => {
      const ps = $$(`#clsbox .plist[data-for="${CSS.escape(c.dataset.cls)}"] [data-part]`), on = ps.filter(x => x.checked).length;
      c.checked = ps.length > 0 && on === ps.length; c.indeterminate = on > 0 && on < ps.length;
    });
  }
  $('#clsbox').addEventListener('change', e => {
    const i = e.target; if (!viewer) return;
    if (i.dataset.cls) viewer.setVisible($$(`#clsbox .plist[data-for="${CSS.escape(i.dataset.cls)}"] [data-part]`).map(x => x.dataset.part), i.checked);
    else if (i.dataset.part) viewer.setVisible([i.dataset.part], i.checked);
  });
  $('#clsbox').addEventListener('click', e => {
    const b = e.target.closest('[data-plist]'); if (!b) return;
    const box = $(`#clsbox .plist[data-for="${CSS.escape(b.dataset.plist)}"]`); if (!box) return;
    box.hidden = !box.hidden; b.setAttribute('aria-expanded', String(!box.hidden)); b.textContent = box.hidden ? '하나씩 ▾' : '접기 ▴';
  });
  $('#clsbox').addEventListener('input', e => {
    if (!('pfilter' in e.target.dataset)) return;
    const q = norm(e.target.value);
    $$('label[data-n]', e.target.parentElement).forEach(l => { l.hidden = !!q && !l.dataset.n.includes(q); });
  });

  /* ── 층별로 벗기기 ── */
  const threeLayer = { id: null, k: 0 };
  function renderLayers() {
    const box = $('#t-layers'), regs = LAYERS.filter(r => r.scenes.includes(sceneLoaded));
    if (!regs.length) { box.innerHTML = '<p class="note">이 장면에 맞춘 층 자료가 없습니다. 「두 번 누르기 = 숨기기」로 겉에서부터 벗겨 보세요.</p>'; return; }
    if (!regs.some(r => r.id === threeLayer.id)) { threeLayer.id = regs[0].id; threeLayer.k = 0; }
    const r = regs.find(x => x.id === threeLayer.id), cur = r.layers.find(l => l.n === threeLayer.k);
    box.innerHTML = `<div class="chips">${regs.map(x => `<button class="chip" data-lr="${esc(x.id)}" aria-pressed="${x.id === r.id}">${esc(x.title.split(' — ')[0])}</button>`).join('')}</div>
      <div class="lbtns"><button class="btn sm${threeLayer.k === 0 ? ' on' : ''}" data-lk="0">전부</button>${r.layers.map(l => `<button class="btn sm${l.n === threeLayer.k ? ' on' : ''}" data-lk="${l.n}" title="${esc(l.ko)}">${l.n}층</button>`).join('')}</div>
      <p class="note">${cur ? `<b>${cur.n}층 — ${esc(cur.ko)}</b>` : '층 번호를 누르면 그보다 얕은 층을 치우고, 그 층에서 처음 보이는 구조물을 강조합니다.'}</p>`;
  }
  function applyDepth() {
    const r = LAYERS.find(x => x.id === threeLayer.id); if (!viewer || !r) return;
    const k = threeLayer.k;
    if (!k) { viewer.showAll(); viewer.clearHighlight(); pick('모든 층이 보이는 상태입니다.'); return; }
    const removed = new Set(r.layers.filter(l => l.n < k).flatMap(l => l.sids));
    const now = r.layers.filter(l => l.n === k).flatMap(l => l.sids);
    viewer.isolate((curData().parts || []).filter(p => !(p.sid && removed.has(p.sid))).map(p => p.id));
    const hit = now.length ? viewer.highlight(now, { focus: false }) : [];
    const l = r.layers.find(x => x.n === k) || {};
    pick(`<b>${esc(r.title.split(' — ')[0])} · ${k}층 — ${esc(l.ko || '')}</b> <span class="note">· 얕은 ${k - 1}층 치움 · 이 장면에서 강조 ${hit.length}개</span>`);
  }
  $('#t-layers').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.lr) { threeLayer.id = b.dataset.lr; threeLayer.k = 0; } else if (b.dataset.lk != null) threeLayer.k = +b.dataset.lk; else return;
    renderLayers(); applyDepth();
  });

  /* ── 단추 · 조작 ── */
  $('#t-reset').addEventListener('click', () => viewer && viewer.resetView());
  $('#t-all').addEventListener('click', () => { if (viewer) { viewer.showAll(); viewer.clearHighlight(); threeLayer.k = 0; renderLayers(); } });
  ['muscle', 'bone', 'organ'].forEach(c => $('#op-' + c).addEventListener('input', e => viewer && viewer.setClassOpacity(c, e.target.value / 100)));
  const toggle = (id, key, fn) => {
    const b = $(id); b.setAttribute('aria-pressed', String(store.get(key, true)));
    b.addEventListener('click', () => { const on = b.getAttribute('aria-pressed') !== 'true'; b.setAttribute('aria-pressed', String(on)); store.set(key, on); if (viewer) fn(on); });
  };
  toggle('#t-xray', 'xray', on => viewer.setXray(on));
  toggle('#t-dim', 'dim', on => viewer.setDimOnSearch(on));
  $('#t-bright').value = store.get('bright', 80);
  $('#t-bright').addEventListener('input', e => { store.set('bright', +e.target.value); viewer && viewer.setBrightness(e.target.value / 100); });
  const sbaseClip = () => {
    const bb = viewer && viewer.getBounds(); if (!bb) return null;
    const h = +$('#t-sbase-h').value / 100;
    return { axis: 'y', value: bb[1] + (bb[4] - bb[1]) * (0.25 + 0.5 * h), keep: 'neg', only: ['bone', 'cartilage'] };
  };
  $('#t-sbase').addEventListener('click', e => {
    if (!viewer) return;
    const b = e.currentTarget, on = b.getAttribute('aria-pressed') !== 'true';
    b.setAttribute('aria-pressed', String(on));
    if (on) {
      viewer.setClassOpacity('bone', 1); viewer.setClassOpacity('cartilage', 1); viewer.setClassTint('bone', 0.82);
      viewer.setClipping(sbaseClip()); $('#op-bone').value = 100; $('#t-bonesolid').setAttribute('aria-pressed', 'true');
      pick('머리뼈 벽을 잘라 내고 <b>바닥만</b> 남겼습니다(신경 · 혈관은 그대로). 위에서 보면 신경이 <b>들어가는 구멍</b>이 보입니다. 바닥이 너무 깎이면 「자르는 높이」를 올리세요.');
    } else {
      viewer.setClassTint('bone', 1); viewer.clearClassOpacity('bone'); viewer.clearClassOpacity('cartilage'); viewer.setClipping(true);
      $('#op-bone').value = $('#t-bonesolid').dataset.base || 100; $('#t-bonesolid').setAttribute('aria-pressed', 'false');
      pick('장면 기본 보기로 되돌렸습니다.');
    }
  });
  $('#t-sbase-h').addEventListener('input', () => { if (viewer && $('#t-sbase').getAttribute('aria-pressed') === 'true') viewer.setClipping(sbaseClip()); });
  $('#t-bonesolid').addEventListener('click', e => {
    if (!viewer) return;
    const b = e.currentTarget, on = b.getAttribute('aria-pressed') !== 'true';
    b.setAttribute('aria-pressed', String(on));
    if (on) { viewer.setClassOpacity('bone', 1); viewer.setClassOpacity('cartilage', 1); $('#op-bone').value = 100;
      pick('뼈를 불투명하게 했습니다. 뼈를 두 번 누르면 그 뼈만 숨깁니다.'); }
    else { viewer.clearClassOpacity('bone'); viewer.clearClassOpacity('cartilage'); $('#op-bone').value = b.dataset.base || 100; pick('뼈를 장면 기본 투명도로 되돌렸습니다.'); }
  });
  let rep = null;
  const stopRep = () => { clearInterval(rep); rep = null; };
  $('#three').addEventListener('pointerdown', e => {
    const b = e.target.closest('.pad button'); if (!b || !viewer) return;
    e.preventDefault();
    const act = () => {
      if (b.dataset.pan) { const [x, y] = b.dataset.pan.split(',').map(Number); viewer.panBy(x * 0.06, y * 0.06); syncHeight(); }
      else if (b.dataset.zoom) viewer.zoomBy(+b.dataset.zoom);
      else if ('reset' in b.dataset) { viewer.resetView(); setTimeout(syncHeight, 500); }
    };
    act(); stopRep(); if (!('reset' in b.dataset)) rep = setInterval(act, 90);
  });
  ['pointerup', 'pointerleave', 'pointercancel'].forEach(ev => $('#three').addEventListener(ev, stopRep));
  const htr = $('#t-height');
  function setThumb(t) { t = Math.max(0, Math.min(1, t)); htr.style.setProperty('--h', (t * 100).toFixed(1) + '%'); htr.setAttribute('aria-valuenow', String(Math.round(t * 100))); }
  function syncHeight() { if (viewer && viewer.getHeight) setThumb(1 - viewer.getHeight()); }
  const setH = y => { const r = htr.getBoundingClientRect(), t = Math.max(0, Math.min(1, (y - r.top) / r.height)); setThumb(t); if (viewer) viewer.setHeight(1 - t); };
  let hDrag = false;
  htr.addEventListener('pointerdown', e => { hDrag = true; htr.setPointerCapture(e.pointerId); setH(e.clientY); e.preventDefault(); });
  htr.addEventListener('pointermove', e => { if (hDrag) setH(e.clientY); });
  ['pointerup', 'pointercancel'].forEach(ev => htr.addEventListener(ev, () => { hDrag = false; }));
  htr.addEventListener('keydown', e => {
    if (!viewer || (e.key !== 'ArrowUp' && e.key !== 'ArrowDown')) return;
    e.preventDefault();
    const cur = 1 - viewer.getHeight();
    viewer.setHeight(1 - Math.max(0, Math.min(1, cur + (e.key === 'ArrowUp' ? -0.05 : 0.05)))); syncHeight();
  });
  $('#t-drag').addEventListener('click', e => {
    const pan = e.currentTarget.getAttribute('aria-pressed') !== 'true';
    e.currentTarget.setAttribute('aria-pressed', String(pan));
    e.currentTarget.textContent = pan ? '끌기: 옮기기' : '끌기: 돌리기';
    if (viewer) viewer.setDragMode(pan ? 'pan' : 'rotate');
  });
  $('#t-nolab').addEventListener('click', () => viewer && viewer.clearLabels());
  $('#t-unhide').addEventListener('click', () => { if (viewer) { viewer.unhideAll(); syncPartList(); pick('숨긴 구조물을 모두 되돌렸습니다.'); } });
  $('#t-undo').addEventListener('click', () => { if (!viewer) return; const r = viewer.undoHide(); pick(r ? `${esc(r.ko || r.en)} — 다시 보입니다.` : '되돌릴 것이 없습니다.'); });

  const hud = $('#hud'), more = $('#t-more');
  const setHud = open => { hud.classList.toggle('compact', !open); more.setAttribute('aria-expanded', String(open)); };
  setHud(window.innerWidth >= 700);
  more.addEventListener('click', () => setHud(hud.classList.contains('compact')));

  /* ── 시작: 주소의 #장면 → 지난번 장면 → 첫 장면 ── */
  const want = decodeURIComponent((location.hash || '').slice(1));
  const start = sceneById.has(want) ? want : (sceneById.has(store.get('scene', '')) ? store.get('scene', '') : SCENES[0].id);
  paintPicker();
  loadScene(start);
  window.Atlas3D = { open: open3D, search: runSearch, get viewer() { return viewer; }, get scene() { return sceneLoaded; } };
})();
