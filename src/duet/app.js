(function () {
'use strict';
const D = window.DUET, still = matchMedia('(prefers-reduced-motion: reduce)').matches, RED = '#c4472d', BLUE = '#2466b8', INK = '#14202a', LEAF = '#e0ae35', VIR = '#0d7a70';
let W = D.world(Math.floor(Math.random() * 1e6) + 1), sound = false, ac = null, vo = null;
const $ = id => document.getElementById(id), cv = ['scene', 'sono', 'exp', 'man'].map($), cx = cv.map(c => c.getContext('2d'));
function fit() { cv.forEach(c => { const r = c.getBoundingClientRect(), d = Math.min(devicePixelRatio || 1, 2); c.width = Math.round(r.width * d); c.height = Math.round(r.height * d); }); H = []; M = []; }
let H = [], M = [], sep = 0;
addEventListener('resize', fit);

/* the paper's own words, chosen by what is happening */
const Q = {
  near: ['if we move the birds within earshot – so that they can hear each other – they synchronise almost immediately.', 'the birds are not simply repeating what they have heard – they are pursuing a narrative embodied by the dynamical attractors (central pattern generators) in their generative models that have been synchronised through sensory exchange.', 'both birds can sing from the same hymn sheet, preserving sequential and hierarchical structure in their shared narrative.'],
  far: ['if the birds cannot hear each other, the chaotic dynamics implicit in their generative models causes their expectations to follow independent trajectories'],
  noatt: ['Put simply, we cannot speak and listen at the same time', 'active inference presents in one of two modes; either attending to sensations or acting during periods of sensory attenuation.'] };
let qi = 0, qKey = '', qT = 0;
function say(now) { const key = !W.attenuate ? 'noatt' : W.earshot ? 'near' : 'far'; if (key !== qKey || now - qT > 11000) { if (key !== qKey) qi = 0; else qi = (qi + 1) % Q[key].length; qKey = key; qT = now; $('quote').innerHTML = '“' + Q[key][qi] + '”<cite>Friston &amp; Frith, 2015</cite>'; } }

/* the voice: one sine per bird, pitch and loudness from the two fast states, as in the paper's syrinx */
const pitch = y => 2000 + 3000 * Math.max(0, Math.min(1, (y + 25) / 50)), loud = z => Math.max(0, Math.min(1, z / 42));
function audio() { if (!ac) { try { ac = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { return; } vo = [-.6, .6].map(p => { const o = ac.createOscillator(), g = ac.createGain(), pn = ac.createStereoPanner ? ac.createStereoPanner() : null; o.type = 'sine'; g.gain.value = 0; o.connect(g); if (pn) { pn.pan.value = p; g.connect(pn); pn.connect(ac.destination); } else g.connect(ac.destination); o.start(); return { o, g }; }); } if (ac.state === 'suspended') ac.resume(); }
function voice() { if (!vo) return; [W.A, W.B].forEach((b, i) => { const on = sound && (b.out[0] || b.out[1]); vo[i].o.frequency.setTargetAtTime(pitch(b.out[0]), ac.currentTime, .01); vo[i].g.gain.setTargetAtTime(on ? loud(b.out[1]) * .05 : 0, ac.currentTime, .02); }); }

/* a small bird, in ink and wash */
function bird(c, x, y, s, col, open, face, bob) { c.save(); c.translate(x, y + bob); c.scale(face * s, s);
  c.fillStyle = col; c.strokeStyle = INK; c.lineWidth = 1.6 / s; c.lineJoin = 'round';
  c.beginPath(); c.moveTo(-34, 4); c.quadraticCurveTo(-70, 22, -78, 40); c.quadraticCurveTo(-52, 30, -30, 20); c.closePath(); c.globalAlpha = .9; c.fill(); c.stroke();                       /* tail */
  const g = c.createRadialGradient(-6, -12, 4, 0, 0, 46); g.addColorStop(0, '#fff'); g.addColorStop(.25, col); g.addColorStop(1, col); c.fillStyle = g; c.globalAlpha = 1;
  c.beginPath(); c.ellipse(0, 4, 38, 28, -.18, 0, 6.2832); c.fill(); c.stroke();                                                                                                                 /* body */
  c.fillStyle = 'rgba(255,253,248,.6)'; c.beginPath(); c.ellipse(8, 14, 22, 14, -.1, 0, 6.2832); c.fill();                                                                                     /* breast */
  c.fillStyle = col; c.beginPath(); c.arc(30, -18, 18, 0, 6.2832); c.fill(); c.stroke();                                                                                                        /* head */
  c.strokeStyle = 'rgba(20,32,42,.55)'; c.beginPath(); c.moveTo(-22, -2); c.quadraticCurveTo(-2, 16, 16, 2); c.stroke(); c.beginPath(); c.moveTo(-18, 6); c.quadraticCurveTo(-2, 20, 10, 10); c.stroke(); /* wing */
  c.strokeStyle = INK; c.fillStyle = LEAF; const a = open * .5; c.beginPath(); c.moveTo(45, -22); c.lineTo(45 + 20 * Math.cos(-a), -20 + 20 * Math.sin(-a) - 2); c.lineTo(46, -17); c.closePath(); c.fill(); c.stroke();
  c.beginPath(); c.moveTo(45, -15); c.lineTo(45 + 18 * Math.cos(a), -15 + 18 * Math.sin(a) + 1); c.lineTo(46, -19); c.closePath(); c.fill(); c.stroke();                                         /* beak */
  c.fillStyle = INK; c.beginPath(); c.arc(34, -22, 2.8, 0, 6.2832); c.fill(); c.fillStyle = '#fff'; c.beginPath(); c.arc(35, -23, 1, 0, 6.2832); c.fill();
  c.strokeStyle = INK; c.lineWidth = 1.4 / s; c.beginPath(); c.moveTo(-4, 30); c.lineTo(-6, 44); c.moveTo(8, 30); c.lineTo(8, 44); c.stroke(); c.restore(); }
function scene(now) { const c = cx[0], w = cv[0].width, h = cv[0].height, u = w / 1000; c.clearRect(0, 0, w, h);
  const bg = c.createLinearGradient(0, 0, 0, h); bg.addColorStop(0, '#fffdf8'); bg.addColorStop(1, '#f6eed6'); c.fillStyle = bg; c.fillRect(0, 0, w, h);
  sep += ((W.earshot ? 0 : 1) - sep) * .06; const by = h * .66, xa = w * (.36 - .2 * sep), xb = w * (.64 + .2 * sep);
  c.strokeStyle = '#4a3a2a'; c.lineCap = 'round'; c.lineWidth = 7 * u; c.beginPath(); c.moveTo(-10, by + 34 * u); c.quadraticCurveTo(w * .25, by + 4 * u, w * (.5 - .1 * sep), by + 14 * u); c.stroke();
  c.beginPath(); c.moveTo(w + 10, by + 30 * u); c.quadraticCurveTo(w * .75, by + 2 * u, w * (.5 + .1 * sep), by + 14 * u); c.stroke();
  for (let i = 0; i < 9; i++) { const lx = w * (.06 + i * .11) + Math.sin(i * 5) * 20 * u, ly = by - 20 * u - (i % 3) * 16 * u, sway = still ? 0 : Math.sin(now / 900 + i) * .12; if (Math.abs(lx - w / 2) < w * .1 * sep) continue; c.save(); c.translate(lx, ly); c.rotate(-.6 + i * .3 + sway); c.fillStyle = i % 2 ? LEAF : VIR; c.globalAlpha = .82; c.beginPath(); c.ellipse(0, 0, 15 * u, 6 * u, 0, 0, 6.2832); c.fill(); c.restore(); }
  const oa = loud(W.A.out[1]), ob = loud(W.B.out[1]), bobA = still ? 0 : Math.sin(now / 130) * oa * 3 * u, bobB = still ? 0 : Math.sin(now / 130) * ob * 3 * u, s = 1.25 * u;
  /* the song in the air: rings from the singer, reaching the listener only if within earshot */
  [[xa, oa, RED, 1], [xb, ob, BLUE, -1]].forEach(([x, o, col, dir]) => { if (o < .03) return; for (let k = 0; k < 4; k++) { const ph = ((now / 520) + k / 4) % 1, r = (30 + ph * (W.earshot ? 190 : 80)) * u; c.strokeStyle = col; c.globalAlpha = (1 - ph) * .5 * o; c.lineWidth = 2 * u; c.beginPath(); c.arc(x + dir * 60 * u, by - 46 * u, r, dir > 0 ? -.7 : Math.PI - .7, dir > 0 ? .7 : Math.PI + .7); c.stroke(); } }); c.globalAlpha = 1;
  bird(c, xa, by - 26 * u, s, RED, oa, 1, bobA); bird(c, xb, by - 26 * u, s, BLUE, ob, -1, bobB); }

function charts() { const A = W.A, B = W.B;
  { const c = cx[1], w = cv[1].width, h = cv[1].height; c.drawImage(cv[1], -2, 0); c.fillStyle = '#fffdf8'; c.fillRect(w - 2, 0, 2, h); [[A, RED], [B, BLUE]].forEach(([b, col]) => { const o = loud(b.out[1]); if (o > .04) { const y = h - (pitch(b.out[0]) - 2000) / 3000 * h; c.globalAlpha = Math.min(1, .25 + o); c.fillStyle = col; c.fillRect(w - 2, y - 2, 2, 4); c.globalAlpha = 1; } }); if (Math.abs((W.t % 2)) < .012) { c.fillStyle = '#d9cfae'; c.fillRect(w - 2, 0, 1, h); } }
  { const c = cx[2], w = cv[2].width, h = cv[2].height; H.push([A.f[1], B.f[1]]); if (H.length > w / 2) H.shift(); c.clearRect(0, 0, w, h); c.strokeStyle = '#d9cfae'; c.lineWidth = 1; c.beginPath(); c.moveTo(0, h / 2); c.lineTo(w, h / 2); c.stroke(); [[0, RED], [1, BLUE]].forEach(([k, col]) => { c.strokeStyle = col; c.lineWidth = 2; c.globalAlpha = .9; c.beginPath(); H.forEach((v, i) => { const x = w - (H.length - i) * 2, y = h / 2 - v[k] / 30 * h * .46; if (i) c.lineTo(x, y); else c.moveTo(x, y); }); c.stroke(); }); c.globalAlpha = 1; }
  { const c = cx[3], w = cv[3].width, h = cv[3].height; M.push([A.f[0], B.f[0], A.f[1], B.f[1], A.f[2] - 25, B.f[2] - 25]); if (M.length > 520) M.shift(); c.clearRect(0, 0, w, h); c.strokeStyle = '#d9cfae'; c.lineWidth = 1; c.beginPath(); c.moveTo(0, h); c.lineTo(w, 0); c.stroke(); const P = v => w / 2 + v / 30 * w * .46, R = v => h / 2 - v / 30 * h * .46;
    [[0, '#0d7a70'], [2, '#b98619'], [4, '#14202a']].forEach(([k, col]) => { c.fillStyle = col; M.forEach((m, i) => { c.globalAlpha = .15 + .6 * i / M.length; c.fillRect(P(m[k]) - 1.5, R(m[k + 1]) - 1.5, 3, 3); }); }); c.globalAlpha = 1; } }

let last = performance.now(), acc = 0;
function frame(now) { requestAnimationFrame(frame); let dt = Math.min(.05, (now - last) / 1000); last = now; if (document.hidden) return; const n = Math.round(dt * 2000); for (let i = 0; i < n; i++) D.tick(W, 1 / 2000);
  scene(now); acc += dt; if (acc > 1 / 50) { acc = 0; charts(); } voice(); say(now);
  const a = W.singer === 'A'; $('whoA').textContent = a ? 'red sings' : 'red listens'; $('whoB').textContent = a ? 'blue listens' : 'blue sings'; }
function toggle(id, key) { const b = $(id); b.onclick = () => { W[key] = !W[key]; b.setAttribute('aria-pressed', W[key] ? 'true' : 'false'); if (id === 'ear') b.textContent = W[key] ? 'Within earshot' : 'Out of earshot'; if (id === 'att') b.textContent = W[key] ? 'Sensory attenuation' : 'No attenuation'; }; }
toggle('ear', 'earshot'); toggle('att', 'attenuate');
$('snd').onclick = () => { sound = !sound; if (sound) audio(); $('snd').setAttribute('aria-pressed', sound ? 'true' : 'false'); };
$('again').onclick = () => { const e = W.earshot, a = W.attenuate; W = D.world(Math.floor(Math.random() * 1e6) + 1); W.earshot = e; W.attenuate = a; H = []; M = []; cx[1].clearRect(0, 0, cv[1].width, cv[1].height); };
fit(); requestAnimationFrame(frame); window.DUETPAGE = { get W() { return W; } };
})();
