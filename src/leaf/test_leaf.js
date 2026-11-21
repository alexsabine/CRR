// Bets are in BETS.md, written before this was first run. This file runs them against the model inside leaf.html.
// Usage: node test_leaf.js > test_output.txt
const fs = require('fs'), path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', '..', 'leaf.html'), 'utf8');
const src = html.match(/<script id="model">([\s\S]*?)<\/script>/)[1];
const mod = { exports: {} }; new Function('module', 'globalThis', src)(mod, {}); const L = mod.exports;
const out = [], say = (...a) => { console.log(...a); }, res = {};
const verdict = (k, ok, note) => { res[k] = ok; say((ok ? 'PASS ' : 'FAIL ') + k + '  ' + note); };
const summer = L.season(196, 0.5, true, 1);
say('settings: alpha', L.ALPHA, 'beta', L.BETA, 'S0 dark', L.S0DARK, 'tau', L.TAU, 'PSII share', L.PSII_SHARE, 'N_REF', L.N_REF.toFixed(3));
say('midsummer pigments', JSON.stringify(summer));

// ---- B1 Kok
{ const seeds = [1, 2, 3, 4, 5], M = 6000, exact = L.kok(40); let a = 0, b = 0, c = 0, d = 0, e = 0, f = 0; const rows = [];
  for (const s of seeds) { const E = L.centres(M, s), Y = []; for (let i = 0; i < 40; i++) Y.push(L.flash(E));
    rows.push(Y.slice(0, 16).map(v => v.toFixed(3)).join(' '));
    const first4 = Y.slice(0, 4); if (first4.indexOf(Math.max(...first4)) === 2) a++;
    if (Y[6] > Y[5] && Y[6] > Y[7] && Y[10] > Y[9] && Y[10] > Y[11]) b++;
    if (Y[0] < 0.05 * Y[2] && Y[1] < 0.25 * Y[2]) c++;
    const sw = x => Math.max(...x) - Math.min(...x); if (sw(Y.slice(16, 20)) < 0.5 * sw(Y.slice(0, 4))) d++;
    const mean = Y.slice(20).reduce((p, q) => p + q, 0) / 20; if (Math.abs(mean / 0.2375 - 1) < 0.05) e++;
    let ok = true; for (let i = 0; i < 12; i++) { const se = Math.sqrt(Math.max(exact[i] * (1 - exact[i]), 1e-4) / M); if (Math.abs(Y[i] - exact[i]) > 4 * se) ok = false; } if (ok) f++; }
  say('\nB1 oxygen per centre per flash, flashes 1-16, five seeds:'); rows.forEach(r => say('  ' + r)); say('  exact: ' + exact.slice(0, 16).map(v => v.toFixed(3)).join(' '));
  verdict('B1a', a === 5, 'peak of first four on flash 3: ' + a + '/5'); verdict('B1b', b === 5, 'flashes 7 and 11 local maxima: ' + b + '/5'); verdict('B1c', c === 5, 'flash 1 < 5% and flash 2 < 25% of flash 3: ' + c + '/5');
  verdict('B1d', d === 5, 'swing over 17-20 under half of swing over 1-4: ' + d + '/5'); verdict('B1e', e === 5, 'mean of 21-40 within 5% of 0.2375: ' + e + '/5'); verdict('B1f', f === 5, 'flashes 1-12 within 4 s.e. of exact chain: ' + f + '/5'); }

// ---- B2 cosine
{ const sun = L.sun(60), run = deg => { const E = L.centres(6000, 9), Lt = L.lightOn(sun, Math.cos(deg * Math.PI / 180), summer); for (let i = 0; i < 4000; i++) L.steady(E, Lt, 1e-4); return E.abs[0] + E.abs[1] + E.abs[2]; };
  const a0 = run(0), rows = [0, 15, 30, 45, 60, 80].map(d => { const n = run(d); return [d, n, n / (a0 * Math.cos(d * Math.PI / 180))]; });
  say('\nB2 incidence, photons absorbed, ratio to cosine law:'); rows.forEach(r => say('  ' + r[0] + ' deg  ' + r[1] + '  ' + r[2].toFixed(4)));
  verdict('B2a', rows.slice(0, 5).every(r => r[2] > 0.95 && r[2] < 1.05), 'within 5% of cosine up to 60 degrees'); verdict('B2b', rows[5][2] < 0.90, 'below cosine at 80 degrees: ' + rows[5][2].toFixed(3)); }

// ---- B3 light response
{ const lights = [25, 50, 100, 200, 400, 800, 1000, 1600, 2000], base = L.lightOn(L.sun(90), 1, summer), rows = [];
  for (const on of lights) { const Lt = Object.assign({}, base, { on, enter: on * (1 - L.F0) }), E = L.centres(6000, 21); for (let i = 0; i < 1000; i++) L.steady(E, Lt, 1e-4); E.o2 = 0; E.abs = [0, 0, 0]; E.ant = 0; const T = 0.6; for (let i = 0; i < T / 1e-4; i++) L.steady(E, Lt, 1e-4);
    const area = E.M / L.N_REF, o2 = E.o2 / T / area, ab = (E.abs[0] + E.abs[1] + E.abs[2]) / T / area; rows.push({ on, o2, ab, yield: o2 / ab, exp: L.expectedO2(Lt) }); }
  say('\nB3 light on blade, O2 measured, O2 by formula, absorbed, O2 per absorbed photon:'); rows.forEach(r => say('  ' + r.on + '  ' + r.o2.toFixed(2) + '  ' + r.exp.toFixed(2) + '  ' + r.ab.toFixed(0) + '  ' + r.yield.toFixed(4)));
  const by = on => rows.find(r => r.on === on); let mono = true; for (let i = 1; i < rows.length; i++) if (rows[i].o2 < rows[i - 1].o2 * 0.97) mono = false;
  verdict('B3a', mono, 'never falls more than 3% as light rises'); verdict('B3b', by(100).o2 / by(50).o2 > 1.6 && by(2000).o2 / by(1000).o2 < 1.15, '50 to 100: x' + (by(100).o2 / by(50).o2).toFixed(2) + '; 1000 to 2000: x' + (by(2000).o2 / by(1000).o2).toFixed(2));
  verdict('B3c', by(25).yield > 0.100 && by(25).yield < 0.125, 'O2 per absorbed photon at 25: ' + by(25).yield.toFixed(4)); verdict('B3d', rows.every(r => Math.abs(r.o2 / r.exp - 1) < 0.05), 'worst departure from formula: ' + (100 * Math.max(...rows.map(r => Math.abs(r.o2 / r.exp - 1)))).toFixed(1) + '%'); }

// ---- B4 colour
{ const sp = L.spectra(summer), at = l => L.LAM.indexOf(l), leave = l => sp.R[at(l)] + sp.T[at(l)], c = L.colour(summer), meanA = sp.A.reduce((p, q) => p + q, 0) / sp.A.length;
  say('\nB4 midsummer  450: R ' + sp.R[at(450)].toFixed(3) + ' T ' + sp.T[at(450)].toFixed(3) + '   550: R ' + sp.R[at(550)].toFixed(3) + ' T ' + sp.T[at(550)].toFixed(3) + '   680: R ' + sp.R[at(680)].toFixed(3) + ' T ' + sp.T[at(680)].toFixed(3));
  say('   reflected colour (linear sRGB) ' + c.R.map(v => v.toFixed(3)) + '   transmitted ' + c.T.map(v => v.toFixed(3)) + '   mean absorptance ' + meanA.toFixed(3));
  verdict('B4a', leave(550) > 2 * leave(450) && leave(550) > 2 * leave(680) && c.R[1] > c.R[0] && c.R[0] > c.R[2], 'green leaves the leaf most; G > R > B');
  verdict('B4b', meanA > 0.78 && meanA < 0.90, 'mean absorptance ' + meanA.toFixed(3));
  const y = L.colour({ chl: 0, car: 7, anth: 0, brown: 0 }).R, r = L.colour({ chl: 0, car: 7, anth: 12, brown: 0 }).R; say('   yellow leaf ' + y.map(v => v.toFixed(3)) + '   red leaf ' + r.map(v => v.toFixed(3)));
  verdict('B4c', y[0] / y[1] > 0.9 && y[0] / y[1] < 1.5 && y[2] < 0.6 * y[1], 'yellow: R/G ' + (y[0] / y[1]).toFixed(2) + ', B/G ' + (y[2] / y[1]).toFixed(2)); verdict('B4d', r[0] > 1.5 * r[1], 'red: R/G ' + (r[0] / r[1]).toFixed(2));
  const rnd = L.rng(5); let ok = true; for (let i = 0; i < 200; i++) { const s = L.spectra({ chl: rnd() * 60, car: rnd() * 15, anth: rnd() * 20, brown: rnd() }); for (let k = 0; k < L.LAM.length; k++) { const sum = s.R[k] + s.T[k] + s.A[k]; if (Math.abs(sum - 1) > 1e-9 || s.R[k] < 0 || s.T[k] < 0 || s.A[k] < -1e-12 || s.R[k] > 1 || s.T[k] > 1) ok = false; } }
  verdict('B4e', ok, 'R + T + A = 1, all in range, 200 random mixes');
  const thin = L.spectra(summer, 1e-5); let worst = 0; for (let k = 0; k < L.LAM.length; k++) worst = Math.max(worst, Math.abs(thin.T[k] / Math.exp(-thin.depth(k)) - 1)); verdict('B4f', worst < 1e-3, 'Beer-Lambert limit, worst relative error ' + worst.toExponential(2)); }

// ---- B5 venation
{ let a = 0, b = 0, c = 0, d = 0; say('\nB5 venation:');
  for (const seed of [1, 2, 3, 4, 5]) { const t0 = Date.now(), V = L.venation(seed); while (!V.done) V.step(); const ms = Date.now() - t0, n = V.X.length; let tree = true; for (let i = 1; i < n; i++) if (!(V.PA[i] >= 0 && V.PA[i] < i)) tree = false;
    const rnd = L.rng(seed + 100); let hit = 0, tot = 0; while (tot < 4000) { const y = rnd(), x = (rnd() * 2 - 1) * L.WMAX; if (!L.inside(x, y, 0.94)) continue; tot++; if (V.nearest(x, y, 0.03)) hit++; }
    const r = V.radii(); let widest = 0; for (let i = 1; i < n; i++) if (r[i] > r[widest]) widest = i;
    say('  seed ' + seed + ': nodes ' + n + ', steps ' + V.k + ', sources left ' + V.sources + ', ' + ms + ' ms, coverage ' + (100 * hit / tot).toFixed(1) + '%, widest node ' + widest + ', root radius ' + r[0].toFixed(4));
    if (tree) a++; if (hit / tot >= 0.95) b++; if (n >= 800 && n <= 9000 && ms < 2000) c++; if (widest <= 1) d++; }
  verdict('B5a', a === 5, 'one tree: ' + a + '/5'); verdict('B5b', b === 5, '95% of blade within 0.03 of a vein: ' + b + '/5'); verdict('B5c', c === 5, 'size and time: ' + c + '/5'); verdict('B5d', d === 5, 'widest at the base: ' + d + '/5'); }

// ---- B6 season
{ let mono = true, prev = Infinity; for (let d = 182; d <= 324; d++) { const p = L.season(d, 0.5, true, 1); if (p.chl > prev + 1e-12) mono = false; prev = p.chl; }
  const j = L.season(196, 0.5, true, 1), o = L.season(298, 0.5, true, 1), hi = L.season(298, 1, true, 1), lo = L.season(298, 0.25, false, 1);
  say('\nB6 15 July ' + JSON.stringify(j) + '\n   25 October ' + JSON.stringify(o));
  verdict('B6a', mono, 'chlorophyll never rises after 1 July'); verdict('B6b', (o.car / o.chl) / (j.car / j.chl) > 3, 'carotenoid:chlorophyll ratio up x' + ((o.car / o.chl) / (j.car / j.chl)).toFixed(1)); verdict('B6c', hi.anth > 3 * lo.anth, 'anthocyanin bright+cold ' + hi.anth.toFixed(2) + ' against dim+mild ' + lo.anth.toFixed(2)); }

const fails = Object.keys(res).filter(k => !res[k]); say('\n' + (Object.keys(res).length - fails.length) + ' of ' + Object.keys(res).length + ' passed' + (fails.length ? '; failed: ' + fails.join(', ') : ''));
