/* Song of Willow: the model. No drawing and no sound in here.
   The score is carried over from the first version of the piece, event for event.
   The tree is a branching skeleton with radii set by Leonardo's rule, hanging shoots (withies) as chains, and leaves that turn. */
(function (root) {
'use strict';
const PI = Math.PI, TAU = 2 * PI;
const { sin, cos, sqrt, abs, floor, max, min, exp, pow, log, atan2 } = Math;
const clamp = (v, a, b) => v < a ? a : v > b ? b : v, lerp = (a, b, t) => a + (b - a) * t, sstep = t => { t = clamp(t, 0, 1); return t * t * (3 - 2 * t); };
/* one seeded random stream (mulberry32) so that a performance can be repeated and tested */
function rng(seed) { let a = seed >>> 0; return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

/* ─── the composition ─────────────────────────────────────────────────────────────────────────── */
const BPM = 66, BEAT = 60 / BPM, SCORE_BEATS = 384;
const SONG_START = 315, SONG_BEATS = 43, SONG2_START = 360, END_BEATS = 408, SEED = 1887;
const Dm = [38, 50, 53, 57, 62], Dm7 = [38, 50, 53, 57, 65], Dm9 = [38, 50, 53, 57, 64], Gm = [43, 55, 58, 62, 67], Gm7 = [43, 55, 58, 62, 65];
const Am = [45, 57, 60, 64, 69], Am7 = [45, 57, 60, 64, 67], Bb = [46, 58, 62, 65, 70], Bbmaj7 = [46, 58, 62, 65, 69];
const Fmaj7 = [41, 53, 57, 60, 64], C_ = [36, 48, 55, 60, 64], Cmaj7 = [36, 48, 55, 59, 64], Dsus = [38, 50, 55, 57, 62], Eaug = [40, 52, 56, 64, 68];
const SECTIONS = [
  { name: 'Seed', start: 0, end: 31, label: 'seed', ar: 0 },
  { name: 'Root', start: 32, end: 63, label: 'roots reaching', ar: .08 },
  { name: 'Sapwood', start: 64, end: 95, label: 'first sap', ar: .15 },
  { name: 'Canopy unfolds', start: 96, end: 135, label: 'leaves unfurling', ar: .25 },
  { name: 'The wind arrives', start: 136, end: 175, label: 'the wind arrives', ar: .45 },
  { name: 'Leaf song', start: 176, end: 215, label: 'ten thousand leaves', ar: .6 },
  { name: 'Storm', start: 216, end: 247, label: 'the storm', ar: .85 },
  { name: 'Delta', start: 248, end: 263, label: 'δ(now)', ar: 1 },
  { name: 'After rain', start: 264, end: 295, label: 'after rain', ar: .4 },
  { name: 'Reflection', start: 296, end: 327, label: 'still water', ar: .25 },
  { name: 'Catkin', start: 328, end: 351, label: 'catkin release', ar: .15 },
  { name: 'Stillness', start: 352, end: END_BEATS - 1, label: 'one leaf', ar: .05 }];
function gS(b) { for (const s of SECTIONS) if (b >= s.start && b <= s.end) return s; return b < 0 ? SECTIONS[0] : SECTIONS[SECTIONS.length - 1]; }

/* The score. This function is the original's buildScore with its random source made explicit. Nothing else is changed. */
function buildScore(seed) {
  const rnd = typeof seed === 'function' ? seed : rng(seed === undefined ? SEED : seed);
  const E = [];
  const sc = (b) => { E.push({ b, t: 'section', s: gS(b) }); };
  const dr = (b, g, d) => { E.push({ b, t: 'drone', g, d }); };
  const n = (b, m, v, d, ty) => { E.push({ b, t: ty || 'tone', midi: m, vel: v, dur: d }); };
  const bs = (ch, b, v, d) => { E.push({ b, t: 'bass', midi: ch[0], vel: v, dur: d }); if (ch[1]) E.push({ b, t: 'bass', midi: ch[1], vel: v * .5, dur: d }); };
  const pd = (ns, b, v, d) => { E.push({ b, t: 'pad', notes: ns, vel: v, dur: d }); };
  const ar = (ch, b, pat, v, sp) => { pat.forEach((ni, i) => { E.push({ b: b + i * sp, t: 'arp', midi: ch[ni % ch.length], vel: v * (.7 + rnd() * .3), dur: sp * 1.8 }); }); };
  const lf = (b, v, c) => { E.push({ b, t: 'leaf', vel: v, cnt: c || 8 }); };
  const cr = (b, v, d) => { E.push({ b, t: 'creak', vel: v, dur: d || 1.5 }); };
  const wn = (b, v, d) => { E.push({ b, t: 'wind', vel: v, dur: d || 2 }); };
  const dp = (b, v, c) => { E.push({ b, t: 'drip', vel: v, cnt: c || 3 }); };
  const cv = (b, v) => { E.push({ b, t: 'cavit', vel: v }); };
  const ch = (b, ns, v, d) => { E.push({ b, t: 'choir', notes: ns, vel: v, dur: d }); };
  const wt = (b, v, d) => { E.push({ b, t: 'water', vel: v, dur: d || 3 }); };
  /* I. SEED 0-31 */
  sc(0); dr(0, .02, 32); for (let i = 0; i < 32; i++) { const l = i; if (i === 0) n(i, 62, .02, 8); if (i === 8) n(i, 57, .03, 6); if (i === 16) n(i, 53, .04, 6); if (i === 24) { n(i, 50, .05, 6); n(i, 62, .03, 6); } if (i % 8 === 4) n(i, 74, .01 + l * .001, 4, 'shim'); }
  /* II. ROOT 32-63 */
  sc(32); dr(32, .08, 32); const rC = [Dm, Dm, Fmaj7, Dm, Gm, Dm, Am, Dm]; for (let i = 32; i < 64; i++) { const l = i - 32, c = rC[floor(l / 4) % 8]; if (l % 8 === 0) bs(c, i, .12, 3); if (l % 4 === 0) n(i, c[0] - 12, .06 + l * .002, 3); if (l % 6 === 0) cv(i, .03 + l * .001); if (l % 8 === 4) wt(i, .04 + l * .001, 4); }
  /* III. SAPWOOD 64-95 */
  sc(64); dr(64, .12, 32); const sC = [Dm, Dm7, Gm7, Am7, Fmaj7, Dm, Gm, C_]; for (let i = 64; i < 96; i++) { const l = i - 64, c = sC[floor(l / 4) % 8]; if (l % 4 === 0) { bs(c, i, .14, 2.5); n(i, c[2], .06, 2.5); } if (l % 2 === 0) n(i, c[3 + floor(rnd() * 2)], .04 + rnd() * .03, 2, 'shim'); if (l % 6 === 0) cv(i, .05 + l * .002); if (l % 8 === 0) wt(i, .06, 4); }
  /* IV. CANOPY 96-135 */
  sc(96); dr(96, .18, 40); const cC = [Dm9, Gm7, Bbmaj7, Fmaj7, Am7, Dm7, C_, Gm]; for (let i = 96; i < 136; i++) { const l = i - 96, c = cC[floor(l / 5) % 8]; if (l % 4 === 0) { bs(c, i, .16, 2); pd(c.slice(2), i, .1, 6); } if (l % 2 === 0) n(i, c[2 + floor(rnd() * 3)], .06 + rnd() * .04, 2, 'shim'); if (l % 3 === 0) lf(i, .04 + l * .002, 3 + floor(l / 8)); if (l % 8 === 0) ar(c, i, [0, 2, 3, 4, 3, 2], .06, .6); if (l % 6 === 0) cv(i, .04); if (l % 8 === 4) wt(i, .05, 3); }
  /* V. WIND 136-175 */
  sc(136); dr(136, .25, 40); const wC = [Gm, Dm, Am, Bb, Fmaj7, Gm, C_, Dm7]; for (let i = 136; i < 176; i++) { const l = i - 136, c = wC[floor(l / 5) % 8]; if (l % 4 === 0) { bs(c, i, .18, 2); pd(c.slice(1), i, .12, 5); } if (l % 2 === 0) { lf(i, .06 + l * .003, 5 + floor(l / 5)); n(i, c[3 + floor(rnd() * 2)], .07, 2); } if (l % 4 === 2) wn(i, .06 + l * .004, 3); if (l % 8 === 0) ar(c, i, [4, 3, 2, 1, 2, 3, 4, 3], .08, .5); if (l % 6 === 0) cr(i, .03 + l * .002, 1.5); if (l % 8 === 4) wt(i, .06, 3); if (l % 3 === 0) cv(i, .04 + l * .001); }
  /* VI. LEAF SONG 176-215 */
  sc(176); dr(176, .3, 40); const lC = [Dm9, Gm, Am7, Bbmaj7, Fmaj7, Dm7, Gm7, C_]; for (let i = 176; i < 216; i++) { const l = i - 176, c = lC[floor(l / 5) % 8]; if (l % 4 === 0) { bs(c, i, .2, 2); pd(c.slice(1), i, .14, 6); } lf(i, .08 + rnd() * .06, 8 + floor(rnd() * 8)); if (l % 2 === 0) { wn(i, .08 + rnd() * .04, 2); n(i, c[2 + floor(rnd() * 3)], .08, 2); } if (l % 4 === 0) ar(c, i, [0, 2, 4, 3, 2, 4, 3, 1], .09, .45); if (l % 8 === 0) cr(i, .05, 2); if (l % 4 === 2) ch(i, c.slice(2), .06, 4); if (l % 8 === 4) wt(i, .07, 3); if (l % 3 === 0) dp(i, .03, 2); }
  /* VII. STORM 216-247 */
  sc(216); dr(216, .45, 32); const stC = [Dm, Gm, Am, Eaug, Bb, Dm, Gm, Dm]; for (let i = 216; i < 248; i++) { const l = i - 216, c = stC[floor(l / 4) % 8]; if (l % 4 === 0) { bs(c, i, .25, 1.5); pd(c.slice(1), i, .18, 4); } lf(i, .12 + rnd() * .08, 12 + floor(rnd() * 12)); wn(i, .12 + l * .005, 2); if (l % 2 === 0) { n(i, c[2 + floor(rnd() * 3)], .1 + rnd() * .05, 1.5); cr(i, .08 + rnd() * .06, 1.5 + rnd()); } if (l % 4 === 0) ar(c, i, [4, 2, 0, 3, 1, 4, 2, 3], .1, .35); if (l % 3 === 0) cv(i, .08 + rnd() * .04); if (l % 6 === 0) ch(i, c.slice(1), .1, 3); if (l % 4 === 2) wt(i, .1, 2); }
  /* VIII. DELTA 248-263 */
  sc(248); dr(248, .5, 16); for (let i = 248; i < 264; i++) { const l = i - 248; if (l === 0) E.push({ b: i, t: 'rupture', vel: .9, dur: 4 }); if (l < 8) { lf(i, .15 - l * .01, 15 - l); wn(i, .15 - l * .015, 2); } if (l < 4) cr(i, .15 - l * .03, 2); if (l >= 4 && l < 12) dp(i, .08 + rnd() * .04, 4 + floor(rnd() * 4)); if (l % 4 === 0 && l >= 4) n(i, Dm[floor(rnd() * 5)], .08 - l * .003, 3); if (l >= 8) { wt(i, .08 + rnd() * .03, 3); n(i, 62, .04, 4, 'shim'); } if (l % 8 === 0 && l > 0) pd(Dm.slice(2), i, .08, 6); }
  /* IX. AFTER RAIN 264-295, with the seven-voice choir */
  sc(264); dr(264, .2, 32); const arC = [Dm9, Fmaj7, Bbmaj7, Gm7, Am7, Cmaj7, Dm7, Gm];
  E.push({ b: 263, t: 'rbchoir', action: 'init' });
  for (let vi = 0; vi < 7; vi++) E.push({ b: 264 + vi * 1.5, t: 'rbchoir', action: 'enter', voice: vi });
  E.push({ b: 280, t: 'rbchoir', action: 'morph', vowel: 'Ah', dur: 4 });
  E.push({ b: 290, t: 'rbchoir', action: 'morph', vowel: 'Eh', dur: 3 });
  E.push({ b: 298, t: 'rbchoir', action: 'fade', dur: 12 });
  for (let i = 264; i < 296; i++) { const l = i - 264, c = arC[floor(l / 4) % 8]; if (l % 4 === 0) { bs(c, i, .14, 2.5); pd(c.slice(2), i, .1, 6); } if (l % 2 === 0) dp(i, .06 + rnd() * .04, 3 + floor(rnd() * 4)); if (l % 3 === 0) n(i, c[3 + floor(rnd() * 2)], .06, 2.5, 'shim'); if (l % 4 === 2) lf(i, .04 + rnd() * .03, 4 + floor(rnd() * 4)); if (l % 6 === 0) wn(i, .03, 3); if (l % 8 === 0) ar(c, i, [0, 3, 4, 3, 2, 4], .06, .7); if (l % 8 === 4) wt(i, .06, 4); }
  /* X. REFLECTION 296-327 */
  sc(296); dr(296, .15, 32); const rfC = [Dm9, Cmaj7, Fmaj7, Dm7, Bbmaj7, Gm7, Am7, Dm9];
  E.push({ b: 301, t: 'robin', action: 'init' });
  E.push({ b: 302, t: 'robin', action: 'land' });
  E.push({ b: 306, t: 'robin', action: 'sing' });
  E.push({ b: 310, t: 'parrot', action: 'land' });
  E.push({ b: 315, t: 'parrot', action: 'sing' });
  for (let i = 296; i < 328; i++) { const l = i - 296, c = rfC[floor(l / 4) % 8]; if (l % 4 === 0) { bs(c, i, .12, 3); pd(c.slice(2), i, .08, 7); } if (l % 4 === 2) n(i, c[4], .05, 3, 'shim'); if (l % 8 === 0) ar(c, i, [4, 3, 2, 1, 0, 1, 2, 3], .05, .8); if (l % 6 === 0) wt(i, .08, 5); if (l % 4 === 0) lf(i, .03, 3); if (l % 8 === 4) dp(i, .03, 1); }
  /* XI. CATKIN 328-351 */
  sc(328); dr(328, .1, 24); const ctC = [Dm, Dsus, Dm9, Fmaj7, Gm, Dm, Am, Dm9]; for (let i = 328; i < 352; i++) { const l = i - 328, c = ctC[floor(l / 3) % 8]; if (l % 4 === 0) { bs(c, i, .1 - l * .003, 2.5); n(i, c[4] + 12, .04, 3, 'shim'); } if (l % 3 === 0) n(i, c[3 + floor(rnd() * 2)] + 12, .04 - l * .001, 2.5); if (l % 6 === 0) pd(c.slice(3), i, .06 - l * .002, 6); if (l % 2 === 0) lf(i, .03 - l * .001, 2); if (l % 8 === 0) wn(i, .02, 2); }
  /* XII. STILLNESS 352-383 */
  sc(352); dr(352, .03, 32); for (let i = 352; i < 384; i++) { const l = i - 352; if (l % 8 === 0 && l < 24) n(i, 62, .02 - l * .0005, 5, 'shim'); if (l % 16 === 0 && l < 16) n(i, 57, .015, 6); if (l === 0) lf(i, .02, 1); if (l === 24) dr(i, .005, 8); }
  E.sort((a, b) => a.b - b.b); return E;
}

/* ─── the song at the end: "What a Lovely Day", D major. Pitch, length in beats, word, phonemes. Unchanged. ─── */
const PARROT_SONG = [
  { m: 62, d: 1, l: 'What', ph: { c: 'w', v: 'ah', x: 't' } }, { m: 64, d: .5, l: 'a', ph: { c: null, v: 'ax', x: null } }, { m: 66, d: 1.5, l: 'love-', ph: { c: 'l', v: 'ah', x: 'v' } }, { m: 69, d: 1, l: 'ly', ph: { c: 'l', v: 'iy', x: null } }, { m: 74, d: 2.5, l: 'day!', ph: { c: 'd', v: 'ey', x: null } }, { m: 0, d: 1, l: '' },
  { m: 74, d: 1, l: 'Oh', ph: { c: null, v: 'ow', x: null } }, { m: 71, d: 1, l: 'what', ph: { c: 'w', v: 'ah', x: 't' } }, { m: 69, d: .5, l: 'a', ph: { c: null, v: 'ax', x: null } }, { m: 66, d: 1.5, l: 'love-', ph: { c: 'l', v: 'ah', x: 'v' } }, { m: 64, d: 1, l: 'ly', ph: { c: 'l', v: 'iy', x: null } }, { m: 62, d: 2.5, l: 'day!', ph: { c: 'd', v: 'ey', x: null } }, { m: 0, d: 1.5, l: '' },
  { m: 62, d: 1, l: 'The', ph: { c: 'dh', v: 'ax', x: null } }, { m: 66, d: 1, l: 'sun', ph: { c: 's', v: 'ah', x: 'n' } }, { m: 69, d: .75, l: 'is', ph: { c: null, v: 'ih', x: 'z' } }, { m: 71, d: 1.5, l: 'shin-', ph: { c: 'sh', v: 'ay', x: 'n' } }, { m: 69, d: .75, l: 'ing', ph: { c: null, v: 'ih', x: 'ng' } }, { m: 69, d: 2, l: 'bright', ph: { c: 'b', v: 'ay', x: 't' } }, { m: 0, d: .75, l: '' },
  { m: 66, d: 1, l: 'And', ph: { c: null, v: 'ae', x: 'n' } }, { m: 69, d: 1, l: 'ev-', ph: { c: null, v: 'eh', x: 'v' } }, { m: 66, d: .75, l: 'ry-', ph: { c: 'r', v: 'iy', x: null } }, { m: 64, d: 1.5, l: 'thing\'s', ph: { c: 'th', v: 'ih', x: 'ng' } }, { m: 62, d: 1, l: 'al-', ph: { c: null, v: 'ao', x: 'l' } }, { m: 62, d: 3, l: 'right!', ph: { c: 'r', v: 'ay', x: 't' } }, { m: 0, d: 2, l: '' },
  { m: 69, d: 1.5, l: 'Love-', ph: { c: 'l', v: 'ah', x: 'v' } }, { m: 71, d: 1, l: 'ly', ph: { c: 'l', v: 'iy', x: null } }, { m: 74, d: 4, l: 'day!', ph: { c: 'd', v: 'ey', x: null } }, { m: 0, d: 2, l: '' }];
/* the lines as shown, split at rests of a beat or more (as the original did for its karaoke) */
const LYRIC_LINES = (function () { const L = []; let line = []; PARROT_SONG.forEach((n, i) => { if (n.m === 0 && n.d >= 1) { if (line.length) { L.push(line); line = []; } } else if (n.l) line.push({ text: n.l, idx: i }); }); if (line.length) L.push(line); return L; })();
/* the second time through, a quiet second voice hums a diatonic third below. This is new. */
const THIRD_BELOW = { 62: 59, 64: 61, 66: 62, 69: 66, 71: 67, 74: 71 };

/* ─── the robins: interval shapes taken from three Doris Day melodies, found by a small genetic search. Carried over. ─── */
const DORIS = {
  queSera: [[0, 2, 4, 5, 7, 5, 4, 2, 0], [0, 4, 7, 9, 7, 4, 2, 0, -1, 0], [0, 2, 4, 7, 12, 11, 9, 7, 5, 4, 2, 0], [0, 5, 4, 2, 0, -1, 0, 2, 4, 5, 7]],
  dreamALittle: [[7, 5, 4, 2, 0, -1, 0], [0, 2, 4, 5, 4, 2, 0, -1, -3, -1, 0], [4, 2, 0, -1, 0, 2, 4, 7, 5, 4], [0, 4, 7, 5, 4, 2, 0, -3, -1, 0, 2]],
  sentimental: [[0, 2, 4, 7, 9, 7, 4, 2, 0], [0, 5, 9, 12, 9, 5, 4, 2, 0, -2, 0], [0, 2, 4, 2, 0, 4, 7, 5, 4, 2], [0, 7, 5, 4, 2, 4, 5, 7, 9, 7, 5, 4, 2, 0]] };
function RobinGA(targets, female, rnd) {
  const G = { targets, popSize: 12, generation: 0, Omega: 1 / PI, C: 0, population: [], bestPhrase: null, bestFitness: 0, baseMidi: female ? 96 : 88 };
  function evaluate() { for (const ind of G.population) { const target = targets[ind.targetIdx]; let err = 0; const len = min(ind.intervals.length, target.length); for (let i = 0; i < len; i++) { const d = ind.intervals[i] - target[i]; err += d * d; } ind.fitness = exp(-err / max(1, len * 4)); } G.population.sort((a, b) => b.fitness - a.fitness); if (G.population[0].fitness > G.bestFitness) { G.bestFitness = G.population[0].fitness; G.bestPhrase = G.population[0].intervals.slice(); } }
  for (let i = 0; i < G.popSize; i++) { const target = targets[floor(rnd() * targets.length)]; const phrase = []; for (let j = 0; j < target.length; j++) phrase.push(target[j] + (rnd() - .5) * 8); G.population.push({ intervals: phrase, targetIdx: floor(rnd() * targets.length), fitness: 0 }); }
  evaluate();
  G.evolve = function () { G.generation++; G.C += G.bestFitness; const expCO = exp(min(8, G.C * G.Omega)); const weights = G.population.map(ind => exp(ind.fitness * expCO)); const wSum = weights.reduce((a, b) => a + b, 0); const np = [];
    np.push({ intervals: G.population[0].intervals.slice(), targetIdx: G.population[0].targetIdx, fitness: G.population[0].fitness });
    for (let i = 1; i < G.popSize; i++) { let r = rnd() * wSum, idx = 0, cum = weights[0]; while (cum < r && idx < G.population.length - 1) { idx++; cum += weights[idx]; } const parent = G.population[idx]; const child = { intervals: parent.intervals.slice(), targetIdx: parent.targetIdx, fitness: 0 }; const mutRate = G.Omega / (1 + G.C * .1); for (let j = 0; j < child.intervals.length; j++) if (rnd() < mutRate * 2) child.intervals[j] += (rnd() - .5) * 3 * mutRate * 10; if (rnd() < .08) child.targetIdx = floor(rnd() * targets.length); np.push(child); }
    G.population = np; evaluate(); return G.population[0]; };
  G.getPhrase = function (songIdx) { const c = G.population.filter(p => p.targetIdx === songIdx); const best = c.length ? c.sort((a, b) => b.fitness - a.fitness)[0] : G.population[0]; return { intervals: best.intervals, baseMidi: G.baseMidi, fitness: best.fitness }; };
  return G;
}
const mtf = m => 440 * pow(2, (m - 69) / 12);
/* all bird events, with times in beats. The original ran the robins on frame timers; here the same procedure is run once, ahead of time. */
function buildBirds(seed) {
  const rnd = rng((seed === undefined ? SEED : seed) ^ 0x51ED), E = [];
  const mT = [DORIS.queSera[0], DORIS.queSera[1], DORIS.sentimental[0], DORIS.sentimental[1], DORIS.dreamALittle[2], DORIS.dreamALittle[3]];
  const fT = [DORIS.dreamALittle[0], DORIS.dreamALittle[1], DORIS.queSera[2], DORIS.queSera[3], DORIS.sentimental[2], DORIS.sentimental[3]];
  const M = RobinGA(mT, false, rnd), F = RobinGA(fT, true, rnd); for (let g = 0; g < 40; g++) { M.evolve(); F.evolve(); }
  function phrase(ph, vel, female, tSec) { const noteLen = female ? .045 + rnd() * .025 : .055 + rnd() * .03, gap = female ? .015 : .02; let off = 0; for (let i = 0; i < ph.intervals.length; i++) { const freq = clamp(mtf(ph.baseMidi + ph.intervals[i]), 1800, 8500), d = noteLen * (.7 + rnd() * .6), v = vel * (.6 + rnd() * .4) * (.8 + .2 * ph.fitness); E.push({ b: (tSec + off) / BEAT, t: 'robinNote', freq, vel: v, dur: d, female, phrase: true }); off += d + gap * (.5 + rnd()); if (rnd() < .15) off += gap * 3; } return off; }
  /* antiphonal duet from beat 306 until the parrot begins at 315 */
  let t = 306 * BEAT + .1, count = 0, song = 0; const stop = SONG_START * BEAT;
  while (t < stop) { const md = phrase(M.getPhrase(song % mT.length), .4 + rnd() * .15, false, t); E.push({ b: t / BEAT, t: 'robinPhrase', female: false, len: md }); count++; t += md + .1; t += .35 + (rnd() - .5) * 2 * (1 / TAU) * .35; if (t >= stop) break;
    const fd = phrase(F.getPhrase(song % fT.length), .35 + rnd() * .15, true, t); E.push({ b: t / BEAT, t: 'robinPhrase', female: true, len: fd }); count++; t += fd + .1; t += .6 + rnd() * .8; M.evolve(); F.evolve(); if (count % 6 === 0) song = (song + 1) % 3; }
  /* the song, twice; robins chirp on every third syllable */
  [[SONG_START, 1], [SONG2_START, 2]].forEach(([start, pass]) => { let b = start; PARROT_SONG.forEach((note, idx) => { if (note.m > 0) { E.push({ b, t: 'syll', idx, pass, midi: note.m, dur: note.d, word: note.l, ph: note.ph }); if (pass === 2) E.push({ b, t: 'hum', idx, midi: THIRD_BELOW[note.m], dur: note.d });
        if (idx % 3 === 0) { const bp = M.getPhrase(0); E.push({ b, t: 'robinNote', freq: clamp(mtf(bp.baseMidi + bp.intervals[floor(rnd() * min(3, bp.intervals.length))]), 2500, 6000), vel: .15, dur: .04, female: false }); if (rnd() > .4) { const fp = F.getPhrase(0); E.push({ b: b + (.08 + rnd() * .06) / BEAT, t: 'robinNote', freq: clamp(mtf(fp.baseMidi + fp.intervals[floor(rnd() * min(3, fp.intervals.length))]), 3000, 7000), vel: .12, dur: .03, female: true }); } } }
      b += note.d; }); });
  /* single notes in the stillness, about one every five or six seconds, as the original's per-frame chance gave */
  let ts = 352 * BEAT; for (;;) { ts += -log(1 - rnd()) / .18; if (ts >= SCORE_BEATS * BEAT) break; const fem = rnd() > .5, G = fem ? F : M, ph = G.getPhrase(0); E.push({ b: ts / BEAT, t: 'robinNote', freq: clamp(mtf(ph.baseMidi + ph.intervals[floor(rnd() * ph.intervals.length)]), 2000, 7000), vel: .15, dur: .08 + rnd() * .06, female: fem }); }
  E.push({ b: SCORE_BEATS, t: 'drone', g: 0, d: 2 / BEAT });        /* the original faded its drone over two seconds when the score ran out */
  E.push({ b: END_BEATS, t: 'end' });
  E.sort((a, b) => a.b - b.b); return E;
}
function timeline(seed) { const E = buildScore(seed).concat(buildBirds(seed)); E.forEach((e, i) => { e.i = i; e.time = e.b * BEAT; }); E.sort((a, b) => a.b - b.b || a.i - b.i); return E; }

/* ─── light and weather: the original's curves, as functions of the beat ─── */
function sunAt(b) { let s; if (b < 32) s = b / 32 * .05; else if (b < 64) s = .05 + (b - 32) / 32 * .12; else if (b < 96) s = .17 + (b - 64) / 32 * .18; else if (b < 136) s = .35 + (b - 96) / 40 * .25; else if (b < 176) s = .6 + (b - 136) / 40 * .2; else if (b < 216) s = .8 + (b - 176) / 40 * .15; else if (b < 248) s = .95 - (b - 216) / 32 * .25; else if (b < 264) s = .7 - (b - 248) / 16 * .15; else if (b < 296) s = .55 + (b - 264) / 32 * .2; else if (b < 328) s = .75 - (b - 296) / 32 * .2; else if (b < 352) s = .55 - (b - 328) / 24 * .3; else s = .25 - (b - 352) / 32 * .22; return clamp(s, .02, 1); }
function rainAt(b) { if (b < 190) return 0; if (b < 216) return (b - 190) / 26 * .5; if (b < 248) return .5 + (b - 216) / 32 * .4; if (b < 264) return .9; if (b < 296) return max(0, .9 - (b - 264) / 32 * .85); return max(0, .05 - (b - 296) * .05); }
function rainbowAt(b) { if (b < 260 || b > 310) return 0; let r = max(0, 1 - rainAt(b) * 2) * clamp((sunAt(b) - .3) / .4, 0, 1); if (b > 295) r *= max(0, 1 - (b - 295) / 15); return r; }

/* wind, taken from the score so that what is seen is what is heard: the level each movement sets, plus every wind event's own swell, plus a little from each burst of leaf sound */
function buildWind(score) {
  const R = 8, N = END_BEATS * R + 1, base = new Float32Array(N), gust = new Float32Array(N), sound = new Float32Array(N);
  for (let i = 0; i < N; i++) { const b = i / R, s = gS(floor(b)); base[i] = b >= 248 && b < 264 ? lerp(1, .4, (b - 248) / 16) : b >= SCORE_BEATS ? .03 : s.ar; }
  for (let k = 0, v = 0; k < N; k++) { v += (base[k] - v) * (1 - exp(-1 / (R * 2.75))); base[k] = v; }
  for (const e of score) {
    if (e.t === 'wind') { const n = e.dur * R; for (let k = 0; k <= n; k++) { const u = k / n, env = u < .2 ? u / .2 : u < .6 ? 1 - (u - .2) / .4 * .2 : .8 * (1 - (u - .6) / .4), i = floor(e.b * R) + k; if (i < N) { gust[i] += e.vel * env * 3.2; sound[i] += e.vel * env; } } }
    else if (e.t === 'leaf') { for (let k = 0; k < 5; k++) { const i = floor(e.b * R) + k; if (i < N) gust[i] += e.vel * e.cnt * .05 * (1 - k / 5); } }
    else if (e.t === 'rupture') { for (let k = 0; k < 3 * R; k++) { const i = floor(e.b * R) + k; if (i < N) gust[i] += .8 * (1 - k / (3 * R)); } }
  }
  const at = (A, b) => { const x = clamp(b, 0, END_BEATS) * R, i = min(N - 2, floor(x)); return lerp(A[i], A[i + 1], x - i); };
  return { level: b => at(base, b) * .82 + at(gust, b), sound: b => at(sound, b) };
}

/* ─── the tree ─────────────────────────────────────────────────────────────────────────────────── */
const QUALITY = { high: { withies: 340, nodes: 12, per: 46 }, mid: { withies: 270, nodes: 11, per: 40 }, low: { withies: 180, nodes: 9, per: 34 } };
const R_WITHY = .0016, R_TIP = .0026, BANK = .034;
function buildTree(seed, Q) {
  const rnd = rng((seed === undefined ? SEED : seed) ^ 0x7EE), D = PI / 180, Br = [];
  /* a branch: K segments with rest angles (from +x, y up), attached to its parent at parameter ta */
  function add(parent, ta, a0, bend, len, K, level, z, gs, gd) { const ang = new Float32Array(K), side = cos(a0) >= 0 ? -1 : 1; for (let i = 0; i < K; i++) { let a = a0 + side * bend * pow((i + .5) / K, 1.4) + (rnd() - .5) * .09; if (level >= 1 && level <= 3) { const lim = level === 3 ? 58 : 34; a = side < 0 ? max(a, -lim * D) : min(a, (180 + lim) * D); } ang[i] = a; } Br.push({ parent, ta, ang, len, K, level, z, gs, ge: gs + gd, ph: rnd() * TAU, om: .5 + rnd() * .5, kids: [], area: new Float64Array(K + 1), creakT: -99, creakA: 0 }); if (parent >= 0) Br[parent].kids.push(Br.length - 1); return Br.length - 1; }
  const trunk = add(-1, 0, 94 * D, 0, .25, 6, 0, 0, 5, 55); Br[trunk].ang.set([97 * D, 95 * D, 91 * D, 88 * D, 86 * D, 89 * D]);
  const A0 = [139, 119, 101, 83, 63, 43], Z0 = [-.25, .75, -.85, .15, .9, -.55], TA = [.8, .95, 1, 1, .92, .78];
  for (let i = 0; i < 6; i++) {
    const a = (A0[i] + (rnd() - .5) * 9) * D, len = .35 + rnd() * .11, gs = 58 + i * 3, li = add(trunk, TA[i], a, (28 + rnd() * 18) * D, len, 7, 1, Z0[i], gs, 18);
    for (let j = 0; j < 4; j++) { const t = [.36, .57, .78, 1][j], up = j % 2 ? 1 : -1, la = Br[li].ang[min(6, floor(t * 7))], sa = t === 1 ? la + (rnd() - .5) * .3 : la + up * (20 + rnd() * 26) * D;
      const sl = (.19 + rnd() * .12) * (1.15 - t * .3), sg = gs + 9 + j * 3.5, si = add(li, t, sa, (50 + rnd() * 30) * D, sl, 5, 2, clamp(Z0[i] + (rnd() - .5) * .6, -1, 1), sg, 16);
      for (let k = 0; k < 3; k++) { const tt = [.4, .7, 1][k], sa2 = Br[si].ang[min(4, floor(tt * 5))], ta2 = tt === 1 ? sa2 + (rnd() - .5) * .3 : sa2 + (k % 2 ? 1 : -1) * (22 + rnd() * 24) * D;
        add(si, tt, ta2, (60 + rnd() * 40) * D, .09 + rnd() * .08, 4, 3, clamp(Br[si].z + (rnd() - .5) * .5, -1, 1), sg + 7 + k * 3, 14); } } }
  const nStruct = Br.length;
  /* roots, creeping down the bank to the water */
  const RA = [200, 222, 243, 258, 288, 305, 322, 340];
  for (let i = 0; i < RA.length; i++) { const a = (RA[i] + (rnd() - .5) * 10) * D, ri = add(-1, 0, a, 0, .07 + rnd() * .09, 5, 4, i % 2 ? .3 : -.3, 28 + i * 2.5 + rnd() * 5, 14); const A = Br[ri].ang; for (let k = 0; k < 5; k++) A[k] = lerp(a, cos(a) > 0 ? -18 * D : 198 * D, k / 6) + (rnd() - .5) * .3; }
  /* rest positions at full growth, to place the shoots */
  const P = restPoints(Br);
  /* shoots (withies): hung from the outer crown; each as long as it needs to be to fall nearly to the water */
  const spots = []; for (let bi = 1; bi < nStruct; bi++) { const b = Br[bi], n = b.level === 1 ? 3 : 4, lo = b.level === 1 ? .6 : b.level === 2 ? .3 : .2; for (let k = 0; k < n; k++) spots.push([bi, lo + (1 - lo) * (k + rnd()) / n]); }
  for (let i = spots.length - 1; i > 0; i--) { const j = floor(rnd() * (i + 1)), q = spots[i]; spots[i] = spots[j]; spots[j] = q; }
  const W = [];
  for (let w = 0; w < Q.withies; w++) { const sp = spots[w < spots.length ? w : floor(rnd() * spots.length)], bi = sp[0], t = w < spots.length ? sp[1] : .3 + rnd() * .7, b = Br[bi], p = pointAt(P[bi], b.K, t), out = clamp(abs(p[0]) / .6, 0, 1);
    const tip = .035 + rnd() * rnd() * (.3 - .14 * out), reach = min(clamp((p[1] - tip) * (.9 + rnd() * .08), .05, .95), max(.05, p[1] - .025)), len = rnd() < .42 + .4 * out ? reach : min(reach, .2 + rnd() * .4), gs = b.gs + 8 + rnd() * 10;
    W.push({ br: bi, t, len, z: clamp(b.z + (rnd() - .5) * .7, -1, 1), gs, ge: gs + 14 + rnd() * 4, side: p[0] >= 0 ? 1 : -1 }); b.nW = (b.nW || 0) + 1; }
  /* short leafy shoots all over the crown, so that the boughs are clothed */
  const nShort = Math.round(Q.withies * .45); for (let w = 0; w < nShort; w++) { let bi; do { bi = 1 + floor(rnd() * (nStruct - 1)); } while (Br[bi].level < 2 && rnd() < .7); const b = Br[bi], t = b.level === 1 ? .35 + rnd() * .65 : rnd(), p = pointAt(P[bi], b.K, t), gs = b.gs + 10 + rnd() * 12;
    W.push({ br: bi, t, len: min(.045 + rnd() * .1, max(.03, p[1] - .03)), z: clamp(b.z + (rnd() - .5) * .7, -1, 1), gs, ge: gs + 10 + rnd() * 4, side: p[0] >= 0 ? 1 : -1, short: true }); }
  W.sort((a, b) => a.z - b.z);
  /* Leonardo's rule: the cross-section below a fork is the sum of the cross-sections above it. The lists say what joins each segment. */
  for (let bi = 0; bi < nStruct; bi++) { const b = Br[bi]; b.segW = []; b.segK = []; for (let i = 0; i < b.K; i++) { b.segW.push([]); b.segK.push([]); } for (const k of b.kids) b.segK[min(b.K - 1, floor(Br[k].ta * b.K))].push(k); }
  W.forEach((w, wi) => { const b = Br[w.br]; b.segW[min(b.K - 1, floor(w.t * b.K))].push(wi); });
  areas(Br, nStruct, null, null);
  for (let bi = nStruct; bi < Br.length; bi++) { const b = Br[bi]; for (let i = 0; i <= b.K; i++) b.area[i] = pow(lerp(.016, .003, i / b.K), 2); }
  /* leaves: alternate along each shoot */
  const L = []; W.forEach((w, wi) => { const n = max(w.short ? 5 : 6, Math.round(Q.per * w.len / .5 * (w.short ? 1.5 : 1))); for (let j = 0; j < n; j++) { const f = .05 + .95 * (j + rnd() * .8) / n, sFloat = f * (Q.nodes - 1), s = min(Q.nodes - 2, floor(sFloat));
      L.push({ w: wi, s, f: sFloat - s, side: j % 2 ? 1 : -1, size: .018 + rnd() * .013, sens: .7 + rnd() * .6, ph: rnd() * TAU, appear: w.gs + 6 + f * 10 + rnd() * 8, fall: 0, regen: 268 + rnd() * 60, shade: rnd() }); } });
  /* the storm takes leaves at the original's rate (a chance per frame rising from beat 220); whatever is left goes at the strike */
  for (const l of L) { const E = -log(1 - rnd()), b = 220 + sqrt(60 * E / .0545); l.fall = b < 250 ? b : 250 + rnd() * .9; }
  /* perches: two robins on outer boughs, the parrot on a thick limb */
  const perch = (test, score) => { let best = null, bs = -1e9; for (let bi = 1; bi < nStruct; bi++) for (let i = 1; i <= Br[bi].K; i++) { const x = P[bi][i * 2], y = P[bi][i * 2 + 1]; if (!test(Br[bi], x, y)) continue; const s = score(Br[bi], x, y); if (s > bs) { bs = s; best = { br: bi, t: i / Br[bi].K }; } } return best || { br: 1, t: .5 }; };
  const perches = { male: perch((b, x, y) => b.level === 2 && x < -.12, (b, x, y) => -abs(y - .6) - abs(x + .3) + b.z * .1), female: perch((b, x, y) => b.level === 2 && x > .12, (b, x, y) => -abs(y - .56) - abs(x - .3) + b.z * .1), parrot: perch((b, x, y) => b.level === 1, (b, x, y) => -abs(y - .47) - abs(x) * 1.2 + b.z * .15) };
  return { Br, nStruct, W, L, Q, perches };
}
/* cross-sections from the tips down. With growth factors given, a part counts for as much as has grown, so the trunk thickens as the crown fills. */
function areas(Br, nStruct, grow, wgrow) { for (let bi = nStruct - 1; bi >= 0; bi--) { const b = Br[bi], g = grow ? grow[bi] : 1; let A = R_TIP * R_TIP * g; b.area[b.K] = A; for (let i = b.K - 1; i >= 0; i--) { const sw = b.segW[i], sk = b.segK[i]; for (let k = 0; k < sw.length; k++) A += R_WITHY * R_WITHY * (wgrow ? wgrow[sw[k]] : 1); for (let k = 0; k < sk.length; k++) A += Br[sk[k]].area[0]; b.area[i] = A; } } }
function pointAt(pts, K, t) { const x = clamp(t, 0, 1) * K, i = min(K - 1, floor(x)), f = x - i; return [lerp(pts[i * 2], pts[i * 2 + 2], f), lerp(pts[i * 2 + 1], pts[i * 2 + 3], f)]; }
function restPoints(Br) { const P = []; for (let bi = 0; bi < Br.length; bi++) { const b = Br[bi], p = new Float32Array((b.K + 1) * 2); let x = 0, y = BANK - .004; if (b.parent >= 0) { const q = pointAt(P[b.parent], Br[b.parent].K, b.ta); x = q[0]; y = q[1]; } p[0] = x; p[1] = y; for (let i = 0; i < b.K; i++) { x += cos(b.ang[i]) * b.len / b.K; y += sin(b.ang[i]) * b.len / b.K; p[i * 2 + 2] = x; p[i * 2 + 3] = y; } P.push(p); } return P; }
/* an independent check: at every segment of every branch, compare the cross-section below with the sum of what is above (found from the attachment positions, not from the lists used to build it) */
function leonardoError(tree, grow, wgrow) { let worst = 0; const { Br, W, nStruct } = tree; for (let bi = 0; bi < nStruct; bi++) { const b = Br[bi]; for (let i = 0; i < b.K; i++) { let above = b.area[i + 1]; W.forEach((w, wi) => { if (w.br === bi && min(b.K - 1, floor(w.t * b.K)) === i) above += R_WITHY * R_WITHY * (wgrow ? wgrow[wi] : 1); }); for (let k = 0; k < Br.length; k++) if (Br[k].parent === bi && k < nStruct && min(b.K - 1, floor(Br[k].ta * b.K)) === i) above += Br[k].area[0]; if (b.area[i] > 0) worst = max(worst, abs(b.area[i] - above) / b.area[i]); } } return worst; }

/* ─── the moving tree ──────────────────────────────────────────────────────────────────────────── */
const G = .98;                      /* gravity in tree heights per second squared, taking the tree as ten metres tall */
const C_STAR = PI;                  /* the count at which a leaf turns: the programme's two-state convention, C* = 1/Omega with Omega = 1/pi */
const LEAF_RATE = 2 * PI;           /* a setting: scales wind load into count, so that a leaf in a steady breeze (level 0.5) turns about every two seconds */
const ATT = 1, FALL = 2, GONE = 0;
function makeSim(seed, quality) {
  const Q = QUALITY[quality || 'high'], tree = buildTree(seed, Q), { Br, W, L, nStruct } = tree, score = buildScore(seed), wind = buildWind(score), rnd = rng((seed || SEED) ^ 0xF411);
  const nb = Br.length, P = Br.map(b => new Float32Array((b.K + 1) * 2)), Rot = Br.map(b => new Float32Array(b.K + 1)), grow = new Float32Array(nb);
  const N = Q.nodes, nw = W.length, px = new Float32Array(nw * N), py = new Float32Array(nw * N), ox = new Float32Array(nw * N), oy = new Float32Array(nw * N), wu = new Float32Array(nw * N), wgrow = new Float32Array(nw), sang = new Float32Array(nw * N);
  const nl = L.length, lx = new Float32Array(nl), ly = new Float32Array(nl), la = new Float32Array(nl), lface = new Float32Array(nl), lglint = new Float32Array(nl), lscale = new Float32Array(nl), lC = new Float32Array(nl), lstate = new Uint8Array(nl), ltarget = new Uint8Array(nl), llast = new Float32Array(nl).fill(-1), lvx = new Float32Array(nl), lvy = new Float32Array(nl), lspin = new Float32Array(nl);
  const S = { tree, Br, W, L, P, Rot, grow, N, px, py, wgrow, wu, lx, ly, la, lface, lglint, lscale, lstate, nl, nw, wind, score, t: 0, beat: 0, U: 0,
    intervals: new Float32Array(600), nInt: 0, flips: 0, landed: [], attached: 0, falling: 0, oneLeaf: -1, tipSpeed: 0, rawIntervals: null };
  /* gusts cross the tree from left to right as travelling fronts */
  function windAt(x, y, t, U) { return U * (.62 + .3 * sin(1.9 * x - 1.25 * t + 1.2 * sin(.8 * y + .31 * t)) + .16 * sin(5.3 * x - 3.1 * t + 2.4 * y)) + .012 * sin(.4 * t + 2 * x); }
  S.windAt = windAt;
  function growth(i, beat) { const b = Br[i]; if (b.parent >= 0 && grow[b.parent] < .3) return 0; return sstep((beat - b.gs) / (b.ge - b.gs)); }
  function structure(beat, t, U) {
    for (let bi = 0; bi < nb; bi++) grow[bi] = growth(bi, beat); areas(Br, nStruct, grow, wgrow);
    for (let bi = 0; bi < nb; bi++) { const b = Br[bi], g = grow[bi], p = P[bi], rot = Rot[bi]; let x = 0, y = BANK - .004, r0 = 0;
      if (b.parent >= 0) { const pp = P[b.parent], pk = Br[b.parent].K, xx = clamp(b.ta, 0, 1) * pk, i = min(pk - 1, floor(xx)), f = xx - i; x = lerp(pp[i * 2], pp[i * 2 + 2], f); y = lerp(pp[i * 2 + 1], pp[i * 2 + 3], f); r0 = lerp(Rot[b.parent][i], Rot[b.parent][i + 1], f); }
      p[0] = x; p[1] = y; rot[0] = r0;
      const flex = b.level === 0 ? .012 : b.level === 1 ? .05 : b.level === 2 ? .1 : b.level === 3 ? .17 : 0, seg = b.len / b.K * g, u = b.level === 4 ? 0 : windAt(x, y, t, U);
      /* a creak is a limb giving a little and ringing down */
      const ct = t - b.creakT, creak = ct < 4 ? b.creakA * exp(-ct * 1.3) * sin(ct * 7.5) : 0; let d = r0;
      for (let i = 0; i < b.K; i++) { const a0 = b.ang[i]; d += (-flex * (u * .9 + .12 * (.25 + U) * sin(b.om * t + b.ph + i * .4)) * sin(a0) + creak) / b.K; const a = a0 + d; x += cos(a) * seg; y += sin(a) * seg; p[i * 2 + 2] = x; p[i * 2 + 3] = y; rot[i + 1] = d; } }
  }
  function attach(wi) { const w = W[wi], b = Br[w.br], p = P[w.br], xx = clamp(w.t, 0, 1) * b.K, i = min(b.K - 1, floor(xx)), f = xx - i; return [lerp(p[i * 2], p[i * 2 + 2], f), lerp(p[i * 2 + 1], p[i * 2 + 3], f), b.ang[i] + Rot[w.br][i]]; }
  function hang(beat) { for (let wi = 0; wi < nw; wi++) { const w = W[wi], g = wgrow[wi] = grow[w.br] < .3 ? 0 : sstep((beat - w.gs) / (w.ge - w.gs)), a = attach(wi), seg = w.len / (N - 1) * g; for (let k = 0; k < N; k++) { const j = wi * N + k; px[j] = ox[j] = a[0] + w.side * .012 * min(k, 3) * g; py[j] = oy[j] = a[1] - seg * k; } } }
  function withies(dt, beat, t, U) {
    let ts = 0, tn = 0;
    for (let wi = 0; wi < nw; wi++) { const w = W[wi], g = wgrow[wi] = grow[w.br] < .3 ? 0 : sstep((beat - w.gs) / (w.ge - w.gs)), o = wi * N, a = attach(wi), seg = w.len / (N - 1) * g;
      px[o] = a[0]; py[o] = a[1]; if (g <= 0) { for (let k = 1; k < N; k++) { px[o + k] = ox[o + k] = a[0]; py[o + k] = oy[o + k] = a[1]; } continue; }
      for (let k = 1; k < N; k++) { const j = o + k, x = px[j], y = py[j], vx = (x - ox[j]) / dt, vy = (y - oy[j]) / dt, u = windAt(x, y, t, U), rel = u - vx, kk = .35 + .4 * abs(rel); wu[j] = u;
        const ax = kk * rel, ay = -G * (w.short ? .4 : 1) - .35 * vy + .05 * u * sin(3 * t + k + wi); ox[j] = x; oy[j] = y; px[j] = x + vx * dt * .999 + ax * dt * dt; py[j] = y + vy * dt * .999 + ay * dt * dt; }
      wu[o] = wu[o + 1];
      /* a shoot leaves its branch in the branch's direction before it droops */
      let dx = cos(a[2]) * .45, dy = sin(a[2]) * .45 - .55; if (w.short) { const nx = -sin(a[2]), ny = cos(a[2]), sg = ny >= 0 ? 1 : -1; dx = cos(a[2]) * .5 + nx * sg * .8; dy = sin(a[2]) * .5 + ny * sg * .8 + .2; }
      const dl = sqrt(dx * dx + dy * dy) || 1; px[o + 1] += (a[0] + dx / dl * seg - px[o + 1]) * .5; py[o + 1] += (a[1] + dy / dl * seg - py[o + 1]) * .5;
      if (w.short) { px[o + 2] += (px[o + 1] + (dx / dl * .8 + w.side * .2) * seg - px[o + 2]) * .3; py[o + 2] += (py[o + 1] + dy / dl * .7 * seg - py[o + 2]) * .3; }
      for (let it = 0; it < 3; it++) for (let k = 1; k < N; k++) { const j = o + k, ex = px[j] - px[j - 1], ey = py[j] - py[j - 1], d = sqrt(ex * ex + ey * ey) || 1e-6, c = (d - seg) / d; if (k === 1) { px[j] -= ex * c; py[j] -= ey * c; } else { px[j] -= ex * c * .5; py[j] -= ey * c * .5; px[j - 1] += ex * c * .5; py[j - 1] += ey * c * .5; } }
      for (let k = 0; k < N - 1; k++) sang[o + k] = atan2(py[o + k + 1] - py[o + k], px[o + k + 1] - px[o + k]);
      if (g > .5) { const j = o + N - 1; ts += sqrt(pow(px[j] - ox[j], 2) + pow(py[j] - oy[j], 2)) / dt; tn++; } }
    S.tipSpeed = tn ? ts / tn : 0;
  }
  function leaves(dt, beat, t, U) {
    let att = 0, fal = 0;
    for (let i = 0; i < nl; i++) { const l = L[i]; let st = lstate[i];
      const want = i === S.oneLeaf && beat >= 352 ? FALL : (beat >= l.appear && (beat < l.fall || beat >= l.regen)) ? ATT : (beat >= l.fall && beat < l.regen ? FALL : GONE);
      if (want === ATT && st !== ATT) { st = lstate[i] = ATT; lC[i] = 0; llast[i] = -1; lscale[i] = 0; }
      else if (want === FALL && st === ATT) { st = lstate[i] = FALL; lvx[i] = (rnd() - .3) * .3 * (.3 + U); lvy[i] = (rnd() - .5) * .1; lspin[i] = (rnd() - .5) * 5; }
      else if (want === GONE && st === ATT) st = lstate[i] = GONE;
      if (st === ATT) { att++; const o = l.w * N + l.s, gw = wgrow[l.w]; if (gw < .5) { lscale[i] = 0; continue; }
        const x = lerp(px[o], px[o + 1], l.f), y = lerp(py[o], py[o + 1], l.f), u = abs(wu[o]) * l.sens;
        lx[i] = x; ly[i] = y; la[i] = sang[o] + l.side * (.62 - .3 * min(1, u)) + sin(t * (5 + 9 * l.shade) + l.ph) * (.05 + .22 * min(1, u));
        lscale[i] = min(1, lscale[i] + dt / (4 * BEAT));
        /* the count: wind load (dynamic pressure, so speed squared) accumulates; at the fixed threshold the leaf turns over and the count starts again */
        lC[i] += LEAF_RATE * u * u * dt;
        if (lC[i] >= C_STAR) { lC[i] = 0; ltarget[i] ^= 1; lglint[i] = 1; S.flips++; if (llast[i] >= 0) { const iv = t - llast[i]; S.intervals[S.nInt % 600] = iv; S.nInt++; if (S.rawIntervals) S.rawIntervals.push(iv); } llast[i] = t; }
        lface[i] += (ltarget[i] - lface[i]) * min(1, dt * 14); lglint[i] *= exp(-dt * 5);
      } else if (st === FALL) { fal++; const u = windAt(lx[i], ly[i], t, U); lvx[i] += (u * .9 - lvx[i]) * min(1, dt * 2.2); lvy[i] += (-.15 - .05 * sin(t * 3 + l.ph) - lvy[i]) * min(1, dt * 1.6); lx[i] += lvx[i] * dt; ly[i] += lvy[i] * dt; la[i] += lspin[i] * dt; lface[i] = .5 + .5 * sin(la[i] * 1.3); lglint[i] *= exp(-dt * 5);
        if (ly[i] <= .012 || abs(lx[i]) > 3) { lstate[i] = GONE; if (S.landed.length < 40) S.landed.push([lx[i], t, i === S.oneLeaf ? 1 : 0]); } }
    }
    S.attached = att; S.falling = fal;
  }
  /* one fixed step of 1/60 s; the caller may take several per frame */
  S.step = function (dt, beat, Uo) { S.t += dt; S.beat = beat; const U = S.U = Uo !== undefined ? Uo : wind.level(beat); structure(beat, S.t, U); withies(dt, beat, S.t, U); leaves(dt, beat, S.t, U); };
  S.seek = function (beat) { S.beat = beat; S.U = wind.level(beat); structure(beat, S.t, 0); hang(beat); lstate.fill(GONE); ltarget.fill(0); lface.fill(0); lC.fill(0); llast.fill(-1); S.landed.length = 0; S.nInt = 0; S.flips = 0;
    if (S.oneLeaf < 0) { structure(200, 0, 0); let best = 0, by = -1; for (let i = 0; i < nl; i += 3) { const l = L[i], w = W[l.w]; if (w.z > .3 && l.s < 3 && l.regen < 330) { const a = attach(l.w); if (a[1] > by && abs(a[0]) < .3) { by = a[1]; best = i; } } } S.oneLeaf = best; structure(beat, S.t, 0); }
    for (let i = 0; i < nl; i++) { const l = L[i]; if (beat >= l.appear && (beat < l.fall || beat >= l.regen) && !(i === S.oneLeaf && beat >= 352)) { lstate[i] = ATT; lscale[i] = sstep((beat - (beat >= l.regen ? l.regen : l.appear)) / 4); ltarget[i] = rnd() < .22 ? 1 : 0; lface[i] = ltarget[i]; lC[i] = rnd() * C_STAR; } }
    for (let k = 0; k < 150; k++) S.step(1 / 60, beat); S.nInt = 0; S.flips = 0; S.landed.length = 0; };
  S.creak = function (vel, k) { const lim = []; for (let i = 1; i < nStruct; i++) if (Br[i].level === 1 || Br[i].level === 2) lim.push(i); const bi = lim[(k * 7 + 3) % lim.length], b = Br[bi]; b.creakT = S.t; b.creakA = min(.1, vel * .7) * (b.level === 1 ? .8 : 1.3) * (k % 2 ? 1 : -1); return bi; };
  /* coefficient of variation of the last (up to) 600 leaf-turn intervals */
  S.cv = function () { const n = min(S.nInt, 600); if (n < 30) return null; let m = 0, v = 0; for (let i = 0; i < n; i++) m += S.intervals[i]; m /= n; for (let i = 0; i < n; i++) v += pow(S.intervals[i] - m, 2); return { cv: sqrt(v / n) / m, n, mean: m }; };
  S.radius = function (bi, i) { const b = Br[bi]; return b.level === 4 ? sqrt(b.area[i]) * grow[bi] * min(1, sqrt(Br[0].area[0]) / .03) : 1.15 * sqrt(b.area[i]) * (b.level === 0 && i === 0 ? 1.55 : b.level === 0 && i === 1 ? 1.12 : 1); };
  S.perch = function (who) { const p = tree.perches[who], b = Br[p.br], q = pointAt(P[p.br], b.K, p.t); return [q[0], q[1] + S.radius(p.br, Math.round(p.t * b.K)), tree.Br[p.br].z]; };
  S.seek(0);
  return S;
}
const bankTop = x => BANK + .01 * sin(x * 1.7 + .6) + .005 * sin(x * 5.1);

const api = { rng, BPM, BEAT, SCORE_BEATS, END_BEATS, SONG_START, SONG_BEATS, SONG2_START, SEED, SECTIONS, gS, buildScore, buildBirds, timeline, PARROT_SONG, LYRIC_LINES, THIRD_BELOW, sunAt, rainAt, rainbowAt, buildWind, buildTree, leonardoError, areas, makeSim, QUALITY, bankTop, BANK, C_STAR, LEAF_RATE, R_WITHY, mtf, ATT, FALL, GONE };
if (typeof module !== 'undefined' && module.exports) module.exports = api;
root.WILLOW = Object.assign(root.WILLOW || {}, api);
})(typeof window !== 'undefined' ? window : globalThis);
