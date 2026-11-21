/* Runs the bets in BETS.md against hive_model.js. Usage: node test_hive.js [bet ...]  */
const H = require('./hive_model.js');
const want = process.argv.slice(2), on = k => !want.length || want.includes(k);
const seeds = [11, 22, 33, 44, 55], f = (v, n) => v === null || v === undefined ? 'n/a' : v.toFixed(n === undefined ? 2 : n);
const out = [];
const say = s => { console.log(s); out.push(s); };
function share(W, id) { const m = H.measure(W); return m.nEmployed ? (m.employed[id] || 0) / m.nEmployed : 0; }

if (on('B1')) { say('\nB1  richer of two patches, then swapped. Pass: >=60% at 300 s and >=60% on the new one at 660 s, in 4 of 5 seeds');
  let ok = 0; for (const s of seeds) { const W = H.create(s, { autoBloom: false, patches: [{ az: -30, d: 900, sp: 1, sugar: 0.9 }, { az: 30, d: 900, sp: 0, sugar: 0.45 }] });
    const a = W.patches[0], b = W.patches[1]; let line = '';
    for (let t = 60; t <= 300; t += 60) { H.run(W, 60); line += ' ' + t + 's:' + f(share(W, a.id)) ; } const s1 = share(W, a.id), n1 = H.measure(W).nEmployed;
    a.sugar = 0.45; b.sugar = 0.9; let l2 = '';
    for (let t = 360; t <= 660; t += 60) { H.run(W, 60); l2 += ' ' + t + 's:' + f(share(W, b.id)); } const s2 = share(W, b.id), n2 = H.measure(W).nEmployed;
    const p = s1 >= 0.6 && s2 >= 0.6; if (p) ok++; say(`  seed ${s}: share on rich patch${line} (n=${n1}) | after swap, share on newly rich${l2} (n=${n2})  ${p ? 'pass' : 'FAIL'}`); }
  say(`  B1 ${ok >= 4 ? 'PASS' : 'FAIL'} (${ok}/5)`); }

if (on('B2')) { say('\nB2  junctions settle to 120 degrees. Pass: settled (>120 s old) mean distance < 2.0 deg, having started > 4.0; control without flow stays > 4.0');
  for (const flow of [true, false]) { const W = H.create(7, { empty: true, flow }); W.bees.forEach((b, i) => { if (i % 2 === 0) { b.th[2] = 0.05; } });
    H.run(W, 600); const all = H.junctionStats(W), old = H.junctionStats(W, 120), m = H.measure(W);
    let s = 0, n = 0; for (const j of W.junc) { if (!H.juncFree(W, j)) continue; const a = H.juncAngles(W, j); s += a[0] + a[1] + a[2]; n += 3; }
    say(`  flow ${flow ? 'on ' : 'off'}: cells built ${m.built}/${m.cells}, builders ${m.n[2]}; junctions older than 120 s: n=${old.n}, distance from 120 now ${f(old.dev)} deg, at formation ${f(old.dev0)} deg; all free junctions n=${all.n}, ${f(all.dev)} deg; mean angle ${f(n ? s / n : null, 4)} (always 120 by arithmetic)`);
    if (flow) say(`  B2 ${old.n > 20 && old.dev < 2 && old.dev0 > 4 ? 'PASS' : 'FAIL'}`); else say(`  B2 control ${old.n > 20 && old.dev > 4 ? 'PASS' : 'FAIL'}`); } }

if (on('B3')) { say('\nB3  the dance matters. Pass: mean loads over 900 s at least 20% lower with the dance off');
  let A = 0, B = 0; for (const s of seeds) { const W1 = H.create(s, { dance: true }), W0 = H.create(s, { dance: false }); H.run(W1, 900); H.run(W0, 900); A += W1.loads; B += W0.loads;
    say(`  seed ${s}: loads with dance ${f(W1.loads, 1)} (recruits ${W1.nRecruit}, found ${W1.nRecruitOk}; scouts ${W1.nScout}, found ${W1.nScoutOk}; abandoned ${W1.nAbandon}; stop signals ${W1.nStop}) | without ${f(W0.loads, 1)} (scouts ${W0.nScout}, found ${W0.nScoutOk})`); }
  const drop = 1 - B / A; say(`  mean with ${f(A / 5, 1)}, without ${f(B / 5, 1)}, fall ${f(drop * 100, 1)}%  B3 ${drop >= 0.2 ? 'PASS' : 'FAIL'}`); }

if (on('B4')) { say('\nB4  task-switch interval CV, reported as measured (candidate value from the CRR programme: 0.159). No pass mark.');
  for (const s of seeds) { const W = H.create(s); H.run(W, 120); W.intervals.length = 0; const n0 = W.nSwitch; W.bees.forEach(b => b.last = -1); const all = []; for (let i = 0; i < 26; i++) { H.run(W, 30); } 
    const xs = W.intervals, mean = xs.reduce((a, b) => a + b, 0) / (xs.length || 1); say(`  seed ${s}: switches ${W.nSwitch - n0}, intervals n=${xs.length}${xs.length >= 600 ? ' (capped at 600, most recent)' : ''}, mean ${f(mean, 1)} s, CV ${f(H.cv(xs), 3)}; tasks now ${H.measure(W).n.join('/')} (${H.TASKS.join('/')})`); } }

if (on('B5')) { say('\nB5  alarm recruits guards; they stand down. Pass (4 of 5): peak guards >= 2x before, hornet gone within 90 s, back within 2 of before 120 s after it leaves');
  let ok = 0; for (const s of seeds) { const W = H.create(s); H.run(W, 60); let g0 = 0; for (let i = 0; i < 60; i++) { H.run(W, 1); g0 += W.n[4]; } g0 /= 60; H.sendHornet(W); let peak = 0, gone = null; for (let i = 0; i < 180; i++) { H.run(W, 1); peak = Math.max(peak, W.n[4]); if (gone === null && !W.hornet.on) gone = i + 1; if (gone !== null && i + 1 >= gone + 120) break; }
    const g1 = W.n[4], p = peak >= 2 * g0 && gone !== null && gone <= 90 && Math.abs(g1 - g0) <= 2; if (p) ok++; say(`  seed ${s}: guards before ${f(g0, 1)}, peak ${peak}, hornet gone after ${gone === null ? 'never' : gone + ' s'}, alarms released ${W.nAlarm}, guards 120 s later ${g1}  ${p ? 'pass' : 'FAIL'}`); }
  say(`  B5 ${ok >= 4 ? 'PASS' : 'FAIL'} (${ok}/5)`); }

if (on('B6')) { say('\nB6  work answers need. Pass (4 of 5): >=3 more fanners when hot, hot-spell temperature < 36.5 C');
  let ok = 0; for (const s of seeds) { const W = H.create(s); H.run(W, 100); let a = 0, b = 0, T = 0; for (let i = 0; i < 100; i++) { H.run(W, 1); a += W.n[3]; } W.weather = 'hot'; H.run(W, 100); for (let i = 0; i < 100; i++) { H.run(W, 1); b += W.n[3]; T += W.temp; }
    a /= 100; b /= 100; T /= 100; const p = b - a >= 3 && T < 36.5; if (p) ok++; say(`  seed ${s}: fanners fair ${f(a, 1)}, hot ${f(b, 1)}, hive ${f(T, 2)} C in the hot spell  ${p ? 'pass' : 'FAIL'}`); }
  say(`  B6 ${ok >= 4 ? 'PASS' : 'FAIL'} (${ok}/5)`); }

if (on('B7')) { say('\nB7  the dance says where (consistency). Pass: mean signed errors < 2 deg and < 3%');
  const W = H.create(5); let ea = 0, ed = 0, n = 0, sa = 0; const seen = new Set(); for (let i = 0; i < 600; i++) { H.run(W, 1); for (const r of W.runs) { if (seen.has(r)) continue; seen.add(r); const e = r.ang / (Math.PI / 180) - (r.taz - H.SET.SUN_AZ); ea += e; sa += Math.abs(e); ed += r.dur / (r.td / 1000) - 1; n++; } }
  say(`  waggle runs ${n}; angle minus (bearing - sun): mean ${f(ea / n, 2)} deg, mean absolute ${f(sa / n, 2)} deg; duration against distance/1000: mean error ${f(100 * ed / n, 2)}%  B7 ${n > 50 && Math.abs(ea / n) < 2 && Math.abs(ed / n) < 0.03 ? 'PASS' : 'FAIL'}`); }
require('fs').writeFileSync(__dirname + '/' + (process.env.OUT || 'test_output_latest.txt'), out.join('\n') + '\n');
