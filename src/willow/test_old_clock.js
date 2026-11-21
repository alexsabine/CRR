// B2, B3 (timing), B10: run the ORIGINAL page's own playback code on a simulated 60 fps clock, with its audio functions replaced by loggers,
// and compare what it dispatched, and when, with what the new engine schedules. Bets are in bets.md (written first).
const { chromium } = require('playwright'), fs = require('fs'), path = require('path');
const W = require('./model.js'), SEED = W.SEED, OUT = process.argv[2] || '/tmp';
(async () => {
  const br = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] }), p = await br.newPage({ viewport: { width: 1280, height: 800 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(() => { let a = 1; const r = () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; Math.random = r; window.__seed = s => { a = s >>> 0; }; });
  await p.goto('file://' + path.resolve(__dirname, '../../song_of_willow.html')); await p.click('#splash'); await p.waitForTimeout(2500);
  const old = await p.evaluate((seed) => {
    const LOG = [], fake = { currentTime: 0, state: 'running' }, Q = []; ac = fake;
    const L = o => { o.at = fake.currentTime; LOG.push(o); };
    window.requestAnimationFrame = () => 0; window.setTimeout = (fn, ms) => { Q.push({ t: fake.currentTime + (ms || 0) / 1000, fn }); return 0; };
    initAudio = () => { }; robinG = {}; parrotG = {}; uAB = () => { }; setDr = (g, tr) => L({ t: 'drone', g, tr });
    pTone = (m, v, d) => L({ t: 'tone', midi: m, vel: v, dur: d }); pShim = (m, v, d) => L({ t: 'shim', midi: m, vel: v, dur: d }); pBass = (m, v, d) => L({ t: 'bass', midi: m, vel: v, dur: d }); pPad = (n, v, d) => L({ t: 'pad', notes: n, vel: v, dur: d }); pArp = (m, v, d) => L({ t: 'arp', midi: m, vel: v, dur: d });
    pLeaf = (v, c) => L({ t: 'leaf', vel: v, cnt: c }); pCreak = (v, d) => L({ t: 'creak', vel: v, dur: d }); pWind = (v, d) => L({ t: 'wind', vel: v, dur: d }); pDrip = (v, c) => L({ t: 'drip', vel: v, cnt: c }); pCavit = v => L({ t: 'cavit', vel: v }); pChoir = (n, v, d) => L({ t: 'choir', notes: n, vel: v, dur: d }); pWater = (v, d) => L({ t: 'water', vel: v, dur: d }); pRupture = (v, d) => L({ t: 'rupture', vel: v, dur: d });
    initRainbowChoir = () => L({ t: 'rbchoir', action: 'init' }); rbChoirSetGain = () => { }; rbChoirEnter = v => L({ t: 'rbchoir', action: 'enter', voice: v }); rbChoirMorph = (v, d) => L({ t: 'rbchoir', action: 'morph', vowel: v, dur: d }); rbChoirFade = d => L({ t: 'rbchoir', action: 'fade', dur: d });
    pRobinNote = (f, v, d, fem) => L({ t: 'robinNote', freq: f, vel: v, dur: d, female: !!fem }); pParrotSyllable = (n, v, d) => { if (n.m) L({ t: 'syll', midi: n.m, word: n.l, dur: d, idx: parrotState.noteIdx }); };
    for (const f of ['drawSky', 'drawRainbow', 'drawSpectralEddies', 'drawReflection', 'drawWater', 'drawKaraoke', 'drawCandleHint', 'drawRain', 'drawTree', 'drawRobins', 'drawParrot', 'drawCandle', 'drawLightning', 'drawMotes', 'drawOverlay', 'updateUI']) window[f] = () => { };
    __seed(seed); startSong(); let ts = lastT; const beats = 412, frames = Math.ceil(beats * 60 / 66 * 60);
    for (let i = 0; i < frames; i++) { fake.currentTime += 1 / 60; ts += 1000 / 60; for (let k = Q.length - 1; k >= 0; k--) if (Q[k].t <= fake.currentTime) { const q = Q.splice(k, 1)[0]; try { q.fn(); } catch (e) { } } frame(ts); }
    return { LOG, perched: parrotState.perched, playing };
  }, SEED);
  await br.close(); fs.writeFileSync(path.join(OUT, 'old_log.json'), JSON.stringify(old.LOG));
  const kinds = new Set(['tone', 'shim', 'bass', 'pad', 'arp', 'leaf', 'creak', 'wind', 'drip', 'cavit', 'choir', 'water', 'rupture']);
  const oldS = old.LOG.filter(e => kinds.has(e.t)), neuS = W.buildScore(SEED).filter(e => kinds.has(e.t));
  let bad = 0, maxLate = 0, minLate = 9, pitchBad = 0; const n = Math.min(oldS.length, neuS.length);
  for (let i = 0; i < n; i++) { const o = oldS[i], e = neuS[i], late = o.at - e.b * W.BEAT; if (o.t !== e.t || o.midi !== e.midi || JSON.stringify(o.notes) !== JSON.stringify(e.notes)) pitchBad++; maxLate = Math.max(maxLate, late); minLate = Math.min(minLate, late); if (late < -1e-9 || late > 1 / 60 + 1e-6) bad++; }
  console.log('page errors in original under the harness:', errs.length, errs.slice(0, 2).join(' | '));
  console.log('B2 sounding score events: original dispatched', oldS.length, 'new schedules', neuS.length, '| kind or pitch mismatches', pitchBad, '| original is late by', (minLate * 1000).toFixed(2), 'to', (maxLate * 1000).toFixed(2), 'ms | outside [0, 16.67 ms]:', bad, (bad || pitchBad || oldS.length !== neuS.length) ? 'FAIL' : 'PASS');
  const os = old.LOG.filter(e => e.t === 'syll'), ns = W.buildBirds(SEED).filter(e => e.t === 'syll');
  let sb = 0, worst = 0, worstK = 0; const first = os.slice(0, 26); first.forEach((o, i) => { const e = ns[i], late = o.at - e.b * W.BEAT, k = e.idx; if (o.midi !== e.midi || o.word !== e.word || Math.abs(o.dur - e.dur * W.BEAT) > 1e-9) sb++; if (late < -1e-9 || late > (k + 1) / 60 + 1e-6) sb++; if (late > worst) { worst = late; worstK = k; } });
  console.log('B3 timing: original sang', os.length, 'syllables in 412 beats (first at beat', (os[0].at / W.BEAT).toFixed(3) + '); first pass compared:', first.length, '| original late by up to', (worst * 1000).toFixed(1), 'ms (at note', worstK + ') | failures', sb, sb || first.length !== 26 ? 'FAIL' : 'PASS');
  if (os.length > 26) console.log('   original second pass began at beat', (os[26].at / W.BEAT).toFixed(2), '(random pause); new second pass begins at beat', W.SONG2_START, '| original syllables after beat 384:', os.filter(e => e.at / W.BEAT > 384).length);
  const win = e => e.at / W.BEAT >= 306 && e.at / W.BEAT < 316.5, or = old.LOG.filter(e => e.t === 'robinNote'), nr = W.buildBirds(SEED).filter(e => e.t === 'robinNote');
  const oc = or.filter(win).length, nc = nr.filter(e => e.b >= 306 && e.b < 316.5).length, fr = nr.filter(e => e.freq < 1800 || e.freq > 8500).length;
  const ph = W.buildBirds(SEED).filter(e => e.t === 'robinPhrase').map(e => e.female ? 'F' : 'M').join(''); const alt = /^(MF)*M?$/.test(ph);
  const sy = ns.filter(e => e.idx % 3 === 0), chirp = sy.filter(s => nr.some(r => !r.female && Math.abs(r.b - s.b) < 1e-9)).length;
  console.log('B10 robins: duet notes original', oc, 'new', nc, 'ratio', (nc / oc).toFixed(2), '| new notes out of 1.8-8.5 kHz:', fr, '| phrase order', ph, alt ? 'alternates' : 'does not alternate', '| chirps on every third syllable', chirp + '/' + sy.length, (nc / oc > .5 && nc / oc < 1.5 && !fr && alt && chirp === sy.length) ? 'PASS' : 'FAIL');
  console.log('   original robin notes in total over 412 beats:', or.length, '| new:', nr.length, '| original after beat 352:', or.filter(e => e.at / W.BEAT >= 352).length, 'new:', nr.filter(e => e.b >= 352).length);
})();
