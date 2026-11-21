/* A Duet for One: the model, with no drawing. After Friston & Frith (2015), Consciousness and Cognition, doi:10.1016/j.concog.2014.12.003.
   Each bird carries the same generative model: a slow Lorenz attractor whose state sets the manifold of a fast one, two of whose states drive a syrinx.
   A bird either sings (it acts to fulfil its own predictions, and turns down the precision of what it hears) or listens (high auditory precision). */
(function (root) {
  const SPEED = 9, SLOW = 1 / 8, GAIN = 1.2, ETA = 0.6, SIG = 10, BETA = 8 / 3, RHO2 = 28, DELAY = 0.045;
  const DR = 1.5, rho1 = y2 => DR * y2 + 10;                         /* a slow state sets the fast attractor's manifold: below 1 it collapses to silence */
  function newBird(rnd) { return { f: [rnd() * 20 - 10, rnd() * 20 - 10, 5 + rnd() * 25], s: [rnd() * 20 - 10, rnd() * 20 - 10, 10 + rnd() * 25], out: [0, 0], buf: [], corr: 0 }; }
  /* one step. heard = [y, z] reaching this bird's ear, or [0,0] for silence. logPi = log precision of audition (2 when listening; 0 when attenuated). */
  function step(b, heard, logPi, singing, dt) {
    const [x, y, z] = b.f, [X, Y, Z] = b.s, r = rho1(Y), Pi = Math.exp(logPi), k = SPEED;
    const ey = heard[0] - y, ez = heard[1] - z;                      /* auditory prediction error */
    const g = SPEED * GAIN * Pi;                                              /* precision-weighted gain on the error */
    const dx = k * (SIG * (y - x)), dy = k * (x * (r - z) - y) + g * ey, dz = k * (x * y - BETA * z) + g * ez;
    /* the slow level explains what the fast level could not: error on the fast flow, passed up through d(rho)/dZ */
    const dYe = ETA * Pi * ey * x * DR;
    const dX = k * SLOW * (SIG * (Y - X)), dY = k * SLOW * (X * (RHO2 - Z) - Y) + dYe, dZ = k * SLOW * (X * Y - BETA * Z);
    b.f = [x + dx * dt, y + dy * dt, z + dz * dt]; b.s = [X + dX * dt, Math.max(-40, Math.min(40, Y + dY * dt)), Z + dZ * dt];
    b.corr = Math.hypot(g * ey, g * ez);                             /* how hard sensation is pulling on expectation */
    b.out = singing ? [b.f[1], b.f[2]] : [0, 0];                     /* action fulfils the prediction: the syrinx does what is expected */
    b.buf.push(b.out); if (b.buf.length > Math.round(DELAY / dt) + 1) b.buf.shift();
    return b;
  }
  function world(seed) { let s = seed || 3; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647; return { t: 0, A: newBird(rnd), B: newBird(rnd), earshot: true, attenuate: true, rnd }; }
  /* turns of two seconds. The singer hears itself a little late; the listener hears the other only if within earshot. */
  function tick(W, dt) { const turn = Math.floor(W.t / 2) % 2, sA = turn === 0, sB = !sA, A = W.A, B = W.B, lateA = A.buf[0] || [0, 0], lateB = B.buf[0] || [0, 0];
    const hearA = sA ? lateA : (W.earshot ? B.out : [0, 0]), hearB = sB ? lateB : (W.earshot ? A.out : [0, 0]);
    step(A, hearA, sA ? (W.attenuate ? 0 : 2) : 2, sA, dt); step(B, hearB, sB ? (W.attenuate ? 0 : 2) : 2, sB, dt); W.t += dt; W.singer = sA ? 'A' : 'B'; return W; }
  const dist = W => Math.hypot(W.A.f[0] - W.B.f[0], W.A.f[1] - W.B.f[1], W.A.f[2] - W.B.f[2]);
  const distSlow = W => Math.hypot(W.A.s[0] - W.B.s[0], W.A.s[1] - W.B.s[1], W.A.s[2] - W.B.s[2]);
  function trial(sec, opt, seed) { const W = world(seed); Object.assign(W, opt || {}); const dt = 1 / 2000; let d = 0, ds = 0, n = 0, c = 0, m = 0; for (let t = 0; t < sec; t += dt) { tick(W, dt); if (t > sec - 4) { d += dist(W); ds += distSlow(W); n++; } const sg = W.singer === 'A' ? W.A : W.B; c += sg.corr; m++; }
    return { fast: +(d / n).toFixed(2), slow: +(ds / n).toFixed(2), pullOnSinger: +(c / m).toFixed(2) }; }
  const api = { world, tick, trial, dist, distSlow, rho1, SPEED }; if (typeof module !== 'undefined') module.exports = api; root.DUET = api;
})(typeof window !== 'undefined' ? window : globalThis);
