// B5 (Node half), B6, B7 (while growing), B8. Bets are in bets.md (written first).
const W = require('./model.js');
const med = a => { a = a.slice().sort((x, y) => x - y); return a[a.length >> 1]; };
// B5: cost of one model step in the storm
for (const q of ['high', 'mid', 'low']) { const S = W.makeSim(W.SEED, q); S.seek(230); const ts = []; for (let i = 0; i < 400; i++) { const a = process.hrtime.bigint(); S.step(1 / 60, 230 + i / 60 / W.BEAT); ts.push(Number(process.hrtime.bigint() - a) / 1e6); } const m = med(ts); console.log('B5 (Node) quality', q, ':', S.nl, 'leaves,', S.nw, 'shoots; model step median', m.toFixed(2), 'ms', q === 'high' ? (m < 2 ? 'PASS' : 'FAIL (bet was under 2 ms)') : ''); }
// B6: the CV the page prints is the CV of the raw intervals. Run LEAF SONG at 60 steps a second.
{ const S = W.makeSim(W.SEED, 'mid'); S.seek(176); S.rawIntervals = []; const dtb = 1 / 60 / W.BEAT; let b = 176; const report = [];
  while (b < 248) { S.step(1 / 60, b); b += dtb; if (Math.abs(b - 216) < dtb / 2 || Math.abs(b - 196) < dtb / 2 || Math.abs(b - 247.9) < dtb / 2) { const shown = S.cv(), raw = S.rawIntervals.slice(-600), m = raw.reduce((a, x) => a + x, 0) / raw.length, sd = Math.sqrt(raw.reduce((a, x) => a + (x - m) * (x - m), 0) / raw.length); report.push({ beat: Math.round(b), shown: shown.cv.toFixed(3), recomputed: (sd / m).toFixed(3), n: shown.n, meanInterval: m.toFixed(2) }); } }
  const ok = report.every(r => r.shown === r.recomputed); console.log('B6 shown against recomputed from raw intervals:', JSON.stringify(report), ok ? 'PASS' : 'FAIL');
  const all = S.rawIntervals, m = all.reduce((a, x) => a + x, 0) / all.length, sd = Math.sqrt(all.reduce((a, x) => a + (x - m) * (x - m), 0) / all.length);
  console.log('   for the record: all', all.length, 'intervals from beat 176 to 248 pooled: CV', (sd / m).toFixed(3), '| candidate 1/(2 pi) =', (1 / (2 * Math.PI)).toFixed(3), '| no bet on this and nothing tuned'); }
// B7 while growing
{ const S = W.makeSim(W.SEED, 'high'); let worst = 0; for (const b of [20, 60, 75, 90, 110, 130, 200]) { S.seek(b); worst = Math.max(worst, W.leonardoError(S.tree, S.grow, S.wgrow)); } console.log('B7 during growth (beats 20 to 200): worst relative error', worst.toExponential(2), worst < 1e-9 ? 'PASS' : 'FAIL'); }
// B8: wind seen against wind heard, whole piece, every quarter beat
{ const S = W.makeSim(W.SEED, 'low'); S.seek(0); const xs = [], ys = []; let b = 0, acc = 0, n = 0, next = .25; const dtb = 1 / 60 / W.BEAT;
  while (b < W.END_BEATS) { S.step(1 / 60, b); acc += S.tipSpeed; n++; b += dtb; if (b >= next) { xs.push(S.wind.sound(next - .125)); ys.push(acc / n); acc = 0; n = 0; next += .25; } }
  const mx = xs.reduce((a, x) => a + x, 0) / xs.length, my = ys.reduce((a, x) => a + x, 0) / ys.length; let sxy = 0, sxx = 0, syy = 0; for (let i = 0; i < xs.length; i++) { sxy += (xs[i] - mx) * (ys[i] - my); sxx += (xs[i] - mx) ** 2; syy += (ys[i] - my) ** 2; }
  const r = sxy / Math.sqrt(sxx * syy); console.log('B8 correlation of wind-sound envelope with mean shoot-tip speed over', xs.length, 'samples:', r.toFixed(3), r > .5 ? 'PASS' : 'FAIL'); }
