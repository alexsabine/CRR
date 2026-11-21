
function midiToFreq(m){return 440*pow(2,(m-69)/12)}
function clamp(v,a,b){return max(a,min(b,v))}

function createNoiseBuf(ctx){
  const b=ctx.createBuffer(2,ctx.sampleRate*2,ctx.sampleRate);
  for(let ch=0;ch<2;ch++){const d=b.getChannelData(ch);for(let i=0;i<d.length;i++)d[i]=random()*2-1}
  return b;
}

function createReverb(ctx){
  const sr=ctx.sampleRate,len=sr*6|0;
  const buf=ctx.createBuffer(2,len,sr);
  for(let ch=0;ch<2;ch++){const d=buf.getChannelData(ch);
    for(let i=0;i<24;i++){const t=(0.003+i*0.01+random()*0.006)*sr|0;
      if(t<len)d[t]=0.25*pow(0.72,i)*(0.5+random()*0.5)}
    for(let i=0;i<len;i++){const t=i/sr;
      d[i]+=(random()*2-1)*0.06*(exp(-t*0.8)*0.5+exp(-t*2.5)*0.5)}}
  const conv=ctx.createConvolver();conv.buffer=buf;return conv;
}
function safeParam(param,val,time){
  const v=isFinite(val)?val:0;
  try{param.setValueAtTime(max(0.0001,abs(v)),time)}catch(e){}
}
const SONG_TYPES = {
  whistle: {durRange:[0.2,0.55], freqRange:[1800,4500], sweepRatio:1.5, harmonics:3, formantQ:7,
    microWarble:true, warbleRate:[15,45], warbleDepth:0.04},
  trill:   {durRange:[0.08,0.18],freqRange:[2200,5500], sweepRatio:1.25, harmonics:3, formantQ:4,
    microWarble:false, warbleRate:[80,200], warbleDepth:0.15},
  warble:  {durRange:[0.25,0.6], freqRange:[1200,3800], sweepRatio:1.8, harmonics:5, formantQ:3,
    microWarble:true, warbleRate:[50,180], warbleDepth:0.25},
  click:   {durRange:[0.008,0.025],freqRange:[3000,9000], sweepRatio:0.2, harmonics:8, formantQ:1.5,
    microWarble:false, warbleRate:[0,0], warbleDepth:0},
  chatter: {durRange:[0.04,0.09],freqRange:[1800,3200], sweepRatio:1.05, harmonics:4, formantQ:5,
    microWarble:false, warbleRate:[100,250], warbleDepth:0.3},
  descend: {durRange:[0.15,0.35],freqRange:[3500,6500], sweepRatio:0.4, harmonics:2, formantQ:8,
    microWarble:true, warbleRate:[8,25], warbleDepth:0.02},
  churr:   {durRange:[0.3,0.8], freqRange:[600,1500], sweepRatio:1.05, harmonics:6, formantQ:2,
    microWarble:false, warbleRate:[30,60], warbleDepth:0.4},
  contact: {durRange:[0.04,0.1], freqRange:[2500,4500], sweepRatio:1.8, harmonics:2, formantQ:6,
    microWarble:false, warbleRate:[0,0], warbleDepth:0},
  squeal:  {durRange:[0.1,0.25],freqRange:[3000,7000], sweepRatio:2.5, harmonics:5, formantQ:2.5,
    microWarble:true, warbleRate:[60,150], warbleDepth:0.2},
  mimic:   {durRange:[0.15,0.4], freqRange:[1500,5500], sweepRatio:1.4, harmonics:3, formantQ:5,
    microWarble:true, warbleRate:[10,40], warbleDepth:0.06}
};
const STARLING_SCALE = [
  [64,67,69,71,74],
  [76,79,81,83,86],
  [88,91,93,95,98]
];
function playDualSyrinx(intensity, startTime, songType, pitchClass, together, birdId, pan) {
  if(!ac || intensity < 0.005) return;
  const now = startTime || ac.currentTime;
  const type = SONG_TYPES[songType] || SONG_TYPES.whistle;
  const dur = type.durRange[0] + random() * (type.durRange[1] - type.durRange[0]);
  const baseFreq = type.freqRange[0] + random() * (type.freqRange[1] - type.freqRange[0]);

  const register = pitchClass < 5 ? 0 : pitchClass < 10 ? 1 : 2;
  const noteIdx = pitchClass % 5;
  const scaleFreq = midiToFreq(STARLING_SCALE[register][noteIdx]);
  const musicalBlend = 0.4 + together * 0.3;
  const targetFreq = baseFreq * (1 - musicalBlend) + scaleFreq * musicalBlend;

  const identity = birdId !== undefined ? (birdId * 0.618033988749895) % 1 : random();
  const voiceBrightness = 0.7 + identity * 0.6;
  const voiceRoughness = 0.1 + (1 - identity) * 0.3;

  const vol = intensity * 0.08;
  const masterG = ac.createGain();
  connectVoice(masterG, pan);

  const leftFreq = targetFreq * (0.48 + identity * 0.08);
  const oL = ac.createOscillator();
  oL.type = 'sawtooth';

  const sweepUp = type.sweepRatio > 1;
  oL.frequency.setValueAtTime(max(20, leftFreq * (sweepUp ? 0.65 : 1.25)), now);
  oL.frequency.exponentialRampToValueAtTime(
    max(20, leftFreq * (sweepUp ? type.sweepRatio : 1/type.sweepRatio)),
    now + dur * 0.35
  );
  if(songType === 'whistle' || songType === 'descend' || songType === 'mimic') {
    oL.frequency.exponentialRampToValueAtTime(max(20, leftFreq * 0.55), now + dur * 0.85);
  } else {
    oL.frequency.exponentialRampToValueAtTime(max(20, leftFreq * 0.6), now + dur * 0.9);
  }

  if(type.microWarble) {
    const warbleRate = type.warbleRate[0] + random() * (type.warbleRate[1] - type.warbleRate[0]);
    const warbleLFO = ac.createOscillator();
    warbleLFO.type = 'sine';
    warbleLFO.frequency.value = warbleRate;
    const warbleGain = ac.createGain();
    warbleGain.gain.value = leftFreq * type.warbleDepth;
    warbleLFO.connect(warbleGain);
    warbleGain.connect(oL.frequency);
    warbleLFO.start(now);
    warbleLFO.stop(now + dur + 0.05);
  }

  const fL = ac.createBiquadFilter();
  fL.type = 'bandpass';
  fL.frequency.value = leftFreq * 1.4 * voiceBrightness;
  fL.Q.value = type.formantQ;
  const fL2 = ac.createBiquadFilter();
  fL2.type = 'peaking';
  fL2.frequency.value = leftFreq * 2.8 * voiceBrightness;
  fL2.gain.value = 4;
  fL2.Q.value = 3;
  const gL = ac.createGain();
  gL.gain.value = vol * 0.6;
  oL.connect(fL); fL.connect(fL2); fL2.connect(gL); gL.connect(masterG);

  const rightFreq = targetFreq * (1.0 + identity * 0.25);
  const oR = ac.createOscillator();
  oR.type = songType === 'click' || songType === 'chatter' ? 'square'
          : songType === 'churr' ? 'triangle' : 'sine';
  oR.frequency.setValueAtTime(max(20, rightFreq * (sweepUp ? 0.75 : 1.15)), now);
  oR.frequency.exponentialRampToValueAtTime(
    max(20, rightFreq * (sweepUp ? type.sweepRatio * 0.85 : 1/(type.sweepRatio*0.85))),
    now + dur * 0.3
  );
  oR.frequency.exponentialRampToValueAtTime(max(20, rightFreq * 0.65), now + dur * 0.82);

  if(type.microWarble) {
    const warbleR = ac.createOscillator();
    warbleR.type = 'sine';
    warbleR.frequency.value = (type.warbleRate[0] + type.warbleRate[1]) * 0.5 * (1.15 + identity * 0.2);
    const wgR = ac.createGain();
    wgR.gain.value = rightFreq * type.warbleDepth * 0.8;
    warbleR.connect(wgR);
    wgR.connect(oR.frequency);
    warbleR.start(now);
    warbleR.stop(now + dur + 0.05);
  }

  const fR = ac.createBiquadFilter();
  fR.type = 'bandpass';
  fR.frequency.value = rightFreq * 1.7 * voiceBrightness;
  fR.Q.value = type.formantQ * 0.8;
  const gR = ac.createGain();
  gR.gain.value = vol * 0.4;
  oR.connect(fR); fR.connect(gR); gR.connect(masterG);

  if(type.harmonics >= 2 && vol > 0.008) {
    const oH = ac.createOscillator();
    oH.type = 'sine';
    oH.frequency.setValueAtTime(leftFreq * 2.02, now);
    oH.frequency.exponentialRampToValueAtTime(max(20, leftFreq * 2.4), now + dur * 0.35);
    oH.frequency.exponentialRampToValueAtTime(max(20, leftFreq * 1.75), now + dur * 0.9);
    const gH = ac.createGain();
    gH.gain.value = vol * 0.12 * voiceBrightness;
    gH.gain.exponentialRampToValueAtTime(0.001, now + dur * 0.92);
    oH.connect(gH); gH.connect(masterG);
    oH.start(now); oH.stop(now + dur + 0.05);
  }

  if(type.harmonics >= 4 && vol > 0.01) {
    const o3 = ac.createOscillator();
    o3.type = 'sine';
    o3.frequency.value = leftFreq * 3.01 + random() * 5;
    const g3 = ac.createGain();
    g3.gain.value = vol * 0.06 * voiceBrightness;
    g3.gain.exponentialRampToValueAtTime(0.001, now + dur * 0.7);
    o3.connect(g3); g3.connect(masterG);
    o3.start(now); o3.stop(now + dur + 0.05);
  }

  if(noiseBuf && (songType === 'click' || songType === 'chatter' || songType === 'squeal' || voiceRoughness > 0.2)) {
    const nSrc = ac.createBufferSource();
    nSrc.buffer = noiseBuf;
    nSrc.loop = true;
    const nBP = ac.createBiquadFilter();
    nBP.type = 'bandpass';
    nBP.frequency.value = songType === 'click' ? 5000 + random() * 3000
                        : songType === 'squeal' ? 4000 + random() * 2000
                        : targetFreq * 2;
    nBP.Q.value = songType === 'click' ? 1 : songType === 'chatter' ? 2 : 4;
    const nG = ac.createGain();
    const noiseVol = songType === 'click' ? vol * 1.5
                   : songType === 'chatter' ? vol * 0.6
                   : songType === 'squeal' ? vol * 0.8
                   : vol * voiceRoughness * 0.15;
    nG.gain.setValueAtTime(0, now);
    nG.gain.linearRampToValueAtTime(noiseVol, now + (songType === 'click' ? 0.001 : dur * 0.1));
    nG.gain.exponentialRampToValueAtTime(0.001, now + dur * 0.9);
    nSrc.connect(nBP); nBP.connect(nG); nG.connect(masterG);
    nSrc.start(now); nSrc.stop(now + dur + 0.05);
  }

  if(type.warbleDepth > 0.1 || songType === 'warble' || songType === 'trill' || songType === 'churr') {
    const amRate = (type.warbleRate[0] + type.warbleRate[1]) * 0.5 + random() * 40;
    const amOsc = ac.createOscillator();
    amOsc.type = 'sine';
    amOsc.frequency.value = amRate;
    const amDepth = type.warbleDepth * 0.5;
    const amGain = ac.createGain();
    amGain.gain.setValueAtTime(0, now);
    amGain.gain.linearRampToValueAtTime(amDepth, now + dur * 0.2);
    amGain.gain.setValueAtTime(amDepth * 0.8, now + dur * 0.6);
    amGain.gain.linearRampToValueAtTime(0, now + dur * 0.95);
    amOsc.connect(amGain);
    amGain.connect(masterG.gain);
    amOsc.start(now); amOsc.stop(now + dur + 0.05);
  }

  if(together > 0.5 && songType !== 'click' && songType !== 'contact') {
    const coupling = (together - 0.5) * 0.3;
    const xL = ac.createGain();
    xL.gain.value = vol * coupling * 0.15;
    oL.connect(xL); xL.connect(fR);
    const xR = ac.createGain();
    xR.gain.value = vol * coupling * 0.12;
    oR.connect(xR); xR.connect(fL);
  }

  masterG.gain.setValueAtTime(0, now);
  if(songType === 'click') {
    masterG.gain.linearRampToValueAtTime(2, now + 0.001);
    masterG.gain.exponentialRampToValueAtTime(0.001, now + dur);
  } else if(songType === 'contact') {
    masterG.gain.linearRampToValueAtTime(1.5, now + 0.005);
    masterG.gain.exponentialRampToValueAtTime(0.001, now + dur * 0.8);
  } else if(songType === 'churr') {
    masterG.gain.linearRampToValueAtTime(0.7, now + dur * 0.25);
    masterG.gain.setValueAtTime(0.65, now + dur * 0.7);
    masterG.gain.exponentialRampToValueAtTime(0.001, now + dur * 0.95);
  } else {
    masterG.gain.linearRampToValueAtTime(1, now + dur * 0.12);
    masterG.gain.setValueAtTime(0.85, now + dur * 0.35);
    masterG.gain.exponentialRampToValueAtTime(0.001, now + dur * 0.93);
  }

  oL.start(now); oR.start(now);
  oL.stop(now + dur + 0.1); oR.stop(now + dur + 0.1);
  setTimeout(() => { try { masterG.disconnect() } catch(e) {} }, (dur + 0.5) * 1000);

  return dur;
}
function playStarlingPhrase(intensity, startTime, phraseLength, mood, birdId, pan) {
  if(!ac || intensity < 0.005) return;
  const now = startTime || ac.currentTime;
  const numSyllables = phraseLength || (3 + floor(random() * 6));
  const pitchBase = floor(random() * 15);

  const phraseTypes = mood === 'alarm'
    ? ['click','squeal','chatter','click','warble','click']
    : mood === 'settle'
    ? ['descend','churr','whistle','descend','mimic']
    : ['whistle','whistle','warble','trill','chatter','mimic','warble','whistle'];

  let t = now;
  for(let i = 0; i < numSyllables; i++) {
    const type = phraseTypes[i % phraseTypes.length];
    const syllDur = SONG_TYPES[type].durRange[0] + random() * (SONG_TYPES[type].durRange[1] - SONG_TYPES[type].durRange[0]);
    const isNewSection = i > 0 && i % 3 === 0;
    const gap = isNewSection ? (0.08 + random() * 0.15) : (0.02 + random() * 0.06);
    const pitchShift = (i * 2 + floor(random() * 3)) % 15;
    const together = mood === 'song' ? 0.3 + (i/numSyllables) * 0.5
                 : mood === 'alarm' ? 0.2 + random() * 0.3
                 : 0.5 + random() * 0.3;
    const iArc = 1 - 0.3 * abs(2 * i / numSyllables - 1);
    playDualSyrinx(
      intensity * iArc * (0.7 + random() * 0.3),
      t, type,
      (pitchBase + pitchShift) % 15,
      together, birdId, pan
    );
    t += syllDur + gap;
  }
  return t - now;
}
function playFalconCry(intensity,startTime){
  if(!ac)return;const now=startTime||ac.currentTime;
  const g=ac.createGain();g.connect(natureGain);
  const o=ac.createOscillator();o.type='sawtooth';
  o.frequency.setValueAtTime(1800,now);
  o.frequency.exponentialRampToValueAtTime(1200,now+0.3);
  o.frequency.exponentialRampToValueAtTime(700,now+0.7);
  const f=ac.createBiquadFilter();f.type='bandpass';f.frequency.value=1200;f.Q.value=2;
  o.connect(f);f.connect(g);
  g.gain.setValueAtTime(0,now);g.gain.linearRampToValueAtTime(intensity*0.15,now+0.03);
  g.gain.setValueAtTime(intensity*0.12,now+0.3);g.gain.exponentialRampToValueAtTime(0.001,now+0.8);
  o.start(now);o.stop(now+0.9);
}
