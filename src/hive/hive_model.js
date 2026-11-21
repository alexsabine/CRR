/* The hive: the model, with no drawing.
   Bee biology is from the literature (see About on the page). The only thing taken from CRR is the timing form:
   a non-negative count since the last event, a fixed threshold, a restart, and a memory built only from the past.
   Every constant in SET is a setting of this model, not a measured property of bees, unless a comment says otherwise. */
(function (root) {
'use strict';
const TASKS = ['tend', 'receive', 'build', 'fan', 'guard', 'forage', 'rest'], TEND = 0, RECV = 1, BUILD = 2, FAN = 3, GUARD = 4, FORAGE = 5, REST = 6;
const SQ3 = Math.sqrt(3), TAU = Math.PI * 2, RAD = Math.PI / 180;
const SET = {
  N: 120,                 /* bees */
  PITCH: 34,              /* cell width in picture units; a bee is about 2.1 cells long, as in life (5.4 mm cells, 12 to 13 mm workers) */
  BEE: 70,
  /* task switching: a count of excess stimulus against the bee's own threshold */
  C_STAR: 1, RATE: 0.1, LEAK: 40, REST: 0.12, MEET: 0.25,
  /* foraging */
  EXPECT: 0.8,            /* profit below this counts as shortfall */
  AB_STAR: 1.5,           /* shortfall count at which a forager abandons her patch */
  K_MEM: 0.5,             /* gain of the forager's own running estimate of her patch */
  MAX_RUNS: 8, DANCE_MIN: 0.4, WAIT_MAX: 12,
  FOLLOW_RUNS: 3, FOLLOW_RATE: 0.25, SCOUT_RATE: 1 / 120,
  RUN_AZ_SD: 8, RUN_D_SD: 0.08,       /* scatter of a dancer's own runs (degrees, fraction) */
  REC_AZ_SD: 10, REC_D_SD: 0.12,      /* extra error of a recruit reading the dance */
  CATCH_AZ: 14, CATCH_D: 0.3, SCOUT_AZ: 22, SCOUT_D: 0.45,
  SEC_PER_KM: 1.0,        /* waggle duration: about one second per kilometre (Seeley 1995; rounded) */
  SUN_AZ: -22,
  MAP_TAU: 60,            /* forgetting time of the colony's forage map */
  /* comb */
  WAX_TIME: 20, DEPOSITS: 4, JITTER: 0.075, FLOW: 1.0, ROUND_TAU: 25,
  /* defence */
  ALARM_TAU: 12, ALARM_HOLD: 0.8, MOB_STAR: 60,
  /* brood, heat */
  HUNGER_TIME: 90, T_SET: 35, T_FAIR: 35.4, T_HOT: 38.6, T_RAIN: 34.6, FAN_COOL: 0.4
};
const GEO = { W: 1600, H: 1000, x0: 130, y0: 112, open: { x: 930, y: 662, w: 580, h: 262 }, floor: { x: 1190, y: 385, r: 200 }, exit: { x: 1215, y: 618 }, horizon: 0.40, D0: 300 };
const SPECIES = [
  { name: 'dandelion', petal: '#f3c52e', heart: '#d98a12', pollen: '#e8922a', sugar: 0.55 },
  { name: 'phacelia', petal: '#8478d8', heart: '#4b3f9e', pollen: '#3f4ea6', sugar: 0.9 },
  { name: 'white clover', petal: '#f6f1e6', heart: '#dba9b4', pollen: '#8d6b38', sugar: 0.7 },
  { name: 'knapweed', petal: '#c0589f', heart: '#7a2f68', pollen: '#e9dfc2', sugar: 0.8 }
];
const clamp = (v, a, b) => v < a ? a : v > b ? b : v;
function mulberry(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function gauss(r) { let u = 0; while (u === 0) u = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(TAU * r()); }

/* where a point of the meadow falls in the picture: bearing az (degrees), ground distance d (m), height h */
function proj(az, d, h) { const o = GEO.open, s = GEO.D0 / (GEO.D0 + d), yh = o.y + o.h * GEO.horizon, cx = o.x + o.w / 2;
  return { x: cx + (az / 58) * (o.w / 2) * (1 - 0.7 * s), y: yh + (o.y + o.h - yh) * s - (h || 0) * s, s }; }

/* ---------- comb ---------- */
function yBottom(x) { const L = 880 - 0.00085 * (x - 500) * (x - 500), k = clamp((x - 840) / 80, 0, 1), s = k * k * (3 - 2 * k); return L * (1 - s) + 600 * s; }
function yBuilt0(x) { return x < 880 ? 585 + 22 * Math.sin(x / 70) + 14 * Math.sin(x / 23 + 1) : 1e9; }
function circum(a, b, c) { const d = 2 * (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y)) || 1e-9, a2 = a.x * a.x + a.y * a.y, b2 = b.x * b.x + b.y * b.y, c2 = c.x * c.x + c.y * c.y;
  return { x: (a2 * (b.y - c.y) + b2 * (c.y - a.y) + c2 * (a.y - b.y)) / d, y: (a2 * (c.x - b.x) + b2 * (a.x - c.x) + c2 * (b.x - a.x)) / d }; }
function buildComb(W, empty) {
  const P = SET.PITCH, rh = P * SQ3 / 2, R = P / SQ3, r = W.rnd, cells = [], grid = {};
  for (let row = 0; row < 28; row++) for (let c = 0; c < 40; c++) { const lx = GEO.x0 + P * (c + 0.5 * (row & 1)), ly = GEO.y0 + row * rh;
    if (ly > yBottom(lx) || lx > 1482) continue;
    const cell = { id: cells.length, c, r: row, lx, ly, x: lx + gauss(r) * P * SET.JITTER, y: ly + gauss(r) * P * SET.JITTER, built: 1, kind: 'honey', fill: 0, capped: false, ripe: 0, born: -1e9, hunger: 0, larva: false, col: 0, rho: 0, nb: [], J: [-1, -1, -1, -1, -1, -1], claim: -1, tone: r() };
    grid[row + ',' + c] = cell.id; cells.push(cell); }
  const at = (row, c) => { const v = grid[row + ',' + c]; return v === undefined ? -1 : v; };
  for (const q of cells) { const o = q.r & 1; q.nb = [at(q.r, q.c + 1), at(q.r + 1, q.c + o), at(q.r + 1, q.c - 1 + o), at(q.r, q.c - 1), at(q.r - 1, q.c - 1 + o), at(q.r - 1, q.c + o)]; }
  /* contents: brood in the middle, a band of pollen round it, honey beyond (the usual pattern; Camazine 1991) */
  const fl = GEO.floor;
  for (const q of cells) { const e = ((q.lx - 600) / 330) ** 2 + ((q.ly - 360) / 185) ** 2;
    if (empty ? q.ly > 200 : q.ly > yBuilt0(q.lx)) { q.built = 0; q.rho = 1; continue; }
    if (e < 1) { q.kind = 'brood'; if (r() < 0.62) q.capped = true; else { q.larva = true; q.hunger = r() * 0.6; } }
    else if (e < 1.5) { q.kind = 'pollen'; q.fill = 0.25 + 0.75 * r(); q.col = Math.floor(r() * SPECIES.length); }
    else { if (q.ly < 185 + 30 * r()) { q.fill = 1; q.capped = true; } else if (Math.hypot(q.lx - fl.x, q.ly - fl.y) < 175) q.fill = r() < 0.5 ? 0 : r() * 0.3; else { q.fill = clamp(r() * 1.35, 0, 1); if (q.fill >= 1 && r() < 0.7) q.capped = true; } }
  }
  /* junctions: one for each three mutually adjacent cells */
  const J = [], jmap = {}, pair = {};
  for (const q of cells) for (let k = 0; k < 6; k++) { const a = q.nb[k], b = q.nb[(k + 1) % 6]; if (a < 0 || b < 0) continue;
    const ids = [q.id, a, b].sort((m, n) => m - n), key = ids.join(','); let j = jmap[key];
    if (j === undefined) { const p = circum(cells[ids[0]], cells[ids[1]], cells[ids[2]]); j = jmap[key] = J.length; J.push({ id: j, x: p.x, y: p.y, cells: ids, nb: [], live: false, born: -1e9, dev0: -1 });
      for (const pr of [[ids[0], ids[1]], [ids[1], ids[2]], [ids[0], ids[2]]]) (pair[pr.join(',')] = pair[pr.join(',')] || []).push(j); }
    q.J[k] = j; }
  for (const k in pair) { const p = pair[k]; if (p.length === 2) { J[p[0]].nb.push(p[1]); J[p[1]].nb.push(p[0]); } }
  W.cells = cells; W.junc = J;
  for (const j of J) j.live = j.cells.every(i => cells[i].built >= 1);
  if (!empty) for (let i = 0; i < 500; i++) relax(W, 0.25);       /* the old comb has long since settled */
  for (const j of J) if (j.live) j.dev0 = -1;
  W.larvae = cells.filter(q => q.larva).map(q => q.id);
  frontier(W);
}
function juncAngles(W, j) { const J = W.junc, a = j.nb.map(n => Math.atan2(J[n].y - j.y, J[n].x - j.x)).sort((p, q) => p - q); return [a[1] - a[0], a[2] - a[1], TAU - (a[2] - a[0])].map(v => v / RAD); }
const juncFree = (W, j) => j.live && j.nb.length === 3 && W.junc[j.nb[0]].live && W.junc[j.nb[1]].live && W.junc[j.nb[2]].live;
function juncDev(W, j) { const a = juncAngles(W, j); return (Math.abs(a[0] - 120) + Math.abs(a[1] - 120) + Math.abs(a[2] - 120)) / 3; }
/* warm wax flows: each free junction moves along the net pull of its three walls (equal line tensions). At rest the three walls meet at 120 degrees (Plateau). */
function relax(W, step) { const J = W.junc; for (const j of J) { if (!juncFree(W, j)) continue; let fx = 0, fy = 0;
    for (const n of j.nb) { const dx = J[n].x - j.x, dy = J[n].y - j.y, d = Math.hypot(dx, dy) || 1; fx += dx / d; fy += dy / d; }
    j.x += fx * step; j.y += fy * step; } }
function frontier(W) { const F = []; for (const q of W.cells) { if (q.built >= 1) continue; let n = 0; for (const k of q.nb) if (k >= 0 && W.cells[k].built >= 1) n++; if (n >= 2 || (q.r === 0)) F.push(q.id); } W.front = F; }
function finishCell(W, q) { q.built = 1; q.rho = 1; q.born = W.t; for (const k of q.J) { if (k < 0) continue; const j = W.junc[k]; if (!j.live && j.cells.every(i => W.cells[i].built >= 1)) { j.live = true; j.born = W.t; j.dev0 = -1; } } frontier(W); W.ev.push({ k: 'cell', x: q.x, y: q.y }); }
function junctionStats(W, minAge) { let s = 0, n = 0, s0 = 0, n0 = 0; for (const j of W.junc) { if (!juncFree(W, j)) continue; if (minAge !== undefined && (j.born < -1e8 || W.t - j.born < minAge)) continue; s += juncDev(W, j); n++; if (j.dev0 >= 0) { s0 += j.dev0; n0++; } } return { n, dev: n ? s / n : null, n0, dev0: n0 ? s0 / n0 : null }; }

/* ---------- flowers ---------- */
function newPatch(W, o) { const r = W.rnd; o = o || {}; let az, d, tries = 0;
  do { az = -48 + 96 * r(); d = 350 + 1350 * r(); tries++; } while (tries < 40 && W.patches.some(p => p.on && Math.abs(p.az - az) < 26 && Math.abs(p.d - d) / d < 0.45));
  const used = W.patches.filter(p => p.on).map(p => p.sp); let sp = Math.floor(r() * SPECIES.length), g = 0; while (used.includes(sp) && g++ < 8) sp = (sp + 1) % SPECIES.length;
  const p = { id: W.pid++, on: true, az: o.az !== undefined ? o.az : az, d: o.d || d, sp: o.sp !== undefined ? o.sp : sp, sugar: 0, bloom: 0, crop: 0, cap: 10, born: W.t - (o.age || 0), life: o.life || (220 + 240 * r()), flowers: [] };
  p.sugar = o.sugar !== undefined ? o.sugar : SPECIES[p.sp].sugar;
  for (let i = 0; i < 70; i++) p.flowers.push({ da: gauss(r) * 7, dd: gauss(r) * 0.16, ph: r() * TAU, sz: 0.75 + 0.5 * r(), dl: r() * 0.5 });
  W.patches.push(p); return p; }
function stepPatches(W, dt) { for (const p of W.patches) { if (!p.on) continue; const age = W.t - p.born;
    p.bloom = W.opt.autoBloom ? clamp(Math.min(age / 30, (p.life - age) / 60), 0, 1) : clamp(age / 30 + 1, 0, 1);
    p.crop = Math.min(p.cap * p.bloom, p.crop + p.bloom * dt);
    if (W.opt.autoBloom && age > p.life) { p.on = false; W.nextBloom = W.t + 10 + 30 * W.rnd(); } }
  if (W.opt.autoBloom) { const on = W.patches.filter(p => p.on).length; if (on < 3 && W.t >= W.nextBloom) { newPatch(W); W.nextBloom = W.t + 20; } }
  if (W.patches.length > 12) W.patches = W.patches.filter(p => p.on || W.t - p.born - p.life < 30); }
/* the button: a rich new bloom somewhere else; the poorest patch begins to fade */
function bloom(W) { const on = W.patches.filter(p => p.on); if (on.length >= 3) { on.sort((a, b) => a.sugar * a.bloom - b.sugar * b.bloom); const p = on[0], age = W.t - p.born; if (p.life - age > 60) p.life = age + 60; } const p = newPatch(W, { sugar: 0.95, life: 360 }); W.nextBloom = W.t + 30; return p; }
const patchById = (W, id) => { for (const p of W.patches) if (p.id === id) return p; return null; };
function nearPatch(W, az, d, daz, dd) { let best = null, bs = 1e9; for (const p of W.patches) { if (!p.on || p.bloom < 0.2) continue; const a = Math.abs(p.az - az) / daz, b = Math.abs(p.d - d) / p.d / dd; if (a < 1 && b < 1 && a + b < bs) { bs = a + b; best = p; } } return best; }

/* ---------- bees ---------- */
function newBee(W, i) { const r = W.rnd, a = (i + r()) / SET.N, n = () => Math.exp(0.3 * gauss(r));
  const th = [(0.12 + 2.2 * a * a) * n(), (0.25 + 12 * (a - 0.45) ** 2) * n(), (0.3 + 12 * (a - 0.4) ** 2) * n(), (0.7 + Math.abs(a - 0.55)) * n(), (0.45 + 6 * (a - 0.6) ** 2) * n(), (0.15 + 5 * (1 - a) ** 2) * n()];
  const k = i % 6, task = a > 0.62 ? FORAGE : a < 0.3 ? TEND : a > 0.56 && k < 4 ? GUARD : k === 0 ? RECV : k === 1 || k === 2 ? BUILD : REST;
  const b = { id: i, age: a, th, C: [0, 0, 0, 0, 0, 0, 0], task, st: 'new', mode: 'walk', x: 200 + 1100 * r(), y: 160 + 400 * r(), hd: r() * TAU, v: 0, t: 0, tx: 0, ty: 0, gait: r() * 9,
    last: -1, patch: -1, m: null, Cab: 0, load: 0, pol: -1, wait: 0, recv: null, dance: null, fol: null, trip: null, o: null, wax: r(), Cg: 0, cell: -1, slot: 0, fan: 0, s: 1, wag: 0, trem: 0 };
  if (task === FORAGE) { b.x = GEO.floor.x + (r() - 0.5) * 240; b.y = GEO.floor.y + (r() - 0.5) * 240; }
  return b; }
function walk(b, tx, ty, sp, dt) { const dx = tx - b.x, dy = ty - b.y, d = Math.hypot(dx, dy); if (d < 3) { b.v = 0; return true; }
  const want = Math.atan2(dy, dx); let da = want - b.hd; da = Math.atan2(Math.sin(da), Math.cos(da)); b.hd += clamp(da, -7 * dt, 7 * dt);
  const v = sp * Math.max(0.15, Math.cos(da)) * Math.min(1, d / 14 + 0.3); b.x += Math.cos(b.hd) * v * dt; b.y += Math.sin(b.hd) * v * dt; b.v = v; b.gait += v * dt * 0.42; return d < 9; }
function face(b, ang, dt) { let da = ang - b.hd; da = Math.atan2(Math.sin(da), Math.cos(da)); b.hd += clamp(da, -5 * dt, 5 * dt); }
function setTask(W, b, j) { if (b.last >= 0) { W.intervals.push(W.t - b.last); if (W.intervals.length > 600) W.intervals.shift(); } b.last = W.t; W.switchT.push(W.t); W.nSwitch++; W.ev.push({ k: 'switch', from: b.task, to: j });
  if (b.cell >= 0) { W.cells[b.cell].claim = -1; b.cell = -1; } if (b.recv) { b.recv.recv = null; b.recv = null; }
  b.task = j; b.C = [0, 0, 0, 0, 0, 0, 0]; b.st = 'new'; b.mode = 'walk'; b.patch = -1; b.m = null; b.Cab = 0; b.dance = null; b.fol = null; b.fan = 0; b.Cg = 0; }
const canSwitch = b => b.mode !== 'out' && b.mode !== 'fly' && (b.task !== FORAGE || ((b.st === 'idle' || b.st === 'new') && b.patch < 0)) && !(b.task === RECV && (b.st === 'xfer' || b.st === 'carry' || b.st === 'put'));

function stimuli(W) { const n = [0, 0, 0, 0, 0, 0, 0]; for (const b of W.bees) n[b.task]++; W.n = n;
  let h = 0, nl = 0, full = 0, nh = 0; for (const q of W.cells) { if (q.built < 1) continue; if (q.larva) { h += q.hunger; nl++; } else if (q.kind === 'honey') { full += q.fill; nh++; } }
  W.fullness = nh ? full / nh : 0; let waiting = 0, unmet = 0; for (const b of W.bees) if (b.st === 'wait') { waiting++; if (!b.recv) unmet++; } W.waiting = waiting;
  /* each stimulus is a real state of the hive that the matching work brings down */
  const s = W.stim; s[TEND] = Math.min(2, 2 * (nl ? h / nl : 0));                       /* hungry brood */
  s[RECV] = Math.min(2, unmet / 2 + W.tremble);                                         /* loaded foragers nobody has met, and tremble dances */
  s[BUILD] = W.front.length ? clamp((W.fullness - 0.4) / 0.25, 0, 1.5) * Math.max(0, 1 - n[BUILD] / 16) : 0;   /* stores filling up while there is room to build */
  s[FAN] = clamp((W.temp - SET.T_SET) / 1.5, 0, 2);                                     /* heat above the brood-nest set point */
  s[GUARD] = Math.min(2.5, 0.8 * Math.max(0, 1 - n[GUARD] / 4) + W.alarm);              /* an unguarded door, and alarm scent */
  s[FORAGE] = W.weather === 'rain' ? 0 : (0.6 + 0.6 * (1 - W.fullness)) * Math.max(0, 1 - n[FORAGE] / (0.42 * SET.N)); }
/* The response of a bee with threshold th to a stimulus s (Bonabeau, Theraulaz & Deneubourg 1996). */
const resp = (s, th) => s * s / (s * s + th * th);
/* The timing rule. For each other task she counts how far its call on her exceeds the call of what she is doing now.
   She meets stimuli by chance, so the count rises in steps. At C_STAR she switches and every count restarts.
   A finished piece of work also restarts her counts: it is unmet stimulus that she counts.
   Bonabeau's model turns the same response into a probability of switching per unit time; here it is integrated to a threshold instead. */
function decide(W, b, dt) { if (!canSwitch(b)) return; const s = W.stim, base = b.task === REST ? SET.REST : resp(s[b.task], b.th[b.task]), meet = W.rnd() < SET.MEET; let go = -1, top = 0;
  for (let j = 0; j < 7; j++) { if (j === b.task) continue; const L = (j === REST ? SET.REST : resp(s[j], b.th[j])) - base; if (L > 0) { if (meet) b.C[j] += L * SET.RATE * dt / SET.MEET; } else b.C[j] *= 1 - dt / SET.LEAK; if (b.C[j] >= SET.C_STAR && b.C[j] > top) { top = b.C[j]; go = j; } }
  if (go >= 0) setTask(W, b, go); }
const acted = b => { const C = b.C; C[0] = C[1] = C[2] = C[3] = C[4] = C[5] = C[6] = 0; };
function stepRest(W, b, dt) { if (b.st === 'new') { b.st = 'rest'; b.t = 0; b.tx = b.x; b.ty = b.y; }
  if ((b.t -= dt) <= 0) { b.t = 4 + 10 * W.rnd(); if (W.rnd() < 0.6) { const q = W.cells[Math.floor(W.rnd() * W.cells.length)]; if (q.built >= 1 && Math.hypot(q.x - b.x, q.y - b.y) < 260) { b.tx = q.x; b.ty = q.y; } } }
  walk(b, b.tx, b.ty, 14, dt); }

function pickCell(W, b, ok, n) { let best = -1, bs = 1e9; const C = W.cells; for (let i = 0; i < n; i++) { const q = C[Math.floor(W.rnd() * C.length)]; if (q.built < 1 || q.claim >= 0 || !ok(q)) continue; const sc = Math.hypot(q.x - b.x, q.y - b.y) * (0.6 + 0.8 * W.rnd()); if (sc < bs) { bs = sc; best = q.id; } } return best; }
const wander = (W, b, cx, cy, r) => { const a = W.rnd() * TAU, d = Math.sqrt(W.rnd()) * r; b.tx = cx + Math.cos(a) * d; b.ty = cy + Math.sin(a) * d * 0.8; b.t = 1.5 + 3 * W.rnd(); };

function stepTend(W, b, dt) {
  if (b.st === 'new' || b.st === 'seek') { let best = -1, bh = 0.15; for (let i = 0; i < 4; i++) { const q = W.cells[W.larvae[Math.floor(W.rnd() * W.larvae.length)]]; if (!q || q.claim >= 0) continue; const sc = q.hunger - Math.hypot(q.x - b.x, q.y - b.y) / 1500; if (sc > bh) { bh = sc; best = q.id; } }
    if (best >= 0) { b.cell = best; W.cells[best].claim = b.id; b.st = 'go'; } else if (b.st === 'new' || (b.t -= dt) <= 0) { wander(W, b, 600, 360, 300); b.st = 'seek'; } else walk(b, b.tx, b.ty, 22, dt); }
  else if (b.st === 'go') { const q = W.cells[b.cell]; if (walk(b, q.x - Math.cos(b.hd) * 18, q.y - Math.sin(b.hd) * 18, 55, dt) || Math.hypot(q.x - b.x, q.y - b.y) < 22) { b.st = 'feed'; b.t = 2; } }
  else if (b.st === 'feed') { const q = W.cells[b.cell]; b.v = 0; if ((b.t -= dt) <= 0) { q.hunger = 0; q.claim = -1; b.cell = -1; b.st = 'seek'; b.t = 0.5; b.tx = b.x; b.ty = b.y; W.nFeeds++; acted(b); } } }

function stepRecv(W, b, dt) { const fl = GEO.floor;
  if (b.st === 'new') { b.st = 'seek'; wander(W, b, fl.x, fl.y, fl.r); }
  if (b.st === 'seek') { let best = null, bd = 1e9; for (const f of W.bees) if (f.st === 'wait' && !f.recv) { const d = Math.hypot(f.x - b.x, f.y - b.y); if (d < bd) { bd = d; best = f; } }
    if (best) { best.recv = b; b.recv = best; b.st = 'meet'; } else { if ((b.t -= dt) <= 0) wander(W, b, fl.x, fl.y, fl.r); walk(b, b.tx, b.ty, 20, dt); } }
  else if (b.st === 'meet') { const f = b.recv; if (!f || f.st !== 'wait') { b.recv = null; b.st = 'seek'; return; } const a = Math.atan2(f.y - b.y, f.x - b.x); if (Math.hypot(f.x - b.x, f.y - b.y) < 62) { b.st = 'xfer'; b.t = 3; f.st = 'xfer'; f.t = 3; f.hd0 = a + Math.PI; } else walk(b, f.x - Math.cos(a) * 56, f.y - Math.sin(a) * 56, 70, dt); }
  else if (b.st === 'xfer') { const f = b.recv; b.v = 0; if (f) face(b, Math.atan2(f.y - b.y, f.x - b.x), dt); if ((b.t -= dt) <= 0) { b.load = f ? f.load : 1; b.recv = null; acted(b); b.cell = pickCell(W, b, q => q.kind === 'honey' && !q.capped && q.fill < 1, 14); if (b.cell >= 0) { W.cells[b.cell].claim = b.id; b.st = 'carry'; } else b.st = 'seek'; } }
  else if (b.st === 'carry') { const q = W.cells[b.cell]; if (walk(b, q.x, q.y + 16, 60, dt) || Math.hypot(q.x - b.x, q.y + 16 - b.y) < 12) { b.st = 'put'; b.t = 2; } }
  else if (b.st === 'put') { b.v = 0; face(b, -Math.PI / 2, dt); if ((b.t -= dt) <= 0) { const q = W.cells[b.cell]; q.fill = Math.min(1, q.fill + 0.2 * b.load); q.claim = -1; b.cell = -1; b.load = 0; b.st = 'seek'; b.t = 0; } } }

function stepBuild(W, b, dt) {
  if (b.st === 'new') b.st = 'hang';
  if (b.st === 'hang') { b.mode = 'hang'; b.wax += dt / SET.WAX_TIME; const g = W.festoon[b.slot] || { x: 480, y: 700, a: -Math.PI / 2 }; const dx = g.x - b.x, dy = g.y - b.y, d = Math.hypot(dx, dy), sp = Math.min(d, 80 * dt); if (d > 0.5) { b.x += dx / d * sp; b.y += dy / d * sp; } b.v = d > 6 ? 60 : 0; if (d > 30) face(b, Math.atan2(dy, dx), dt); else face(b, g.a, dt); if (d > 6) b.gait += 25 * dt;
    if (b.wax >= 1 && W.front.length) { let best = -1, bs = 1e9; for (const id of W.front) { const q = W.cells[id]; if (q.claim >= 0) continue; const sc = Math.hypot(q.lx - b.x, q.ly - b.y) * 0.3 * (0.5 + W.rnd()) + q.ly * 1.6 - q.built * 60; if (sc < bs) { bs = sc; best = id; } } if (best >= 0) { b.cell = best; W.cells[best].claim = b.id; b.st = 'lay'; b.mode = 'walk'; } } }
  else if (b.st === 'lay') { const q = W.cells[b.cell]; if (walk(b, q.x, q.y - 14, 55, dt) || Math.hypot(q.x - b.x, q.y - 14 - b.y) < 12) { b.st = 'work'; b.t = 1.6; } }
  else if (b.st === 'work') { b.v = 0; face(b, Math.PI / 2, dt); if ((b.t -= dt) <= 0) { const q = W.cells[b.cell]; q.claim = -1; b.cell = -1; b.wax = 0; W.nWax++; acted(b); W.ev.push({ k: 'wax', x: q.x, y: q.y }); if (q.built < 1) { q.built = Math.min(1, q.built + 1 / SET.DEPOSITS + 1e-6); if (q.built >= 1) finishCell(W, q); } b.st = 'hang'; } } }
/* festoons: short chains of wax-makers hanging head-up beneath the growing edge, each holding the one above */
function layFestoon(W) { const hang = W.bees.filter(b => b.task === BUILD && b.mode === 'hang'); W.festoon = []; if (!hang.length) return;
  let xs = 0, n = 0; const yb = {}; for (const id of W.front) { xs += W.cells[id].lx; n++; } const cx0 = n ? xs / n : 480;
  for (const q of W.cells) if (q.built >= 1) { const k = Math.round(q.lx / 34); if (!(yb[k] > q.ly)) yb[k] = q.ly; }
  const edge = x => (yb[Math.round(x / 34)] || 560) + 14; let i = 0, c = 0; const lens = [3, 2, 4, 3, 2, 3, 4, 2], nc = Math.ceil(hang.length / 3);
  while (i < hang.length) { const xc = clamp(cx0 + (c - (nc - 1) / 2) * 50 + ((c * 37) % 11 - 5), 170, 800), y0 = edge(xc), m = Math.min(lens[c % 8], hang.length - i), sw = Math.sin(W.t * 0.6 + c * 1.7);
    for (let k = 0; k < m; k++, i++) { hang[i].slot = W.festoon.length; W.festoon.push({ x: xc + sw * 2.4 * (k + 1) + ((c * 13 + k * 7) % 9 - 4), y: y0 + 32 + k * 53, a: -Math.PI / 2 + sw * 0.05 * (k + 1) + ((c * 5 + k * 3) % 7 - 3) * 0.035, c, k, m }); } c++; } }
const FAN_SLOT = i => ({ x: 962 + 44 * (i % 12), y: 944 + 14 * Math.floor(i / 12) + ((i * 7) % 3) * 3 });
const GUARD_SLOT = i => i < 4 ? { x: 912, y: 700 + 56 * i } : i < 12 ? { x: 975 + 66 * (i - 4), y: 646 } : { x: 1526, y: 700 + 40 * (i - 12) };
function stepFan(W, b, dt) { if (b.st === 'new') { b.st = 'post'; const used = {}; for (const o of W.bees) if (o.task === FAN && o !== b && o.st !== 'new') used[o.slot] = 1; let i = 0; while (used[i]) i++; b.slot = i; }
  const p = FAN_SLOT(b.slot); if (Math.hypot(p.x - b.x, p.y - b.y) > 8) { walk(b, p.x, p.y, 65, dt); b.fan = 0; } else { b.v = 0; face(b, Math.PI / 2 + ((b.id % 5) - 2) * 0.08, dt); b.fan = 1; if (W.temp > SET.T_SET - 0.4) acted(b); } }
function stepGuard(W, b, dt) { const H = W.hornet;
  if (b.st === 'new') { b.st = 'post'; const used = {}; for (const o of W.bees) if (o.task === GUARD && o !== b && o.st !== 'new') used[o.slot] = 1; let i = 0; while (used[i]) i++; b.slot = i; b.t = 0; }
  const near = H.on && H.phase === 'hawk';
  if (near && (W.alarm > 0.4 || b.hot)) { /* mob it */ b.mode = 'fly'; const a = b.id * 2.4 + W.t * 1.3, tx = H.x + Math.cos(a) * 30, ty = H.y + Math.sin(a) * 22, dx = tx - b.x, dy = ty - b.y, d = Math.hypot(dx, dy), sp = Math.min(d, 300 * dt); if (d > 1) { b.x += dx / d * sp; b.y += dy / d * sp; b.hd = Math.atan2(H.y - b.y, H.x - b.x); } if (d < 60) { H.near++; acted(b); } return; }
  if (b.mode === 'fly') { b.mode = 'walk'; }
  const p = GUARD_SLOT(b.slot % 16); if ((b.t -= dt) <= 0) { b.t = 1 + 2.5 * W.rnd(); b.tx = p.x + (W.rnd() - 0.5) * 34; b.ty = p.y + (W.rnd() - 0.5) * 34; }
  walk(b, b.tx, b.ty, Math.hypot(p.x - b.x, p.y - b.y) > 60 ? 75 : 16, dt); if (b.slot < 4) acted(b);
  if (near) { const d = Math.hypot(H.x - b.x, H.y - b.y); b.Cg += 0.4 * dt / (1 + d / 200);      /* she counts what she sees of the hornet; at 1 she releases alarm scent and goes for it */
    if (b.Cg >= 1) { b.Cg = 0; b.hot = 1; W.alarm += 0.5; W.nAlarm++; W.ev.push({ k: 'alarm', x: b.x, y: b.y }); } } else if (!H.on) { b.Cg = 0; b.hot = 0; } }

function recordRun(W, b) { const D = b.dance, az = D.az + gauss(W.rnd) * SET.RUN_AZ_SD, d = D.d * (1 + gauss(W.rnd) * SET.RUN_D_SD); W.runs.push({ t: W.t, patch: D.patch, az, d, ang: D.runAng, dur: D.dur, taz: D.az, td: D.d }); W.nRuns++;
  const i = clamp(Math.floor((az + 60) / 5), 0, 23), k = clamp(Math.floor(d / 200), 0, 9); W.map[k * 24 + i] += 1;
  for (const f of W.bees) if (f.fol === b) { f.folRuns++; if (f.folRuns >= SET.FOLLOW_RUNS) { f.fol = null; f.trip = { kind: 'recruit', az: az + gauss(W.rnd) * SET.REC_AZ_SD, d: Math.max(120, d * (1 + gauss(W.rnd) * SET.REC_D_SD)) }; f.st = 'toexit'; W.nRecruit++; } } }
function startRun(W, b) { const D = b.dance; D.runAz = D.az; D.runAng = (D.az - SET.SUN_AZ) * RAD + gauss(W.rnd) * 3 * RAD; D.dur = D.d / 1000 * SET.SEC_PER_KM; D.ph = 'w'; D.t = 0; D.side = -D.side; }
function flyable(W) { return W.weather !== 'rain' && W.alarm < SET.ALARM_HOLD; }
function afterTrip(W, b) { /* she is home and unloaded: update her estimate of the patch, count shortfall, then dance, go again or give up */
  const p = patchById(W, b.patch), profit = b.profit; b.load = 0; b.pol = -1;
  if (!p) { b.patch = -1; b.m = null; b.st = 'idle'; return; }
  b.m = b.m === null ? profit : b.m + SET.K_MEM * (profit - b.m);                 /* past-only memory update */
  b.Cab += Math.max(0, SET.EXPECT - profit);                                      /* shortfall count */
  if (b.frac < 0.5) for (const o of W.bees) if (o.st === 'dance' && o.dance.patch === b.patch) { o.dance.left = Math.max(0, o.dance.left - 3); W.nStop++; W.ev.push({ k: 'stop' }); break; }   /* stop signal (Nieh 2010) */
  if (b.Cab >= SET.AB_STAR) { b.Cab = 0; b.patch = -1; b.m = null; b.st = 'idle'; W.nAbandon++; return; }
  const runs = W.opt.dance ? Math.round(SET.MAX_RUNS * clamp((b.m - SET.DANCE_MIN) / (1 - SET.DANCE_MIN), 0, 1) * clamp(1 - b.wait / SET.WAIT_MAX, 0, 1)) : 0;
  if (runs >= 1) { const fl = GEO.floor; b.dance = { left: runs, patch: p.id, az: p.az, d: p.d, side: 1, cx: clamp(b.x, fl.x - 150, fl.x + 150), cy: clamp(b.y, fl.y - 120, fl.y + 120), ph: 'go', t: 0 }; b.st = 'dance'; W.nDances++; }
  else { b.trip = { kind: 'work', az: p.az, d: p.d }; b.st = 'toexit'; } }
function stepForage(W, b, dt) { const fl = GEO.floor, ex = GEO.exit, r = W.rnd;
  switch (b.st) {
  case 'new': b.st = 'idle'; wander(W, b, fl.x, fl.y, fl.r); break;
  case 'idle': { if ((b.t -= dt) <= 0) wander(W, b, fl.x, fl.y, fl.r); walk(b, b.tx, b.ty, 22, dt);
    if (b.patch >= 0) { if (flyable(W)) { const p = patchById(W, b.patch); if (p) { b.trip = { kind: 'work', az: p.az, d: p.d }; b.st = 'toexit'; } else b.patch = -1; } break; }
    if (W.opt.dance && W.dancers.length && r() < SET.FOLLOW_RATE * dt) { b.fol = W.dancers[Math.floor(r() * W.dancers.length)]; b.folRuns = 0; b.st = 'follow'; b.side = (r() - 0.5) * 2; }
    else if (flyable(W) && r() < SET.SCOUT_RATE * dt) { b.trip = { kind: 'scout', az: -50 + 100 * r(), d: 300 + 1500 * r() }; b.st = 'toexit'; W.nScout++; } break; }
  case 'follow': { const d = b.fol; if (!d || d.st !== 'dance') { b.fol = null; b.st = 'idle'; b.t = 0; break; } const a = d.hd + Math.PI + b.side * 0.9, tx = d.x + Math.cos(a) * 52, ty = d.y + Math.sin(a) * 52; walk(b, tx, ty, 75, dt); if (Math.hypot(tx - b.x, ty - b.y) < 16) face(b, Math.atan2(d.y - b.y, d.x - b.x), dt * 3); break; }
  case 'toexit': if (!flyable(W)) { b.st = 'idle'; if (b.trip && b.trip.kind !== 'work') b.trip = null; b.t = 0; break; } if (walk(b, ex.x + (b.id % 7 - 3) * 14, ex.y, 85, dt)) { b.st = 'out'; b.mode = 'out'; b.o = { u: 0, T: 3 + b.trip.d / 200, x0: b.x, y0: b.y, ph: r() * TAU }; W.nTrips++; } break;
  case 'out': b.o.u += dt / b.o.T; if (b.o.u >= 1) { b.o.u = 1; b.st = 'gather'; b.t = 4 + 2 * r(); } break;
  case 'gather': if ((b.t -= dt) <= 0) { let p = null; if (b.trip.kind === 'work') p = patchById(W, b.patch); else if (b.trip.kind === 'recruit') p = nearPatch(W, b.trip.az, b.trip.d, SET.CATCH_AZ, SET.CATCH_D); else p = nearPatch(W, b.trip.az, b.trip.d, SET.SCOUT_AZ, SET.SCOUT_D);
      if (p && p.on) { if (b.trip.kind !== 'work') { if (b.trip.kind === 'recruit') W.nRecruitOk++; else W.nScoutOk++; b.patch = p.id; b.m = null; b.Cab = 0; b.trip.az = p.az; b.trip.d = p.d; }
        const f = Math.min(1, p.crop); p.crop -= f; b.frac = f; b.load = f; b.profit = clamp(p.sugar * f - 0.06 * p.d / 1000, 0, 1); b.pol = r() < 0.25 ? p.sp : -1; }
      else { b.frac = 0; b.load = 0; b.profit = 0; if (b.trip.kind !== 'work') b.patch = -1; }
      b.st = 'back'; } break;
  case 'back': b.o.u -= dt / b.o.T; if (b.o.u <= 0) { b.mode = 'walk'; b.x = ex.x + (b.id % 7 - 3) * 14; b.y = ex.y; b.hd = -Math.PI / 2; b.o = null; const a = r() * TAU, d = Math.sqrt(r()) * fl.r * 0.9; b.tx = fl.x + Math.cos(a) * d; b.ty = fl.y + Math.sin(a) * d * 0.8; b.st = 'tofloor'; } break;
  case 'tofloor': if (walk(b, b.tx, b.ty, 85, dt)) { if (b.patch < 0) { b.st = 'idle'; b.t = 0; b.trip = null; } else if (b.pol >= 0) { b.cell = pickCell(W, b, q => q.kind === 'pollen' && q.fill < 0.95, 30); if (b.cell >= 0) { W.cells[b.cell].claim = b.id; b.st = 'pollen'; } else { b.pol = -1; b.wait = 0; b.st = 'wait'; } } else { b.wait = 0; b.st = b.load > 0.02 ? 'wait' : 'done'; } } break;
  case 'pollen': { const q = W.cells[b.cell]; if (walk(b, q.x, q.y + 16, 70, dt) || Math.hypot(q.x - b.x, q.y + 16 - b.y) < 12) { b.v = 0; if (b.pol >= 0) { b.t = 2; b.polc = b.pol; b.pol = -2; } } if (b.pol === -2) { face(b, -Math.PI / 2, dt); if ((b.t -= dt) <= 0) { q.col = b.polc; q.fill = Math.min(1, q.fill + 0.34); q.claim = -1; b.cell = -1; b.pol = -1; W.nPollen++; b.wait = 0; b.st = 'done'; } } break; }
  case 'wait': b.v = 0; b.wait += dt; if (b.wait > SET.WAIT_MAX && b.trem === 0) { b.trem = 1; W.tremble += 0.4; W.nTremble++; }   /* a long wait: she trembles, which calls for receivers (Seeley 1992) */
    if (b.wait > 25) { if (b.recv) { b.recv.recv = null; b.recv.st = 'seek'; b.recv = null; } b.st = 'done'; W.intake.push(W.t); W.loads += b.load; } break;
  case 'xfer': b.v = 0; if (b.hd0 !== undefined) face(b, b.hd0, dt); if ((b.t -= dt) <= 0) { b.recv = null; W.intake.push(W.t); W.loads += b.load; W.waits.push(b.wait); if (W.waits.length > 200) W.waits.shift(); b.st = 'done'; } break;
  case 'done': b.trem = 0; afterTrip(W, b); break;
  case 'dance': { const D = b.dance; if (D.ph === 'go') { if (walk(b, D.cx, D.cy, 70, dt)) startRun(W, b); break; }
    D.t += dt; const ax = Math.sin(D.runAng), ay = -Math.cos(D.runAng), len = Math.max(14, 44 * D.dur), hd = Math.atan2(ay, ax);
    if (D.ph === 'w') { const u = Math.min(1, D.t / D.dur); b.x = D.cx + ax * len * (u - 0.5); b.y = D.cy + ay * len * (u - 0.5); b.wag = Math.sin(W.t * TAU * 14); b.hd = hd + b.wag * 0.22; b.v = 30; b.gait += 30 * dt;
      if (D.t >= D.dur) { b.wag = 0; recordRun(W, b); D.left--; D.ph = 'r'; D.t = 0; } }
    else { const T = 1.5, u = Math.min(1, D.t / T), th = Math.PI * u, rr = len / 2 + 14, px = -ay * D.side, py = ax * D.side;                    /* the return loop, alternately to either side */
      b.x = D.cx + ax * (len / 2) * Math.cos(th) + px * rr * Math.sin(th) * 0.9; b.y = D.cy + ay * (len / 2) * Math.cos(th) + py * rr * Math.sin(th) * 0.9;
      const tx = -ax * Math.sin(th) + px * Math.cos(th) * 1.8, ty = -ay * Math.sin(th) + py * Math.cos(th) * 1.8; face(b, Math.atan2(ty, tx), dt * 3); b.v = 50; b.gait += 50 * dt;
      if (D.t >= T) { if (D.left > 0) startRun(W, b); else { b.dance = null; const p = patchById(W, b.patch); if (p) { b.trip = { kind: 'work', az: p.az, d: p.d }; b.st = 'toexit'; } else { b.patch = -1; b.st = 'idle'; } } } }
    break; }
  }
  if (b.mode === 'out') { const o = b.o, tr = b.trip, e = o.u * o.u * (3 - 2 * o.u), d = tr.d * e, hov = b.st === 'gather' ? 1 : 0, P = proj(tr.az * Math.min(1, e * 1.6) + hov * 2.2 * Math.sin(W.t * 1.7 + o.ph), d * (1 + hov * 0.03 * Math.sin(W.t * 1.1 + o.ph)), 26 + 60 * Math.sin(Math.PI * e) * (1 - hov) + hov * 10 * Math.sin(W.t * 2.3 + o.ph) + 6 * Math.sin(W.t * 5 + o.ph));
    const k = Math.min(1, o.u * 9), nx = o.x0 + (P.x - o.x0) * k, ny = o.y0 + (P.y - o.y0) * k; const vx = nx - b.x, vy = ny - b.y; if (Math.abs(vx) + Math.abs(vy) > 0.05) b.hd = Math.atan2(vy, vx); b.x = nx; b.y = ny; b.s = 1 + (P.s - 1) * k; } else b.s = 1;
}

function stepHornet(W, dt) { const H = W.hornet; if (!H.on) return; H.t += dt; const o = GEO.open, hx = o.x + o.w * 0.5, hy = o.y + o.h * 0.6;
  if (H.phase === 'in') { const u = Math.min(1, H.t / 4), e = u * u * (3 - 2 * u), P = proj(H.az * (1 - e), 900 * (1 - e) * (1 - e), 40); H.x = P.x + (hx - P.x) * e * e; H.y = P.y + (hy - P.y) * e * e; H.s = P.s + (1 - P.s) * e; if (u >= 1) { H.phase = 'hawk'; H.t = 0; } }
  else if (H.phase === 'hawk') { const nx = hx + Math.sin(H.t * 0.9) * o.w * 0.3 + Math.sin(H.t * 2.3) * 22, ny = hy + Math.sin(H.t * 1.8) * o.h * 0.2; H.hd = Math.atan2(ny - H.y, nx - H.x); H.x = nx; H.y = ny; H.s = 1;
    H.C += H.near * dt; H.mob = H.near; H.near = 0;                                        /* bee-seconds of mobbing */
    if (H.C >= SET.MOB_STAR) { H.phase = 'flee'; H.t = 0; H.x0 = H.x; H.y0 = H.y; W.ev.push({ k: 'gone' }); W.hornetLog.push({ came: H.t0, left: W.t }); } }
  else { const u = Math.min(1, H.t / 3.5), e = u * u, P = proj(H.az, 1400 * e, 60); H.x = H.x0 + (P.x - H.x0) * e; H.y = H.y0 + (P.y - H.y0) * Math.sqrt(u); H.s = 1 + (P.s - 1) * e; H.hd = Math.atan2(P.y - H.y0, P.x - H.x0); if (u >= 1) { H.on = false; for (const b of W.bees) if (b.task === GUARD) { b.Cg = 0; b.hot = 0; b.mode = 'walk'; } } } }
function sendHornet(W) { const H = W.hornet; if (H.on) return false; Object.assign(H, { on: true, phase: 'in', t: 0, t0: W.t, C: 0, near: 0, mob: 0, az: (W.rnd() - 0.5) * 70, x: 0, y: 0, s: 0.2, hd: 0 }); return true; }

function create(seed, opt) { const W = { t: 0, rnd: mulberry(seed || 1), opt: Object.assign({ dance: true, autoBloom: true, flow: true, empty: false, patches: null }, opt || {}), bees: [], patches: [], pid: 0, weather: 'fair', temp: 35.2, alarm: 0, tremble: 0, stim: [0, 0, 0, 0, 0, 0, 0], n: [0, 0, 0, 0, 0, 0, 0], ev: [], intervals: [], switchT: [], intake: [], waits: [], runs: [], map: new Float32Array(240), festoon: [], dancers: [], hornet: { on: false }, hornetLog: [], nextBloom: 0, acc: 0, loads: 0,
    nSwitch: 0, nFeeds: 0, nWax: 0, nRuns: 0, nDances: 0, nRecruit: 0, nRecruitOk: 0, nScout: 0, nScoutOk: 0, nAbandon: 0, nStop: 0, nTremble: 0, nTrips: 0, nPollen: 0, nAlarm: 0, fullness: 0, waiting: 0 };
  buildComb(W, W.opt.empty);
  if (W.opt.patches) for (const p of W.opt.patches) newPatch(W, p); else { newPatch(W, { age: 60 }); newPatch(W, { age: 150 }); newPatch(W, { age: 20 }); }
  for (let i = 0; i < SET.N; i++) W.bees.push(newBee(W, i));
  stimuli(W); return W; }

function step(W, dt) { W.t += dt; const B = W.bees;
  stepPatches(W, dt); stepHornet(W, dt);
  W.dancers.length = 0; for (const b of B) if (b.st === 'dance' && b.dance.ph !== 'go') W.dancers.push(b);
  for (const b of B) { switch (b.task) { case TEND: stepTend(W, b, dt); break; case RECV: stepRecv(W, b, dt); break; case BUILD: stepBuild(W, b, dt); break; case FAN: stepFan(W, b, dt); break; case GUARD: stepGuard(W, b, dt); break; case REST: stepRest(W, b, dt); break; default: stepForage(W, b, dt); } }
  /* walkers keep a little apart, and stay inside the hive */
  for (let i = 0; i < B.length; i++) { const a = B[i]; if (a.mode !== 'walk' || a.st === 'dance') continue; for (let k = i + 1; k < B.length; k++) { const c = B[k]; if (c.mode !== 'walk') continue; const dx = c.x - a.x, dy = c.y - a.y; if (dx > 40 || dx < -40 || dy > 40 || dy < -40) continue; const d2 = dx * dx + dy * dy; if (d2 < 1444 && d2 > 0.01) { const d = Math.sqrt(d2), p = (38 - d) * 0.5 * Math.min(1, dt * 9); const ux = dx / d * p, uy = dy / d * p; if (c.st !== 'dance') { c.x += ux; c.y += uy; a.x -= ux; a.y -= uy; } else { a.x -= 2 * ux; a.y -= 2 * uy; } } }
    a.x = clamp(a.x, 80, 1535); a.y = clamp(a.y, 96, 968); }
  /* slower things, four times a second */
  W.acc += dt; if (W.acc >= 0.25) { const h = W.acc; W.acc = 0; stimuli(W); for (const b of B) decide(W, b, h); layFestoon(W);
    for (const q of W.cells) { if (q.built < 1) continue; if (q.larva) q.hunger = Math.min(1, q.hunger + h / SET.HUNGER_TIME); else if (q.kind === 'honey' && !q.capped && q.fill >= 1) { q.ripe += h / 45; if (q.ripe >= 1) { q.capped = true; W.ev.push({ k: 'cap', x: q.x, y: q.y }); } } if (q.rho > 0 && W.opt.flow) q.rho = Math.max(0, q.rho - q.rho * h / SET.ROUND_TAU * warm(W)); }
    { const q = W.cells[Math.floor(W.rnd() * W.cells.length)]; if (q.built >= 1 && !q.capped && q.kind === 'honey' && q.fill > 0) q.fill = Math.max(0, q.fill - 0.03); else if (q.kind === 'pollen') q.fill = Math.max(0.05, q.fill - 0.02); }
    const Teq = W.weather === 'hot' ? SET.T_HOT : W.weather === 'rain' ? SET.T_RAIN : SET.T_FAIR; let nf = 0; for (const b of B) if (b.task === FAN && b.fan) nf++; W.fanning = nf; W.temp += (Teq - SET.FAN_COOL * nf - W.temp) * h / 8;
    W.alarm *= Math.exp(-h / SET.ALARM_TAU); W.tremble *= Math.exp(-h / 20); const dk = Math.exp(-h / SET.MAP_TAU); for (let i = 0; i < 240; i++) W.map[i] *= dk;
    for (const j of W.junc) if (j.live && j.dev0 < 0 && juncFree(W, j)) j.dev0 = juncDev(W, j);
    while (W.intake.length && W.intake[0] < W.t - 60) W.intake.shift(); while (W.switchT.length && W.switchT[0] < W.t - 60) W.switchT.shift(); while (W.runs.length && W.runs[0].t < W.t - 60) W.runs.shift();
    if (W.ev.length > 300) W.ev.splice(0, W.ev.length - 300); }
  if (W.opt.flow) relax(W, SET.FLOW * warm(W) * dt); }
/* beeswax softens as it nears 40 C; the bees keep the building comb near brood-nest temperature */
const warm = W => clamp((W.temp - 31) / 4, 0, 1.5);

function cv(xs) { const n = xs.length; if (n < 3) return null; let m = 0; for (const x of xs) m += x; m /= n; let v = 0; for (const x of xs) v += (x - m) * (x - m); return m > 0 ? Math.sqrt(v / (n - 1)) / m : null; }
function measure(W) { let out = 0, emp = {}, ne = 0; for (const b of W.bees) { if (b.mode === 'out') out++; if (b.task === FORAGE && b.patch >= 0) { emp[b.patch] = (emp[b.patch] || 0) + 1; ne++; } }
  const by = {}; for (const r of W.runs) by[r.patch] = (by[r.patch] || 0) + 1; let lead = -1, top = 0; for (const k in by) if (by[k] > top) { top = by[k]; lead = +k; }
  const js = junctionStats(W); let built = 0; for (const q of W.cells) if (q.built >= 1) built++;
  return { t: W.t, foragersOut: out, employed: emp, nEmployed: ne, intake60: W.intake.length, switches60: W.switchT.length, cv: cv(W.intervals), cvN: W.intervals.length, runs60: W.runs.length, lead, consensus: W.runs.length ? top / W.runs.length : null, juncDev: js.dev, juncN: js.n, temp: W.temp, fullness: W.fullness, alarm: W.alarm, n: W.n.slice(), built, cells: W.cells.length, dancers: W.dancers.length }; }
function run(W, sec, dt) { dt = dt || 1 / 30; const n = Math.round(sec / dt); for (let i = 0; i < n; i++) { step(W, dt); if (W.ev.length > 200) W.ev.length = 0; } return W; }

const api = { create, step, run, measure, bloom, junctionStats, juncAngles, juncFree, juncDev, sendHornet, newPatch, patchById, proj, cv, relax, SET, GEO, SPECIES, TASKS, FAN_SLOT, GUARD_SLOT };
if (typeof module !== 'undefined' && module.exports) module.exports = api; root.HIVE = api;
})(typeof window !== 'undefined' ? window : globalThis);
