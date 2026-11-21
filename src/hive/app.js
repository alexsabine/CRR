/* The hive: the picture. Everything drawn here is read from the model in window.HIVE; nothing here changes what the bees do. */
(function () {
'use strict';
const H = window.HIVE, SET = H.SET, GEO = H.GEO, SP = H.SPECIES, O = GEO.open, TAU = Math.PI * 2, RAD = Math.PI / 180, SQ3 = Math.sqrt(3);
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
const $ = id => document.getElementById(id), cv = $('scene'), ctx = cv.getContext('2d');
const clamp = (v, a, b) => v < a ? a : v > b ? b : v, mix = (a, b, t) => a + (b - a) * t;
function rng(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const mk = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };

let W = H.create((Date.now() % 100000) + 1); H.run(W, 50); W.ev.length = 0;
let paused = still, sound = false, view = innerWidth < 700 ? 'floor' : 'hive', quality = 1, cw = 0, ch = 0, dpr = 1, onscreen = true, clock = 0;
const VIEWS = { hive: { x: -10, y: 10, w: 1620, h: 985 }, comb: { x: 205, y: 430, w: 590, h: 390 }, floor: { x: 880, y: 225, w: 670, h: 730 }, meadow: { x: O.x + 6, y: O.y + 4, w: O.w - 12, h: O.h - 10 } };
const cam = { x: 800, y: 500, z: 0.5, moving: true };
function target() { const v = VIEWS[view], z = Math.min(cw / v.w, ch / v.h), vw = cw / z, vh = ch / z; let x = v.x + v.w / 2, y = v.y + v.h / 2;
  if (view !== 'meadow') { x = vw < 1700 ? clamp(x, vw / 2 - 50, 1650 - vw / 2) : 800; y = vh < 1100 ? clamp(y, vh / 2 - 50, 1050 - vh / 2) : 500; } return { x, y, z }; }
function fit() { const r = cv.getBoundingClientRect(); dpr = Math.min(window.devicePixelRatio || 1, innerWidth < 700 ? 1.5 : 2) * quality; cw = r.width; ch = r.height; cv.width = Math.round(cw * dpr); cv.height = Math.round(ch * dpr); stat.width = cv.width; stat.height = cv.height; statT = -1; const t = target(); if (cam.first === undefined) { cam.x = t.x; cam.y = t.y; cam.z = t.z; cam.first = 1; } cam.moving = true; }
const stat = mk(2, 2), sx = stat.getContext('2d'); let statT = -1;
const world = c => c.setTransform(cam.z * dpr, 0, 0, cam.z * dpr, (cw / 2 - cam.x * cam.z) * dpr, (ch / 2 - cam.y * cam.z) * dpr);

/* ---------- things painted once ---------- */
function paintWood() { const c = mk(1600, 1000), g = c.getContext('2d'), r = rng(5);
  g.fillStyle = '#1d130a'; g.fillRect(0, 0, 1600, 1000);
  for (let i = 0; i < 8; i++) { const x = i * 200, gr = g.createLinearGradient(x, 0, x + 200, 0); const b = 22 + r() * 10; gr.addColorStop(0, `rgb(${b + 8},${b * 0.62 + 3 | 0},${b * 0.34 | 0})`); gr.addColorStop(1, `rgb(${b + 18},${b * 0.68 + 6 | 0},${b * 0.38 + 2 | 0})`); g.fillStyle = gr; g.fillRect(x, 0, 199, 1000); }
  for (let i = 0; i < 900; i++) { const x = r() * 1600, y = r() * 1000, l = 60 + r() * 240; g.strokeStyle = r() < 0.5 ? 'rgba(0,0,0,.16)' : 'rgba(190,140,80,.05)'; g.lineWidth = 0.6 + r() * 1.6; g.beginPath(); g.moveTo(x, y); g.bezierCurveTo(x + (r() - 0.5) * 8, y + l / 3, x + (r() - 0.5) * 8, y + 2 * l / 3, x + (r() - 0.5) * 5, y + l); g.stroke(); }
  for (let i = 0; i < 7; i++) { const x = r() * 1600, y = r() * 1000, kr = 8 + r() * 14, gr = g.createRadialGradient(x, y, 1, x, y, kr); gr.addColorStop(0, 'rgba(10,5,2,.7)'); gr.addColorStop(1, 'rgba(10,5,2,0)'); g.fillStyle = gr; g.beginPath(); g.ellipse(x, y, kr * 0.7, kr, 0, 0, TAU); g.fill(); }
  /* the box: walls, top bar, floor */
  const board = (x, y, w, h, vert, base) => { const gr = vert ? g.createLinearGradient(x, 0, x + w, 0) : g.createLinearGradient(0, y, 0, y + h); gr.addColorStop(0, base[0]); gr.addColorStop(0.5, base[1]); gr.addColorStop(1, base[2]); g.fillStyle = gr; g.fillRect(x, y, w, h);
    for (let i = 0; i < w * h / 260; i++) { const px = x + r() * w, py = y + r() * h, l = 30 + r() * 120; g.strokeStyle = r() < 0.6 ? 'rgba(20,10,4,.22)' : 'rgba(230,180,110,.07)'; g.lineWidth = 0.5 + r(); g.beginPath(); if (vert) { g.moveTo(px, py); g.lineTo(px + (r() - 0.5) * 3, Math.min(y + h, py + l)); } else { g.moveTo(px, py); g.lineTo(Math.min(x + w, px + l), py + (r() - 0.5) * 3); } g.stroke(); } };
  const wd = ['#3a2512', '#553a1e', '#3f2914'];
  board(0, 0, 62, 1000, true, wd); board(1538, 0, 62, 1000, true, wd); board(0, 968, 1600, 32, false, ['#4a321a', '#3a2613', '#24170b']); board(0, 0, 1600, 52, false, ['#2c1c0d', '#46301a', '#3a2613']);
  board(62, 52, 1476, 44, false, ['#6a4a26', '#5a3e20', '#33210f']);                                                      /* the bar the comb hangs from */
  let gr = g.createLinearGradient(0, 96, 0, 150); gr.addColorStop(0, 'rgba(0,0,0,.55)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(62, 96, 1476, 54);
  gr = g.createLinearGradient(62, 0, 120, 0); gr.addColorStop(0, 'rgba(0,0,0,.5)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(62, 96, 58, 872);
  /* the frame round the entrance */
  const f = 30; board(O.x - f, O.y - f, O.w + 2 * f, f, false, ['#4a3219', '#5e4222', '#4a3219']); board(O.x - f, O.y + O.h, O.w + 2 * f, f + 14, false, ['#6a4c28', '#523a1e', '#33210f']); board(O.x - f, O.y, f, O.h, true, ['#4a3219', '#5e4222', '#523a1e']); board(O.x + O.w, O.y, f, O.h, true, ['#523a1e', '#5e4222', '#3f2914']);
  g.strokeStyle = 'rgba(0,0,0,.45)'; g.lineWidth = 2; g.strokeRect(O.x - f, O.y - f, O.w + 2 * f, O.h + 2 * f + 14);
  for (let i = 0; i < 26; i++) { const x = 80 + r() * 1440, rr = 3 + r() * 7; g.fillStyle = `rgba(${90 + r() * 50 | 0},${45 + r() * 25 | 0},10,.5)`; g.beginPath(); g.ellipse(x, 96 + r() * 5, rr * 1.6, rr * 0.6, 0, 0, TAU); g.fill(); }   /* propolis */
  return c; }
const wood = paintWood();

const meadows = {};
function paintMeadow(wx) { if (meadows[wx]) return meadows[wx]; const S = 3, c = mk(O.w * S, O.h * S), g = c.getContext('2d'), r = rng(9), w = O.w, h = O.h, yh = h * GEO.horizon; g.scale(S, S);
  const sky = { fair: ['#5d9bd6', '#a9cfee', '#e6f0ee'], hot: ['#8db9de', '#cfe0e6', '#f6ecd2'], rain: ['#5f6b76', '#8a949b', '#b4bcbd'] }[wx];
  let gr = g.createLinearGradient(0, 0, 0, yh); gr.addColorStop(0, sky[0]); gr.addColorStop(0.6, sky[1]); gr.addColorStop(1, sky[2]); g.fillStyle = gr; g.fillRect(0, 0, w, yh + 2);
  const sunx = w / 2 + (SET.SUN_AZ / 58) * (w / 2), suny = h * 0.1;
  if (wx !== 'rain') { gr = g.createRadialGradient(sunx, suny, 2, sunx, suny, wx === 'hot' ? 170 : 120); gr.addColorStop(0, 'rgba(255,252,235,1)'); gr.addColorStop(0.06, 'rgba(255,248,220,.95)'); gr.addColorStop(0.12, 'rgba(255,240,190,.45)'); gr.addColorStop(1, 'rgba(255,240,190,0)'); g.fillStyle = gr; g.fillRect(0, 0, w, yh); }
  const cloud = (x, y, s, col) => { for (let i = 0; i < 9; i++) { const px = x + (r() - 0.5) * 60 * s, py = y + (r() - 0.5) * 10 * s, rr = (10 + r() * 16) * s, q = g.createRadialGradient(px, py - rr * 0.2, 1, px, py, rr); q.addColorStop(0, col + '.75)'); q.addColorStop(1, col + '0)'); g.fillStyle = q; g.beginPath(); g.ellipse(px, py, rr * 1.5, rr * 0.7, 0, 0, TAU); g.fill(); } };
  if (wx === 'rain') { for (let i = 0; i < 16; i++) cloud(r() * w, 6 + r() * 70, 1.6, 'rgba(70,78,88,'); } else for (let i = 0; i < (wx === 'hot' ? 3 : 6); i++) cloud(r() * w, 20 + r() * 55, 0.7 + r() * 0.7, 'rgba(255,255,255,');
  const ridge = (y0, amp, col, k) => { g.fillStyle = col; g.beginPath(); g.moveTo(0, yh + 2); for (let x = 0; x <= w; x += 4) g.lineTo(x, y0 - amp * (0.5 + 0.5 * Math.sin(x * 0.011 * k + k)) - amp * 0.4 * Math.sin(x * 0.031 * k + 2 * k)); g.lineTo(w, yh + 2); g.fill(); };
  const dim = wx === 'rain';
  ridge(yh - 8, 12, dim ? '#7f8d90' : '#9db9c0', 1); ridge(yh - 3, 8, dim ? '#6c7f78' : '#86a996', 1.7);
  for (let x = -4; x < w; x += 3 + r() * 5) { const rr = 2 + r() * 4.5; g.fillStyle = dim ? `rgb(${52 + r() * 12 | 0},${74 + r() * 12 | 0},${60 | 0})` : `rgb(${58 + r() * 22 | 0},${98 + r() * 26 | 0},${62 + r() * 14 | 0})`; g.beginPath(); g.ellipse(x, yh - rr * 0.5, rr * 1.2, rr, 0, 0, TAU); g.fill(); }
  const gc = { fair: ['#c3cf82', '#8fb65a', '#4c8a38'], hot: ['#d9d08c', '#a9b860', '#5f8e3a'], rain: ['#8a9a72', '#64844e', '#38633a'] }[wx];
  gr = g.createLinearGradient(0, yh, 0, h); gr.addColorStop(0, gc[0]); gr.addColorStop(0.3, gc[1]); gr.addColorStop(1, gc[2]); g.fillStyle = gr; g.fillRect(0, yh, w, h - yh);
  for (let i = 0; i < 90; i++) { const s = Math.pow(r(), 1.6), y = yh + (h - yh) * s, x = r() * w; g.fillStyle = r() < 0.5 ? 'rgba(250,240,150,.08)' : 'rgba(20,70,30,.09)'; g.beginPath(); g.ellipse(x, y, (40 + r() * 80) * (0.15 + s), (3 + r() * 6) * (0.15 + s), 0, 0, TAU); g.fill(); }
  for (let i = 0; i < 7000; i++) { const s = Math.pow(r(), 1.3), y = yh + (h - yh) * s, x = r() * w, l = 1 + 9 * s; g.strokeStyle = r() < 0.55 ? `rgba(28,78,30,${0.12 + 0.2 * s})` : `rgba(215,225,130,${0.1 + 0.16 * s})`; g.lineWidth = 0.25 + 0.7 * s; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (r() - 0.5) * 3 * s, y - l); g.stroke(); }
  for (let i = 0; i < 500; i++) { const s = Math.pow(r(), 1.2), y = yh + (h - yh) * s, x = r() * w; g.fillStyle = ['rgba(255,255,255,.5)', 'rgba(250,225,90,.5)', 'rgba(240,200,220,.4)'][i % 3]; g.beginPath(); g.arc(x, y - 2 * s, 0.25 + 0.8 * s, 0, TAU); g.fill(); }   /* the common small flowers of the sward, not forage patches */
  gr = g.createLinearGradient(0, yh - 4, 0, yh + 34); gr.addColorStop(0, 'rgba(240,245,235,0)'); gr.addColorStop(0.2, dim ? 'rgba(200,208,205,.5)' : 'rgba(240,245,230,.42)'); gr.addColorStop(1, 'rgba(240,245,235,0)'); g.fillStyle = gr; g.fillRect(0, yh - 4, w, 38);
  return (meadows[wx] = c); }

/* a bee seen from above, painted once and reused. Local units: 70 long, head towards +x, origin on the thorax. */
function paintBee(hornet) { const S = 5, c = mk(80 * S, 40 * S), g = c.getContext('2d'), r = rng(hornet ? 3 : 2); g.scale(S, S); g.translate(45, 20); g.lineCap = 'round';
  const ab = () => { g.beginPath(); if (hornet) { g.moveTo(-6, 0); g.bezierCurveTo(-8, -8.5, -22, -10, -31, -6); g.bezierCurveTo(-37, -3.4, -42, -1, -44, 0); g.bezierCurveTo(-42, 1, -37, 3.4, -31, 6); g.bezierCurveTo(-22, 10, -8, 8.5, -6, 0); } else { g.moveTo(-5, 0); g.bezierCurveTo(-6, -9.8, -22, -11.6, -30, -7.2); g.bezierCurveTo(-36, -4, -41, -1.2, -42, 0); g.bezierCurveTo(-41, 1.2, -36, 4, -30, 7.2); g.bezierCurveTo(-22, 11.6, -6, 9.8, -5, 0); } g.closePath(); };
  g.save(); ab(); g.clip(); g.fillStyle = hornet ? '#e9b524' : '#2a1a0c'; g.fillRect(-46, -14, 46, 28);
  const xs = [-6, -13.5, -21, -28, -34.5, -43], band = hornet ? ['#4a2410', '#4a2410', '#3a1c0c', '#3a1c0c', '#3a1c0c'] : ['#dc9d30', '#d39428', '#c18222', '#8a6226', '#4a3418'], frac = hornet ? [0.95, 0.6, 0.36, 0.3, 0.26] : [0.62, 0.58, 0.52, 0.45, 0.35];
  for (let i = 0; i < 5; i++) { const x1 = xs[i], x2 = x1 - (x1 - xs[i + 1]) * frac[i]; g.fillStyle = band[i]; g.beginPath(); g.moveTo(x1, -13); g.quadraticCurveTo(x1 - 2.6, 0, x1, 13); g.lineTo(x2, 13); g.quadraticCurveTo(x2 - 2.6, 0, x2, -13); g.fill();
    if (hornet && i > 0) { g.beginPath(); g.arc(x2 - 1.2, -4.2, 1.5, 0, TAU); g.arc(x2 - 1.2, 4.2, 1.5, 0, TAU); g.fill(); }
    g.strokeStyle = hornet ? 'rgba(255,240,170,.25)' : 'rgba(236,220,165,.6)'; g.lineWidth = 0.55; g.beginPath(); g.moveTo(x1, -13); g.quadraticCurveTo(x1 - 2.6, 0, x1, 13); g.stroke(); }
  let gr = g.createLinearGradient(0, -11.5, 0, 11.5); gr.addColorStop(0, 'rgba(0,0,0,.66)'); gr.addColorStop(0.3, 'rgba(0,0,0,.05)'); gr.addColorStop(0.42, 'rgba(255,244,210,.2)'); gr.addColorStop(0.56, 'rgba(0,0,0,0)'); gr.addColorStop(1, 'rgba(0,0,0,.66)'); g.fillStyle = gr; g.fillRect(-46, -14, 46, 28);
  gr = g.createLinearGradient(-44, 0, -28, 0); gr.addColorStop(0, 'rgba(0,0,0,.5)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(-46, -14, 20, 28); g.restore();
  /* thorax, with its coat of branched hair */
  gr = g.createRadialGradient(-1, -2, 1, 0, 0, 9.6); if (hornet) { gr.addColorStop(0, '#6e3319'); gr.addColorStop(0.7, '#48200f'); gr.addColorStop(1, '#2a1208'); } else { gr.addColorStop(0, '#a98646'); gr.addColorStop(0.65, '#644621'); gr.addColorStop(1, '#3a260f'); }
  g.fillStyle = gr; g.beginPath(); g.ellipse(0, 0, 9.4, 9, 0, 0, TAU); g.fill();
  for (let i = 0; i < (hornet ? 60 : 300); i++) { const a = r() * TAU, d = Math.sqrt(r()) * 9.8, l = 1.2 + r() * 2.4, x = Math.cos(a) * d, y = Math.sin(a) * d * 0.96; g.strokeStyle = hornet ? `rgba(150,90,50,${0.2 + 0.3 * r()})` : `rgba(${205 + r() * 30 | 0},${170 + r() * 30 | 0},${100 + r() * 30 | 0},${0.2 + 0.45 * r()})`; g.lineWidth = 0.32; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a + 0.6) * l, y + Math.sin(a + 0.6) * l); g.stroke(); }
  /* head, eyes, antennae */
  g.strokeStyle = hornet ? '#3a1c0c' : '#1a1009'; g.lineWidth = 1; g.lineJoin = 'round'; for (const s of [-1, 1]) { g.beginPath(); g.moveTo(16.5, s * 2.2); g.lineTo(23.5, s * 6.6); g.lineTo(30.5, s * 5.2); g.stroke(); }
  g.fillStyle = hornet ? '#e39a1c' : '#241609'; g.beginPath(); g.ellipse(12.8, 0, hornet ? 6.2 : 5.6, hornet ? 8.4 : 7.8, 0, 0, TAU); g.fill();
  if (!hornet) for (let i = 0; i < 50; i++) { const a = r() * TAU, d = Math.sqrt(r()) * 5; g.strokeStyle = 'rgba(190,160,110,.3)'; g.lineWidth = 0.3; g.beginPath(); g.moveTo(12.8 + Math.cos(a) * d, Math.sin(a) * d * 1.3); g.lineTo(12.8 + Math.cos(a) * (d + 1.4), Math.sin(a) * (d + 1.4) * 1.3); g.stroke(); }
  for (const s of [-1, 1]) { g.fillStyle = hornet ? '#2a1408' : '#0e0906'; g.beginPath(); g.ellipse(13.6, s * 6.1, 3.5, 2.6, s * 0.45, 0, TAU); g.fill(); g.fillStyle = 'rgba(190,180,160,.45)'; g.beginPath(); g.ellipse(14.6, s * 6.5, 1.1, 0.6, s * 0.45, 0, TAU); g.fill(); }
  return c; }
const beeSpr = paintBee(false), hornetSpr = paintBee(true), beeSmall = mk(160, 80); { const g = beeSmall.getContext('2d'); g.imageSmoothingQuality = 'high'; g.drawImage(beeSpr, 0, 0, 160, 80); }

/* ---------- the comb ---------- */
const P12 = new Float32Array(24);
function cellPts(q) { const J = W.junc, R = SET.PITCH / SQ3, Rc = SET.PITCH * 0.5, rho = q.rho; let px, py;
  for (let k = 0; k < 6; k++) { const j = q.J[k]; if (j >= 0) { px = J[j].x; py = J[j].y; } else { const a = (30 + 60 * k) * RAD; px = q.x + R * Math.cos(a); py = q.y + R * Math.sin(a); } P12[4 * k] = px; P12[4 * k + 1] = py; }
  for (let k = 0; k < 6; k++) { const n = (k + 1) % 6; P12[4 * k + 2] = (P12[4 * k] + P12[4 * n]) / 2; P12[4 * k + 3] = (P12[4 * k + 1] + P12[4 * n + 1]) / 2; }
  if (rho > 0.01) for (let i = 0; i < 12; i++) { const dx = P12[2 * i] - q.x, dy = P12[2 * i + 1] - q.y, d = Math.hypot(dx, dy) || 1, f = (1 - rho) + rho * Rc / d; P12[2 * i] = q.x + dx * f; P12[2 * i + 1] = q.y + dy * f; } }
function cellPath(c, q, sc) { const X = i => q.x + (P12[2 * i] - q.x) * sc, Y = i => q.y + (P12[2 * i + 1] - q.y) * sc; c.beginPath();
  if (q.rho < 0.03) { c.moveTo(X(0), Y(0)); for (let k = 1; k < 6; k++) c.lineTo(X(2 * k), Y(2 * k)); }
  else { c.moveTo((X(11) + X(0)) / 2, (Y(11) + Y(0)) / 2); for (let i = 0; i < 12; i++) { const n = (i + 1) % 12; c.quadraticCurveTo(X(i), Y(i), (X(i) + X(n)) / 2, (Y(i) + Y(n)) / 2); } }
  c.closePath(); }
const LIGHT = { x: O.x + O.w * 0.5, y: O.y + O.h * 0.55 };
const WALL = ['#f0c766', '#b5843a', '#e2b254'], FRESH = '#f7ecc4';
const hex2 = h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)], mixc = (a, b, t) => { const A = hex2(a), B = hex2(b); return `rgb(${mix(A[0], B[0], t) | 0},${mix(A[1], B[1], t) | 0},${mix(A[2], B[2], t) | 0})`; };
const wallCache = {}; function wallCol(q) { const k = q.kind === 'brood' ? 1 : q.kind === 'pollen' ? 2 : 0, f = Math.round(clamp(1 - (W.t - q.born) / 260, 0, 1) * 6), key = k * 10 + f; return wallCache[key] || (wallCache[key] = mixc(WALL[k], FRESH, f / 6)); }
function drawComb(c, z) { const vw = cw / z, vh = ch / z, x0 = cam.x - vw / 2 - 30, x1 = cam.x + vw / 2 + 30, y0 = cam.y - vh / 2 - 30, y1 = cam.y + vh / 2 + 30, px = SET.PITCH * z * dpr, fine = px > 15, rich = px > 40, C = W.cells, vis = [];
  for (const q of C) if (q.built > 0 && q.x > x0 && q.x < x1 && q.y > y0 && q.y < y1) vis.push(q);
  c.lineJoin = 'round';
  c.fillStyle = 'rgba(6,3,0,.5)'; c.beginPath(); for (const q of vis) if (q.built >= 1) { c.moveTo(q.x + 9 + 23, q.y + 15); c.arc(q.x + 9, q.y + 15, 23, 0, TAU); } c.fill();      /* the comb's shadow on the wall behind */
  /* the wax itself: thin, so the light comes through it */
  for (const q of vis) { if (q.built < 1) continue; cellPts(q); cellPath(c, q, 1.045); c.fillStyle = wallCol(q); c.fill(); }
  for (const q of vis) { const x = q.x, y = q.y;
    if (q.built < 1) { c.beginPath(); c.arc(q.lx, q.ly, 15.5, 0, TAU); c.fillStyle = `rgba(60,36,10,${0.5 * q.built})`; c.fill(); c.strokeStyle = `rgba(247,236,196,${0.3 + 0.7 * q.built})`; c.lineWidth = 1.2 + 3.2 * q.built; c.stroke(); continue; }
    cellPts(q); cellPath(c, q, 0.87);
    let lx = LIGHT.x - x, ly = LIGHT.y - y; const ld = Math.hypot(lx, ly) || 1; lx /= ld; ly /= ld; const lit = clamp(1.15 - ld / 1500, 0.45, 1);
    if (q.capped) { if (q.kind === 'brood') { if (fine) { const g = c.createRadialGradient(x + lx * 4, y + ly * 4, 1, x, y, 17); g.addColorStop(0, q.tone > 0.5 ? '#cfa56c' : '#c39a62'); g.addColorStop(1, q.tone > 0.3 ? '#9a7340' : '#8c6636'); c.fillStyle = g; } else c.fillStyle = '#b48a50'; c.fill(); }
      else { const wet = q.tone > 0.72; if (fine) { const g = c.createRadialGradient(x + lx * 5, y + ly * 5, 1, x, y, 17); g.addColorStop(0, wet ? '#e0bf78' : '#f7ecc8'); g.addColorStop(1, wet ? '#bf9647' : '#dcc48a'); c.fillStyle = g; } else c.fillStyle = wet ? '#d0aa5e' : '#ead8a6'; c.fill();
        if (rich) { c.strokeStyle = 'rgba(120,90,40,.16)'; c.lineWidth = 0.6; c.beginPath(); c.arc(x - 3 + q.tone * 6, y + 2, 6, 3.6 + q.tone, 5.2 + q.tone); c.stroke(); c.beginPath(); c.arc(x + 2, y - 3 + q.tone * 5, 5, 0.4 + q.tone, 1.8 + q.tone); c.stroke(); } }
      continue; }
    /* an open cell: you look down into it. The wall facing the entrance is lit, the near side is in shade. */
    if (fine) { const g = c.createRadialGradient(x + lx * 6, y + ly * 6, 1.5, x, y, 17.5); if (q.kind === 'brood') { g.addColorStop(0, '#24140a'); g.addColorStop(0.6, '#5a3916'); g.addColorStop(1, '#9a6c2c'); } else { g.addColorStop(0, '#3a2108'); g.addColorStop(0.6, '#7d5016'); g.addColorStop(1, '#cf9c3e'); } c.fillStyle = g; } else c.fillStyle = q.kind === 'brood' ? '#553614' : '#7c5118';
    c.fill();
    if (q.kind === 'honey') { if (q.fill > 0.04) { c.globalAlpha = 0.35 + 0.62 * q.fill; if (fine) { const g = c.createRadialGradient(x + lx * 7, y + ly * 7, 1, x, y, 17); g.addColorStop(0, '#ffc84e'); g.addColorStop(0.45, '#e39a1e'); g.addColorStop(1, '#a8630a'); c.fillStyle = g; } else c.fillStyle = '#d28c18'; c.fill(); c.globalAlpha = 1;
        if (fine) { const a = Math.atan2(ly, lx), gx = x + lx * 7.5, gy = y + ly * 7.5, k = q.fill * lit; c.fillStyle = `rgba(255,248,222,${0.8 * k})`; c.beginPath(); c.ellipse(gx, gy, 2.2 + q.tone, 4.6, a, 0, TAU); c.fill(); c.fillStyle = `rgba(255,236,170,${0.34 * k})`; c.beginPath(); c.ellipse(x - lx * 6, y - ly * 6, 2.2, 6.5, a, 0, TAU); c.fill(); } }
      else if (rich) { c.strokeStyle = 'rgba(255,214,140,.16)'; c.lineWidth = 0.7; c.beginPath(); for (let k = 0; k < 3; k++) { const a = (90 + 120 * k) * RAD; c.moveTo(x, y); c.lineTo(x + Math.cos(a) * 12, y + Math.sin(a) * 12); } c.stroke(); } }
    else if (q.kind === 'pollen') { const col = SP[q.col].pollen, rr = 9 + 5 * q.fill; c.fillStyle = col; c.beginPath(); c.arc(x, y, rr, 0, TAU); c.fill();
      if (fine) { const g = c.createRadialGradient(x + lx * 4, y + ly * 4, 1, x, y, rr); g.addColorStop(0, 'rgba(255,255,255,.2)'); g.addColorStop(0.6, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,.34)'); c.fillStyle = g; c.fill(); if (rich) { c.fillStyle = 'rgba(255,255,255,.2)'; for (let k = 0; k < 5; k++) { const a = q.tone * 9 + k * 2.1; c.beginPath(); c.arc(x + Math.cos(a) * rr * 0.5, y + Math.sin(a) * rr * 0.5, 1.2, 0, TAU); c.fill(); } } } }
    else if (q.larva) { if (fine) { c.fillStyle = 'rgba(236,228,200,.22)'; c.beginPath(); c.arc(x, y, 12, 0, TAU); c.fill(); const a0 = q.tone * TAU; c.lineCap = 'round'; c.strokeStyle = '#cfc4a6'; c.lineWidth = 7.4; c.beginPath(); c.arc(x, y, 7, a0, a0 + 4.2); c.stroke(); c.strokeStyle = '#ece3cc'; c.lineWidth = 5.4; c.beginPath(); c.arc(x, y, 7.1, a0 + 0.05, a0 + 4.15); c.stroke(); c.strokeStyle = 'rgba(255,253,246,.7)'; c.lineWidth = 1.6; c.beginPath(); c.arc(x, y, 8, a0 + 0.3, a0 + 3.9); c.stroke();
        if (rich) { c.strokeStyle = 'rgba(150,130,95,.35)'; c.lineWidth = 0.5; c.beginPath(); for (let k = 0; k < 9; k++) { const a = a0 + 0.3 + k * 0.45; c.moveTo(x + Math.cos(a) * 4.6, y + Math.sin(a) * 4.6); c.lineTo(x + Math.cos(a) * 9.6, y + Math.sin(a) * 9.6); } c.stroke(); } c.lineCap = 'butt'; }
      else { c.fillStyle = '#e9dfc6'; c.beginPath(); c.arc(x, y, 8, 0, TAU); c.fill(); } }
  } }
function drawStatic() { sx.setTransform(1, 0, 0, 1, 0, 0); sx.fillStyle = '#120b06'; sx.fillRect(0, 0, stat.width, stat.height); world(sx);
  sx.fillStyle = '#2b1b0d'; sx.fillRect(-900, -700, 3400, 2400); sx.fillStyle = 'rgba(0,0,0,.25)'; for (let y = -700; y < 1700; y += 150) sx.fillRect(-900, y, 3400, 3);
  sx.imageSmoothingQuality = 'high'; sx.drawImage(wood, 0, 0, 1600, 1000); drawComb(sx, cam.z); }

/* ---------- bees ---------- */
const LEG = [[5.5, 0.9], [0, 1.62], [-5, 2.35]];
function drawBee(c, b, pxLen) { const s = b.s, flying = b.mode === 'out' || b.mode === 'fly', fan = b.fan && !flying, hang = b.mode === 'hang';
  if (pxLen < 7) { c.fillStyle = 'rgba(40,26,10,.9)'; c.beginPath(); c.ellipse(b.x, b.y, 22 * s, 11 * s, b.hd, 0, TAU); c.fill(); c.fillStyle = 'rgba(240,238,225,.35)'; c.beginPath(); c.arc(b.x, b.y, 24 * s, 0, TAU); c.fill(); return; }
  c.save(); c.translate(b.x, b.y); c.rotate(b.hd); if (s !== 1) { const k = s * (0.62 + 0.38 * s); c.scale(k, k); } if (b.wag) c.translate(0, b.wag * 2.6);
  if (b.trem) c.translate(Math.sin(clock * 47 + b.id) * 0.9, Math.cos(clock * 53 + b.id) * 0.9);
  if (pxLen > 24) { c.strokeStyle = '#1c120a'; c.lineWidth = 1.5; c.lineCap = 'round'; c.lineJoin = 'round'; c.beginPath();
    for (let i = 0; i < 3; i++) for (const sd of [-1, 1]) { const sw = flying ? 0.5 : hang ? (i === 0 ? -0.5 : i === 2 ? 0.45 : 0) : b.v > 3 ? Math.sin(b.gait + (i % 2 ? Math.PI : 0) + (sd > 0 ? 0 : Math.PI)) * 0.3 : 0, a = (LEG[i][1] + sw) * sd, l1 = hang ? 11 : flying ? 6 : 8.5, l2 = hang ? 12 : flying ? 7 : 9.5, bx = LEG[i][0], by = sd * 5, kx = bx + Math.cos(a) * l1, ky = by + Math.sin(a) * l1, a2 = a + sd * (i === 0 ? -0.5 : 0.55); c.moveTo(bx, by); c.lineTo(kx, ky); c.lineTo(kx + Math.cos(a2) * l2, ky + Math.sin(a2) * l2); }
    c.stroke(); }
  if (b.polc >= 0 || b.pol >= 0) { const col = SP[b.pol >= 0 ? b.pol : b.polc]; if (col && (b.pol >= 0 || b.pol === -2)) { c.fillStyle = col.pollen; c.beginPath(); c.ellipse(-9, -11.5, 4.4, 3.2, 0.3, 0, TAU); c.ellipse(-9, 11.5, 4.4, 3.2, -0.3, 0, TAU); c.fill(); } }
  c.drawImage(pxLen > 150 ? beeSpr : beeSmall, -45, -20, 80, 40);
  if (flying || fan) { const fl = 0.5 + 0.5 * Math.sin(clock * 90 + b.id * 3); for (const sd of [-1, 1]) { c.fillStyle = `rgba(238,236,226,${0.16 + 0.1 * fl})`; c.beginPath(); c.moveTo(-1, sd * 4); c.arc(-1, sd * 4, 31, sd > 0 ? 1.15 : -2.75, sd > 0 ? 2.75 : -1.15); c.closePath(); c.fill(); c.strokeStyle = 'rgba(255,255,255,.3)'; c.lineWidth = 0.6; const a = sd * (1.3 + 1.3 * fl); c.beginPath(); c.moveTo(-1, sd * 4); c.lineTo(-1 + Math.cos(a) * 30, sd * 4 + Math.sin(a) * 30); c.stroke(); } }
  else for (const sd of [-1, 1]) { c.fillStyle = 'rgba(214,208,190,.3)'; c.strokeStyle = 'rgba(70,52,34,.42)'; c.lineWidth = 0.5; c.beginPath(); c.moveTo(-1, sd * 3.2); c.bezierCurveTo(-10, sd * 1.5, -24, sd * 4.5, -33, sd * 9.5); c.bezierCurveTo(-28, sd * 13.5, -12, sd * 10.5, -1, sd * 3.2); c.fill(); c.stroke(); if (pxLen > 60) { c.strokeStyle = 'rgba(255,255,255,.28)'; c.beginPath(); c.moveTo(-5, sd * 4.5); c.quadraticCurveTo(-18, sd * 5.5, -30, sd * 10); c.stroke(); } }
  c.restore(); }
function drawHornet(c) { const Hn = W.hornet; if (!Hn.on) return; const s = 1.55 * Hn.s; c.save(); c.translate(Hn.x, Hn.y); c.rotate((Hn.hd || 0) * 0.35 - Math.PI / 2 * 0.2); c.scale(s, s); const fl = 0.5 + 0.5 * Math.sin(clock * 70);
  for (const sd of [-1, 1]) { c.fillStyle = `rgba(214,160,90,${0.2 + 0.1 * fl})`; c.beginPath(); c.moveTo(-1, sd * 4); c.arc(-1, sd * 4, 36, sd > 0 ? 1.1 : -2.8, sd > 0 ? 2.8 : -1.1); c.closePath(); c.fill(); }
  c.strokeStyle = '#3a1c0c'; c.lineWidth = 1.5; c.lineCap = 'round'; c.beginPath(); for (let i = 0; i < 3; i++) for (const sd of [-1, 1]) { const a = (LEG[i][1] + 0.4) * sd; c.moveTo(LEG[i][0], sd * 5); c.lineTo(LEG[i][0] + Math.cos(a) * 12, sd * 5 + Math.sin(a) * 12); } c.stroke();
  c.drawImage(hornetSpr, -45, -20, 80, 40); c.restore(); }
const inFront = b => b.mode === 'out' || b.mode === 'fly' || (b.x > O.x - 26 && b.x < O.x + O.w + 26 && b.y > O.y - 26 && b.y < O.y + O.h + 44);

/* ---------- the meadow, through the entrance ---------- */
const blades = []; { const r = rng(4); for (let i = 0; i < 70; i++) blades.push({ x: O.x + r() * O.w, h: 10 + r() * 30, ph: r() * TAU, lean: (r() - 0.5) * 12, c: r() < 0.5 ? '#2f6a2c' : '#4f8a34', w: 1.4 + r() * 2 }); }
function drawMeadow(c) { const z = cam.z; c.save(); c.beginPath(); c.rect(O.x, O.y, O.w, O.h); c.clip(); c.imageSmoothingQuality = 'high'; c.drawImage(paintMeadow(W.weather), O.x, O.y, O.w, O.h);
  /* where the dance floor has been pointing in the last minute or so: a leaky sum of waggle runs */
  let mx = 0; for (let i = 0; i < 240; i++) if (W.map[i] > mx) mx = W.map[i];
  if (mx > 0.5) for (let k = 0; k < 10; k++) for (let i = 0; i < 24; i++) { const v = W.map[k * 24 + i]; if (v < 0.4) continue; const az = -60 + 5 * i + 2.5, d = 200 * k + 100, p = H.proj(az, d, 0), p2 = H.proj(az + 4, d, 0), rx = Math.max(3, (p2.x - p.x) * 1.6), g = c.createRadialGradient(p.x, p.y, 0, p.x, p.y, rx); const a = Math.min(0.55, 0.1 + 0.05 * v); g.addColorStop(0, `rgba(255,222,110,${a})`); g.addColorStop(1, 'rgba(255,222,110,0)'); c.fillStyle = g; c.save(); c.translate(p.x, p.y); c.scale(1, 0.34); c.translate(-p.x, -p.y); c.beginPath(); c.arc(p.x, p.y, rx, 0, TAU); c.fill(); c.restore(); }
  const ps = W.patches.filter(p => p.bloom > 0.01).sort((a, b) => b.d - a.d), wind = still ? 0 : 1;
  for (const p of ps) { const sp = SP[p.sp]; for (const f of p.flowers) { const open = clamp(p.bloom * 1.6 - f.dl, 0, 1); if (open <= 0) continue; const q = H.proj(p.az + f.da, p.d * (1 + f.dd), 0), sz = 15 * f.sz * q.s * (0.4 + 0.6 * open), x = q.x + wind * Math.sin(clock * 1.3 + f.ph) * 2.2 * q.s, st = 26 * q.s * f.sz, y = q.y - st, px = sz * z * dpr;
      c.strokeStyle = 'rgba(50,100,40,.8)'; c.lineWidth = Math.max(0.25, 1.1 * q.s); c.beginPath(); c.moveTo(q.x, q.y); c.quadraticCurveTo(q.x, q.y - st * 0.6, x, y); c.stroke(); c.globalAlpha = 0.35 + 0.65 * open;
      if (px > 3.2) { c.fillStyle = sp.petal; for (let k = 0; k < 6; k++) { const a = f.ph + k * TAU / 6; c.beginPath(); c.ellipse(x + Math.cos(a) * sz * 0.5, y + Math.sin(a) * sz * 0.36, sz * 0.42, sz * 0.3, a, 0, TAU); c.fill(); } c.fillStyle = sp.heart; c.beginPath(); c.ellipse(x, y, sz * 0.3, sz * 0.24, 0, 0, TAU); c.fill(); }
      else { c.fillStyle = sp.petal; c.beginPath(); c.ellipse(x, y, Math.max(sz * 0.75, 0.5), Math.max(sz * 0.55, 0.4), 0, 0, TAU); c.fill(); } c.globalAlpha = 1; } }
  if (z > 0.3) for (const b of blades) { const sw = wind * Math.sin(clock * 1.1 + b.ph) * 4; c.strokeStyle = b.c; c.lineWidth = b.w; c.lineCap = 'round'; c.beginPath(); c.moveTo(b.x, O.y + O.h + 2); c.quadraticCurveTo(b.x + b.lean * 0.3, O.y + O.h - b.h * 0.6, b.x + b.lean + sw, O.y + O.h - b.h); c.stroke(); }
  if (W.weather === 'rain') { c.strokeStyle = 'rgba(225,232,240,.4)'; c.lineWidth = 0.7; c.beginPath(); for (let i = 0; i < 90; i++) { const x = O.x + ((i * 97.3 + clock * 60) % O.w), y = O.y + ((i * 53.7 + clock * (500 + (i % 7) * 40)) % O.h), l = 9 + (i % 5) * 3; c.moveTo(x, y); c.lineTo(x - 2, y + l); } c.stroke(); }
  /* what the featured dancer is saying, drawn on the ground: the way to the sun and the way to her flowers */
  const D = feature && feature.dance; if (D && cam.z > 0.9 && (view === 'meadow' || view === 'floor')) { const a = H.proj(0, 0, 0), s1 = H.proj(SET.SUN_AZ, 5000, 0), p1 = H.proj(D.az, D.d, 0); c.setLineDash([3, 3]); c.lineWidth = 0.9; c.strokeStyle = 'rgba(255,240,200,.55)'; c.beginPath(); c.moveTo(a.x, a.y); c.lineTo(s1.x, s1.y); c.stroke(); c.strokeStyle = 'rgba(255,214,90,.8)'; c.beginPath(); c.moveTo(a.x, a.y); c.lineTo(p1.x, p1.y); c.stroke(); c.setLineDash([]); }
  c.restore();
  /* the thickness of the wall round the opening, catching the daylight */
  const t = 9, q = (pts, col) => { c.fillStyle = col; c.beginPath(); c.moveTo(pts[0], pts[1]); for (let i = 2; i < pts.length; i += 2) c.lineTo(pts[i], pts[i + 1]); c.fill(); }, x0 = O.x, y0 = O.y, x1 = O.x + O.w, y1 = O.y + O.h, dim = W.weather === 'rain';
  q([x0, y0, x1, y0, x1 - t, y0 + t, x0 + t, y0 + t], dim ? '#3a2a18' : '#5a3f20'); q([x0, y0, x0 + t, y0 + t, x0 + t, y1 - t, x0, y1], dim ? '#5a442a' : '#9a7440'); q([x1, y0, x1, y1, x1 - t, y1 - t, x1 - t, y0 + t], dim ? '#4a3620' : '#8a6636'); q([x0, y1, x0 + t, y1 - 13, x1 - t, y1 - 13, x1, y1], dim ? '#77603c' : '#cfa765');
  c.strokeStyle = 'rgba(255,240,200,.28)'; c.lineWidth = 1; c.beginPath(); c.moveTo(x0 + t, y1 - 13); c.lineTo(x1 - t, y1 - 13); c.stroke(); }

/* ---------- a frame ---------- */
const trails = new Map(); let feature = null;
function render() { const z = cam.z; ctx.setTransform(1, 0, 0, 1, 0, 0);
  if (cam.moving || statT < 0 || clock - statT > 0.5) { drawStatic(); statT = clock; }
  ctx.globalCompositeOperation = 'source-over'; ctx.drawImage(stat, 0, 0); world(ctx);
  const B = W.bees, pxBee = SET.BEE * z * dpr, vw = cw / z, vh = ch / z, x0 = cam.x - vw / 2 - 60, x1 = cam.x + vw / 2 + 60, y0 = cam.y - vh / 2 - 60, y1 = cam.y + vh / 2 + 60, seen = b => b.x > x0 && b.x < x1 && b.y > y0 && b.y < y1;
  /* the festoon: bees hanging leg to leg beneath the growing edge */
  const F = W.festoon; if (F.length && pxBee > 14) { const at = {}; for (const b of B) if (b.task === 2 && b.mode === 'hang') { const g = F[b.slot]; if (g && Math.hypot(g.x - b.x, g.y - b.y) < 12) at[g.c + ':' + g.k] = b; }
    ctx.strokeStyle = 'rgba(96,70,40,.95)'; ctx.lineWidth = 1.6; ctx.lineCap = 'round'; ctx.beginPath(); for (const key in at) { const b = at[key], [c, k] = key.split(':').map(Number), up = at[c + ':' + (k - 1)]; for (const sd of [-1, 1]) { if (up) { ctx.moveTo(b.x + sd * 5, b.y - 6); ctx.quadraticCurveTo(b.x + sd * 11, b.y - 20, up.x + sd * 6, up.y + 24); } else if (k === 0) { ctx.moveTo(b.x + sd * 5, b.y - 6); ctx.quadraticCurveTo(b.x + sd * 12, b.y - 18, b.x + sd * 9, b.y - 33); } } } ctx.stroke(); }
  feature = W.dancers.length ? (feature && feature.st === 'dance' && feature.dance.ph !== 'go' ? feature : W.dancers[0]) : null;
  if (feature && pxBee > 20) { const g = ctx.createRadialGradient(feature.x, feature.y, 6, feature.x, feature.y, 64); g.addColorStop(0, 'rgba(255,226,130,.42)'); g.addColorStop(1, 'rgba(255,226,130,0)'); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(feature.x, feature.y, 64, 0, TAU); ctx.fill(); }
  const back = [], front = []; for (const b of B) { if (!seen(b)) continue; (inFront(b) ? front : back).push(b); }
  if (pxBee > 12) { ctx.fillStyle = 'rgba(14,7,0,.3)'; for (const b of back) { ctx.beginPath(); ctx.ellipse(b.x + 4, b.y + 6, 27, 10, b.hd, 0, TAU); ctx.fill(); } }
  for (const b of back) drawBee(ctx, b, pxBee);
  /* the dance, made visible: each dancer's own track, and for one of them the upright and her line */
  if (pxBee > 20) { for (const d of W.dancers) { let tr = trails.get(d.id); if (!tr) trails.set(d.id, tr = []); tr.push(d.x, d.y, clock); if (tr.length > 600) tr.splice(0, 3); }
    for (const [id, tr] of trails) { while (tr.length && clock - tr[2] > 4.5) tr.splice(0, 3); if (!tr.length) { trails.delete(id); continue; } ctx.lineWidth = 1.6; ctx.lineCap = 'round'; for (let i = 3; i < tr.length; i += 3) { const a = 1 - (clock - tr[i + 2]) / 4.5; ctx.strokeStyle = `rgba(255,232,150,${0.75 * a})`; ctx.beginPath(); ctx.moveTo(tr[i - 3], tr[i - 2]); ctx.lineTo(tr[i], tr[i + 1]); ctx.stroke(); } }
    const D = feature && feature.dance; if (D && D.ph !== 'go' && D.runAng !== undefined) { const L = 62, ax = Math.sin(D.runAng), ay = -Math.cos(D.runAng), pc = SP[(H.patchById(W, D.patch) || { sp: 0 }).sp].petal; ctx.lineWidth = 1.5; ctx.setLineDash([3, 4]); ctx.strokeStyle = 'rgba(255,248,224,.92)'; ctx.beginPath(); ctx.moveTo(D.cx, D.cy); ctx.lineTo(D.cx, D.cy - L); ctx.stroke(); ctx.setLineDash([]);
      ctx.strokeStyle = 'rgba(255,214,90,.95)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(D.cx, D.cy); ctx.lineTo(D.cx + ax * L, D.cy + ay * L); ctx.stroke(); ctx.beginPath(); ctx.arc(D.cx, D.cy, 26, -Math.PI / 2, -Math.PI / 2 + D.runAng, D.runAng < 0); ctx.stroke();
      ctx.fillStyle = '#ffe9a8'; ctx.beginPath(); ctx.arc(D.cx, D.cy - L - 7, 3.6, 0, TAU); ctx.fill(); ctx.strokeStyle = '#ffe9a8'; ctx.lineWidth = 0.9; ctx.beginPath(); for (let k = 0; k < 8; k++) { const a = k * TAU / 8; ctx.moveTo(D.cx + Math.cos(a) * 5.4, D.cy - L - 7 + Math.sin(a) * 5.4); ctx.lineTo(D.cx + Math.cos(a) * 8, D.cy - L - 7 + Math.sin(a) * 8); } ctx.stroke();
      ctx.fillStyle = pc; ctx.strokeStyle = 'rgba(20,10,0,.5)'; ctx.lineWidth = 0.6; ctx.beginPath(); ctx.arc(D.cx + ax * (L + 7), D.cy + ay * (L + 7), 4, 0, TAU); ctx.fill(); ctx.stroke(); } }
  /* light: it comes in at the entrance and falls off across the comb */
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0); const lx = (LIGHT.x - cam.x) * z + cw / 2, ly = (LIGHT.y - cam.y) * z + ch / 2, wx = W.weather;
  let g = ctx.createRadialGradient(lx, ly, 160 * z, lx, ly, 1500 * z); g.addColorStop(0, wx === 'rain' ? '#c9c4bd' : '#ffffff'); g.addColorStop(0.4, wx === 'rain' ? '#a59a8c' : '#d9c09a'); g.addColorStop(1, wx === 'rain' ? '#4d4438' : '#5e4630'); ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = g; ctx.fillRect(0, 0, cw, ch);
  g = ctx.createRadialGradient(lx, ly, 0, lx, ly, 760 * z); const k = wx === 'rain' ? 0.1 : wx === 'hot' ? 0.34 : 0.26; g.addColorStop(0, `rgba(255,226,170,${k})`); g.addColorStop(0.4, `rgba(255,214,150,${k * 0.4})`); g.addColorStop(1, 'rgba(255,214,150,0)'); ctx.globalCompositeOperation = 'screen'; ctx.fillStyle = g; ctx.fillRect(0, 0, cw, ch); ctx.globalCompositeOperation = 'source-over';
  world(ctx); drawMeadow(ctx);
  front.sort((a, b) => a.s - b.s); for (const b of front) { if (b.mode === 'walk' && pxBee > 12) { ctx.fillStyle = 'rgba(14,7,0,.3)'; ctx.beginPath(); ctx.ellipse(b.x + 4, b.y + 6, 27, 10, b.hd, 0, TAU); ctx.fill(); } drawBee(ctx, b, pxBee * b.s); }
  drawHornet(ctx); }

/* ---------- sound: the old page's hum, kept. One loop of brown noise through two band-passes near 234 and 602 Hz. ---------- */
let ac = null, au = null;
function audioStart() { if (ac) { ac.resume(); return; } try { ac = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { return; }
  const sr = ac.sampleRate, len = sr * 4, buf = ac.createBuffer(1, len, sr), d = buf.getChannelData(0); let last = 0; for (let i = 0; i < len; i++) { last = (last + 0.02 * (Math.random() * 2 - 1)) / 1.02; d[i] = last * 3.5; }
  const wb = ac.createBuffer(1, sr * 2, sr), wd = wb.getChannelData(0); for (let i = 0; i < wd.length; i++) wd[i] = Math.random() * 2 - 1;
  const master = ac.createGain(); master.gain.value = 0.6; master.connect(ac.destination);
  const src = ac.createBufferSource(); src.buffer = buf; src.loop = true; const b1 = ac.createBiquadFilter(); b1.type = 'bandpass'; b1.frequency.value = 234; b1.Q.value = 4.5; const b2 = ac.createBiquadFilter(); b2.type = 'bandpass'; b2.frequency.value = 602; b2.Q.value = 2; const g2 = ac.createGain(); g2.gain.value = 0.25; const hum = ac.createGain(); hum.gain.value = 0;
  src.connect(b1); b1.connect(hum); src.connect(b2); b2.connect(g2); g2.connect(hum); hum.connect(master); src.start();
  const rs = ac.createBufferSource(); rs.buffer = wb; rs.loop = true; const rf = ac.createBiquadFilter(); rf.type = 'highpass'; rf.frequency.value = 2400; const rain = ac.createGain(); rain.gain.value = 0; rs.connect(rf); rf.connect(rain); rain.connect(master); rs.start();
  const ho = ac.createOscillator(); ho.type = 'sawtooth'; ho.frequency.value = 104; const hf = ac.createBiquadFilter(); hf.type = 'lowpass'; hf.frequency.value = 520; const hg = ac.createGain(); hg.gain.value = 0; ho.connect(hf); hf.connect(hg); hg.connect(master); ho.start();
  au = { master, hum, b1, b2, rain, hg, ho, tick: 0 }; }
function blip(f0, f1, vol, dur) { if (!au || ac.currentTime - au.tick < 0.05) return; au.tick = ac.currentTime; const t = ac.currentTime, o = ac.createOscillator(), g = ac.createGain(); o.type = 'sine'; o.frequency.setValueAtTime(f0, t); o.frequency.exponentialRampToValueAtTime(f1, t + dur * 0.7); g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(vol, t + 0.005); g.gain.exponentialRampToValueAtTime(0.0001, t + dur); o.connect(g); g.connect(au.master); o.start(t); o.stop(t + dur + 0.02); }
function audioTick() { if (!au) return; const t = ac.currentTime, on = sound && !paused, v = VIEWS[view], near = view === 'meadow' ? 0.45 : 1; let inside = 0, fans = 0; for (const b of W.bees) { if (b.mode !== 'out') inside++; if (b.fan) fans++; }
  au.hum.gain.setTargetAtTime(on ? Math.min(0.2, (0.03 + inside * 0.0011 + fans * 0.004 + W.alarm * 0.03) * near) : 0, t, 0.3); au.b1.frequency.setTargetAtTime(234 + Math.min(30, W.alarm * 14), t, 0.4); au.b2.frequency.setTargetAtTime(602 + Math.min(60, W.alarm * 30), t, 0.4);
  au.rain.gain.setTargetAtTime(on && W.weather === 'rain' ? 0.035 : 0, t, 0.6); au.hg.gain.setTargetAtTime(on && W.hornet.on ? 0.05 * clamp(W.hornet.s, 0.1, 1) : 0, t, 0.15); au.ho.frequency.setTargetAtTime(104 + 6 * Math.sin(clock * 5), t, 0.05); }
function events() { for (const e of W.ev) { if (!sound || !au) break; if (e.k === 'wax') blip(820, 420, 0.035, 0.08); else if (e.k === 'cap') blip(520, 300, 0.03, 0.12); } W.ev.length = 0; }

/* ---------- words and numbers, all read from the run ---------- */
const deg = v => Math.round(Math.abs(v));
function say() { const m = lastM, el = $('say'); let s; const Hn = W.hornet;
  if (Hn.on && Hn.phase !== 'flee') s = `A hornet at the door. ${m.n[4]} bees are on guard${W.alarm > 0.3 ? ', drawn by alarm scent' : ''}.`;
  else if (W.weather === 'rain') s = `Rain. No one flies. ${m.n[5]} foragers wait on the comb.`;
  else if (view === 'comb') { let hang = 0; for (const b of W.bees) if (b.task === 2 && b.mode === 'hang') hang++; s = m.built < m.cells ? `${hang} bees hang in the festoon, making wax. ${m.built} of ${m.cells} cells are built. New ones are round at first.` : 'The comb is finished.'; }
  else if (feature && feature.dance && feature.dance.runAng !== undefined) { const D = feature.dance, a = D.runAng / RAD, p = H.patchById(W, D.patch); s = `One dancer says: ${deg(a) < 3 ? 'straight towards the sun' : deg(a) + '° to the ' + (a > 0 ? 'right' : 'left') + ' of the sun'}, ${(D.dur).toFixed(1)} seconds a run, about ${Math.round(D.dur * 1000 / SET.SEC_PER_KM / 50) * 50} metres.${p ? ' That is the ' + SP[p.sp].name + '.' : ''}`; }
  else s = m.foragersOut ? `No one is dancing just now. ${m.foragersOut} foragers are out.` : 'The dance floor is quiet.';
  if (el.textContent !== s) el.textContent = s; }
let lastM = H.measure(W);
function readout() { const m = lastM = H.measure(W); $('rOut').textContent = m.foragersOut; $('rIn').textContent = m.intake60; $('rSw').textContent = m.switches60;
  const p = m.lead >= 0 ? H.patchById(W, m.lead) : null; $('rCon').innerHTML = m.consensus === null ? '&ndash;<small>no waggle runs in the last minute</small>' : `<i style="background:${p ? SP[p.sp].petal : '#999'}"></i>${Math.round(m.consensus * 100)}%<small>${p ? SP[p.sp].name : 'a patch now gone'}, of ${m.runs60} runs</small>`;
  $('rCv').innerHTML = m.cv === null ? '&ndash;<small>too few switches yet</small>' : `${m.cv.toFixed(2)}<small>from ${m.cvN} intervals. Candidate value 0.159</small>`;
  $('rJ').innerHTML = m.juncDev === null ? '&ndash;' : `${m.juncDev.toFixed(1)}&deg;<small>mean over ${m.juncN} junctions</small>`; }

/* ---------- running ---------- */
let last = performance.now(), slow = 0, rd = 0, fastN = 0;
function frame(now) { requestAnimationFrame(frame); const real = Math.min(0.1, (now - last) / 1000); last = now; if (document.hidden || !onscreen) return;
  const t = target(), e = still ? 1 : 1 - Math.exp(-real * 3.4), lz = Math.log(cam.z) + (Math.log(t.z) - Math.log(cam.z)) * e; cam.x += (t.x - cam.x) * e; cam.y += (t.y - cam.y) * e; cam.z = Math.exp(lz);
  const mv = Math.abs(t.x - cam.x) * cam.z > 0.3 || Math.abs(t.y - cam.y) * cam.z > 0.3 || Math.abs(t.z / cam.z - 1) > 0.0015; if (!mv && cam.moving) { cam.x = t.x; cam.y = t.y; cam.z = t.z; statT = -1; } const was = cam.moving; cam.moving = mv;
  if (!paused) { clock += real; const n = real > 0.034 ? 2 : 1; for (let i = 0; i < n; i++) H.step(W, real / n); events(); }
  else if (!mv && !was && statT >= 0 && !dirty) return;
  dirty = false; render(); audioTick();
  rd += real; if (rd > 0.5) { rd = 0; readout(); say(); }
  if (real > 0.03) slow++; else fastN++; if (slow + fastN > 120) { if (slow > 80 && quality > 0.55) { quality -= 0.22; fit(); } slow = fastN = 0; } }
let dirty = true;
document.querySelectorAll('[data-view]').forEach(b => b.onclick = () => { view = b.dataset.view; document.querySelectorAll('[data-view]').forEach(o => o.setAttribute('aria-pressed', o === b ? 'true' : 'false')); cam.moving = true; dirty = true; rd = 1; });
document.querySelectorAll('[data-view]').forEach(o => o.setAttribute('aria-pressed', o.dataset.view === view ? 'true' : 'false'));
const WX = ['fair', 'hot', 'rain']; $('weather').onclick = () => { W.weather = WX[(WX.indexOf(W.weather) + 1) % 3]; $('weather').textContent = 'Weather: ' + W.weather; dirty = true; };
$('bloom').onclick = () => { H.bloom(W); dirty = true; };
$('hornet').onclick = () => { H.sendHornet(W); };
$('snd').onclick = () => { sound = !sound; if (sound) audioStart(); $('snd').setAttribute('aria-pressed', sound ? 'true' : 'false'); };
const pb = $('pause'); const setPause = p => { paused = p; pb.textContent = p ? 'Play' : 'Pause'; pb.setAttribute('aria-pressed', p ? 'true' : 'false'); }; pb.onclick = () => setPause(!paused); setPause(paused);
const sheet = $('sheet'); $('about').onclick = () => { sheet.hidden = false; sheet.scrollTop = 0; $('abt').focus({ preventScroll: true }); }; $('close').onclick = () => { sheet.hidden = true; $('about').focus(); }; sheet.addEventListener('click', e => { if (e.target === sheet) $('close').click(); });
addEventListener('keydown', e => { if (e.key === 'Escape' && !sheet.hidden) $('close').click(); });
addEventListener('resize', fit); if ('IntersectionObserver' in window) new IntersectionObserver(es => { onscreen = es[0].isIntersecting; last = performance.now(); }).observe(cv);
fit(); readout(); say(); requestAnimationFrame(frame);
window.HIVEPAGE = { get W() { return W; }, set W(v) { W = v; }, cam, setView: v => { view = v; cam.moving = true; dirty = true; }, get quality() { return quality; }, render, step: (s) => { H.run(W, s); W.ev.length = 0; clock += s; statT = -1; dirty = true; } };
})();
