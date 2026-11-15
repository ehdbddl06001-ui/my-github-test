/* MedKOS 3D 아틀라스 — 3D 뷰어 (classic script, file:// 에서 동작)
 * 필요: three@0.147.0 build/three.min.js + examples/js/controls/OrbitControls.js 를 먼저 <script> 로 불러온다.
 * 장면 데이터: models/<장면>.js (window.BP3D[<장면>]) — 없으면 loadScene 이 <script> 로 불러온다.
 * 3D: BodyParts3D © The Database Center for Life Science, CC BY-SA 2.1 JP (학교 제공 자료 아님)
 *
 * var v = Viewer3D.createViewer(container, {onPick: fn, modelsBase: 'models/'});
 * v.loadScene(name) -> Promise
 * v.setClassVisible(cls, bool) · v.setClassOpacity(cls, 0..1)
 * v.highlight(ids, {focus:true, ghost:false, dim:false, bestView:false, reveal:false}) — ids = 부품 id 또는 structures.json sid(같은 sid 부품 전부) · ghost = 나머지를 하얗게·투명 · bestView = 덜 가리는 쪽으로 돌림
 * v.clearHighlight() · v.isolate(ids) · v.showAll() · v.resetVisibility() · v.resetView()
 * v.panBy(fx,fy) · v.zoomBy(f) · v.setHeight(0..1) · v.getHeight() · v.setDragMode('rotate'|'pan') · 두 번 누르기 = 그 구조물 숨기기(opts.onHide) · v.undoHide() · v.unhide(ids) · v.focusPart(id) · 방향키 = 이동
 * v.setXray(bool) — 뼈 · 근육 · 장기 뒤나 속으로 들어간 동맥 · 신경 구간을 옅게 비춰 보기(기본 켬)
 * v.setLabelsVisible(bool) · v.setClipping(true|false|{axis,value,keep}) · v.getParts() · v.getScene() · v.dispose()
 * onPick({partId, sid, ko, en, cls, side, fma}) — 빈 곳을 누르면 onPick(null)
 */
(function () {
  'use strict';
  var CLS_COLOR = {
    bone: '#e8dcc0', muscle: '#b5534c', artery: '#d42a2a', vein: '#2f5fc0', nerve: '#f2c84b',
    organ: '#d9a58e', ligament: '#b9c8da', cartilage: '#a8c6d6', space: '#9fb7a8', bursa: '#c9b8e0', lymph: '#8fbf7f', other: '#bdbdbd'
  };
  var CLASSES = ['bone', 'muscle', 'artery', 'vein', 'nerve', 'organ', 'ligament', 'cartilage', 'space', 'bursa', 'lymph', 'other'];
  var XRAY_OP = 0.3;
  var HL_COLOR = '#19d3c5', HL_EMISSIVE = '#0b6f68', SEL_EMISSIVE = '#1f5a8a', HOVER_EMISSIVE = '#3a3a3a';
  // 찾기 — 나머지를 옅게(불투명도 · 흰색 섞기) · 찾은 구조물 위에 덧칠하는 빛 색(신경은 분홍 — 노란 신경 사이에서 구별)
  var DIM_OP = 0.28, DIM_WHITE = 0.5, GLOW_C = '#3ffff0', GLOW_N = '#ff4fe0';

  function b64bytes(s) {
    var bin = atob(s), n = bin.length, u = new Uint8Array(n);
    for (var i = 0; i < n; i++) u[i] = bin.charCodeAt(i);
    return u;
  }
  var scriptCache = {};
  function loadScript(src) {
    if (scriptCache[src]) return scriptCache[src];
    scriptCache[src] = new Promise(function (res, rej) {
      var s = document.createElement('script');
      s.src = src; s.async = true;
      s.onload = function () { res(); };
      s.onerror = function () { delete scriptCache[src]; rej(new Error('3D 모델을 불러오지 못함: ' + src)); };
      document.head.appendChild(s);
    });
    return scriptCache[src];
  }

  function createViewer(container, opts) {
    var THREE = window.THREE;
    if (!THREE || !THREE.OrbitControls) throw new Error('three.min.js 와 OrbitControls.js 를 먼저 불러와야 함');
    opts = opts || {};
    var base = opts.modelsBase == null ? 'models/' : opts.modelsBase;
    var onPick = opts.onPick || function () {};
    var onHide = opts.onHide || function () {};
    var onVisChange = opts.onVisChange || null;   // 보이는 부품 묶음이 바뀌면 한 번 알림(보이기 칸 체크 맞추기, 2026-10-18)
    var selectOnPick = opts.selectOnPick !== false;
    var hoverTip = opts.hoverTooltip !== false;

    if (getComputedStyle(container).position === 'static') container.style.position = 'relative';
    var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: !!opts.preserveDrawingBuffer });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.localClippingEnabled = true;
    var cv = renderer.domElement;
    cv.style.cssText = 'display:block;width:100%;height:100%;touch-action:none;outline:none;';
    container.appendChild(cv);

    var overlay = document.createElement('div');
    overlay.style.cssText = 'position:absolute;inset:0;pointer-events:none;overflow:hidden;font:12px/1.3 system-ui,-apple-system,"Malgun Gothic",sans-serif;';
    container.appendChild(overlay);
    var tip = document.createElement('div');
    tip.style.cssText = 'position:absolute;display:none;padding:3px 7px;border-radius:6px;background:rgba(20,20,24,.82);color:#fff;white-space:nowrap;transform:translate(12px,12px);';
    overlay.appendChild(tip);

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(30, 1, 1, 20000);
    scene.add(camera);
    // 밝기 — 예전엔 합이 1.65 라 옅은 색(뇌 · 백색질)이 하얗게 날아감(사용자 2026-10-17). 기본 0.8배 · setBrightness 로 조절
    // 바탕 빛은 위아래 같은 색 — 위(하늘) 흰빛 · 아래 갈색이면 머리뼈 안쪽(위를 보는 면)만 하얗게 떠서 바깥 뼈색과 달라 보임(사용자 2026-10-17).
    // 세기는 예전 위아래 평균(0.65 × (1 + 0.43) / 2 ≈ 0.47)으로, 명암은 카메라에 붙은 빛(key · fill)이 맡는다.
    var LIGHT0 = { hemi: 0.47, key: 0.75, fill: 0.25 }, bright = 0.8;
    var hemi = new THREE.HemisphereLight(0xffffff, 0xffffff, LIGHT0.hemi * bright);
    scene.add(hemi);
    var key = new THREE.DirectionalLight(0xffffff, LIGHT0.key * bright);
    key.position.set(0.4, 0.7, 1);
    camera.add(key);
    var fill = new THREE.DirectionalLight(0xffffff, LIGHT0.fill * bright);
    fill.position.set(-0.6, -0.3, 0.4);
    camera.add(fill);
    var root = new THREE.Group();
    scene.add(root);

    var controls = new THREE.OrbitControls(camera, cv);
    controls.enableDamping = true;
    controls.dampingFactor = 0.12;
    controls.screenSpacePanning = true;
    controls.rotateSpeed = 0.85;
    controls.zoomSpeed = 1.1;
    controls.enableZoom = false;   // 휠은 아래 onWheel 이 맡는다(두 손가락 벌리기 확대는 아래 touches 가 맡음)
    if (THREE.TOUCH) controls.touches = { ONE: THREE.TOUCH.ROTATE, TWO: THREE.TOUCH.DOLLY_PAN };

    var S = {
      data: null, name: null, meshes: [], byId: {}, bySid: {}, classVis: {}, classOp: {},
      tint: {}, xray: true, clipSusp: false, dim: false, dimPref: true, glow: new Map(), force: new Set(), visSig: '', hl: new Set(), ghost: false, iso: null, hidden: new Set(), hideStack: [], wheel: 'zoom', sel: null, hover: null, labels: true, clip: null,
      dirty: true, autoFit: true, tween: null, raf: 0, disposed: false, labelEls: new Map()
    };
    var clipPlane = new THREE.Plane(new THREE.Vector3(-1, 0, 0), 0);

    // ── 크기 ────────────────────────────────────────────────
    function resize() {
      var w = container.clientWidth || 300, h = container.clientHeight || 300;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      S.dirty = true;
      if (S.autoFit && S.data && !S.tween) resetView(false);
    }
    var ro = window.ResizeObserver ? new ResizeObserver(resize) : null;
    if (ro) ro.observe(container); else window.addEventListener('resize', resize);
    resize();

    // ── 장면 만들기 ─────────────────────────────────────────
    function clearScene() {
      S.meshes.forEach(function (m) { m.geometry.dispose(); m.material.dispose(); if (m.userData.xray) m.userData.xray.material.dispose(); root.remove(m); });
      S.glow.forEach(function (gm) { gm.material.dispose(); }); S.glow = new Map(); S.dim = false; S.clipSusp = false;
      S.meshes = []; S.byId = {}; S.bySid = {}; S.hl = new Set(); S.iso = null; S.sel = null; S.hover = null;
      S.classVis = {}; S.classOp = {}; S.hidden = new Set(); S.force = new Set(); S.hideStack = []; S.visSig = '';
      S.labelEls.forEach(function (el) { el.remove(); });
      S.labelEls = new Map();
    }

    function build(data) {
      clearScene();
      S.data = data;
      var pos = new Int16Array(b64bytes(data.pos).buffer);
      var ib = b64bytes(data.idx).buffer;
      var idx = data.idx32 ? new Uint32Array(ib) : new Uint16Array(ib);
      var sc = data.scale, nV = pos.length / 3;
      var fpos = new Float32Array(pos.length);
      for (var i = 0; i < nV; i++) {
        fpos[3 * i] = pos[3 * i] * sc[0];
        fpos[3 * i + 1] = pos[3 * i + 1] * sc[1];
        fpos[3 * i + 2] = pos[3 * i + 2] * sc[2];
      }
      data.parts.forEach(function (p, k) { addMesh(p, fpos, idx, k); });
      S.clip = data.clip || null;
      applyClip();
      refresh();
      resetView();
    }

    // 부품 하나를 장면에 넣기 — fpos(장면 중심 기준 mm) · idx 에서 p.r 구간을 잘라 쓴다
    function addMesh(p, fpos, idx, k) {
        var r = p.r;
        var g = new THREE.BufferGeometry();
        g.setAttribute('position', new THREE.BufferAttribute(fpos.slice(3 * r[0], 3 * (r[0] + r[1])), 3));
        g.setIndex(new THREE.BufferAttribute(idx.slice(r[2], r[2] + r[3]), 1));
        g.computeVertexNormals();
        g.computeBoundingBox();
        g.computeBoundingSphere();
        // 인대는 장면 자료의 색(HRA · Open3D 장면은 인대마다 다른 색)을 쓰지 않고 한 색 — 인대가 한눈에 인대로 보이게(사용자 2026-10-17)
        var col = new THREE.Color((p.cls === 'ligament' ? null : p.color) || CLS_COLOR[p.cls] || CLS_COLOR.other);
        // 아주 옅은 장기 색(뇌 겉질 · 백색질 등)은 조금 어둡게 — 주름 · 경계가 보이게
        if (p.cls === 'organ' && (0.299 * col.r + 0.587 * col.g + 0.114 * col.b) > 0.78) col.multiplyScalar(0.86);
        var mat = new THREE.MeshPhongMaterial({
          color: col, specular: 0x1c1c1c, shininess: p.cls === 'bone' ? 12 : 22, side: THREE.DoubleSide
        });
        if (p.ov) { mat.polygonOffset = true; mat.polygonOffsetFactor = -1; mat.polygonOffsetUnits = -4; }
        var m = new THREE.Mesh(g, mat);
        m.userData = { part: p, baseColor: col.clone(), baseOp: p.op == null ? 1 : p.op, baseVis: p.vis !== 0, k: k };
        // 비춰 보기 — 동맥 · 신경이 뼈 · 근육 · 장기(불투명) 뒤나 속으로 들어간 구간을 옅게 비춰 그림(깊이가 더 먼 곳에만 그려짐).
        // 가지가 어느 시점에 안 보이게 묻히는 일을 없앰(사용자 2026-10-17). 고르기(raycast)에는 안 걸림.
        if (p.cls === 'artery' || p.cls === 'nerve') {
          var xmat = new THREE.MeshBasicMaterial({ color: col.clone(), transparent: true, opacity: XRAY_OP, depthWrite: false, depthFunc: THREE.GreaterDepth, side: THREE.FrontSide });
          var xm = new THREE.Mesh(g, xmat);
          xm.renderOrder = 5; xm.raycast = function () {}; xm.visible = S.xray;
          m.add(xm); m.userData.xray = xm;
        }
        root.add(m);
        S.meshes.push(m);
        S.byId[p.id] = m;
        if (p.sid) (S.bySid[p.sid] = S.bySid[p.sid] || []).push(m);
        return m;
    }

    // 다른 장면(같은 몸 · 같은 좌표)의 부품을 지금 장면에 덧넣기 — 세계 좌표(pos × scale + offset)를 지금 장면 중심 기준으로 옮김.
    // 찾기에서 「지금 장면엔 없지만 같은 모형의 다른 장면엔 있는」 구조물을 그 자리에 바로 보여 주려고(사용자 2026-10-18). 장면을 바꾸면 사라짐.
    function borrow(data, ids) {
      if (!S.data || !data || data === S.data) return [];
      var want = {}; (Array.isArray(ids) ? ids : [ids]).forEach(function (x) { want[x] = 1; });
      var pick = data.parts.filter(function (p) { return (want[p.id] || (p.sid && want[p.sid])) && !S.byId['b:' + data.id + ':' + p.id]; });
      if (!pick.length) return [];
      var pos = new Int16Array(b64bytes(data.pos).buffer), ib = b64bytes(data.idx).buffer;
      var idx = data.idx32 ? new Uint32Array(ib) : new Uint16Array(ib);
      var sc = data.scale, o = data.offset || [0, 0, 0], o0 = S.data.offset || [0, 0, 0], out = [];
      pick.forEach(function (p) {
        var r = p.r, f = new Float32Array(3 * r[1]);
        for (var i = 0; i < r[1]; i++) {
          var j = r[0] + i;
          f[3 * i] = pos[3 * j] * sc[0] + o[0] - o0[0];
          f[3 * i + 1] = pos[3 * j + 1] * sc[1] + o[1] - o0[1];
          f[3 * i + 2] = pos[3 * j + 2] * sc[2] + o[2] - o0[2];
        }
        var q = Object.assign({}, p, { id: 'b:' + data.id + ':' + p.id, from: data.id, op: null, vis: 1, r: [0, r[1], 0, r[3]] });
        var m = addMesh(q, f, idx.slice(r[2], r[2] + r[3]), S.meshes.length);
        m.userData.borrowed = true;
        out.push(q.id);
      });
      applyClip();
      refresh();
      return out;
    }

    // ── 보이기 · 불투명도 · 강조 ────────────────────────────
    function effVis(m) {
      var p = m.userData.part;
      if (S.hidden.has(m)) return false;
      if (S.hl.has(m)) return true;
      if (S.force.has(m)) return true;
      if (S.iso) return S.iso.has(m);
      var cv = S.classVis[p.cls];
      return cv == null ? m.userData.baseVis : cv;
    }
    function effOp(m) {
      var p = m.userData.part;
      if (S.hl.has(m)) return 1;
      var op = S.classOp[p.cls] != null ? S.classOp[p.cls] : m.userData.baseOp;
      if (S.ghost && S.hl.size) op = Math.min(op, 0.16);
      else if (S.dim && S.hl.size) op = Math.min(op, DIM_OP);   // 찾기 — 나머지를 옅게(두꺼운 근육 · 뼈에 묻혀도 찾은 것이 보이게)
      return op;
    }
    var hlC = new THREE.Color(HL_COLOR), hlN = new THREE.Color('#ff3fd2'), WHITE = new THREE.Color('#ffffff');
    // 찾은 구조물 위에 한 겹 더 그리는 빛 — 옅게 한 구조물(투명)보다 나중에, 찾은 구조물의 앞면에만(같은 깊이) 그려져 덮인 층을 뚫고 또렷이 보임
    function glowOf(m) {
      var gm = S.glow.get(m);
      if (!gm) {
        var gmat = new THREE.MeshBasicMaterial({ color: m.userData.part.cls === 'nerve' ? GLOW_N : GLOW_C, transparent: true, opacity: 0.5,
          depthWrite: false, depthFunc: THREE.LessEqualDepth, side: THREE.DoubleSide });
        gmat.clippingPlanes = m.material.clippingPlanes;
        gm = new THREE.Mesh(m.geometry, gmat);
        gm.renderOrder = 20; gm.raycast = function () {};
        m.add(gm); S.glow.set(m, gm);
      }
      return gm;
    }
    function dropGlow(m) {
      var gm = S.glow.get(m);
      if (gm) { m.remove(gm); gm.material.dispose(); S.glow.delete(m); }
    }
    function refresh() {
      var t = performance.now() / 1000;
      var pulse = 0.35 + 0.25 * Math.sin(t * 4);
      S.meshes.forEach(function (m) {
        var mat = m.material, op = effOp(m), vis = effVis(m);
        m.visible = vis && op > 0.01;
        mat.opacity = op;
        var tr = op < 0.999;
        if (mat.transparent !== tr) { mat.transparent = tr; mat.needsUpdate = true; }
        mat.depthWrite = !tr;
        m.renderOrder = tr ? 1 : 0;
        if (S.hl.has(m)) {
          mat.color.copy(m.userData.baseColor).lerp(m.userData.part.cls === 'nerve' ? hlN : hlC, 0.7);
          mat.emissive.set(HL_EMISSIVE).multiplyScalar(pulse);
          var gm = glowOf(m);
          gm.material.opacity = 0.32 + 0.3 * (0.5 + 0.5 * Math.sin(t * 4));   // 0.32~0.62 로 맥박
        } else {
          if (S.glow.has(m)) dropGlow(m);
          mat.color.copy(m.userData.baseColor);
          if (S.tint[m.userData.part.cls]) mat.color.multiplyScalar(S.tint[m.userData.part.cls]);
          if (S.ghost && S.hl.size) mat.color.lerp(WHITE, 0.75);   // 주변을 하얗게 — 이름 가리기 대상이 장기에 가려도 보이게(사용자 2026-10-17)
          else if (S.dim && S.hl.size) mat.color.lerp(WHITE, DIM_WHITE);   // 찾기 — 주변은 흐린 색(사용자 2026-10-18)
          if (m === S.sel) mat.emissive.set(SEL_EMISSIVE);
          else if (m === S.hover) mat.emissive.set(HOVER_EMISSIVE);
          else mat.emissive.setRGB(0, 0, 0);
        }
        var xm = m.userData.xray;
        if (xm) {
          // 이름 가리기 강조(나머지 하얗게)일 때는 강조한 구조물만 비춤
          xm.visible = S.xray && (!((S.ghost || S.dim) && S.hl.size) || S.hl.has(m));
          xm.material.color.copy(mat.color);
          xm.material.opacity = XRAY_OP * Math.min(1, op);
        }
      });
      if (onVisChange) {
        var sig = 0, cnt = 0;
        S.meshes.forEach(function (m, k) { if (effVis(m)) { cnt++; sig = (sig * 31 + k + 1) % 2147483647; } });
        var key = cnt + ':' + sig;
        if (key !== S.visSig) { S.visSig = key; setTimeout(function () { try { onVisChange(); } catch (err) { console.error(err); } }, 0); }
      }
      S.dirty = true;
    }

    function resolve(ids) {
      var out = new Set();
      (Array.isArray(ids) ? ids : [ids]).forEach(function (id) {
        if (id == null) return;
        if (S.byId[id]) out.add(S.byId[id]);
        (S.bySid[id] || []).forEach(function (m) { out.add(m); });
      });
      return out;
    }

    function boxOf(set) {
      var b = new THREE.Box3(), tb = new THREE.Box3();
      set.forEach(function (m) { tb.copy(m.geometry.boundingBox); b.union(tb); });
      return b;
    }

    function fly(target, dist, dir) {
      var from = { t: controls.target.clone(), p: camera.position.clone() };
      var d = dir ? dir.clone().normalize() : camera.position.clone().sub(controls.target).normalize();
      var to = { t: target.clone(), p: target.clone().add(d.multiplyScalar(dist)) };
      S.tween = { from: from, to: to, t0: performance.now(), dur: 450 };
      S.dirty = true;
    }

    // 덜 가리는 방향 찾기 — 방향 27개 × 점 3개 광선을 한 번에 하면 큰 장면(전신)에서 1초 넘게 화면이 멈춤 →
    // 12 ms 씩 나눠 계산하고 끝나면 cb(방향). 다시 강조하거나 사용자가 돌리기 시작하면(controls start) 그만둠(2026-10-17).
    var bestJob = 0;
    function bestDirAsync(set, dist, cb) {
      var job = ++bestJob;
      var b = boxOf(set), c = new THREE.Vector3(), sz = new THREE.Vector3();
      b.getCenter(c); b.getSize(sz);
      var ax = sz.x >= sz.y && sz.x >= sz.z ? new THREE.Vector3(1, 0, 0) : sz.y >= sz.z ? new THREE.Vector3(0, 1, 0) : new THREE.Vector3(0, 0, 1);
      var L = Math.max(sz.x, sz.y, sz.z) * 0.3;
      var samples = [c.clone(), c.clone().addScaledVector(ax, L), c.clone().addScaledVector(ax, -L)];
      // 가릴 수 있는 것 = 대상 둘레 dist 안에 걸치는 부품만(광선이 그 거리까지만 감) — 전신 장면에서 1초 넘던 계산을 줄임
      var reach = dist * 1.05 + L + sz.length() / 2;
      var vis = S.meshes.filter(function (m) {
        if (!m.visible) return false;
        var bs = m.geometry.boundingSphere;
        return bs.center.distanceTo(c) - bs.radius < reach;
      });
      var cur = camera.position.clone().sub(controls.target).normalize();
      var dirs = [cur];
      [-1, 0, 1].forEach(function (x) { [-1, 0, 1].forEach(function (y) { [-1, 0, 1].forEach(function (z) {
        if (x || y || z) dirs.push(new THREE.Vector3(x, y, z).normalize());
      }); }); });
      var rc = new THREE.Raycaster(), best = null;
      function evalDir(k) {
        var d = dirs[k], score = 0;
        samples.forEach(function (s) {
          var from = s.clone().addScaledVector(d, dist);
          rc.set(from, s.clone().sub(from).normalize());
          rc.far = dist * 1.05;
          var hits = rc.intersectObjects(vis, false), seen = new Set();
          for (var i = 0; i < hits.length; i++) {
            var o = hits[i].object;
            if (!S.clipSusp && clipsMesh(o) && clipPlane.distanceToPoint(hits[i].point) < 0) continue;   // 단면으로 잘려 안 보이는 쪽은 가리지 않음
            if (set.has(o)) break;               // 대상에 닿음 — 그 앞의 것만 센다
            if (seen.has(o)) continue;
            seen.add(o);
            score += o.material.opacity > 0.5 ? 1 : 0.3;
          }
        });
        // 같은 점수면 지금 방향 → 앞쪽(+Z) 을 조금 우대
        score -= (k === 0 ? 0.25 : 0) + Math.max(0, d.z) * 0.1;
        if (!best || score < best.s) best = { s: score, d: d };
      }
      var k = 0;
      (function step() {
        if (job !== bestJob || S.disposed) return;
        var t0 = performance.now();
        while (k < dirs.length && performance.now() - t0 < 12) evalDir(k++);
        if (k < dirs.length) setTimeout(step, 0);
        else cb(best ? best.d : cur);
      })();
    }
    function fitDist(sphereR) {
      var fov = camera.fov * Math.PI / 180;
      var fovH = 2 * Math.atan(Math.tan(fov / 2) * camera.aspect);
      var f = Math.min(fov, fovH);
      if (!(camera.aspect > 0.15 && camera.aspect < 8)) f = fov;
      return Math.max(sphereR / Math.sin(f / 2) * 1.02, 30);
    }

    function resetView(animate) {
      if (!S.data) return;
      var vis = new Set(S.meshes.filter(function (m) { return m.visible; }));
      if (!vis.size) vis = new Set(S.meshes);
      var vb = S.data.view && S.data.view.box;
      var b = (!S.iso && vb) ? new THREE.Box3(new THREE.Vector3(vb[0], vb[1], vb[2]), new THREE.Vector3(vb[3], vb[4], vb[5])) : boxOf(vis);
      var c = new THREE.Vector3(), sz = new THREE.Vector3();
      b.getCenter(c); b.getSize(sz);
      var r = sz.length() / 2;
      var dir = new THREE.Vector3().fromArray((S.data.view && S.data.view.dir) || [0, 0, 1]).normalize();
      camera.near = Math.max(r / 200, 0.5); camera.far = r * 40 + 2000; camera.updateProjectionMatrix();
      S.autoFit = true;
      if (animate) { fly(c, fitDist(r), dir); return; }
      S.tween = null;
      controls.target.copy(c);
      camera.position.copy(c).add(dir.multiplyScalar(fitDist(r)));
      camera.up.set(0, 1, 0);
      controls.update();
      S.dirty = true;
    }

    function applyClip() {
      var planes = [];
      if (S.clip) {
        var ax = { x: 0, y: 1, z: 2 }[S.clip.axis] || 0;
        var n = new THREE.Vector3(); n.setComponent(ax, S.clip.keep === 'pos' ? 1 : -1);
        clipPlane.normal.copy(n);
        clipPlane.constant = S.clip.keep === 'pos' ? -S.clip.value : S.clip.value;
        if (!S.clipSusp) planes = [clipPlane];   // clipSusp = 잘려 나간 쪽 구조물을 강조하는 동안만 단면을 끔
      }
      S.meshes.forEach(function (m) {
        m.material.clippingPlanes = clipsMesh(m) ? planes : []; m.material.needsUpdate = true;
        if (m.userData.xray) { m.userData.xray.material.clippingPlanes = m.material.clippingPlanes; m.userData.xray.material.needsUpdate = true; }
        var gm = S.glow.get(m); if (gm) { gm.material.clippingPlanes = m.material.clippingPlanes; gm.material.needsUpdate = true; }
      });
      S.dirty = true;
    }
    function clipsMesh(m) { return !!S.clip && (!S.clip.only || S.clip.only.indexOf(m.userData.part.cls) >= 0); }
    // 단면으로 통째로 잘려 나가는 부품인가(경계상자 꼭짓점 8개가 모두 잘리는 쪽)
    var _cb = new THREE.Box3(), _cp = new THREE.Vector3();
    function fullyClipped(m) {
      if (!S.clip || !clipsMesh(m)) return false;
      _cb.copy(m.geometry.boundingBox).applyMatrix4(m.matrixWorld);
      for (var i = 0; i < 8; i++) {
        _cp.set(i & 1 ? _cb.max.x : _cb.min.x, i & 2 ? _cb.max.y : _cb.min.y, i & 4 ? _cb.max.z : _cb.min.z);
        if (clipPlane.distanceToPoint(_cp) >= 0) return false;
      }
      return true;
    }
    // 강조할 것이 전부 잘려 나간 쪽에 있으면 그동안 단면을 끄고, 아니면 다시 켬
    function clipFor(set) {
      var off = !!S.clip && set.size > 0 && Array.from(set).every(fullyClipped);
      if (off !== S.clipSusp) { S.clipSusp = off; applyClip(); }
    }

    // ── 고르기 · 마우스 올림 ─────────────────────────────────
    var ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
    function pickAt(clientX, clientY) {
      var rc = cv.getBoundingClientRect();
      ndc.set(((clientX - rc.left) / rc.width) * 2 - 1, -((clientY - rc.top) / rc.height) * 2 + 1);
      ray.setFromCamera(ndc, camera);
      var cand = S.meshes.filter(function (m) { return m.visible && m.material.opacity >= 0.3; });
      var hits = ray.intersectObjects(cand, false);
      for (var i = 0; i < hits.length; i++) {
        if (clipsMesh(hits[i].object) && clipPlane.distanceToPoint(hits[i].point) < 0) continue;
        return hits[i].object;
      }
      return null;
    }
    function info(m) {
      var p = m.userData.part;
      return { partId: p.id, sid: p.sid || null, ko: p.ko || null, en: p.en, cls: p.cls, side: p.side || null, fma: p.fma || null };
    }
    var down = null;
    function onDown(e) { controls.enableZoom = e.pointerType === 'touch'; down = { x: e.clientX, y: e.clientY, t: performance.now(), type: e.pointerType }; tip.style.display = 'none'; }
    function onUp(e) {
      if (!down) return;
      var moved = Math.hypot(e.clientX - down.x, e.clientY - down.y);
      var quick = performance.now() - down.t < 600;
      down = null;
      if (moved > 7 || !quick) return;
      var now = performance.now();
      if (e.pointerType !== 'mouse' && now - lastTap < 320) { lastTap = 0; hideAt(e.clientX, e.clientY); return; }
      lastTap = now;
      var m = pickAt(e.clientX, e.clientY);
      if (!m) { S.labelEls.forEach(function (el) { el.remove(); }); S.labelEls = new Map(); S.dim = false; }
      if (selectOnPick) { S.sel = m; addLabel(m); }
      refresh();
      try { onPick(m ? info(m) : null); } catch (err) { console.error(err); }
    }
    // 두 번 누르기(더블클릭·더블탭) = 그 점으로 회전 중심을 옮기고 조금 다가감
    var lastTap = 0;
    function focusAt(clientX, clientY) {
      var rc = cv.getBoundingClientRect();
      ndc.set(((clientX - rc.left) / rc.width) * 2 - 1, -((clientY - rc.top) / rc.height) * 2 + 1);
      ray.setFromCamera(ndc, camera);
      var cand = S.meshes.filter(function (m) { return m.visible && m.material.opacity >= 0.3; });
      var hits = ray.intersectObjects(cand, false);
      for (var i = 0; i < hits.length; i++) {
        if (clipsMesh(hits[i].object) && clipPlane.distanceToPoint(hits[i].point) < 0) continue;
        S.autoFit = false;
        fly(hits[i].point, camera.position.distanceTo(controls.target) * 0.6);
        return true;
      }
      return false;
    }
    function hideMesh(m) {
      if (!m || S.hidden.has(m)) return;
      S.hidden.add(m); S.hideStack.push(m); S.hl.delete(m);
      if (S.sel === m) S.sel = null;
      var el = S.labelEls.get(m); if (el) { el.remove(); S.labelEls.delete(m); }
      refresh();
      try { onHide(info(m), true); } catch (err) { console.error(err); }
    }
    function hideAt(clientX, clientY) {
      var m = pickAt(clientX, clientY);
      if (!m) {   // 반투명(고르기 제외) 뼈 등도 두 번 누르면 숨길 수 있게 — 뒤에 불투명한 것이 없을 때만
        var rc = cv.getBoundingClientRect();
        ndc.set(((clientX - rc.left) / rc.width) * 2 - 1, -((clientY - rc.top) / rc.height) * 2 + 1);
        ray.setFromCamera(ndc, camera);
        var hits = ray.intersectObjects(S.meshes.filter(function (x) { return x.visible; }), false);
        for (var i = 0; i < hits.length; i++) { if (!(clipsMesh(hits[i].object) && clipPlane.distanceToPoint(hits[i].point) < 0)) { m = hits[i].object; break; } }
      }
      hideMesh(m);
    }
    function onDbl(e) { hideAt(e.clientX, e.clientY); }
    function onWheel(e) {
      e.preventDefault();
      var k = e.deltaMode === 1 ? 33 : e.deltaMode === 2 ? 400 : 1;
      var dy = e.deltaY * k, dx = e.deltaX * k;
      if (e.ctrlKey || e.metaKey || S.wheel === 'zoom') { zoomBy(Math.pow(1.0015, dy)); return; }
      if (e.shiftKey && !dx) { dx = dy; dy = 0; }
      panBy(dx * 0.0011, -dy * 0.0011);
    }
    function panBy(fx, fy) {
      var dist = camera.position.distanceTo(controls.target);
      var h = 2 * dist * Math.tan(camera.fov * Math.PI / 360);
      var right = new THREE.Vector3().setFromMatrixColumn(camera.matrix, 0);
      var up = new THREE.Vector3().setFromMatrixColumn(camera.matrix, 1);
      var off = right.multiplyScalar(fx * h).add(up.multiplyScalar(fy * h));
      S.tween = null; S.autoFit = false;
      camera.position.add(off); controls.target.add(off);
      controls.update(); S.dirty = true;
    }
    function zoomBy(f) {
      var d = camera.position.clone().sub(controls.target).multiplyScalar(f);
      if (d.length() < 5) return;
      S.tween = null; S.autoFit = false;
      camera.position.copy(controls.target).add(d);
      controls.update(); S.dirty = true;
    }
    function visBox() {
      var vis = new Set(S.meshes.filter(function (m) { return m.visible; }));
      return boxOf(vis.size ? vis : new Set(S.meshes));
    }
    function onKey(e) {
      if (e.target && /INPUT|TEXTAREA|SELECT/.test(e.target.tagName)) return;
      var k = e.key, st = e.shiftKey ? 0.25 : 0.08;
      if (k === 'ArrowUp') panBy(0, st); else if (k === 'ArrowDown') panBy(0, -st);
      else if (k === 'ArrowLeft') panBy(-st, 0); else if (k === 'ArrowRight') panBy(st, 0);
      else if (k === '+' || k === '=') zoomBy(0.8); else if (k === '-' || k === '_') zoomBy(1.25);
      else return;
      e.preventDefault();
    }
    var hoverReq = null;
    function onMove(e) {
      if (e.pointerType !== 'mouse' || down) return;
      hoverReq = { x: e.clientX, y: e.clientY };
    }
    function onLeave() { hoverReq = null; if (S.hover) { S.hover = null; refresh(); } tip.style.display = 'none'; cv.style.cursor = ''; }
    function doHover() {
      if (!hoverReq) return;
      var q = hoverReq; hoverReq = null;
      var m = pickAt(q.x, q.y);
      if (m !== S.hover) { S.hover = m; refresh(); }
      cv.style.cursor = m ? 'pointer' : '';
      if (m && hoverTip) {
        var p = m.userData.part, rc = container.getBoundingClientRect();
        tip.textContent = p.ko ? p.ko + '  ·  ' + p.en : p.en;
        tip.style.left = (q.x - rc.left) + 'px'; tip.style.top = (q.y - rc.top) + 'px';
        tip.style.display = 'block';
      } else tip.style.display = 'none';
    }
    cv.addEventListener('pointerdown', onDown);
    cv.addEventListener('dblclick', onDbl);
    cv.addEventListener('wheel', onWheel, { passive: false });
    cv.tabIndex = 0;
    cv.addEventListener('keydown', onKey);
    cv.addEventListener('pointerenter', function () { try { cv.focus({ preventScroll: true }); } catch (e) {} });
    cv.addEventListener('pointerup', onUp);
    cv.addEventListener('pointermove', onMove);
    cv.addEventListener('pointerleave', onLeave);
    controls.addEventListener('change', function () { S.dirty = true; });
    controls.addEventListener('start', function () { S.autoFit = false; S.tween = null; bestJob++; });

    // ── 이름표 ───────────────────────────────────────────────
    function addLabel(m) {
      S.labelEls.forEach(function (el, mm) { if (!S.hl.has(mm) && mm !== m) { el.remove(); S.labelEls.delete(mm); } });
      if (m && !S.labelEls.has(m)) {
        var el = document.createElement('div');
        var p = m.userData.part;
        el.textContent = p.ko || p.en;
        el.title = p.en;
        el.style.cssText = 'position:absolute;left:0;top:0;padding:2px 7px;border-radius:10px;background:rgba(255,255,255,.92);color:#1b1b1f;border:1px solid rgba(0,0,0,.25);box-shadow:0 1px 3px rgba(0,0,0,.25);white-space:nowrap;transform:translate(-50%,-130%);';
        overlay.appendChild(el);
        S.labelEls.set(m, el);
      }
      S.dirty = true;
    }
    var v3 = new THREE.Vector3();
    function placeLabels() {
      var w = cv.clientWidth, h = cv.clientHeight;
      S.labelEls.forEach(function (el, m) {
        if (!S.labels || !m.visible) { el.style.display = 'none'; return; }
        m.geometry.boundingSphere.center && v3.copy(m.geometry.boundingSphere.center);
        v3.project(camera);
        if (v3.z > 1 || v3.z < -1) { el.style.display = 'none'; return; }
        el.style.display = 'block';
        el.style.left = ((v3.x + 1) / 2 * w) + 'px';
        el.style.top = ((1 - v3.y) / 2 * h) + 'px';
      });
    }

    // ── 그리기 ───────────────────────────────────────────────
    function loop() {
      if (S.disposed) return;
      S.raf = requestAnimationFrame(loop);
      doHover();
      if (S.tween) {
        var k = Math.min(1, (performance.now() - S.tween.t0) / S.tween.dur);
        var e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
        controls.target.lerpVectors(S.tween.from.t, S.tween.to.t, e);
        camera.position.lerpVectors(S.tween.from.p, S.tween.to.p, e);
        if (k >= 1) S.tween = null;
        S.dirty = true;
      }
      if (controls.update()) S.dirty = true;
      if (S.hl.size) refresh();
      if (S.dirty) {
        S.dirty = false;
        renderer.render(scene, camera);
        placeLabels();
      }
    }
    loop();

    // ── API ──────────────────────────────────────────────────
    var api = {
      loadScene: function (name) {
        var go = function () {
          var d = window.BP3D && window.BP3D[name];
          if (!d) throw new Error('3D 장면 없음: ' + name);
          S.name = name;
          build(d);
          return api.getScene();
        };
        if (window.BP3D && window.BP3D[name]) return Promise.resolve().then(go);
        return loadScript(base + name + '.js').then(go);
      },
      setClassVisible: function (cls, on) { S.classVis[cls] = !!on; refresh(); },
      setClassOpacity: function (cls, a) { S.classOp[cls] = Math.max(0, Math.min(1, +a)); refresh(); },
      clearClassOpacity: function (cls) { delete S.classOp[cls]; refresh(); },
      setBrightness: function (f) { bright = Math.max(0.3, Math.min(1.5, +f || 0.8)); hemi.intensity = LIGHT0.hemi * bright; key.intensity = LIGHT0.key * bright; fill.intensity = LIGHT0.fill * bright; S.dirty = true; },
      /** 가려진 동맥 · 신경 비춰 보기 켜고 끄기 */
      setXray: function (on) { S.xray = !!on; refresh(); },
      getXray: function () { return S.xray; },
      /** 찾을 때 나머지를 옅게 할지(기본 켬) — 끄면 빛만 */
      setDimOnSearch: function (on) { S.dimPref = !!on; if (!on) S.dim = false; refresh(); },
      /** 지금 나머지를 옅게 한 상태인지 */
      isDimmed: function () { return S.dim && S.hl.size > 0; },
      setClassTint: function (cls, f) { if (f && f !== 1) S.tint[cls] = f; else delete S.tint[cls]; refresh(); },
      /** 장면 범위(중심 기준 mm) — [xmin, ymin, zmin, xmax, ymax, zmax] */
      getBounds: function () { return (S.data && S.data.bbox) || null; },
      highlight: function (ids, o) {
        o = o || {};
        bestJob++;   // 앞서 찾던 방향은 버림
        S.hl = resolve(ids);
        S.ghost = !!o.ghost;
        S.dim = !!o.dim && S.dimPref && !S.ghost;
        if (o.reveal) S.hl.forEach(function (m) { S.hidden.delete(m); });   // 찾기 — 전에 두 번 눌러 숨긴 구조물이면 다시 보이게
        clipFor(S.hl);
        S.labelEls.forEach(function (el) { el.remove(); });
        S.labelEls = new Map();
        if (o.label !== false) S.hl.forEach(function (m) { addLabel(m); });
        refresh();
        if (S.hl.size && o.focus !== false) {
          S.autoFit = false;
          var b = boxOf(S.hl), c = new THREE.Vector3(), sz = new THREE.Vector3();
          b.getCenter(c); b.getSize(sz);
          var r = Math.max(sz.length() / 2, 25), dist = fitDist(r * 1.6);
          fly(c, dist, null);   // 먼저 지금 방향에서 그 구조물로 다가감(바로 빛남)
          if (o.bestView) {     // bestView = 가리는 부품이 가장 적은 쪽을 찾아 끝나면 그쪽으로 돌림
            var hl = S.hl;
            bestDirAsync(hl, dist, function (d) { if (S.hl === hl) fly(c, dist, d); });
          }
        }
        return Array.from(S.hl).map(function (m) { return m.userData.part.id; });
      },
      clearHighlight: function () {
        bestJob++;
        S.hl = new Set(); S.ghost = false; S.dim = false; S.sel = null;
        if (S.clipSusp) { S.clipSusp = false; applyClip(); }
        S.labelEls.forEach(function (el) { el.remove(); });
        S.labelEls = new Map();
        refresh();
      },
      isolate: function (ids) { var s = resolve(ids); S.hidden = new Set(); S.force = new Set(); S.iso = s.size ? s : null; refresh(); resetView(true); },
      showAll: function () {
        S.iso = null; S.hidden = new Set(); S.force = new Set();
        CLASSES.forEach(function (c) { S.classVis[c] = true; });
        refresh();
      },
      resetVisibility: function () { S.iso = null; S.classVis = {}; S.classOp = {}; S.force = new Set(); refresh(); },
      resetView: function () { resetView(true); },
      panBy: panBy,
      /** 이름 가리기 모드 — 마우스 올림 이름과 눌렀을 때 이름표를 끈다 */
      setQuizMode: function (on) {
        hoverTip = !on; selectOnPick = !on;
        if (on) { S.labelEls.forEach(function (el) { el.remove(); }); S.labelEls = new Map(); S.sel = null; tip.style.display = 'none'; }
        refresh();
      },
      /** 'pan' = 휠로 위아래 이동(기본) · 'zoom' = 휠로 확대 */
      setWheelMode: function (mode) { S.wheel = mode === 'zoom' ? 'zoom' : 'pan'; },
      clearLabels: function () { S.labelEls.forEach(function (el) { el.remove(); }); S.labelEls = new Map(); S.sel = null; refresh(); },
      /** 고른 부품만 남기기 — keepCls 의 부류(예: 뼈)는 같이 둔다 */
      showOnly: function (ids, keepCls, opt) {
        opt = opt || {};   // opt.ctx = 같이 보일 맥락 부품(이름표 없음) · opt.dir = 보는 방향(3D 도해 「3D로 돌려 보기」)
        var picked = resolve(ids), s2 = new Set(picked);
        if (opt.ctx) resolve(opt.ctx).forEach(function (m) { s2.add(m); });
        (keepCls || []).forEach(function (c) { S.meshes.forEach(function (m) { if (m.userData.part.cls === c) s2.add(m); }); });
        // 강조(층 · 검색)를 먼저 풀어야 고른 것만 남는다 — 강조된 부품은 iso 와 상관없이 보이기 때문
        S.hl = new Set(); S.ghost = false; S.dim = false;
        S.labelEls.forEach(function (el) { el.remove(); }); S.labelEls = new Map();
        S.hidden = new Set(); S.force = new Set(); S.iso = s2.size ? s2 : null;
        clipFor(picked);
        picked.forEach(function (m) { addLabel(m); });
        refresh();
        // 고른 부품에 맞춰 시점을 잡는다(뼈 전체가 아니라)
        if (picked.size) {
          S.autoFit = false;
          var b = boxOf(picked), c = new THREE.Vector3(), sz = new THREE.Vector3();
          b.getCenter(c); b.getSize(sz);
          fly(c, fitDist(Math.max(sz.length() / 2, 25) * 1.3), opt.dir ? new THREE.Vector3().fromArray(opt.dir) : null);
        } else resetView(true);
      },
      hide: function (ids) { resolve(ids).forEach(function (m) { S.force.delete(m); if (S.hidden.has(m)) return; S.hidden.add(m); S.hideStack.push(m); S.hl.delete(m); if (S.sel === m) S.sel = null; var el = S.labelEls.get(m); if (el) { el.remove(); S.labelEls.delete(m); } }); refresh(); },
      unhide: function (ids) { resolve(ids).forEach(function (m) { S.hidden.delete(m); var k = S.hideStack.indexOf(m); if (k >= 0) S.hideStack.splice(k, 1); }); refresh(); },
      /** 방금 숨긴 것 하나 되살리기 — 되살린 부품 정보를 돌려준다 */
      undoHide: function () {
        while (S.hideStack.length) {
          var m = S.hideStack.pop();
          if (S.hidden.has(m)) { S.hidden.delete(m); refresh(); try { onHide(info(m), false); } catch (err) {} return info(m); }
        }
        return null;
      },
      borrow: borrow,
      /** 지금 장면 자료(offset 등) */
      getData: function () { return S.data; },
      isHidden: function (id) { var m = S.byId[id]; return !!(m && S.hidden.has(m)); },
      /** 지금 보이는지(투명도와 상관없이 켜져 있는지) — 보이기 칸 체크 맞추기 */
      isVisible: function (id) { var m = S.byId[id]; return !!(m && effVis(m)); },
      /** 부품 켜고 끄기(보이기 칸) — 켜면 분류를 껐거나 기본 숨김 · 이것만 보기여도 보이고, 끄면 숨김(되돌리기 목록에는 안 넣음) */
      setVisible: function (ids, on) {
        resolve(ids).forEach(function (m) {
          if (on) { S.hidden.delete(m); S.force.add(m); var k = S.hideStack.indexOf(m); if (k >= 0) S.hideStack.splice(k, 1); }
          else { S.force.delete(m); S.hidden.add(m); S.hl.delete(m); if (S.sel === m) S.sel = null; var el = S.labelEls.get(m); if (el) { el.remove(); S.labelEls.delete(m); } }
        });
        refresh();
      },
      /** 그 부품을 회전 중심으로 — 예전 「두 번 누르기 = 중심」을 버튼으로 옮김 */
      focusPart: function (id) {
        var s2 = resolve([id]); if (!s2.size) return;
        S.autoFit = false;
        var b = boxOf(s2), c = new THREE.Vector3(), sz = new THREE.Vector3();
        b.getCenter(c); b.getSize(sz);
        fly(c, fitDist(Math.max(sz.length() / 2, 25) * 1.6));
      },
      unhideAll: function () { S.hidden = new Set(); S.hideStack = []; S.iso = null; refresh(); },
      onVisChange: function (fn) { onVisChange = fn; S.visSig = ''; refresh(); },
      zoomBy: zoomBy,
      /** 0 = 보이는 모형의 맨 아래, 1 = 맨 위 — 회전 중심을 그 높이로 옮긴다 */
      setHeight: function (t) {
        var b = visBox(); if (b.isEmpty()) return;
        var y = b.min.y + Math.max(0, Math.min(1, t)) * (b.max.y - b.min.y);
        var dy = y - controls.target.y;
        S.tween = null; S.autoFit = false;
        camera.position.y += dy; controls.target.y = y;
        controls.update(); S.dirty = true;
      },
      getHeight: function () {
        var b = visBox(); if (b.isEmpty()) return 0.5;
        return (controls.target.y - b.min.y) / Math.max(1e-6, b.max.y - b.min.y);
      },
      /** 'rotate' = 끌면 회전(기본) · 'pan' = 끌면 위아래·좌우 이동 */
      setDragMode: function (mode) {
        var pan = mode === 'pan';
        controls.mouseButtons = { LEFT: pan ? THREE.MOUSE.PAN : THREE.MOUSE.ROTATE, MIDDLE: THREE.MOUSE.DOLLY, RIGHT: pan ? THREE.MOUSE.ROTATE : THREE.MOUSE.PAN };
        if (THREE.TOUCH) controls.touches = { ONE: pan ? THREE.TOUCH.PAN : THREE.TOUCH.ROTATE, TWO: THREE.TOUCH.DOLLY_PAN };
      },
      setLabelsVisible: function (on) { S.labels = !!on; S.dirty = true; },
      setClipping: function (c) {
        S.clipSusp = false;
        if (c === true) S.clip = (S.data && S.data.clip) || { axis: 'x', value: 0, keep: 'neg' };
        else if (!c) S.clip = null;
        else S.clip = c;
        applyClip();
      },
      getClipping: function () { return S.clip; },
      getParts: function () {
        return S.meshes.map(function (m) { var o = info(m); o.visible = m.visible; o.kos = m.userData.part.kos || null; return o; });
      },
      getScene: function () {
        var d = S.data;
        if (!d) return null;
        var cls = {};
        d.parts.forEach(function (p) { cls[p.cls] = (cls[p.cls] || 0) + 1; });
        return { id: d.id, title: d.title, note: d.note, attr: d.attr, classes: cls, parts: d.parts.length, clip: d.clip };
      },
      classColors: CLS_COLOR,
      renderer: renderer, camera: camera, controls: controls,
      dispose: function () {
        S.disposed = true;
        cancelAnimationFrame(S.raf);
        if (ro) ro.disconnect(); else window.removeEventListener('resize', resize);
        cv.removeEventListener('pointerdown', onDown);
        cv.removeEventListener('pointerup', onUp);
        cv.removeEventListener('pointermove', onMove);
        cv.removeEventListener('pointerleave', onLeave);
        cv.removeEventListener('dblclick', onDbl);
        cv.removeEventListener('wheel', onWheel);
        cv.removeEventListener('keydown', onKey);
        clearScene();
        controls.dispose();
        renderer.dispose();
        if (renderer.forceContextLoss) renderer.forceContextLoss();
        cv.remove(); overlay.remove();
      }
    };
    return api;
  }

  window.Viewer3D = { createViewer: createViewer, CLASS_COLORS: CLS_COLOR, CLASSES: CLASSES };
})();
