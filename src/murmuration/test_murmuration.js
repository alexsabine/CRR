// Runs the bets in bets.md. Output is kept as it comes out, failures included.
const M = require('./model.js'); const dt = 1 / 60, only = process.argv[2] || '';
const log = (...a) => console.log(...a), f = (x, d) => (+x).toFixed(d === undefined ? 3 : d);
const run = k => !only || only.split(',').includes(k);
const deg = r => r * 180 / Math.PI;

if (run('B1')) { log('--- B1 order at seven neighbours (N=2000, 60 s, second half)'); const res = {};
  for (const rule of [true, false]) { res[rule] = []; for (const seed of [3, 11, 29]) { const r = M.trial(60, 2000, { rule, seed }); res[rule].push(r.pol); log(rule ? 'rule ' : 'plain', 'seed', seed, 'pol', f(r.pol), 'largest set', f(r.share), 'commits/bird/s', f(r.commitsPerBirdPerSec, 2)); } }
  const ok = [true, false].every(m => res[m].every(p => p >= .85)); log('B1', ok ? 'PASS' : 'FAIL', '(needs every run >= 0.85)');
  const a = res[true].reduce((x, y) => x + y) / 3, b = res[false].reduce((x, y) => x + y) / 3; log('B7a rule mean', f(a), 'plain mean', f(b), 'difference', f(a - b), Math.abs(a - b) < .05 ? 'PASS' : 'FAIL', '(needs |difference| < 0.05)'); }

if (run('B2')) { log('--- B2 one or two neighbours (N=2000, 40 s, rule)'); const out = {};
  const rad = S => { let q = 0; for (let i = 0; i < S.n; i++) q += (S.px[i] - S.cx) ** 2 + (S.py[i] - S.cy) ** 2 + (S.pz[i] - S.cz) ** 2; return Math.sqrt(q / S.n); };
  for (const k of [1, 2, 7]) { out[k] = []; for (const seed of [3, 11, 29]) { const r = M.trial(60, 2000, { k, seed }); r.rad = rad(r.S); out[k].push(r); log('k', k, 'seed', seed, 'pol', f(r.pol), 'largest set', f(r.share), 'sets', r.groups, 'rms radius', f(r.rad, 1), 'm'); } }
  const ok = out[1].every(r => r.share < .1 && r.pol < .6) && out[2].every(r => r.share < .6) && out[7].every(r => r.share >= .95); log('B2', ok ? 'PASS' : 'FAIL', '(as first written)');
  { const r = M.trial(60, 2000, { k: 1, seed: 3, rule: false }); log('for comparison, plain steering, k 1 seed 3: pol', f(r.pol), 'largest set', f(r.share), 'rms radius', f(rad(r.S), 1), 'm'); }
  const m = k => out[k].reduce((a, r) => a + r.rad, 0) / 3; log('B2v2 rms radius after 60 s: k=1', f(m(1), 1), 'k=2', f(m(2), 1), 'k=7', f(m(7), 1), 'ratio k1/k7', f(m(1) / m(7), 2), m(1) / m(7) >= 1.5 ? 'PASS' : 'FAIL', '(needs >= 1.5)'); }

if (run('B3')) { log('--- B3 seven is enough (N=2000, 40 s, rule, seed 5)'); const p = {};
  for (const k of [1, 2, 3, 5, 7, 10, 12]) { const r = M.trial(40, 2000, { k, seed: 5 }); p[k] = r.pol; log('k', k, 'pol', f(r.pol), 'largest set', f(r.share)); }
  log('B3 pol(12)-pol(7) =', f(p[12] - p[7]), p[12] - p[7] < .05 ? 'PASS' : 'FAIL'); }

function turnTest(rule, frac, label) {
  /* two identical flocks with the roost on; in one, the seed birds are held on a new course for 3 s. Everything is measured as the difference between the two. */
  const n = 3000, mk = () => { const S = M.makeFlock(n, { rule, seed: 17 }); for (let s = 0; s < 14 * 60; s++) M.step(S, dt); return S; }, S = mk(), Q = mk();
  const H = [S.Hx, 0, S.Hz], hl = Math.hypot(H[0], H[2]); H[0] /= hl; H[2] /= hl; const a = [-H[2], 0, H[0]];
  const proj = new Float32Array(n); const order = []; for (let i = 0; i < n; i++) { proj[i] = (S.px[i] - S.cx) * a[0] + (S.pz[i] - S.cz) * a[2]; order.push(i); } order.sort((p, q) => proj[q] - proj[p]);
  const ns = Math.max(1, Math.round(n * frac)), seeds = new Set(order.slice(0, ns)), c = Math.cos(Math.PI / 3), s = Math.sin(Math.PI / 3), dir = [H[0] * c + a[0] * s, 0, H[2] * c + a[2] * s];
  const NB = 8, bins = []; const rest = order.slice(ns); for (let b = 0; b < NB; b++) bins.push(rest.slice(Math.floor(b * rest.length / NB), Math.floor((b + 1) * rest.length / NB)));
  const dist = bins.map(b => proj[order[0]] - b.reduce((x, i) => x + proj[i], 0) / b.length);
  const ang = (W, b) => { let x = 0, z = 0; for (const i of b) { x += W.hx[i]; z += W.hz[i]; } return Math.atan2(x * a[0] + z * a[2], x * H[0] + z * H[2]); };
  const wrap = x => Math.atan2(Math.sin(x), Math.cos(x)), series = bins.map(() => []); S.pin = { has: i => seeds.has(i), dir }; const T = 6 * 60; let farAt3 = 0;
  for (let st = 0; st < T; st++) { if (st === 3 * 60) S.pin = null; M.step(S, dt); M.step(Q, dt); bins.forEach((b, q) => series[q].push(wrap(ang(S, b) - ang(Q, b)))); if (st === 3 * 60 - 1) farAt3 = (series[NB - 1][st] + series[NB - 2][st]) / 2; }
  let peak = 0, peakAt = 0; for (let st = 0; st < 4 * 60; st++) { const v = (series[NB - 1][st] + series[NB - 2][st]) / 2; if (Math.abs(v) > Math.abs(peak)) { peak = v; peakAt = st * dt; } }
  /* arrival: when a slice first differs from the control by 3 degrees, and stays so for a quarter of a second */
  const at3 = series.map(sr => sr[3 * 60 - 1]), arr = series.map(sr => { for (let st = 0; st < T - 15; st++) { let ok = true; for (let q = 0; q < 15; q++) if (Math.abs(sr[st + q]) < .052) { ok = false; break; } if (ok) return st * dt; } return null; });
  let speed = null; { const pts = dist.map((d, q) => [d, arr[q]]).filter(p => p[1] !== null); if (pts.length >= 4) { const mx = pts.reduce((x, p) => x + p[0], 0) / pts.length, my = pts.reduce((x, p) => x + p[1], 0) / pts.length; let sxy = 0, sxx = 0; for (const p of pts) { sxy += (p[0] - mx) * (p[1] - my); sxx += (p[0] - mx) ** 2; } const slope = sxy / sxx; speed = slope > 0 ? 1 / slope : Infinity; } }
  log(label, rule ? 'rule ' : 'plain', 'seeds', ns, '| far quarter turned', f(deg(farAt3), 1), 'deg at 3 s | turn per slice at 3 s (deg)', at3.map(x => f(deg(x), 0)).join(' '), '| slice distance from seeds (m)', dist.map(x => f(x, 0)).join(' '), '| arrival (s)', arr.map(x => x === null ? '-' : f(x, 2)).join(' '), '| front speed', speed === null ? 'n/a' : (isFinite(speed) ? f(speed, 1) + ' m/s' : 'no delay with distance'), '| largest turn of the far quarter in the first 4 s', f(deg(peak), 1), 'deg at', f(peakAt, 2), 's');
  return { far: deg(farAt3), speed, half: arr, peak: deg(peak), peakAt };
}
if (run('B4')) { log('--- B4 a turn started at one edge (N=3000, roost on, measured against an identical flock left alone)'); const r = {};
  for (const rule of [true, false]) { r[rule] = { a: turnTest(rule, .02, 'B4  2%'), b: turnTest(rule, .10, 'B4b 10%') }; }
  log('B4 ', [true, false].every(m => r[m].a.far >= 20) ? 'PASS' : 'FAIL', '(needs far quarter >= 20 deg at 3 s in both modes)');
  log('B4b', [true, false].every(m => r[m].b.far >= 20) ? 'PASS' : 'FAIL');
  log('B4 front faster than flight (10 m/s):', [true, false].map(m => (m ? 'rule ' : 'plain ') + ['a', 'b'].map(q => r[m][q].speed === null ? 'n/a' : (r[m][q].speed > 10 ? 'yes' : 'no')).join('/')).join(', '));
  const tr = r[true].b.half[7], tp = r[false].b.half[7]; log('B7b turn arrives at the far slice: rule', tr, 's, plain', tp, 's', tr !== null && tp !== null ? (tr > tp ? 'PASS (rule later)' : 'FAIL (rule not later)') : 'not measurable'); }
if (run('B5')) { log('--- B5 one bird'); const r = [true, false].map(rule => turnTest(rule, 1 / 1500, 'B5 1 bird')); log('B5', r.every(x => Math.abs(x.far) < 5) ? 'PASS' : 'FAIL', '(needs far quarter < 5 deg)'); }

if (run('B6')) { log('--- B6 scale-free correlation (rule, 40 s, mean of 6 samples in the last 10 s)'); const res = [];
  for (const n of [500, 1000, 2000, 4000]) { let xi = 0, L = 0, m = 0; M.trial(40, n, { seed: 9 }, (S, t) => { if (t > 30 && Math.round(t * 60) % 100 === 0) { const c = M.correlation(S, 500, true); if (c.xi > 0) { xi += c.xi; L += c.L; m++; } } }); xi /= m; L /= m; res.push({ n, xi, L }); log('N', n, 'xi', f(xi, 1), 'm  L', f(L, 1), 'm  xi/L', f(xi / L)); }
  const ok = res.every(r => r.xi / r.L >= .2 && r.xi / r.L <= .5) && res[3].xi / res[0].xi >= 1.5; log('B6', ok ? 'PASS' : 'FAIL', 'xi(4000)/xi(500) =', f(res[3].xi / res[0].xi, 2)); }

if (run('B8')) { log('--- B8 the falcon (N=2000, rule, sent at 20 s)');
  for (const seed of [3, 11]) { const S = M.makeFlock(2000, { seed }); let minShare = 1, minAt = 0, at40 = null, pre = 0, preN = 0, dur = 0, durN = 0, t = 0, peak = 0; const trace = [];
    for (let st = 0; st < 75 * 60; st++) { if (st === 20 * 60) M.sendFalcon(S); M.step(S, dt); t = st * dt;
      if (st % 6 === 0 && (t > 15 && t < 20 || (S.falcon.on && !S.falcon.leaving))) { let u = 0, c = 0, sc = 0; for (let i = 0; i < S.n; i += 3) { if (S.thr[i] < .02) { u += Math.hypot(S.ux[i], S.uy[i], S.uz[i]); c++; } else sc++; }
        if (c > 30) { if (t < 20) { pre += u / c; preN++; } else if (sc > 5) { dur += u / c; durN++; if (u / c > peak) peak = u / c; } } }
      if (st >= 20 * 60 && st % 60 === 0) { const g = M.largestGroup(S).share; trace.push(f(g, 2)); if (t - 20 <= 15 && g < minShare) { minShare = g; minAt = t - 20; } if (st === 60 * 60) at40 = g; } }
    const ratio = durN ? (dur / durN) / (pre / preN) : 0;
    log('seed', seed, 'smallest share of birds in the largest set', f(minShare, 2), 'at', f(minAt, 1), 's | share at 40 s', f(at40, 2), '| turn rate of birds not themselves frightened: before', f(pre / preN, 3), 'while some bird is frightened', f(durN ? dur / durN : 0, 3), 'ratio', f(ratio, 2), 'peak', f(peak, 3), '| falcon gone:', !S.falcon.on);
    log('   share each second after launch:', trace.join(' '));
    log('B8a', minShare < .9 ? 'PASS' : 'FAIL', 'B8b', at40 >= .95 ? 'PASS' : 'FAIL', 'B8c', ratio >= 1.5 ? 'PASS' : 'FAIL'); } }

if (run('B9')) { log('--- B9 cost'); const S = M.makeFlock(4000, {}); for (let s = 0; s < 60; s++) M.step(S, dt); const t0 = process.hrtime.bigint(); for (let s = 0; s < 300; s++) M.step(S, dt); const ms = Number(process.hrtime.bigint() - t0) / 1e6 / 300; log('4000 birds:', f(ms, 2), 'ms a step', ms < 4 ? 'PASS' : 'FAIL', '(load average ' + require('os').loadavg()[0].toFixed(1) + ')');
  log('--- commit intervals (rule, N=1000, 30 s, birds 0..99)'); const T = M.makeFlock(1000, { seed: 4 }), lastC = new Float32Array(100), iv = []; let prev = Float32Array.from(T.C.slice(0, 100));
  for (let s = 0; s < 1800; s++) { M.step(T, dt); for (let i = 0; i < 100; i++) { if (T.C[i] < prev[i]) { if (lastC[i] > 10) iv.push(s * dt - lastC[i]); lastC[i] = s * dt; } prev[i] = T.C[i]; } }
  const mean = iv.reduce((a, b) => a + b, 0) / iv.length, sd = Math.sqrt(iv.reduce((a, b) => a + (b - mean) ** 2, 0) / iv.length); log('intervals', iv.length, 'mean', f(mean), 's  CV', f(sd / mean), ' (measurement only)'); }
