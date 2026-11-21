// B4 (no clipping) and the new half of B2 (scheduled times): the whole piece through OfflineAudioContexts, in stretches of 24 beats with a 14-beat run-in
// (one context for all six minutes holds every node at once and takes over half an hour on this machine). Bets are in bets.md (written first).
const { chromium } = require('playwright'), path = require('path'), W = require('./model.js');
(async () => {
  const br = await chromium.launch(), p = await br.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.setContent('<!doctype html><title>h</title>'); await p.addScriptTag({ path: path.join(__dirname, 'model.js') }); await p.addScriptTag({ path: path.join(__dirname, 'audio.js') });
  const tl = W.timeline(), byI = new Map(tl.map(e => [e.i, e])), STEP = 24, END = W.END_BEATS + 8; const t0 = Date.now();
  async function pass(mix, lo, hi, label) { let peak = 0, pb = 0, worst = 0, n = 0, diff = 0, sum = 0, secs = 0; const rows = [];
    for (let from = lo; from < hi; from += STEP) { const r = await p.evaluate(([from, to, mix]) => WILLOW.renderOffline({ from, to, mix, keepLog: true }), [from, Math.min(hi, from + STEP), mix]);
      if (r.peak > peak) { peak = r.peak; pb = r.peakBeat; } diff += r.diff; sum += r.sum; secs += r.seconds; rows.push(...r.rms); for (const l of r.log) { const e = byI.get(l.i); if (e && e.b >= from) { n++; worst = Math.max(worst, Math.abs(l.at - e.b * W.BEAT)); } } }
    return { peak, pb, worst, n, width: diff / sum, secs, rows, label }; }
  const a = await pass(undefined, 0, END);
  console.log('offline render:', a.secs.toFixed(1), 's of audio measured, in', ((Date.now() - t0) / 1000).toFixed(0), 's | page errors', errs.length, errs.slice(0, 3).join(' | '));
  console.log('B2 (new side): scheduled time minus beat x 60/66, worst over', a.n, 'events of', tl.length, ':', a.worst.toExponential(2), 's', a.worst <= 1e-6 && a.n >= tl.length - 14 ? 'PASS' : 'FAIL');
  console.log('B4 default mix: peak', a.peak.toFixed(4), '=', (20 * Math.log10(a.peak)).toFixed(2), 'dBFS at beat', a.pb.toFixed(2), a.peak < 1 ? (a.peak <= .891 ? 'PASS (and within the -1 dBFS target)' : 'PASS (below 0 dBFS, but above the -1 dBFS target)') : 'FAIL', '| stereo difference/sum', a.width.toFixed(3));
  console.log('   level by 8 beats [beat, RMS dB, peak]:', a.rows.map(x => x.join(' ')).join(' | '));
  const m = await pass({ reverb: 1, wind: 1, leaf: 1, wood: 1, water: 1 }, 168, 312);
  console.log('B4 every slider at maximum (beats 168-312, the loud part): peak', m.peak.toFixed(4), '=', (20 * Math.log10(m.peak)).toFixed(2), 'dBFS at beat', m.pb.toFixed(2), m.peak < 1 ? 'PASS' : 'FAIL');
  await br.close();
})();
