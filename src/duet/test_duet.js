// Bets, written before the run:
// B1 within earshot: mean distance between the two birds' fast expectations over the last 4 s of 16 s is under 2.0 (attractor is about 40 across) in 5 of 5 seeds.
// B2 out of earshot: the same distance stays above 8 in 5 of 5 seeds.
// B3 without sensory attenuation, sensation pulls on the singer at least 3 times harder than with it.
const D = require('./duet_model.js'); const seeds = [3, 11, 29, 57, 101];
const near = seeds.map(s => D.trial(16, { earshot: true }, s)), far = seeds.map(s => D.trial(16, { earshot: false }, s)), noatt = seeds.map(s => D.trial(16, { earshot: true, attenuate: false }, s));
console.log('near ', JSON.stringify(near)); console.log('far  ', JSON.stringify(far)); console.log('noatt', JSON.stringify(noatt));
console.log('B1', near.filter(r => r.fast < 2).length + '/5', 'B2', far.filter(r => r.fast > 8).length + '/5', 'B3 ratio', (noatt.reduce((a, r) => a + r.pullOnSinger, 0) / near.reduce((a, r) => a + r.pullOnSinger, 0)).toFixed(2));
