/* Threads Under the Leaves: the model, with no drawing. It runs without a screen (see src/mycelium/test_mycelium.js).
   A graph of strands on a 20 cm square of soil. Lengths in cm, time in days, resource in arbitrary units (u).
   Flow: pressure at colonised wood, leaks at growing tips and at wood being colonised, conductance of a strand proportional to
   the number of hyphae in it (after Heaton et al. 2010, 2012). Branching by surplus supply at the tip (after Prosser & Trinci 1979).
   One timing rule is used five times: a count builds from a signal, reaches a fixed threshold, something happens, the count restarts. */
(function (root) {
  'use strict';
  function rng(seed) { let a = (seed >>> 0) || 1; return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  const sm = (a, b, x) => { const t = Math.max(0, Math.min(1, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
  const P = {
    W: 20, H: 20, R: 9.5, dt: 0.02, seg: 0.15,
    vmax: 0.8, Ihalf: 0.3, gTip: 1.6, cLen: 1,          /* tip: fastest extension cm/day; supply for half speed; sink strength; u per cm of new strand */
    pLo: 0.10, pHi: 0.25,                               /* a tip stops drawing when the pressure behind it falls through this range */
    Cb: 0.5,                                            /* branch: surplus (u) gathered at the tip before a branch is made */
    rs: 0.22, kf: 1.5, Fb: 1,                             /* fusion: range cm; count rate per day at contact; threshold */
    kap: 40, q0: 1.0, Ub: 0.5, Db: 0.4, need1: 0.3, keep: 0.25, crowdLo: 8, crowdHi: 20, NMAX: 24, Kmem: 0.3,   /* strands: conductance per hypha; flow one hypha carries; thresholds */
    recycle: 0.5, kr: 0.6,                                /* share of a withdrawn strand recovered; rate at which it is fed back, per day */
    gUp: 150, S0: 6000, gCol: 300, colNeed: 600,           /* wood: uptake conductance, store, sink strength while colonised, u to colonise */
    fruitP: 0.75, kF: 0.5, fruitF: 1, fruitNeed: 25, gFruit: 3, fruitLife: 14,
    ka: 0.08, kw: 1.2, kh: 1.6, Km: 0.1, turn: 3, maxTurn: 4, sigma: 0.35, tipCap: 600
  };
  const moistGrow = m => (0.25 + 0.75 * sm(0.1, 0.6, m)) * (1 - 0.45 * sm(0.85, 1, m));     /* too dry and too wet both slow a tip */
  const moistFruit = m => sm(0.55, 0.75, m);
  const act = p => sm(P.pLo, P.pHi, p);
  const edge = (x, y) => P.R - Math.hypot(x - P.W / 2, y - P.H / 2);                      /* the patch is round: distance in from its rim */

  /* ---- nodes, strands, tips ---- */
  function newNode(W, x, y, blk) { let i = W.free.length ? W.free.pop() : W.nx.length; W.nx[i] = x; W.ny[i] = y; W.nd[i] = 0; W.nb[i] = blk === undefined ? -1 : blk; W.nr[i] = 0; W.na[i] = 1;
    if (i >= W.p.length) { const q = new Float64Array(W.p.length * 2); q.set(W.p); W.p = q; W.wk = null; } W.p[i] = 0; return i; }
  function dropNode(W, i) { if (W.nb[i] >= 0 || !W.na[i]) return; W.na[i] = 0; W.nd[i] = 0; W.lost += Math.max(0, W.nr[i]); W.nr[i] = 0; W.p[i] = 0; W.free.push(i); }
  function newEdge(W, a, b, pts, n) { const e = { a, b, pts, len: 0, n: n || 1, g: 0, Q: 0, cU: 0, cD: 0, mem: 0, tip: null, alive: true, born: W.t }; for (let i = 2; i < pts.length; i += 2) e.len += Math.hypot(pts[i] - pts[i - 2], pts[i + 1] - pts[i - 1]); W.nd[a]++; W.nd[b]++; W.edges.push(e); return e; }
  function newTip(W, node, th, from) { const x = W.nx[node], y = W.ny[node], nn = newNode(W, x, y); W.p[nn] = W.p[node]; const e = newEdge(W, node, nn, [x, y, x, y], 1);
    const t = { edge: e, x, y, th, C: 0, F: 0, mx: from ? from.mx : 0, my: from ? from.my : 0, tC: W.t, since: 0, alive: true, I: 0, v: 0, g: 0, heir: null, near: 9 }; e.tip = t; W.tips.push(t); return t; }
  function killTip(W, t) { t.alive = false; if (t.edge) t.edge.tip = null; }
  function removeEdge(W, e, why) { if (!e.alive) return; e.alive = false; if (e.tip) killTip(W, e.tip);
    const a = e.a, b = e.b, keep = W.nd[a] > 1 || W.nb[a] >= 0 ? a : b, give = e.len * e.n * P.cLen * P.recycle;
    if (why !== 'cut') { W.withdrawn += e.len; W.recycled += give; W.nr[keep] += give; W.ev.drop++; }
    for (const i of [a, b]) { W.nd[i]--; if (W.nd[i] <= 0 && W.nb[i] < 0) { const o = i === a ? b : a; if (W.na[o] && o !== i) { W.nr[o] += W.nr[i]; W.nr[i] = 0; } dropNode(W, i); } } }
  /* split a strand at point k (0 < k < last): returns the new junction */
  function split(W, e, k) { const x = e.pts[2 * k], y = e.pts[2 * k + 1], j = newNode(W, x, y); W.p[j] = (W.p[e.a] + W.p[e.b]) / 2; const tail = e.pts.slice(2 * k), ob = e.b, tip = e.tip;
    e.pts.length = 2 * k + 2; W.nd[ob]--; e.b = j; W.nd[j]++; e.tip = null; e.len = 0; for (let i = 2; i < e.pts.length; i += 2) e.len += Math.hypot(e.pts[i] - e.pts[i - 2], e.pts[i + 1] - e.pts[i - 1]);
    const f = newEdge(W, j, ob, tail, e.n); f.Q = e.Q; f.cU = e.cU; f.cD = e.cD; f.mem = e.mem; f.born = e.born; if (tip) { f.tip = tip; tip.edge = f; } return j; }

  /* ---- wood and litter ---- */
  function local(b, x, y) { const c = Math.cos(b.rot), s = Math.sin(b.rot), dx = x - b.x, dy = y - b.y; return [dx * c + dy * s, -dx * s + dy * c]; }
  function inBlock(b, x, y, pad) { const l = local(b, x, y); return Math.abs(l[0]) < b.hw + (pad || 0) && Math.abs(l[1]) < b.hh + (pad || 0); }
  function distBlock(b, x, y) { const l = local(b, x, y), dx = Math.max(Math.abs(l[0]) - b.hw, 0), dy = Math.max(Math.abs(l[1]) - b.hh, 0); return Math.hypot(dx, dy); }
  function rim(b, ang) { const c = Math.cos(ang - b.rot), s = Math.sin(ang - b.rot), k = Math.min(b.hw / Math.max(1e-6, Math.abs(c)), b.hh / Math.max(1e-6, Math.abs(s))) * 1.02; return [b.x + Math.cos(ang) * k, b.y + Math.sin(ang) * k]; }
  function addBlock(W, x, y, opt) { const o = opt || {}, kind = o.kind || 'wood', size = o.size || 1, lit = kind === 'litter';
    const b = { x, y, rot: o.rot === undefined ? (W.rnd() - 0.5) * 1.2 : o.rot, hw: (lit ? 0.75 : 1.25) * size, hh: (lit ? 0.42 : 0.85) * size, kind, state: o.state || 'new', S0: (lit ? 0.07 : 1) * P.S0 * size * size, S: 0,
      gUp: (lit ? 0.2 : 1) * P.gUp * size, gCol: (lit ? 0.15 : 1) * P.gCol * size, colNeed: (lit ? 0.08 : 1) * P.colNeed * size * size, col: 0, cF: 0, hub: -1, placed: W.t, tContact: -1, tSource: -1, out: 0, id: W.blocks.length, seed: W.rnd() };
    b.S = b.S0; b.hub = newNode(W, x, y, b.id); W.blocks.push(b);
    if (b.state === 'new' && o.touch !== false) { let made = 0; for (const e of W.edges.slice()) { if (!e.alive || made >= 3) continue; const q = e.pts, np = q.length / 2; for (let k = 1; k < np - 1; k++) if (inBlock(b, q[2 * k], q[2 * k + 1], -0.1)) { const j = split(W, e, k); newEdge(W, j, b.hub, [W.nx[j], W.ny[j], x, y], 1); made++; break; } }
      if (made) { b.state = 'col'; b.tContact = W.t; W.ev.contact++; } } if (b.state === 'source') { b.tSource = W.t; sprout(W, b, o.tips || 10); } return b; }
  function sprout(W, b, k) { const a0 = W.rnd() * 6.2832; for (let i = 0; i < k; i++) { const ang = a0 + (i + (W.rnd() - 0.5) * 0.5) * 6.2832 / k, r = rim(b, ang), t = newTip(W, b.hub, ang), e = t.edge;
      e.pts[2] = r[0]; e.pts[3] = r[1]; e.pts.push(r[0], r[1]); e.len = Math.hypot(r[0] - b.x, r[1] - b.y); t.x = r[0]; t.y = r[1]; W.nx[e.b] = r[0]; W.ny[e.b] = r[1]; } }

  /* ---- a world ---- */
  function create(opt) { const o = Object.assign({ seed: 1, moisture: 0.7, fusion: true, litter: 0, inoculum: [6, 10] }, opt || {});
    const W = { t: 0, seed: o.seed, rnd: rng(o.seed), moisture: o.moisture, fusion: o.fusion, nx: [], ny: [], nd: [], nb: [], nr: [], na: [], free: [], p: new Float64Array(1024), wk: null,
      edges: [], tips: [], blocks: [], fruits: [], ev: { branch: 0, fuse: 0, thick: 0, thin: 0, drop: 0, fruit: 0, contact: 0, cut: 0 }, withdrawn: 0, grown: 0, recycled: 0, lost: 0, cutLen: 0,
      intervals: [], log: [], fusions: [], branches: [], steps: 0, hc: null, hn: 0, hE: [], hI: [], keepBranches: !!o.keepBranches };
    addBlock(W, o.inoculum[0], o.inoculum[1], { state: 'source', rot: 0.25, size: 0.85, tips: 10 });
    for (let i = 0, g = 0; i < o.litter && g < 400; g++) { const x = 1.5 + W.rnd() * (P.W - 3), y = 1.5 + W.rnd() * (P.H - 3); if (edge(x, y) > 1.6 && W.blocks.every(b => Math.hypot(b.x - x, b.y - y) > 3.2)) { addBlock(W, x, y, { kind: 'litter', rot: W.rnd() * 6.28, size: 0.8 + 0.5 * W.rnd() }); i++; } }
    return W; }

  /* ---- where things are: a grid of strand points, rebuilt each step ---- */
  const GC = 0.5, GW = Math.ceil(P.W / GC), GH = Math.ceil(P.H / GC);
  function hash(W) { const cells = W.hc || (W.hc = new Array(GW * GH)); for (let i = 0; i < cells.length; i++) if (cells[i]) cells[i].length = 0; const hE = W.hE; hE.length = 0; let m = 0;
    for (const e of W.edges) { if (!e.alive) continue; const q = e.pts, id = hE.length; hE.push(e);
      for (let i = 0; i < q.length; i += 2) { const cx = Math.min(GW - 1, Math.max(0, (q[i] / GC) | 0)), cy = Math.min(GH - 1, Math.max(0, (q[i + 1] / GC) | 0)), c = cx + GW * cy; (cells[c] || (cells[c] = [])).push(id, i >> 1); m++; } } W.hn = m; }
  function dens0(W, cx, cy) { if (cx < 0 || cy < 0 || cx >= GW || cy >= GH) return 8; const c = W.hc[cx + GW * cy]; return c ? c.length / 2 : 0; }
  function dens(W, x, y) { const fx = x / GC - 0.5, fy = y / GC - 0.5, ix = Math.floor(fx), iy = Math.floor(fy), tx = fx - ix, ty = fy - iy;               /* strand points per cell, smoothed between cells */
    return (dens0(W, ix, iy) * (1 - tx) + dens0(W, ix + 1, iy) * tx) * (1 - ty) + (dens0(W, ix, iy + 1) * (1 - tx) + dens0(W, ix + 1, iy + 1) * tx) * ty; }

  /* ---- flow: (Laplacian + leaks) p = sources, by conjugate gradients from the last answer ---- */
  function conduct(e) { return P.kap * e.n / Math.max(0.03, e.len); }
  function solve(W, iters, tol, noLeak, rhs, pOut) { const N = W.nx.length; if (!W.wk || W.wk.N < N) { const M = W.p.length; W.wk = { N: M, d: new Float64Array(M), b: new Float64Array(M), r: new Float64Array(M), z: new Float64Array(M), q: new Float64Array(M), s: new Float64Array(M) }; }
    const { d, b, r, z, q, s } = W.wk, p = pOut || W.p, E = W.edges, mg = moistGrow(W.moisture); d.fill(0, 0, N); b.fill(0, 0, N);
    if (!W.fa || W.fa.length < E.length) { const c = Math.max(256, E.length * 2); W.fa = new Int32Array(c); W.fb = new Int32Array(c); W.fg = new Float64Array(c); }
    const fa = W.fa, fb = W.fb, fg = W.fg; let m = 0;
    for (let i = 0; i < E.length; i++) { const e = E[i]; if (!e.alive) continue; const g = e.g = conduct(e); d[e.a] += g; d[e.b] += g; fa[m] = e.a; fb[m] = e.b; fg[m++] = g; }
    if (!noLeak) { for (const t of W.tips) { if (!t.alive) continue; const i = t.edge.b; t.g = P.gTip * mg * act(W.p[i]) * (1 - sm(P.crowdLo, P.crowdHi, dens(W, t.x, t.y))) * sm(0.2, 1.5, edge(t.x, t.y));    /* poorly supplied, hemmed in, or at the edge of the patch: the tip stops drawing */ d[i] += t.g; }
      for (const k of W.blocks) { if (k.state === 'col') d[k.hub] += k.gCol; else if (k.state === 'source') { const Pb = 1.25 * k.S / (k.S + 0.25 * k.S0); k.Pb = Pb; d[k.hub] += k.gUp; b[k.hub] += k.gUp * Pb; } }
      for (const f of W.fruits) if (f.state === 0) d[W.blocks[f.block].hub] += P.gFruit;
      for (let i = 0; i < N; i++) if (W.na[i] && W.nr[i] > 0) { const g = P.kr * W.nr[i]; d[i] += g; b[i] += g; } }      /* what was taken back is offered again, at the pressure of fresh wood */
    else for (let i = 0; i < N; i++) b[i] = rhs[i];
    for (let i = 0; i < N; i++) { if (!W.na[i] || d[i] === 0) { d[i] = 1; b[i] = 0; p[i] = 0; } else d[i] += 1e-7; }
    const mv = (x, y) => { for (let i = 0; i < N; i++) y[i] = d[i] * x[i]; for (let k = 0; k < m; k++) { const g = fg[k], i = fa[k], j = fb[k]; y[i] -= g * x[j]; y[j] -= g * x[i]; } };
    mv(p, q); let rz = 0, bb = 0; for (let i = 0; i < N; i++) { r[i] = b[i] - q[i]; z[i] = r[i] / d[i]; s[i] = z[i]; rz += r[i] * z[i]; bb += b[i] * b[i]; }
    const stop = (tol || 1e-5) * (tol || 1e-5) * (bb + 1e-30); let it = 0;
    for (; it < iters; it++) { let rr = 0; for (let i = 0; i < N; i++) rr += r[i] * r[i]; if (rr <= stop) break; mv(s, q); let sq = 0; for (let i = 0; i < N; i++) sq += s[i] * q[i]; if (!(sq > 0)) break; const al = rz / sq; let rz2 = 0;
      for (let i = 0; i < N; i++) { p[i] += al * s[i]; r[i] -= al * q[i]; z[i] = r[i] / d[i]; rz2 += r[i] * z[i]; } const be = rz2 / rz; rz = rz2; for (let i = 0; i < N; i++) s[i] = z[i] + be * s[i]; }
    if (!noLeak) { for (const e of E) if (e.alive) e.Q = e.g * (p[e.a] - p[e.b]); for (const t of W.tips) if (t.alive) t.I = t.g * Math.max(0, p[t.edge.b]); }
    return it; }

  /* ---- events ---- */
  function note(W, k, x, y) { W.log.push({ k, x, y, t: W.t }); if (W.log.length > 80) W.log.shift(); }
  function gauss(W) { return Math.sqrt(-2 * Math.log(1 - W.rnd())) * Math.cos(6.2831853 * W.rnd()); }
  function branch(W, t) { const e = t.edge, q = e.pts, np = q.length / 2; W.ev.branch++; W.intervals.push(W.t - t.tC); if (W.intervals.length > 6000) W.intervals.splice(0, 1000); if (W.keepBranches) W.branches.push(t.x, t.y); note(W, 'b', t.x, t.y);
    const cr = Math.cos(t.th) * t.my - Math.sin(t.th) * t.mx, side = Math.abs(cr) > 1e-4 ? Math.sign(cr) : (W.rnd() < 0.5 ? -1 : 1);     /* the side the tip has lately been drawn to */
    t.C = 0; t.tC = W.t;
    if (e.len > 0.75 && np >= 5) {                                 /* lateral: a branch leaves the strand a little behind the tip */
      let k = np - 1, back = 0; while (k > 1 && back < 0.3) { back += Math.hypot(q[2 * k] - q[2 * k - 2], q[2 * k + 1] - q[2 * k - 1]); k--; }
      if (k < 1) k = 1; const th0 = Math.atan2(q[2 * k + 1] - q[2 * k - 1], q[2 * k] - q[2 * k - 2]), j = split(W, e, k); return newTip(W, j, th0 + side * (1.13 + 0.17 * gauss(W)), t); }
    const j = e.b; e.tip = null; t.alive = false;                 /* apical: the tip itself divides */
    const a = newTip(W, j, t.th - side * 0.3, t), b = newTip(W, j, t.th + side * (0.6 + 0.15 * gauss(W)), t); a.F = t.F; t.heir = a; return b; }
  function fuse(W, t, E, k) { const e = t.edge, last = E.pts.length / 2 - 1, own = e.b; let node;
    if (k <= 0) node = E.a; else if (k >= last) { node = E.b; if (E.tip) killTip(W, E.tip); } else node = split(W, E, k);
    if (node === e.a) return false;
    const x = W.nx[node], y = W.ny[node]; e.len += Math.hypot(x - t.x, y - t.y); e.pts[e.pts.length - 2] = x; e.pts[e.pts.length - 1] = y;
    W.nr[node] += W.nr[own]; W.nr[own] = 0; W.nd[own]--; dropNode(W, own); e.b = node; W.nd[node]++; killTip(W, t); W.ev.fuse++; W.fusions.push(x, y, W.t); if (W.fusions.length > 3000) W.fusions.splice(0, 600); note(W, 'f', x, y); return true; }
  function contact(W, t, b) { const e = t.edge, own = e.b; e.pts.push(b.x, b.y); e.len += Math.hypot(b.x - t.x, b.y - t.y); W.nr[b.hub] += W.nr[own]; W.nr[own] = 0; W.nd[own]--; dropNode(W, own); e.b = b.hub; W.nd[b.hub]++; killTip(W, t); W.ev.contact++;
    if (b.state === 'new') { b.state = 'col'; b.tContact = W.t; note(W, 'c', b.x, b.y); } }
  function startFruit(W, b) { let best = null, bv = -1; for (const e of W.edges) if (e.alive && (e.a === b.hub || e.b === b.hub)) { const v = e.mem + Math.abs(e.Q) * 0.1; if (v > bv) { bv = v; best = e; } }
    let ang = W.rnd() * 6.2832; if (best) { const q = best.pts, i = best.a === b.hub ? 2 : q.length - 4; ang = Math.atan2(q[i + 1] - b.y, q[i] - b.x); }
    const k = 3 + ((W.rnd() * 3) | 0); for (let i = 0; i < k; i++) { const a = ang + (i - (k - 1) / 2) * 0.33 + (W.rnd() - 0.5) * 0.2, r = rim(b, a), o = 0.12 + 0.3 * W.rnd();
      W.fruits.push({ block: b.id, x: r[0] + Math.cos(a) * o, y: r[1] + Math.sin(a) * o, got: 0, need: P.fruitNeed * (0.6 + 0.8 * W.rnd()), size: 0, state: 0, t0: W.t, tM: -1, lean: (W.rnd() - 0.5) * 0.5, hue: W.rnd() }); }
    W.ev.fruit++; note(W, 'm', b.x, b.y); }
  /* a cut: everything within r of (x, y) is removed. Cut ends that still have supply put out new tips. */
  function cut(W, x, y, r) { if (W.blocks.some(b => inBlock(b, x, y, 0))) return 0; let n = 0; const r2 = r * r, list = W.edges.slice();
    for (const e of list) { if (!e.alive) continue; const q = e.pts, np = q.length / 2; let i0 = -1, i1 = -1; for (let i = 0; i < np; i++) { const dx = q[2 * i] - x, dy = q[2 * i + 1] - y; if (dx * dx + dy * dy < r2) { if (i0 < 0) i0 = i; i1 = i; } } if (i0 < 0) continue; n++;
      const L = q.slice(0, 2 * i0), R = q.slice(2 * i1 + 2), tip = e.tip, a = e.a, b = e.b, lv = e.n; e.tip = null; W.cutLen += e.len; e.alive = false; W.nd[a]--; W.nd[b]--;
      if (L.length >= 4) { const j = newNode(W, L[L.length - 2], L[L.length - 1]); W.p[j] = W.p[a]; const f = newEdge(W, a, j, L, lv); f.mem = e.mem; W.cutLen -= f.len; newTip(W, j, Math.atan2(L[L.length - 1] - L[L.length - 3], L[L.length - 2] - L[L.length - 4])); } else if (W.nd[a] <= 0) dropNode(W, a);
      if (R.length >= 4) { const j = newNode(W, R[0], R[1]); W.p[j] = W.p[b]; const f = newEdge(W, j, b, R, lv); f.mem = e.mem; W.cutLen -= f.len; if (tip) { f.tip = tip; tip.edge = f; } newTip(W, j, Math.atan2(R[1] - R[3], R[0] - R[2])); } else { if (tip) killTip(W, tip); if (W.nd[b] <= 0) dropNode(W, b); } }
    if (n) { W.ev.cut++; note(W, 'x', x, y); } W.edges = W.edges.filter(e => e.alive); return n; }

  /* ---- one step of dt days ---- */
  function step(W, iters) { const dt = P.dt, E = W.edges, B = W.blocks, p = W.p; hash(W); solve(W, iters || 30, 1e-5);
    /* strands: thicken where flow keeps passing, thin and withdraw where it does not */
    let dead = 0;
    for (let i = 0, n = E.length; i < n; i++) { const e = E[i]; if (!e.alive) { dead++; continue; } const aq = Math.abs(e.Q), full = P.q0 * e.n, need = e.n > 1 ? P.keep * P.q0 * (e.n - 1) : P.q0 * P.need1;
      if (aq > full && e.n < P.NMAX) { e.cU += (aq - full) * dt; if (e.cU >= P.Ub) { e.cU = 0; e.cD = 0; e.n++; e.mem += P.Kmem * (aq - e.mem); W.ev.thick++; let big = null; for (const k of B) if (k.state === 'source' && (!big || k.S > big.S)) big = k; if (big) big.S = Math.max(0, big.S - e.len * P.cLen * 0.5); } }
      else if (aq < need) { e.cD += (need - aq) * dt; if (e.cD >= P.Db * e.n) { e.cD = 0; e.cU = 0; if (e.n > 1) { e.n--; e.mem += P.Kmem * (aq - e.mem); const give = e.len * P.cLen * P.recycle; W.nr[p[e.a] >= p[e.b] ? e.a : e.b] += give; W.recycled += give; W.ev.thin++; } else if (aq > 1e-3 || W.nd[e.a] <= 1 || W.nd[e.b] <= 1) { removeEdge(W, e); dead++; } else e.cD = P.Db * 0.999; } } }
    /* tips */
    const T = W.tips, cells = W.hc, sdt = Math.sqrt(dt); let nt = 0, deadT = 0; for (const t of T) if (t.alive) nt++;
    for (let ti = 0, tn = T.length; ti < tn; ti++) { const t = T[ti]; if (!t.alive) { deadT++; continue; } const e = t.edge, I = t.I, v = P.vmax * I / (I + P.Ihalf), sur = I - v * P.cLen; t.v = v; if (sur > 0) t.C += sur * dt;
      const hx = Math.cos(t.th), hy = Math.sin(t.th); let gx = 0, gy = 0;
      { const lx = Math.cos(t.th + 0.9), ly = Math.sin(t.th + 0.9), rx = Math.cos(t.th - 0.9), ry = Math.sin(t.th - 0.9), dl = dens(W, t.x + lx * 0.7, t.y + ly * 0.7), dr = dens(W, t.x + rx * 0.7, t.y + ry * 0.7), w = P.ka * (dr - dl) * 2; gx += w * (lx - rx); gy += w * (ly - ry); }            /* keep away from other hyphae */
      let hit = null; for (const b of B) { if (b.state === 'spent') continue; const d = distBlock(b, t.x, t.y); if (d <= 0 && !(e.a === b.hub && e.len < 2.5)) { hit = b; break; }
        if ((b.state === 'new' || b.state === 'col') && d < 1.6 && d > 0) { const w = P.kw * Math.exp(-d / 0.6), l = Math.hypot(b.x - t.x, b.y - t.y); gx += w * (b.x - t.x) / l; gy += w * (b.y - t.y) / l; } }
      if (hit) { contact(W, t, hit); continue; }
      { const ed = edge(t.x, t.y); if (ed < 1.3) { const rr = Math.hypot(t.x - P.W / 2, t.y - P.H / 2) || 1, k = (1.3 - ed) * 1.6; gx -= k * (t.x - P.W / 2) / rr; gy -= k * (t.y - P.H / 2) / rr; } }
      /* the nearest strand that is not its own: within range the tip turns to it and a count builds; at the threshold they fuse */
      let bd = P.rs * P.rs, bE = null, bk = 0; const cx = (t.x / GC) | 0, cy = (t.y / GC) | 0, young = e.len < 0.8;
      for (let jy = cy - 1; jy <= cy + 1; jy++) { if (jy < 0 || jy >= GH) continue; for (let jx = cx - 1; jx <= cx + 1; jx++) { if (jx < 0 || jx >= GW) continue; const c = cells[jx + GW * jy]; if (!c) continue;
        for (let q = 0; q < c.length; q += 2) { const o = W.hE[c[q]]; if (o === e || !o.alive) continue; if (young && (o.a === e.a || o.b === e.a)) continue; const k = c[q + 1]; if (2 * k + 1 >= o.pts.length) continue; const dx = o.pts[2 * k] - t.x, dy = o.pts[2 * k + 1] - t.y, d2 = dx * dx + dy * dy; if (d2 < bd) { bd = d2; bE = o; bk = k; } } } }
      t.near = bE ? Math.sqrt(bd) : 9;
      if (bE && W.fusion) { const d = Math.sqrt(bd) || 1e-6; t.F += P.kf * (1 - d / P.rs) * dt; const w = P.kh * 4 * Math.max(0, t.F - 0.3); gx += w * (bE.pts[2 * bk] - t.x) / d; gy += w * (bE.pts[2 * bk + 1] - t.y) / d;
        if (t.F >= P.Fb) { t.F = 0; if (fuse(W, t, bE, bk)) continue; } }
      t.mx += P.Km * (gx - t.mx); t.my += P.Km * (gy - t.my);                                                   /* a fading memory of where it has been drawn */
      const cr = hx * gy - hy * gx; t.th += Math.max(-P.maxTurn, Math.min(P.maxTurn, cr * P.turn)) * dt + P.sigma * sdt * gauss(W);
      const ds = v * dt; if (ds > 0) { t.x += Math.cos(t.th) * ds; t.y += Math.sin(t.th) * ds; { const rr = Math.hypot(t.x - P.W / 2, t.y - P.H / 2); if (rr > P.R) { t.x = P.W / 2 + (t.x - P.W / 2) * P.R / rr; t.y = P.H / 2 + (t.y - P.H / 2) * P.R / rr; } } const q = e.pts, L = q.length; q[L - 2] = t.x; q[L - 1] = t.y; W.nx[e.b] = t.x; W.ny[e.b] = t.y; e.len += ds; t.since += ds; W.grown += ds; if (t.since >= P.seg) { q.push(t.x, t.y); t.since = 0; } }
      if (t.C >= P.Cb) { if (nt < P.tipCap) { branch(W, t); nt++; } else t.C = P.Cb * 0.999; } }
    /* wood: stores, colonising, fruiting */
    const mf = moistFruit(W.moisture);
    for (const b of B) { const ph = p[b.hub];
      if (b.state === 'source') { b.out = b.gUp * (b.Pb - ph); b.S = Math.min(b.S0, Math.max(0, b.S - b.out * dt)); if (b.S < 0.01 * b.S0) { b.state = 'spent'; b.out = 0; }
        if (b.kind === 'wood') { b.cF += mf * P.kF * Math.max(0, ph - P.fruitP) * dt; if (b.cF >= P.fruitF) { b.cF = 0; startFruit(W, b); } } }
      else if (b.state === 'col') { b.out = -b.gCol * Math.max(0, ph); b.col += -b.out * dt; if (b.col >= b.colNeed) { b.col = 0; b.state = 'source'; b.tSource = W.t; sprout(W, b, b.kind === 'litter' ? 3 : 9); note(W, 's', b.x, b.y); } } }
    for (let i = W.fruits.length - 1; i >= 0; i--) { const f = W.fruits[i], b = B[f.block]; if (f.state === 0) { f.got += P.gFruit * Math.max(0, p[b.hub]) * dt; f.size = Math.min(1, f.got / f.need); if (f.size >= 1) { f.state = 1; f.tM = W.t; } if (W.t - f.t0 > 40 && f.size < 0.15) W.fruits.splice(i, 1); }
      else if (W.t - f.tM > P.fruitLife + 4) W.fruits.splice(i, 1); else if (W.t - f.tM > P.fruitLife) f.state = 2; }
    for (let i = 0, N = W.nx.length; i < N; i++) if (W.nr[i] > 0) W.nr[i] = Math.max(0, W.nr[i] - P.kr * W.nr[i] * (1 - p[i]) * dt);
    if (dead > 200 || dead > E.length / 3) W.edges = E.filter(e => e.alive); if (deadT > 100) W.tips = T.filter(t => t.alive);
    W.t += dt; W.steps++; }
  function runTo(W, t, each) { while (W.t < t - 1e-9) { step(W); if (each) each(W); } return W; }

  /* ---- measuring ---- */
  function find(u, i) { while (u[i] !== i) { u[i] = u[u[i]]; i = u[i]; } return i; }
  function stats(W) { const N = W.nx.length, u = new Int32Array(N); for (let i = 0; i < N; i++) u[i] = i; let E = 0, len = 0, mat = 0, qmax = 0, tips = 0, deliv = 0, cords = 0;
    for (const e of W.edges) { if (!e.alive) continue; E++; len += e.len; mat += e.len * e.n; if (e.n >= 4) cords += e.len; const aq = Math.abs(e.Q); if (aq > qmax) qmax = aq; u[find(u, e.a)] = find(u, e.b); }
    let V = 0, comps = 0; for (let i = 0; i < N; i++) if (W.na[i] && W.nd[i] > 0) { V++; if (find(u, i) === i) comps++; }
    for (const t of W.tips) if (t.alive) { tips++; deliv += t.I; }
    const iv = W.intervals, n = iv.length; let cv = NaN, mean = NaN; if (n >= 2) { let s = 0, s2 = 0; for (let i = 0; i < n; i++) { s += iv[i]; s2 += iv[i] * iv[i]; } mean = s / n; cv = Math.sqrt(Math.max(0, s2 / n - mean * mean)) / mean; }
    return { t: W.t, len, mat, edges: E, nodes: V, comps, loops: E - V + comps, tips, deliv, qmax, cords, withdrawn: W.withdrawn, grown: W.grown, recycled: W.recycled, fusions: W.ev.fuse, branches: W.ev.branch, fruits: W.fruits.length, fruitStarts: W.ev.fruit, cv, cvN: n, ivMean: mean }; }
  /* effective conductance between two blocks: unit current in at one, out at the other, no leaks. 0 if they are not joined. */
  function conductance(W, A, B, tol, po) { const N = W.nx.length, u = new Int32Array(N); for (let i = 0; i < N; i++) u[i] = i; for (const e of W.edges) if (e.alive) u[find(u, e.a)] = find(u, e.b); if (find(u, A.hub) !== find(u, B.hub)) return 0;
    const rhs = new Float64Array(W.p.length); if (!po || po.length < W.p.length) po = new Float64Array(W.p.length); rhs[A.hub] = 1; rhs[B.hub] = -1; solve(W, tol ? 600 : 4000, tol || 1e-9, true, rhs, po); const dp = po[A.hub] - po[B.hub]; return dp > 0 ? 1 / dp : 0; }
  function efficiency(W, A, B, tol, po) { const G = conductance(W, A, B, tol, po); if (!G) return 0; let mat = 0; for (const e of W.edges) if (e.alive) mat += e.len * e.n; const d = Math.hypot(A.x - B.x, A.y - B.y); return G * d * d / (P.kap * mat); }
  /* the path between two blocks whose thinnest strand is thickest; ties go to the shorter */
  function widest(W, A, B) { const N = W.nx.length, adj = new Array(N); for (const e of W.edges) { if (!e.alive) continue; (adj[e.a] || (adj[e.a] = [])).push(e); (adj[e.b] || (adj[e.b] = [])).push(e); }
    const bn = new Float64Array(N).fill(-1), ln = new Float64Array(N).fill(Infinity), done = new Uint8Array(N); bn[A.hub] = 99; ln[A.hub] = 0;
    for (;;) { let b = -1; for (let i = 0; i < N; i++) if (!done[i] && bn[i] >= 0 && (b < 0 || bn[i] > bn[b] || (bn[i] === bn[b] && ln[i] < ln[b]))) b = i; if (b < 0) return null; if (b === B.hub) return { thinnest: bn[b], length: ln[b] }; done[b] = 1;
      for (const e of adj[b] || []) { const o = e.a === b ? e.b : e.a, w = Math.min(bn[b], e.n), l = ln[b] + e.len; if (!done[o] && (w > bn[o] || (w === bn[o] && l < ln[o]))) { bn[o] = w; ln[o] = l; } } } }

  const api = { P, rng, sm, create, step, runTo, solve, stats, addBlock, cut, conductance, efficiency, widest, moistGrow, moistFruit, act, edge, inBlock, distBlock, CANDIDATE_CV: 1 / (2 * Math.PI) };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; root.MYC = api;
})(typeof window !== 'undefined' ? window : globalThis);
