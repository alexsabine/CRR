// Bets B1-B7 and B9 (see BETS.md). Run: node test-model.js   Output is also written to results-model.txt
const F = require('./load.js'), fs = require('fs');
const out = []; let fails = 0;
const say = (id, ok, msg) => { if (!ok) fails++; const s = `${ok ? 'PASS' : 'FAIL'}  ${id}  ${msg}`; out.push(s); console.log(s); };
const md = d => String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');

// B1
{ let eq = 0, bad = [], about = 0;
  for (const y of [2026, 2027]) { const ev = F.generateYearEvents(y); for (const name in F.MOV[y]) { const e = ev.find(e => e.name === name); if (e && md(e.date) === F.MOV[y][name] && e.date.getFullYear() === y) eq++; else bad.push(y + ' ' + name + ' -> ' + (e ? md(e.date) : 'missing')); } }
  const e28 = F.generateYearEvents(2028); for (const name in F.MOV[2026]) if (e28.find(e => e.name === name + ' (about)')) about++;
  say('B1', eq === 20 && about === 10, `movable feasts equal to table: ${eq}/20; marked "(about)" in 2028: ${about}/10 ${bad.join('; ')}`); }
// B2
{ const g = (y, n) => md(F.generateYearEvents(y).find(e => e.name === n).date);
  const r = [g(2027, 'Easter Sunday'), g(2026, 'Easter Sunday'), g(2026, 'Thanksgiving'), g(2027, 'Thanksgiving')];
  say('B2', r.join() === '03-28,04-05,11-26,11-25', `Easter 2027 ${r[0]}, Easter 2026 ${r[1]}, Thanksgiving 2026 ${r[2]}, 2027 ${r[3]}`); }
// B3
{ let worstMid = -99, worstNoon = 0, n = 0, bad = 0;
  for (const lat of [-35, 0, 35, 52, 60]) for (let mo = 0; mo < 12; mo++) { const t0 = Date.UTC(2026, mo, 15); const mid = F.sunPosition(new Date(t0), lat, 0).alt * 180 / Math.PI; if (mid > worstMid) worstMid = mid;
    let best = -9, bt = 0; for (let k = 0; k < 1440; k++) { const a = F.sunPosition(new Date(t0 + k * 60000), lat, 0).alt; if (a > best) { best = a; bt = k; } } const off = Math.abs(bt - 720); if (off > worstNoon) worstNoon = off; n++; if (mid >= 0 || off > 20) bad++; }
  const j = F.sunPosition(new Date(Date.UTC(2026, 5, 21, 12)), 51.5, -0.1).alt * 180 / Math.PI, d = F.sunPosition(new Date(Date.UTC(2026, 11, 21, 12)), 51.5, -0.1).alt * 180 / Math.PI;
  say('B3', bad === 0 && Math.abs(j - 61.9) < 0.5 && Math.abs(d - 15.1) < 0.5, `${n} cases; highest midnight altitude ${worstMid.toFixed(2)} deg; largest offset of solar noon from 12:00 UTC ${worstNoon} min; London noon 21 Jun ${j.toFixed(2)} deg, 21 Dec ${d.toFixed(2)} deg`); }
// B4
{ const a = F.moonPosition(new Date(Date.UTC(2026, 7, 12, 17, 46)), 52, 0), b = F.moonPosition(new Date(Date.UTC(2026, 2, 3, 11, 34)), 52, 0), ea = a.elong * 180 / Math.PI, eb = b.elong * 180 / Math.PI;
  say('B4', ea < 3 && eb > 177, `elongation at solar eclipse ${ea.toFixed(2)} deg (illum ${a.illum.toFixed(4)}); at lunar eclipse ${eb.toFixed(2)} deg (illum ${b.illum.toFixed(4)})`); }
// B5
{ let ok = true; const notes = [];
  for (const [name, seed] of [['broad', 1000], ['tall', 1037], ['birch', 1111]]) { const sp = F.SPECIES[name], t0 = Date.now(), tr = F.growTree(F.rng(seed), sp), ms = Date.now() - t0, sum = new Float64Array(tr.n); let worst = 0, thicker = 0;
    for (let j = 1; j < tr.n; j++) { sum[tr.P[j]] += Math.pow(tr.R[j], sp.pipe); if (tr.R[j] > tr.R[tr.P[j]] * (1 + 1e-6)) thicker++; }
    for (let j = 0; j < tr.n; j++) if (tr.K[j] > 0) { const e = Math.abs(sum[j] - Math.pow(tr.R[j], sp.pipe)) / Math.pow(tr.R[j], sp.pipe); if (e > worst) worst = e; }
    let top = 0; for (let j = 0; j < tr.n; j++) if (tr.Y[j] > top) top = tr.Y[j]; const ratio = 2 * tr.R[0] / top;
    const good = worst < 1e-4 && thicker === 0 && ratio > 1 / 50 && ratio < 1 / 15 && tr.n >= 1500 && tr.n <= 16000; if (!good) ok = false;
    notes.push(`${name}: ${tr.n} nodes (${tr.structural} structural) in ${ms} ms, pipe error ${worst.toExponential(1)}, thicker children ${thicker}, trunk diameter/height 1/${(1 / ratio).toFixed(1)}, height ${top.toFixed(2)}`); }
  say('B5', ok, notes.join(' | ')); }
// B6
{ const p = (m, d, lat) => F.phenology(new Date(2026, m, d), lat, 0), a = p(0, 15, 52), b = p(3, 15, 52), c = p(6, 1, 52), d = p(9, 20, 52), e = p(10, 21, 52), s = p(0, 15, -35);
  const ok = a.cover < 0.08 && b.cover > 0.1 && b.cover < 0.9 && c.cover > 0.95 && c.turn === 0 && d.turn > 0.5 && d.cover > 0.3 && e.cover > 0.02 && e.cover < 0.3 && s.cover > 0.95;
  say('B6', ok, `cover 15 Jan ${a.cover.toFixed(3)}, 15 Apr ${b.cover.toFixed(3)}, 1 Jul ${c.cover.toFixed(3)} (turn ${c.turn}), 20 Oct ${d.cover.toFixed(3)} (turn ${d.turn.toFixed(2)}), 21 Nov ${e.cover.toFixed(3)} (${e.stage}); south 15 Jan ${s.cover.toFixed(3)}`); }
// B7 and B9
{ const trees = (letGo) => [-0.84, -0.45, -0.03, 0.37, 0.8].map(x => ({ x, base: 0.215, cy: 0.6, rx: 0.2, ry: 0.2, leaf: 0.005, letGo, C: 0 }));
  const envDay = { temp: 9, rain: 0, wind: 0.6, night: 0, crowd: 7 }, lg = F.phenologyAt(298, 0).letGo;
  const W = F.newWorld(5, { half: 0.89, trees: trees(lg), env: envDay, birds: 22 });
  for (let i = 0; i < 2000; i++) F.step(W, 1 / 60, envDay);
  const N = 20000, t0 = process.hrtime.bigint(); for (let i = 0; i < N; i++) F.step(W, 1 / 60, envDay); const ms = Number(process.hrtime.bigint() - t0) / 1e6 / N;
  say('B7', ms < 0.10, `mean model step ${ms.toFixed(4)} ms over ${N} steps (${W.parties.length} parties, ${W.birds.length} birds, ${W.leaves.length} leaves at the end); that is ${(ms / 16.67 * 100).toFixed(2)}% of a 60 Hz frame`);
  const W2 = F.newWorld(9, { half: 0.89, trees: trees(0), env: envDay, birds: 0 }); let cOK = true; for (let i = 0; i < 2 * 3600 * 20; i++) { F.step(W2, 1 / 20, envDay); for (const p of W2.parties) if (!(p.C >= 0 && p.C < 1)) cOK = false; }
  const envA = { temp: 9, rain: 0, wind: 0.5, night: 0, crowd: 0 }, W3 = F.newWorld(3, { half: 0.89, trees: trees(lg), env: envA, birds: 0 }); for (let i = 0; i < 600 * 30; i++) F.step(W3, 1 / 30, envA);
  const lgJ = F.phenologyAt(182, 0).letGo, W4 = F.newWorld(3, { half: 0.89, trees: trees(lgJ), env: envA, birds: 0 }); for (let i = 0; i < 600 * 30; i++) F.step(W4, 1 / 30, envA);
  say('B9', W2.stats.pauses > 0 && cOK && W3.stats.released > 0 && W4.stats.released === 0, `pauses in two hours ${W2.stats.pauses}; counts stayed in [0,1): ${cOK}; leaves released in ten minutes on 25 Oct ${W3.stats.released} (letGo ${lg.toFixed(2)}), on 1 Jul ${W4.stats.released}`); }
out.push(`${fails} failed`); console.log(`${fails} failed`);
fs.writeFileSync(__dirname + '/results-model.txt', new Date().toISOString() + '\n' + out.join('\n') + '\n', { flag: 'a' });
