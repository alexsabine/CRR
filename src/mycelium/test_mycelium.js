// Bets are in BETS.md, written before the model was first run. This file runs B1 to B9 against the model inside mycelium.html.
// Usage: node test_mycelium.js > test_output.txt      (B10, the page itself, is in test_page.js)
const fs = require('fs'), path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', '..', 'mycelium.html'), 'utf8');
const src = html.match(/<script id="model">([\s\S]*?)<\/script>/)[1];
const mod = { exports: {} }; new Function('module', 'globalThis', src)(mod, {}); const M = mod.exports, P = M.P;
const say = (...a) => console.log(...a), res = {}, SEEDS = [1, 2, 3, 4, 5];
const verdict = (k, ok, note) => { res[k] = ok; say((ok ? 'PASS ' : 'FAIL ') + k + '  ' + note); };
const std = (seed, o) => M.create(Object.assign({ seed, inoculum: [6, 10], litter: 0, moisture: 0.7 }, o || {}));
const A = [6, 10], B = [12, 10];
say('settings: ' + JSON.stringify(P)); say('');
const points = W => { const s = []; for (const e of W.edges) if (e.alive) for (let i = 0; i < e.pts.length; i += 2) s.push(e.pts[i], e.pts[i + 1]); return s; };
const key = (x, y) => Math.round(x * 2000) + ':' + Math.round(y * 2000);
const offRoute = (x, y) => { const t = Math.max(0, Math.min(1, (x - A[0]) / (B[0] - A[0]))); return Math.hypot(x - (A[0] + t * (B[0] - A[0])), y - A[1]) > 3; };
function gone(W, set) { const now = new Set(), p = points(W); for (let i = 0; i < p.length; i += 2) now.add(key(p[i], p[i + 1])); let g = 0; for (const k of set) if (!now.has(k)) g++; return set.length ? g / set.length : NaN; }
function offSet(W) { const p = points(W), s = []; for (let i = 0; i < p.length; i += 2) if (offRoute(p[i], p[i + 1])) s.push(key(p[i], p[i + 1])); return s; }

// ---- B1 loops
{ let a = 0, b = 0; const rows = []; for (const s of SEEDS) { const W0 = M.runTo(std(s, { fusion: false }), 12), W1 = M.runTo(std(s), 12), l0 = M.stats(W0).loops, l1 = M.stats(W1).loops; rows.push(s + ': ' + l0 + ' / ' + l1); if (l0 === 0) a++; if (l1 >= 5) b++; }
  say('B1 cyclomatic number at day 12, fusion off / on, by seed:  ' + rows.join('   ')); verdict('B1a', a === 5, 'no loops without fusion: ' + a + '/5'); verdict('B1b', b === 5, 'at least 5 loops with fusion: ' + b + '/5'); }

// ---- B2, B4 new food; B3 a cut
{ let a = 0, b = 0, c = 0, d = 0, e4 = 0, over = 0, c3a = 0, c3b = 0, c3c = 0; say('\nB2/B3/B4 by seed:');
  for (const s of SEEDS) { const W = M.runTo(std(s), 12), nb = M.addBlock(W, B[0], B[1], { rot: 0 }), b0 = W.blocks[0]; while (nb.tContact < 0 && W.t < 40) M.step(W); const tc = nb.tContact, set = offSet(W);
    const Wc = M.runTo(std(s), tc < 0 ? 40 : tc), setC = offSet(Wc);
    let line = '  seed ' + s + ': contact ' + (tc < 0 ? 'never' : (tc - 12).toFixed(2) + ' d after placing');
    if (tc >= 0) { if (tc - 12 <= 5) a++; let emax = 0; const Es = {};
      for (let day = 1; day <= 20; day++) { M.runTo(W, tc + day); const E = M.efficiency(W, b0, nb); Es[day] = E; emax = Math.max(emax, E);
        if (day === 10) { const w = M.widest(W, b0, nb); line += '; widest path at +10 d: thinnest ' + (w ? w.thinnest : '-') + ', length ' + (w ? w.length.toFixed(1) : '-') + ' (straight 6.0)'; if (w && w.thinnest >= 3 && w.length <= 9) b++; }
        if (day === 15) { M.runTo(Wc, tc + 15); const g1 = gone(W, set), g0 = gone(Wc, setC); line += '; off-route withdrawn at +15 d: ' + (100 * g1).toFixed(0) + '% of ' + set.length + ' points (no new wood: ' + (100 * g0).toFixed(0) + '% of ' + setC.length + ')'; if (g1 >= 0.30) c++; if (g1 - g0 >= 0.10) d++; } }
      line += '; E at +1 d ' + Es[1].toFixed(4) + ', +20 d ' + Es[20].toFixed(4) + ', largest ' + emax.toFixed(4); if (Es[20] >= 1.5 * Es[1]) e4++; if (emax > 1) over++;
      // the cut, on a fresh copy of the same seed
      const V = M.runTo(std(s), 12), vb = M.addBlock(V, B[0], B[1], { rot: 0 }); M.runTo(V, tc + 15); const v0 = V.blocks[0], G0 = M.conductance(V, v0, vb), tCut = V.t; let nc = 0; for (let y = 8; y <= 12.001; y += 0.3) nc += M.cut(V, 9, y, 0.45);
      const G1 = M.conductance(V, v0, vb); M.runTo(V, tCut + 8); const G2 = M.conductance(V, v0, vb); let nf = 0; for (let i = 0; i < V.fusions.length; i += 3) if (V.fusions[i + 2] > tCut && Math.abs(V.fusions[i] - 9) < 1.5 && V.fusions[i + 1] > 6.5 && V.fusions[i + 1] < 13.5) nf++;
      line += '\n          cut ' + nc + ' strands: G before ' + G0.toFixed(2) + ', just after ' + G1.toFixed(2) + ', 8 d later ' + G2.toFixed(2) + '; fusions near the cut since: ' + nf; if (G1 < 0.5 * G0) c3a++; if (G2 > 0 && G2 >= 0.5 * G0) c3b++; if (nf >= 1) c3c++; }
    say(line); }
  verdict('B2a', a === 5, 'contact within 5 days: ' + a + '/5'); verdict('B2b', b >= 4, 'direct route of 3 hyphae or more at +10 d: ' + b + '/5'); verdict('B2c', c >= 4, '30% of off-route strand withdrawn at +15 d: ' + c + '/5'); verdict('B2d', d >= 4, '10 points more than with no new wood: ' + d + '/5');
  verdict('B3a', c3a >= 4, 'conductance halved by the cut: ' + c3a + '/5'); verdict('B3b', c3b >= 4, 'recovered to half within 8 d: ' + c3b + '/5'); verdict('B3c', c3c >= 4, 'a new fusion near the cut: ' + c3c + '/5');
  verdict('B4', e4 >= 4 && over === 0, 'E at +20 d at least 1.5 x E at +1 d: ' + e4 + '/5; seeds with E above 1: ' + over); }

// ---- B5 branch timing
{ let ok = 0; say('\nB5 time between branchings at day 30 (candidate value for comparison ' + M.CANDIDATE_CV.toFixed(4) + '):'); for (const s of SEEDS) { const st = M.stats(M.runTo(std(s), 30)); say('  seed ' + s + ': CV ' + st.cv.toFixed(3) + ', n = ' + st.cvN + ', mean ' + st.ivMean.toFixed(2) + ' d'); if (st.cv >= 0.3 && st.cv <= 1.2) ok++; }
  verdict('B5', ok === 5, 'my guess, CV between 0.3 and 1.2: ' + ok + '/5'); }

// ---- B6 bookkeeping
{ const W = std(1); let worstNode = 0, worstBal = 0, bad = 0, checks = 0, nb = null;
  while (W.t < 20) { M.step(W); if (!nb && W.t >= 12) nb = M.addBlock(W, B[0], B[1], { rot: 0 });
    for (const t of W.tips) if (t.alive && !(t.C >= 0 && t.C < P.Cb && t.F >= 0 && t.F < P.Fb)) bad++; for (const e of W.edges) if (e.alive && !(e.cU >= 0 && e.cU < P.Ub && e.cD >= 0 && e.cD < P.Db * e.n)) bad++; for (const b of W.blocks) if (!(b.cF >= 0 && b.cF < P.fruitF && b.col >= 0 && b.col < b.colNeed)) bad++;
    if (W.steps % 50 === 0) { checks++; M.solve(W, 20000, 1e-13); const N = W.nx.length, net = new Float64Array(N), leak = new Uint8Array(N); let src = 0, snk = 0;
      for (const e of W.edges) if (e.alive) { const q = P.kap * e.n / Math.max(0.03, e.len) * (W.p[e.a] - W.p[e.b]); net[e.a] -= q; net[e.b] += q; }
      for (const t of W.tips) if (t.alive) { leak[t.edge.b] = 1; snk += t.g * W.p[t.edge.b]; } for (const b of W.blocks) { leak[b.hub] = 1; if (b.state === 'source') src += b.gUp * (b.Pb - W.p[b.hub]); else if (b.state === 'col') snk += b.gCol * W.p[b.hub]; }
      for (const f of W.fruits) if (f.state === 0) snk += P.gFruit * W.p[W.blocks[f.block].hub]; for (let i = 0; i < N; i++) if (W.na[i]) { src += P.kr * W.nr[i] * (1 - W.p[i]); snk += 1e-7 * W.p[i]; if (W.nr[i] !== 0) leak[i] = 1; }
      for (let i = 0; i < N; i++) if (W.na[i] && !leak[i]) worstNode = Math.max(worstNode, Math.abs(net[i]) / src); worstBal = Math.max(worstBal, Math.abs(src - snk) / src); } }
  say('\nB6 seed 1, days 0 to 20, ' + checks + ' tight solves: worst junction residual ' + worstNode.toExponential(2) + ' of the total; worst source-sink mismatch ' + worstBal.toExponential(2) + ' (the 1e-7 regulariser is counted as a sink); counts out of range ' + bad);
  verdict('B6a', worstNode < 1e-6, 'current conserved at junctions'); verdict('B6b', worstBal < 1e-6, 'sources equal sinks'); verdict('B6c', bad === 0, 'every count within [0, threshold) after every step'); }

// ---- B7 moisture
{ let a = 0, b = 0, c = 0; const rows = []; for (const s of SEEDS) { const run = m => { const W = M.runTo(std(s, { moisture: m }), 12); M.addBlock(W, B[0], B[1], { rot: 0 }); M.runTo(W, 60); return W.ev.fruit; }, f8 = run(0.8), f3 = run(0.3), l2 = M.stats(M.runTo(std(s, { moisture: 0.2 }), 8)).len, l7 = M.stats(M.runTo(std(s), 8)).len;
    rows.push('  seed ' + s + ': clusters started by day 60, wet ' + f8 + ', dry ' + f3 + '; length at day 8, moisture 0.2: ' + l2.toFixed(0) + ' cm, 0.7: ' + l7.toFixed(0) + ' cm'); if (f8 >= 1) a++; if (f3 === 0) b++; if (l2 < 0.75 * l7) c++; }
  say('\nB7'); rows.forEach(r => say(r)); verdict('B7a', a >= 4, 'fruits when wet: ' + a + '/5'); verdict('B7b', b === 5, 'none when dry: ' + b + '/5'); verdict('B7c', c === 5, 'dry soil slows growth: ' + c + '/5'); }

// ---- B8 dense near food
{ let ok = 0; const rows = []; for (const s of SEEDS) { const W = std(s, { keepBranches: true }); let near = 0, far = 0; while (W.t < 14) { M.step(W); for (const t of W.tips) if (t.alive) { const r = Math.hypot(t.x - A[0], t.y - A[1]); if (r < 3) near += t.v * P.dt; else if (r > 5) far += t.v * P.dt; } }
    let bn = 0, bf = 0; for (let i = 0; i < W.branches.length; i += 2) { const r = Math.hypot(W.branches[i] - A[0], W.branches[i + 1] - A[1]); if (r < 3) bn++; else if (r > 5) bf++; } const dn = bn / near, df = bf / far; rows.push(s + ': ' + dn.toFixed(2) + ' / ' + df.toFixed(2)); if (dn >= 2 * df) ok++; }
  say('\nB8 branchings per cm grown, within 3 cm / beyond 5 cm:  ' + rows.join('   ')); verdict('B8', ok >= 4, 'twice as dense near the wood: ' + ok + '/5'); }

// ---- B9 cost
{ let mxN = 0, mxT = 0, mxL = 0, ms = 0, steps = 0; for (const s of [1, 2]) { const W = M.runTo(std(s), 12); M.addBlock(W, B[0], B[1], { rot: 0 }); const t0 = process.hrtime.bigint(), s0 = W.steps; for (let d = 13; d <= 60; d++) { M.runTo(W, d); const st = M.stats(W); mxN = Math.max(mxN, st.nodes); mxT = Math.max(mxT, st.tips); mxL = Math.max(mxL, st.len); } ms += Number(process.hrtime.bigint() - t0) / 1e6; steps += W.steps - s0; }
  say('\nB9 mean step ' + (ms / steps).toFixed(3) + ' ms (includes a stats call each day; this machine is also busy with other work); most nodes ' + mxN + ', tips ' + mxT + ', strand ' + mxL.toFixed(0) + ' cm'); verdict('B9', ms / steps < 2 && mxN <= 6000 && mxT <= 600 && mxL <= 2500, 'under 2 ms a step and within the size limits'); }

const keys = Object.keys(res); say('\n' + keys.filter(k => res[k]).length + ' of ' + keys.length + ' passed. Failed: ' + (keys.filter(k => !res[k]).join(', ') || 'none'));
