// B5 (browser half) and B9, and a live run with sound. Bets are in bets.md (written first).
const { chromium, devices } = require('playwright'), path = require('path');
const GL = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'], URL = 'file://' + path.resolve(__dirname, '../../willow.html'), SHOTS = process.argv[2] || '/tmp';
(async () => {
  const br = await chromium.launch({ args: GL });
  for (const [name, opt] of [['desktop 1280x800', { viewport: { width: 1280, height: 800 } }], ['iPhone 13', devices['iPhone 13']]]) {
    const ctx = await br.newContext(opt), p = await ctx.newPage(), errs = []; p.on('pageerror', e => errs.push('pageerror ' + e.message)); p.on('console', m => { if (m.type() === 'error') errs.push('console ' + m.text()); });
    await p.addInitScript(() => { window.__ac = 0; for (const k of ['AudioContext', 'webkitAudioContext']) { const A = window[k]; if (A) window[k] = function (...a) { window.__ac++; return new A(...a); }; } });
    await p.goto(URL); await p.waitForTimeout(4000);
    const before = await p.evaluate(() => ({ ac: window.__ac, sw: document.documentElement.scrollWidth, iw: innerWidth, small: [...document.querySelectorAll('button, a.home, input')].filter(e => e.offsetParent && e.getBoundingClientRect().height < 43.5).map(e => (e.id || e.textContent) + ':' + Math.round(e.getBoundingClientRect().height)), q: WILLOW_PAGE.quality }));
    await p.click('#play'); await p.waitForTimeout(9000);
    const live = await p.evaluate(() => ({ ac: window.__ac, mode: WILLOW_PAGE.mode, beat: WILLOW_PAGE.beat, state: WILLOW_PAGE.player.ac && WILLOW_PAGE.player.ac.state, fired: WILLOW_PAGE.player.engine && WILLOW_PAGE.player.engine.fired, label: document.getElementById('play').textContent }));
    await p.click('#play'); await p.waitForTimeout(1500); const b1 = await p.evaluate(() => WILLOW_PAGE.beat); await p.waitForTimeout(1500); const b2 = await p.evaluate(() => WILLOW_PAGE.beat);
    await p.click('#ann'); await p.click('#mixb'); await p.click('#about'); await p.waitForTimeout(500); await p.screenshot({ path: path.join(SHOTS, 'about_' + name.split(' ')[0] + '.png') }); await p.click('#close');
    console.log('B9', name, '| quality', before.q, '| AudioContexts before Play:', before.ac, 'after:', live.ac, '| scrollWidth', before.sw, 'of', before.iw, '| controls under 44 px:', JSON.stringify(before.small), '| live: mode', live.mode, 'beat', live.beat && live.beat.toFixed(2), 'context', live.state, 'events handed to the clock', live.fired, '| paused holds:', Math.abs(b2 - b1) < 1e-6, '| errors', errs.length, errs.slice(0, 4).join(' ; '), (before.ac === 0 && live.ac === 1 && before.sw <= before.iw && !before.small.length && !errs.length && live.mode === 'playing' && live.beat > 1) ? 'PASS' : 'FAIL');
    if (name.startsWith('desktop')) {
      // frame cost in the storm, playing on the manual clock (no sound), 300 frames
      await p.evaluate(() => { WILLOW_PAGE.run(226); }); await p.waitForFunction(() => WILLOW_PAGE.costs.length >= 300 && WILLOW_PAGE.beat > 227, null, { timeout: 0, polling: 1000 }).catch(() => { });
      const c = await p.evaluate(() => { const a = WILLOW_PAGE.costs.slice().sort((x, y) => x - y); return { n: a.length, med: a[a.length >> 1], p95: a[Math.floor(a.length * .95)], dc: WILLOW_PAGE.drawCalls, beat: WILLOW_PAGE.beat }; });
      console.log('B5 (browser, storm, quality ' + before.q + '): JavaScript side of a frame over', c.n, 'frames: median', c.med.toFixed(2), 'ms, 95th centile', c.p95.toFixed(2), 'ms | draw calls', c.dc, (c.med < 4 && c.p95 < 8 && c.dc <= 16) ? 'PASS' : 'FAIL', '(software WebGL: gl calls can block on the rasteriser, so this overstates a real GPU)');
      // the strike
      await p.evaluate(() => WILLOW_PAGE.run(247.7)); await p.waitForFunction(() => WILLOW_PAGE.beat > 248.02, null, { timeout: 0, polling: 200 }).catch(() => { }); await (await p.$('#stage')).screenshot({ path: path.join(SHOTS, 'strike.png') });
    }
    await ctx.close();
  }
  await br.close();
})();
