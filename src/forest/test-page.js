// Bets B8 and B10 (see BETS.md), plus layout checks. Run: node test-page.js   Output appended to results-page.txt
const { chromium, devices } = require('playwright'), fs = require('fs'), path = require('path');
const ROOT = 'file://' + path.join(__dirname, '..', '..');
const ARGS = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'];
const out = []; let fails = 0;
const say = (id, ok, msg) => { if (ok === false) fails++; const s = `${ok === null ? 'NOTE' : ok ? 'PASS' : 'FAIL'}  ${id}  ${msg}`; out.push(s); console.log(s); };
// counts what is drawn inside each animation frame
const COUNTER = () => { const S = window.__count = { frames: [], cur: null, on: false };
  const wrap = (proto, names, kind) => names.forEach(n => { const d = Object.getOwnPropertyDescriptor(proto, n); if (!d || typeof d.value !== 'function') return; const f = d.value; proto[n] = function () { if (S.cur) { S.cur.all2d += kind === '2d' ? 1 : 0; if (kind === 'gl') S.cur.gl++; if (n === 'fill' || n === 'stroke' || n === 'drawImage' || n === 'fillRect' || n === 'strokeRect' || n === 'fillText') S.cur.paint++; if (/^create(Radial|Linear|Conic)Gradient$|^createPattern$/.test(n)) S.cur.grad++; } return f.apply(this, arguments); }; });
  wrap(CanvasRenderingContext2D.prototype, Object.getOwnPropertyNames(CanvasRenderingContext2D.prototype).filter(n => n !== 'constructor'), '2d');
  wrap(WebGLRenderingContext.prototype, ['drawArrays', 'drawElements'], 'gl');
  const raf = window.requestAnimationFrame.bind(window); window.requestAnimationFrame = cb => raf(ts => { if (S.on) { S.cur = { all2d: 0, paint: 0, grad: 0, gl: 0, ms: 0 }; const t0 = performance.now(); cb(ts); S.cur.ms = performance.now() - t0; S.frames.push(S.cur); S.cur = null; } else cb(ts); }); };
const mean = (a, k) => a.reduce((s, f) => s + f[k], 0) / a.length, max = (a, k) => a.reduce((s, f) => Math.max(s, f[k]), 0);
async function open(browser, url, opt, init) { const ctx = await browser.newContext(opt || { viewport: { width: 1280, height: 800 } }), page = await ctx.newPage(), errs = [];
  page.on('pageerror', e => errs.push('pageerror: ' + e.message)); page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await page.route('**/fonts.g*/**', r => r.fulfill({ body: '', contentType: 'text/css' })); if (init) await page.addInitScript(init); await page.goto(url); return { ctx, page, errs }; }
const ready = async page => { const t0 = Date.now(); while (Date.now() - t0 < 120000) { if (await page.evaluate(() => window.__forest && window.__forest.ready)) return true; await page.waitForTimeout(500); } return false; };

(async () => { const browser = await chromium.launch({ args: ARGS });
  // B8: new page
  let nw, old;
  { const { ctx, page, errs } = await open(browser, ROOT + '/forest.html?q=1&at=2026-10-25T14:30&wx=wind', null, COUNTER); await ready(page); await page.waitForTimeout(3000);
    await page.evaluate(() => { window.__count.frames = []; window.__count.on = true; }); const t0 = Date.now(); while (Date.now() - t0 < 90000) { if (await page.evaluate(() => window.__count.frames.length) >= 12) break; await page.waitForTimeout(500); }
    const fr = await page.evaluate(() => window.__count.frames), info = await page.evaluate(() => ({ parties: __forest.world.parties.length, people: __forest.world.parties.reduce((s, p) => s + p.members.length, 0), birds: __forest.world.birds.length, leaves: __forest.world.leaves.length }));
    nw = { n: fr.length, all: mean(fr, 'all2d'), allMax: max(fr, 'all2d'), paint: mean(fr, 'paint'), paintMax: max(fr, 'paint'), grad: max(fr, 'grad'), glMin: Math.min(...fr.map(f => f.gl)), glMax: max(fr, 'gl'), ms: mean(fr, 'ms') };
    say('B8-new', nw.n >= 5 && nw.glMin === 1 && nw.glMax === 1 && nw.grad === 0 && nw.paintMax <= 220 && nw.allMax <= 2500, `${nw.n} frames; WebGL draw calls per frame ${nw.glMin} to ${nw.glMax}; gradients created ${nw.grad}; 2D fill/stroke/drawImage per frame mean ${nw.paint.toFixed(0)}, max ${nw.paintMax}; all 2D method calls mean ${nw.all.toFixed(0)}, max ${nw.allMax}; scene: ${info.parties} parties (${info.people} figures and dogs), ${info.birds} birds, ${info.leaves} loose leaves; script time per frame ${nw.ms.toFixed(2)} ms (software GL, busy machine); errors: ${errs.length ? errs.join(' / ') : 'none'}`);
    await ctx.close(); }
  { const { ctx, page } = await open(browser, ROOT + '/crr-forest-seasonal.html', null, COUNTER); await page.waitForTimeout(14000);
    await page.evaluate(() => { window.__count.frames = []; window.__count.on = true; }); const t0 = Date.now(); while (Date.now() - t0 < 90000) { if (await page.evaluate(() => window.__count.frames.length) >= 12) break; await page.waitForTimeout(500); }
    const fr = await page.evaluate(() => window.__count.frames); old = { n: fr.length, all: mean(fr, 'all2d'), paint: mean(fr, 'paint'), grad: mean(fr, 'grad'), ms: mean(fr, 'ms') };
    say('B8-old', null, `old page, same counter: ${old.n} frames; gradients created per frame ${old.grad.toFixed(0)}; 2D fill/stroke/drawImage per frame ${old.paint.toFixed(0)}; all 2D method calls per frame ${old.all.toFixed(0)}; script time per frame ${old.ms.toFixed(2)} ms`);
    say('B8-ratio', nw.all <= old.all / 4, `new/old 2D method calls per frame = ${nw.all.toFixed(0)}/${old.all.toFixed(0)} = ${(nw.all / old.all).toFixed(3)} (bet: at most 0.25)`);
    await ctx.close(); }
  // B10 a: geolocation denied
  const shows = page => page.evaluate(() => ({ time: document.getElementById('time').textContent.trim(), ev: document.querySelectorAll('#events li').length, say: document.getElementById('say').textContent, season: document.getElementById('season').textContent, pressed: document.getElementById('wx').getAttribute('aria-pressed') }));
  { const { ctx, page, errs } = await open(browser, ROOT + '/forest.html?q=1'); await ready(page); await page.click('#wx'); await page.waitForTimeout(2500); const s = await shows(page);
    say('B10-denied', errs.length === 0 && /\d/.test(s.time) && s.ev === 3, `clock "${s.time}", events ${s.ev}, message "${s.say}", errors: ${errs.length ? errs.join(' / ') : 'none'}`); await ctx.close(); }
  // B10 b: weather request fails
  { const { ctx, page, errs } = await open(browser, ROOT + '/forest.html?q=1', { viewport: { width: 1280, height: 800 }, permissions: ['geolocation'], geolocation: { latitude: 53.48, longitude: -2.24 } });
    await page.route('**/api.open-meteo.com/**', r => r.abort()); await ready(page); await page.click('#wx'); await page.waitForTimeout(3000); const s = await shows(page);
    const mine = errs.filter(e => !/Failed to load resource/.test(e));
    say('B10-nofetch', errs.length === 0 && /\d/.test(s.time) && s.ev === 3, `clock "${s.time}", events ${s.ev}, message "${s.say}", errors: ${errs.length ? errs.join(' / ') : 'none'}; errors other than the browser's own line for the blocked request: ${mine.length}`); await ctx.close(); }
  // weather arrives (mocked reply): snow
  { const { ctx, page, errs } = await open(browser, ROOT + '/forest.html?q=1', { viewport: { width: 1280, height: 800 }, permissions: ['geolocation'], geolocation: { latitude: -33.87, longitude: 151.21 } });
    await page.route('**/api.open-meteo.com/**', r => r.fulfill({ contentType: 'application/json', body: JSON.stringify({ current: { temperature_2m: -1.4, relative_humidity_2m: 92, precipitation: 0.4, rain: 0, showers: 0, snowfall: 0.3, snow_depth: 0.06, cloud_cover: 100, wind_speed_10m: 9, visibility: 3000, weather_code: 73 } }) }));
    await ready(page); await page.click('#wx'); await page.waitForTimeout(6000); const s = await shows(page), e = await page.evaluate(() => ({ snow: __forest.env.snowCover, lat: __forest.place.lat }));
    say('weather-mock', errs.length === 0 && s.pressed === 'true' && /snow, -1°C/.test(s.season) && /southern/.test(s.season), `season line "${s.season}", button pressed ${s.pressed}, snow cover moving to ${e.snow.toFixed(2)}, latitude ${e.lat}; errors: ${errs.length ? errs.join(' / ') : 'none'}`); await ctx.close(); }
  // B10 c: no WebGL
  { const { ctx, page, errs } = await open(browser, ROOT + '/forest.html?q=1', null, () => { const g = HTMLCanvasElement.prototype.getContext; HTMLCanvasElement.prototype.getContext = function (t) { return /webgl/.test(t) ? null : g.apply(this, arguments); }; });
    await page.waitForTimeout(9000); const s = await shows(page), gl = await page.evaluate(() => __forest.gl); await page.screenshot({ path: path.join(__dirname, 'no-webgl.png') });
    say('B10-nowebgl', errs.length === 0 && gl === false && /\d/.test(s.time) && s.ev === 3, `WebGL in use: ${gl}; clock "${s.time}", events ${s.ev}; errors: ${errs.length ? errs.join(' / ') : 'none'}`); await ctx.close(); }
  // layout: phone width, touch targets, reduced motion, calendar chooser
  { const { ctx, page, errs } = await open(browser, ROOT + '/forest.html?q=1&at=2026-11-21T12:00', devices['iPhone 13']); await ready(page);
    const m = await page.evaluate(() => { const r = s => { const b = document.querySelector(s).getBoundingClientRect(); return [Math.round(b.width), Math.round(b.height)]; }; return { sw: document.documentElement.scrollWidth, iw: innerWidth, home: r('.home'), sel: r('#frame'), btn: r('#wx'), label: document.getElementById('top').getAttribute('aria-label') }; });
    say('layout-phone', m.sw <= m.iw && m.home[1] >= 44 && m.sel[1] >= 44 && m.btn[1] >= 44 && errs.length === 0, `scroll width ${m.sw} of ${m.iw}; heights: home ${m.home[1]}, select ${m.sel[1]}, button ${m.btn[1]}; canvas label "${m.label}"; errors: ${errs.length ? errs.join(' / ') : 'none'}`);
    const names = async () => page.evaluate(() => [...document.querySelectorAll('#events li')].map(li => li.querySelector('.count').textContent + ' ' + li.querySelector('.name').textContent).join(' | '));
    const a = await names(); await page.selectOption('#frame', 'The Jewish year'); await page.waitForTimeout(400); const b = await names(); await page.selectOption('#frame', 'East Asia'); await page.waitForTimeout(400); const c = await names();
    say('chooser', /Thanksgiving/.test(a) && /Hanukkah/.test(b) && !/Thanksgiving|Hanukkah/.test(c) && /Winter Solstice/.test(c), `Everyone: ${a} || The Jewish year: ${b} || East Asia: ${c}`); await ctx.close(); }
  { const { ctx, page, errs } = await open(browser, ROOT + '/forest.html?q=1', { viewport: { width: 1280, height: 800 }, reducedMotion: 'reduce' }, COUNTER); await page.waitForTimeout(8000);
    await page.evaluate(() => { window.__count.frames = []; window.__count.on = true; }); await page.waitForTimeout(3000); const n = await page.evaluate(() => window.__count.frames.length), s = await shows(page);
    say('reduced-motion', n === 0 && errs.length === 0 && s.ev === 3, `animation frames in 3 s with reduced motion: ${n}; clock "${s.time}"; errors: ${errs.length ? errs.join(' / ') : 'none'}`); await ctx.close(); }
  await browser.close(); out.push(`${fails} failed`); console.log(`${fails} failed`);
  fs.writeFileSync(path.join(__dirname, 'results-page.txt'), new Date().toISOString() + '\n' + out.join('\n') + '\n', { flag: 'a' });
})();
