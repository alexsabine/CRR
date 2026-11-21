// B1: the new score against the original's buildScore, same random stream. Bets are in bets.md (written first).
const fs = require('fs'), W = require('./model.js');
const src = fs.readFileSync(__dirname + '/../../song_of_willow.html', 'utf8');
const a = src.indexOf('const BPM=66'), b = src.indexOf('// ═══ §4 AUDIO ENGINE'); if (a < 0 || b < 0) throw new Error('could not find the original score');
const code = src.slice(a, b);                                   // §2 composition and §3 event score, untouched
const make = new Function('rnd', 'const {sin,cos,sqrt,abs,floor,ceil,max,min,atan2,exp,pow,log,round,tanh}=Math;const PI=Math.PI;' + code + ';return {buildScore,PARROT_SONG:null,BEAT_S,TOTAL_BEATS};');
let allOk = true;
for (const seed of [1887, 7, 20261121]) {
  const old = make(W.rng(seed)).buildScore(), neu = W.buildScore(seed); let bad = 0, first = null;
  if (old.length !== neu.length) { bad++; first = 'count ' + old.length + ' vs ' + neu.length; }
  for (let i = 0; i < Math.min(old.length, neu.length); i++) { const o = old[i], n = neu[i]; let ok = o.t === n.t && o.b === n.b && o.midi === n.midi && o.dur === n.dur && o.d === n.d && o.g === n.g && o.cnt === n.cnt && o.action === n.action && o.voice === n.voice && o.vowel === n.vowel && JSON.stringify(o.notes) === JSON.stringify(n.notes) && (o.vel === undefined ? n.vel === undefined : Math.abs(o.vel - n.vel) <= 1e-12);
    if (o.t === 'section') ok = ok && o.s.start === n.s.start && o.s.ar === n.s.ar && o.s.label === n.s.label;
    if (!ok) { bad++; if (!first) first = 'index ' + i + ' ' + JSON.stringify(o) + ' vs ' + JSON.stringify(n); } }
  console.log('B1 seed', seed, 'events', old.length, 'mismatches', bad, bad ? 'FAIL ' + first : 'PASS'); if (bad) allOk = false;
}
const o = make(Math.random); console.log('original BEAT_S', o.BEAT_S, 'new BEAT', W.BEAT, 'equal', o.BEAT_S === W.BEAT, '| original TOTAL_BEATS', o.TOTAL_BEATS, 'new SCORE_BEATS', W.SCORE_BEATS);
// B3 (first half): the song's notes against the original's PARROT_SONG table
const pa = src.indexOf('const PARROT_SONG = ['), pb = src.indexOf('];', pa); const OLD = new Function(src.slice(pa, pb + 2) + ';return PARROT_SONG;')();
let sb = 0; OLD.forEach((n, i) => { const m = W.PARROT_SONG[i]; if (!m || n.m !== m.m || n.d !== m.d || n.l !== m.l || JSON.stringify(n.ph || null) !== JSON.stringify(m.ph || null)) sb++; });
const sy = W.buildBirds(1887).filter(e => e.t === 'syll' && e.pass === 1); let b0 = 315, tb = 0, k = 0; OLD.forEach(n => { if (n.m > 0) { const e = sy[k++]; if (!e || e.midi !== n.m || e.dur !== n.d || e.word !== n.l || Math.abs(e.b - b0) > 1e-9) tb++; } b0 += n.d; });
console.log('B3 table: entries', OLD.length, 'mismatches', sb, '| first pass: syllables', sy.length, 'expected', OLD.filter(n => n.m > 0).length, 'pitch/length/word/onset mismatches', tb, (sb || tb || sy.length !== 26) ? 'FAIL' : 'PASS');
// B7: Leonardo's rule
for (const q of ['high', 'mid', 'low']) { const t = W.buildTree(W.SEED, W.QUALITY[q]); const e = W.leonardoError(t); console.log('B7', q, 'forks checked on', t.nStruct, 'branches,', t.W.length, 'shoots; worst relative error', e.toExponential(2), e < 1e-9 ? 'PASS' : 'FAIL'); }
process.exitCode = allOk ? 0 : 1;
