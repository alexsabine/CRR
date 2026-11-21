/* The murmuration model. No drawing in here. Runs in a browser or in node.
   Units are metres and seconds, loosely: flight speed about 10 m/s, birds about a metre and a half apart.

   What comes from the literature:
   - each bird attends to its k nearest neighbours whatever their distance (Ballerini et al. 2008), k = 7 by default
   - headings have inertia: a bird's turn rate is a state of its own, pulled toward its target and lightly damped,
     which is what lets a turn travel as a wave (Attanasi et al. 2014; Cavagna et al. 2015, the inertial spin model)
   - a roost the flock will not leave, level flight preferred, banked turns (Hildenbrandt, Carere and Hemelrijk 2010)
   What is this page's own choice:
   - the timing rule (P.rule = true): a bird does not re-read its neighbours every instant. It keeps a count C of its
     mismatch with them and with the course it expected; when C reaches Cstar it commits to a new course built from its
     neighbours' recent past, and C restarts. With P.rule = false the bird re-reads its neighbours at every step.
     Everything else (the body, the forces, the noise) is identical in the two modes. */
(function (root) {
'use strict';
const KMAX = 12, GR = 48;
const DEFAULTS = {
  k: 7, v0: 10, s0: 2.2, rs: 2.1, flat: 1.8, air: 1.2,
  wa: 1.0, wc: 0.2, ws: 0.3, wl: 0.3,
  tau: 0.045, zeta: 0.2, wmax: 1.7, noise: 1.0,
  roost: 1, roostX: 0, roostY: 24, roostZ: -108, roostR: 36, roostSpan: 20, wr: 0.7, wy: 0.45, yMin: 9, yMax: 40,
  wind: 0,
  rule: true, Cstar: Math.PI, L0: 40, ka: 300, gain: 1, salient: 0, ks: 6, kf: 40, tauM: 0.03,
  fearR: 15, wf: 5.0, slices: 4
};
function rng(seed) { let s = seed || 7; return () => (s = (s * 16807) % 2147483647) / 2147483647; }

function makeFlock(n, opt) {
  const P = Object.assign({}, DEFAULTS, opt || {}), rnd = rng(P.seed || 7);
  const f = () => new Float32Array(n);
  const S = { n, nMax: n, P, rnd, t: 0, frame: 0, commits: 0, commitsTotal: 0,
    px: f(), py: f(), pz: f(), hx: f(), hy: f(), hz: f(), ux: f(), uy: f(), uz: f(), gx: f(), gy: f(), gz: f(),
    mx: f(), my: f(), mz: f(), C: f(), roll: f(), ph: f(), sp: f(), thr: f(), fl: f(),
    nb: new Int32Array(n * KMAX), cs: new Float32Array(n * KMAX), nc: new Uint8Array(n), kn: new Uint8Array(n),
    cell: new Int32Array(n), cellStart: new Int32Array(GR * GR * GR + 1), cellItems: new Int32Array(n), grid: null,
    falcon: { on: false, x: 0, y: 0, z: 0, vx: 0, vy: 0, vz: 0, t: 0, pass: 0, leaving: false },
    cx: 0, cy: 0, cz: 0, pol: 0, Hx: 1, Hy: 0, Hz: 0, pin: null };
  const R = P.s0 * Math.cbrt(3 * n / (4 * Math.PI)) * 0.95;
  for (let i = 0; i < n; i++) {
    let x, y, z; do { x = rnd() * 2 - 1; y = rnd() * 2 - 1; z = rnd() * 2 - 1; } while (x * x + y * y + z * z > 1);
    S.px[i] = P.roostX - 14 + x * R * 1.35; S.py[i] = P.roostY + y * R * 0.4; S.pz[i] = P.roostZ + 24 + z * R * 1.1;
    let a = (rnd() - .5) * .5, e = (rnd() - .5) * .2; S.hx[i] = Math.cos(a) * Math.cos(e); S.hy[i] = Math.sin(e); S.hz[i] = Math.sin(a) * Math.cos(e);
    S.gx[i] = S.mx[i] = S.hx[i]; S.gy[i] = S.my[i] = S.hy[i]; S.gz[i] = S.mz[i] = S.hz[i];
    S.C[i] = rnd() * P.Cstar; S.ph[i] = rnd() * 6.283; S.sp[i] = P.v0; S.fl[i] = 8.5 + rnd() * 2.5;
  }
  buildGrid(S); for (let i = 0; i < n; i++) knn(S, i, Math.min(P.k, KMAX));
  measure(S); return S;
}

/* ─── who is near: a uniform grid, rebuilt each step, so that finding the k nearest is cheap ─── */
function buildGrid(S) {
  const n = S.n, px = S.px, py = S.py, pz = S.pz; let x0 = 1e9, y0 = 1e9, z0 = 1e9, x1 = -1e9, y1 = -1e9, z1 = -1e9;
  for (let i = 0; i < n; i++) { const x = px[i], y = py[i], z = pz[i]; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; if (z < z0) z0 = z; if (z > z1) z1 = z; }
  const ext = Math.max(x1 - x0, y1 - y0, z1 - z0) + 1e-3, cs = Math.max(S.P.s0 * 1.05, ext / (GR - 1) * 1.001), inv = 1 / cs;
  const gx = Math.min(GR, Math.floor((x1 - x0) * inv) + 1), gy = Math.min(GR, Math.floor((y1 - y0) * inv) + 1), gz = Math.min(GR, Math.floor((z1 - z0) * inv) + 1), nc = gx * gy * gz;
  const start = S.cellStart, cell = S.cell, items = S.cellItems; start.fill(0, 0, nc + 1);
  for (let i = 0; i < n; i++) { const c = Math.floor((px[i] - x0) * inv) + gx * (Math.floor((py[i] - y0) * inv) + gy * Math.floor((pz[i] - z0) * inv)); cell[i] = c; start[c + 1]++; }
  for (let c = 0; c < nc; c++) start[c + 1] += start[c];
  const fill = S._fill && S._fill.length >= nc ? S._fill : (S._fill = new Int32Array(GR * GR * GR)); for (let c = 0; c < nc; c++) fill[c] = start[c];
  for (let i = 0; i < n; i++) items[fill[cell[i]]++] = i;
  S.grid = { x0, y0, z0, inv, cs, gx, gy, gz };
}
const bD = new Float32Array(KMAX), bJ = new Int32Array(KMAX), oJ = new Int32Array(KMAX), oC = new Float32Array(KMAX);
function knn(S, i, k) {
  const G = S.grid, px = S.px, py = S.py, pz = S.pz, x = px[i], y = py[i], z = pz[i], start = S.cellStart, items = S.cellItems;
  const cx = Math.floor((x - G.x0) * G.inv), cy = Math.floor((y - G.y0) * G.inv), cz = Math.floor((z - G.z0) * G.inv);
  let found = 0, worst = 1e30;
  for (let r = 1; r <= 2; r++) {
    found = 0; worst = 1e30;
    const a0 = Math.max(0, cx - r), a1 = Math.min(G.gx - 1, cx + r), b0 = Math.max(0, cy - r), b1 = Math.min(G.gy - 1, cy + r), c0 = Math.max(0, cz - r), c1 = Math.min(G.gz - 1, cz + r);
    for (let c = c0; c <= c1; c++) for (let b = b0; b <= b1; b++) { const row = G.gx * (b + G.gy * c);
      for (let q = start[row + a0], e = start[row + a1 + 1]; q < e; q++) { const j = items[q]; if (j === i) continue; const dx = px[j] - x, dy = py[j] - y, dz = pz[j] - z, d = dx * dx + dy * dy + dz * dz;
        if (d >= worst) continue; let w = found < k ? found++ : k - 1; while (w > 0 && bD[w - 1] > d) { bD[w] = bD[w - 1]; bJ[w] = bJ[w - 1]; w--; } bD[w] = d; bJ[w] = j; if (found === k) worst = bD[k - 1]; } }
    const reach = r * G.cs; if (found >= k && bD[k - 1] <= reach * reach) break;
  }
  if (found < k) {                                             /* a straggler: look further afield, through a sample of the whole flock */
    const stride = Math.max(1, Math.floor(S.n / 240));
    for (let j = (i * 7 + S.frame) % stride; j < S.n; j += stride) { if (j === i) continue; let dup = false; for (let q = 0; q < found; q++) if (bJ[q] === j) { dup = true; break; } if (dup) continue;
      const dx = px[j] - x, dy = py[j] - y, dz = pz[j] - z, d = dx * dx + dy * dy + dz * dz; if (found === k && d >= bD[k - 1]) continue;
      let w = found < k ? found++ : k - 1; while (w > 0 && bD[w - 1] > d) { bD[w] = bD[w - 1]; bJ[w] = bJ[w - 1]; w--; } bD[w] = d; bJ[w] = j; }
  }
  /* each neighbour keeps the share of this bird's count that it has earned, as long as it stays a neighbour */
  const o = i * KMAX, was = S.nc[i], nb = S.nb, cs = S.cs; for (let q = 0; q < was; q++) { oJ[q] = nb[o + q]; oC[q] = cs[o + q]; }
  for (let q = 0; q < found; q++) { const j = bJ[q]; let v = 0; for (let p = 0; p < was; p++) if (oJ[p] === j) { v = oC[p]; break; } nb[o + q] = j; cs[o + q] = v; } S.nc[i] = found; S.kn[i] = k;
}

/* ─── the falcon ─── */
function sendFalcon(S, from) {
  const F = S.falcon; if (F.on) return false; const fr = from || [95, 48, 70];
  F.on = true; F.t = 0; F.pass = 0; F.leaving = false; F.x = S.cx + fr[0]; F.y = S.cy + fr[1]; F.z = S.cz + fr[2];
  const dx = S.cx - F.x, dy = S.cy - F.y, dz = S.cz - F.z, d = Math.hypot(dx, dy, dz) || 1; F.vx = dx / d * 27; F.vy = dy / d * 27; F.vz = dz / d * 27; F.inside = false; return true;
}
function stepFalcon(S, dt) {
  const F = S.falcon; if (!F.on) return; F.t += dt;
  let tx = S.cx, ty = S.cy, tz = S.cz; if (F.leaving) { tx = F.x - 300; ty = F.y + 120; tz = F.z - 200; }
  let dx = tx - F.x, dy = ty - F.y, dz = tz - F.z; const d = Math.hypot(dx, dy, dz) || 1; dx /= d; dy /= d; dz /= d;
  const sp = Math.hypot(F.vx, F.vy, F.vz) || 1; let vx = F.vx / sp, vy = F.vy / sp, vz = F.vz / sp;
  const ahead = dx * vx + dy * vy + dz * vz;
  if (!F.leaving) { if (d < 9) F.inside = true; if (F.inside && ahead < 0 && d > 55) { F.pass++; F.inside = false; } if (F.pass >= 2 || F.t > 22) F.leaving = true; }
  /* turn toward the target, but only so fast; a stooping falcon cannot jink like a starling */
  const turn = (F.inside || (ahead < 0 && d < 55 && !F.leaving) ? 0.15 : 1.25) * dt; let ex = dx - ahead * vx, ey = dy - ahead * vy, ez = dz - ahead * vz; const el = Math.hypot(ex, ey, ez);
  if (el > 1e-5) { const a = Math.min(turn, Math.atan2(el, ahead)), s = Math.sin(a) / el, c = Math.cos(a); vx = vx * c + ex * s; vy = vy * c + ey * s; vz = vz * c + ez * s; }
  const v = F.leaving ? 22 : 27; F.vx = vx * v; F.vy = vy * v; F.vz = vz * v; F.x += F.vx * dt; F.y += F.vy * dt; F.z += F.vz * dt; if (F.y < 6) { F.y = 6; F.vy = Math.abs(F.vy); }
  if (F.leaving && Math.hypot(F.x - S.cx, F.y - S.cy, F.z - S.cz) > 230) F.on = false;
}

/* ─── one step for every bird ─── */
function step(S, dt) {
  const P = S.P, n = S.n, k = Math.max(1, Math.min(P.k | 0, KMAX)), rnd = S.rnd;
  const px = S.px, py = S.py, pz = S.pz, hx = S.hx, hy = S.hy, hz = S.hz, ux = S.ux, uy = S.uy, uz = S.uz, gx = S.gx, gy = S.gy, gz = S.gz, mx = S.mx, my = S.my, mz = S.mz, C = S.C, nb = S.nb, nc = S.nc, thr = S.thr;
  S.t += dt; S.frame++;
  buildGrid(S); const sl = Math.max(1, P.slices | 0); for (let i = S.frame % sl; i < n; i += sl) knn(S, i, k);
  stepFalcon(S, dt); const F = S.falcon;
  const K = 1 / (P.tau * P.tau), damp = 2 * P.zeta / P.tau, sig = P.noise * (1 + 1.5 * P.wind) * Math.sqrt(dt), mk = Math.min(1, dt / P.tauM);
  const gust = P.wind * (1 + .35 * Math.sin(S.t * .7) + .2 * Math.sin(S.t * 1.9 + 1)), windX = 5.5 * gust, windZ = 1.2 * gust * Math.sin(S.t * .23);
  const rule = !!P.rule, Cstar = P.Cstar, fearR = P.fearR; let commits = 0;
  const air = P.air * (1 + 2.5 * P.wind), ta = S.t * .31, tb = S.t * .23 + 1.7, tc = S.t * .27 + 4.1;
  const fsp = Math.hypot(F.vx, F.vy, F.vz) || 1, fvx = F.vx / fsp, fvy = F.vy / fsp, fvz = F.vz / fsp;
  for (let i = 0; i < n; i++) {
    const x = px[i], y = py[i], z = pz[i], h0 = hx[i], h1 = hy[i], h2 = hz[i], o = i * KMAX, c = Math.min(nc[i], k);
    /* what the neighbours are doing now */
    let ax = 0, ay = 0, az = 0, ox = 0, oy = 0, oz = 0, sx = 0, sy = 0, sz = 0, d1 = 1e9;
    for (let q = 0; q < c; q++) { const j = nb[o + q], dx = px[j] - x, dy = py[j] - y, dz = pz[j] - z, d = Math.sqrt(dx * dx + dy * dy + dz * dz) + 1e-6;
      ax += hx[j]; ay += hy[j]; az += hz[j]; ox += dx; oy += dy; oz += dz; if (d < d1) d1 = d;
      if (d < P.rs) { const f = (1 - d / P.rs) / d; sx -= dx * f; sy -= dy * f; sz -= dz * f; } }
    if (c) { const ic = 1 / c; ax *= ic; ay *= ic; az *= ic; ox *= ic / P.s0; oy *= ic / P.s0; oz *= ic / P.s0; }
    { const sl = Math.sqrt(sx * sx + sy * sy + sz * sz); if (sl > 1.2) { const f = 1.2 / sl; sx *= f; sy *= f; sz *= f; } }
    let ol = Math.sqrt(ox * ox + oy * oy + oz * oz); if (ol > 1.5) { const f = 1.5 / ol; ox *= f; oy *= f; oz *= f; ol = 1.5; }
    /* everything that is not the neighbours' heading: spacing, the roost, level flight, the falcon */
    let ex = P.wc * ox + P.ws * sx, ey = P.wc * P.flat * oy + P.ws * sy - P.wl * h1, ez = P.wc * oz + P.ws * sz, out = 0;
    if (P.roost) { const rx = x - P.roostX, rz = z - P.roostZ, rd = Math.sqrt(rx * rx + rz * rz) + 1e-6;
      /* outside the roost's reach a bird leans back toward it: a sideways push, never a demand to reverse, so the flock wheels and does not fold */
      if (rd > P.roostR) { out = (rd - P.roostR) / P.roostSpan; const away = (h0 * rx + h2 * rz) / rd, f = P.wr * Math.min(out, 4) / rd; ex -= (rx - away * rd * h0) * f; ez -= (rz - away * rd * h2) * f; if (out > 1) out = 1; }
      /* lower over the middle of the roost, higher toward its edge, so the flock swoops */
      const q = Math.min(1, rd / (P.roostR + P.roostSpan)), yc = P.yMin + (P.yMax - P.yMin) * (.15 + .6 * q * q * (3 - 2 * q)), dy = (yc - y) / 12; ey += P.wy * Math.max(-1, Math.min(1, dy));
      if (y < P.yMin) out += Math.min(1, (P.yMin - y) / 8); else if (y > P.yMax) out += Math.min(1, (y - P.yMax) / 8); }
    let th = thr[i] * Math.exp(-dt / 1.2);
    if (F.on) { const dx = x - F.x, dy = y - F.y, dz = z - F.z, d = Math.sqrt(dx * dx + dy * dy + dz * dz) + 1e-6; if (d < fearR) { const f = 1 - d / fearR; if (f > th) th = f;
        const al = (dx * fvx + dy * fvy + dz * fvz) / d * .6; let qx = dx / d - al * fvx, qy = dx / d * 0 + dy / d - al * fvy, qz = dz / d - al * fvz; const ql = Math.sqrt(qx * qx + qy * qy + qz * qz) || 1, w = P.wf * f / ql; ex += qx * w; ey += qy * w; ez += qz * w; } }
    thr[i] = th;
    let tx, ty, tz;
    if (rule) {
      /* coherence: the running count. Each neighbour adds to it by as much as that neighbour has departed from the course this bird
         last settled on; being badly placed, or frightened, adds more. It climbs slowly in calm flight and fast when a neighbour turns. */
      const g0 = gx[i], g1 = gy[i], g2 = gz[i]; let add = 0;
      if (c) { const kk = P.ka / c * dt; for (let q = 0; q < c; q++) { const j = nb[o + q], dp = hx[j] * g0 + hy[j] * g1 + hz[j] * g2, inc = kk * Math.sqrt(Math.max(0, 2 - 2 * dp)); S.cs[o + q] += inc; add += inc; } }
      const crowd = d1 < P.rs * .6 ? (P.rs * .6 - d1) / P.rs : 0;
      C[i] += add + (P.L0 + P.ks * (ol + crowd * 3 + out) + P.kf * th) * dt;
      if (C[i] >= Cstar) {                                    /* rupture: settle on a new course, rebuilt from the neighbours' recent past.
                                                                 Each neighbour is weighted by exp(its share of the count / Omega), with Omega = 1 / Cstar: those that departed furthest count most. */
        let bx = 0, by = 0, bz = 0, ws = 0; for (let q = 0; q < c; q++) { const j = nb[o + q], w = Math.exp(Math.min(S.cs[o + q] * Cstar * P.gain, 6)); bx += mx[j] * w; by += my[j] * w; bz += mz[j] * w; ws += w; S.cs[o + q] = 0; }
        if (ws) { bx /= ws; by /= ws; bz /= ws; } else { bx = h0; by = h1; bz = h2; }
        let vx = P.wa * bx + ex, vy = P.wa * by + ey, vz = P.wa * bz + ez; const vl = Math.sqrt(vx * vx + vy * vy + vz * vz) || 1; gx[i] = vx / vl; gy[i] = vy / vl; gz[i] = vz / vl; C[i] = 0; commits++; }
      tx = gx[i]; ty = gy[i]; tz = gz[i];
    } else {
      if (P.salient > 0 && c) { /* optional, for comparison only: continuous steering that also attends most to the neighbour that differs most */
        let bx = 0, by = 0, bz = 0, ws = 0; for (let q = 0; q < c; q++) { const j = nb[o + q], dp = hx[j] * h0 + hy[j] * h1 + hz[j] * h2, w = Math.exp(Math.min(P.salient * Math.sqrt(Math.max(0, 2 - 2 * dp)), 6)); bx += hx[j] * w; by += hy[j] * w; bz += hz[j] * w; ws += w; } ax = bx / ws; ay = by / ws; az = bz / ws; }
      tx = P.wa * ax + ex; ty = P.wa * ay + ey; tz = P.wa * az + ez; if (!c) { tx += h0; ty += h1; tz += h2; } const tl = Math.sqrt(tx * tx + ty * ty + tz * tz) || 1; tx /= tl; ty /= tl; tz /= tl; gx[i] = tx; gy[i] = ty; gz[i] = tz; }
    if (S.pin && S.pin.has(i)) { tx = S.pin.dir[0]; ty = S.pin.dir[1]; tz = S.pin.dir[2]; gx[i] = tx; gy[i] = ty; gz[i] = tz; }
    /* the body: heading has inertia. The turn rate u is pulled toward the target and lightly damped. */
    const dot = tx * h0 + ty * h1 + tz * h2; let qx = tx - dot * h0, qy = ty - dot * h1, qz = tz - dot * h2;
    if (dot < 0) { const ql = Math.sqrt(qx * qx + qy * qy + qz * qz); if (ql > 1e-6) { qx /= ql; qy /= ql; qz /= ql; } else { qx = -h2; qy = 0; qz = h0; } }
    let u0 = ux[i] + (K * qx - damp * ux[i]) * dt + (rnd() - .5) * sig * 3.46, u1 = uy[i] + (K * qy - damp * uy[i]) * dt + (rnd() - .5) * sig * 1.7, u2 = uz[i] + (K * qz - damp * uz[i]) * dt + (rnd() - .5) * sig * 3.46;
    const ud = u0 * h0 + u1 * h1 + u2 * h2; u0 -= ud * h0; u1 -= ud * h1; u2 -= ud * h2;
    const um = Math.sqrt(u0 * u0 + u1 * u1 + u2 * u2), lim = P.wmax * (1 + .6 * th); if (um > lim) { const f = lim / um; u0 *= f; u1 *= f; u2 *= f; }
    let n0 = h0 + u0 * dt, n1 = h1 + u1 * dt, n2 = h2 + u2 * dt; if (n1 > .6) n1 = .6; else if (n1 < -.6) n1 = -.6; const nl = Math.sqrt(n0 * n0 + n1 * n1 + n2 * n2) || 1; n0 /= nl; n1 /= nl; n2 /= nl;
    hx[i] = n0; hy[i] = n1; hz[i] = n2; ux[i] = u0; uy[i] = u1; uz[i] = u2;
    /* speed: a little faster when behind the neighbours, a little slower when ahead, faster when frightened */
    const lead = Math.max(-1, Math.min(1, ox * n0 + oy * n1 + oz * n2)), vt = P.v0 * (1 + .14 * lead + .3 * th); let sp = S.sp[i]; sp += (vt - sp) * Math.min(1, dt * 2); S.sp[i] = sp;
    /* the air is never still: slow eddies, tens of metres across, carry the birds with them and pull the flock out of shape */
    const e1 = Math.sin(.052 * z + .031 * y + ta) + .5 * Math.sin(.21 * z - .17 * x + 2 * ta), e2 = Math.sin(.047 * x - .04 * y - tb) + .5 * Math.sin(.19 * x + .23 * z - 2 * tb), e3 = Math.sin(.06 * x + .05 * z + tc);
    px[i] = x + (n0 * sp + windX + air * e1) * dt; py[i] = y + (n1 * sp + air * .35 * e3) * dt; pz[i] = z + (n2 * sp + windZ + air * e2) * dt; if (py[i] < 2.5) { py[i] = 2.5; if (hy[i] < 0) hy[i] = 0; }
    /* bank into the turn, as a bird must */
    const yawRate = n2 * u0 - n0 * u2, rt = Math.max(-1.25, Math.min(1.25, Math.atan(sp * yawRate / 9.81))); S.roll[i] += (rt - S.roll[i]) * Math.min(1, dt * 7);
    S.ph[i] += dt * 6.2832 * S.fl[i] * (1 + .25 * th);
  }
  /* memory: each bird's recent past, a past-only running average of its own heading */
  for (let i = 0; i < n; i++) { mx[i] += (hx[i] - mx[i]) * mk; my[i] += (hy[i] - my[i]) * mk; mz[i] += (hz[i] - mz[i]) * mk; }
  S.commits = commits; S.commitsTotal += commits; measure(S); return S;
}

/* ─── measurements ─── */
function measure(S) { const n = S.n; let a = 0, b = 0, c = 0, x = 0, y = 0, z = 0; for (let i = 0; i < n; i++) { a += S.hx[i]; b += S.hy[i]; c += S.hz[i]; x += S.px[i]; y += S.py[i]; z += S.pz[i]; }
  const l = Math.hypot(a, b, c) || 1; S.pol = l / n; S.Hx = a / l; S.Hy = b / l; S.Hz = c / l; S.cx = x / n; S.cy = y / n; S.cz = z / n; }
/* the share of birds in the largest set joined, directly or through others, by who is attending to whom */
function largestGroup(S) { const n = S.n, k = Math.min(S.P.k, KMAX), par = S._par && S._par.length >= n ? S._par : (S._par = new Int32Array(S.nMax)), size = S._size || (S._size = new Int32Array(S.nMax));
  for (let i = 0; i < n; i++) { par[i] = i; size[i] = 1; }
  const find = i => { while (par[i] !== i) { par[i] = par[par[i]]; i = par[i]; } return i; };
  for (let i = 0; i < n; i++) { const c = Math.min(S.nc[i], k); for (let q = 0; q < c; q++) { const j = S.nb[i * KMAX + q]; if (j >= n) continue; let a = find(i), b = find(j); if (a !== b) { if (size[a] < size[b]) { const t = a; a = b; b = t; } par[b] = a; size[a] += size[b]; } } }
  let best = 0, groups = 0, root = 0; for (let i = 0; i < n; i++) if (par[i] === i) { groups++; if (size[i] > best) { best = size[i]; root = i; } }
  S._root = root; return { share: best / n, groups }; }
/* how far a change of course is shared: the distance at which two birds' departures from the flock's mean heading stop agreeing
   (the first zero of the correlation function, as in Cavagna et al. 2010), and the flock's size L (the largest distance in the sample) */
function correlation(S, m, onlyLargest) { const n = S.n; let idx = []; const want = Math.min(m || 400, n), st = n / want;
  let find = null; if (onlyLargest) { largestGroup(S); const par = S._par; find = i => { while (par[i] !== i) i = par[i]; return i; }; }
  for (let q = 0; q < want; q++) { const i = Math.min(n - 1, Math.floor(q * st)); if (!find || find(i) === S._root) idx.push(i); }
  const M = idx.length; if (M < 20) return { xi: 0, L: 0, ratio: 0 };
  let a = 0, b = 0, c = 0; for (const i of idx) { a += S.hx[i]; b += S.hy[i]; c += S.hz[i]; } a /= M; b /= M; c /= M;
  let L = 0; for (let p = 0; p < M; p += 3) for (let q = p + 1; q < M; q += 3) { const i = idx[p], j = idx[q], d = Math.hypot(S.px[i] - S.px[j], S.py[i] - S.py[j], S.pz[i] - S.pz[j]); if (d > L) L = d; }
  const NB = 36, sum = new Float64Array(NB), cnt = new Float64Array(NB), bw = L / NB * 1.0001 + 1e-9;
  for (let p = 0; p < M; p++) { const i = idx[p], fx = S.hx[i] - a, fy = S.hy[i] - b, fz = S.hz[i] - c; for (let q = p + 1; q < M; q++) { const j = idx[q], d = Math.hypot(S.px[i] - S.px[j], S.py[i] - S.py[j], S.pz[i] - S.pz[j]), bn = Math.min(NB - 1, Math.floor(d / bw)); sum[bn] += fx * (S.hx[j] - a) + fy * (S.hy[j] - b) + fz * (S.hz[j] - c); cnt[bn]++; } }
  let xi = 0, prev = null; for (let q = 0; q < NB; q++) { if (cnt[q] < 8) continue; const v = sum[q] / cnt[q]; if (prev && prev.v > 0 && v <= 0) { xi = (prev.r + (q + .5) * bw * 0 + ((q + .5) * bw - prev.r) * prev.v / (prev.v - v)); break; } prev = { v, r: (q + .5) * bw }; }
  return { xi, L, ratio: L ? xi / L : 0 }; }

/* a run with no pictures */
function trial(sec, n, opt, onStep) { const S = makeFlock(n || 1000, opt), dt = 1 / 60; let pol = 0, m = 0; const steps = Math.round(sec / dt);
  for (let s = 0; s < steps; s++) { step(S, dt); if (s > steps / 2) { pol += S.pol; m++; } if (onStep) onStep(S, s * dt); }
  const g = largestGroup(S); return { S, pol: pol / m, share: g.share, groups: g.groups, commitsPerBirdPerSec: S.commitsTotal / S.n / sec }; }

const API = { KMAX, DEFAULTS, makeFlock, step, measure, largestGroup, correlation, sendFalcon, trial, knn, buildGrid };
if (typeof module !== 'undefined' && module.exports) module.exports = API; root.MURMUR = API;
})(typeof window !== 'undefined' ? window : globalThis);
