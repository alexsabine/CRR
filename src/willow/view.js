/* Song of Willow: the picture and the page. WebGL for the scene (sky, land, tree, leaves, then water as a rippled mirror of all of it); a 2D layer on top for the birds and small events. */
(function () {
'use strict';
const WL = window.WILLOW, { BEAT, END_BEATS, SECTIONS, BANK } = WL, $ = id => document.getElementById(id);
const { sin, cos, sqrt, abs, floor, max, min, exp, pow, atan2, PI } = Math, TAU = 2 * PI;
const clamp = (v, a, b) => v < a ? a : v > b ? b : v, lerp = (a, b, t) => a + (b - a) * t, sstep = (a, b, x) => { const t = clamp((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
const still = matchMedia('(prefers-reduced-motion: reduce)').matches, small = Math.min(innerWidth, innerHeight) < 600;
const stage = $('stage'), cv = $('scene'), ov = $('over'), o2 = ov.getContext('2d');
const gl = cv.getContext('webgl', { antialias: false, alpha: false, premultipliedAlpha: false, powerPreference: 'high-performance' });
const inst = gl && gl.getExtension('ANGLE_instanced_arrays');
if (!gl || !inst) { $('fail').hidden = false; return; }
let quality = small || (navigator.hardwareConcurrency || 4) <= 4 ? (small ? 'low' : 'mid') : 'high';
const sim = WL.makeSim(WL.SEED, quality), player = WL.makePlayer({ seed: WL.SEED }), TL = player.timeline, rv = WL.rng(4242);

/* ─── shaders ─── */
const NOISE = `precision highp float;
float hash(vec2 p){p=fract(p*vec2(123.34,456.21));p+=dot(p,p+45.32);return fract(p.x*p.y);}
float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x),f.y);}
float fbm(vec2 p){float a=.5,s=0.;for(int i=0;i<5;i++){s+=a*noise(p);p=p*2.03+vec2(17.1,9.2);a*=.5;}return s;}
float fbm3(vec2 p){float a=.5,s=0.;for(int i=0;i<3;i++){s+=a*noise(p);p=p*2.03+vec2(17.1,9.2);a*=.5;}return s;}`;
const QUAD_VS = `attribute vec2 aP;uniform vec4 uCam;varying vec2 vW;varying vec2 vUv;void main(){vUv=aP*.5+.5;vW=uCam.xy+aP*uCam.zw;gl_Position=vec4(aP,0.,1.);}`;
const SKY_FS = NOISE + `
varying vec2 vW;uniform float uT,uStars,uCloud,uFlash,uWind,uWet;uniform vec3 uZen,uMid,uHor,uGlowCol,uSun,uMoon,uCloudLit,uCloudDark,uLand,uGrass,uAmb;uniform vec4 uGlow,uBow;
float bankTop(float x){return ${BANK.toFixed(4)}+.01*sin(x*1.7+.6)+.005*sin(x*5.1);}
vec3 spectrum(float k){return clamp(vec3(1.6-abs(k-.12)*4.2, 1.5-abs(k-.5)*3.6, 1.5-abs(k-.86)*4.2),0.,1.);}
void main(){
  float e=clamp((vW.y-.03)/1.1,0.,1.);
  vec3 col=mix(uHor,uMid,smoothstep(0.,.3,e));col=mix(col,uZen,smoothstep(.16,.95,e));
  float gx=(vW.x-uGlow.x);col+=uGlowCol*uGlow.y*exp(-gx*gx*.8)*exp(-e*4.2);
  /* stars, moon, sun */
  vec2 sp=vW*46.;vec2 sc=floor(sp);float h=hash(sc);vec2 so=fract(sp)-.5-(vec2(hash(sc+3.1),hash(sc+7.7))-.5)*.7;
  float st=step(.972,h)*smoothstep(.1,.0,length(so))*(.55+.45*sin(uT*(1.+h*3.)+h*40.))*(.4+.6*hash(sc+1.3));col+=vec3(.8,.86,1.)*st*uStars*smoothstep(.0,.3,e);
  float md=length(vW-uMoon.xy);float mm=smoothstep(.033,.028,md);vec2 mq=(vW-uMoon.xy)/.03;col=mix(col,vec3(.9,.91,.86)*(.62+.22*fbm3(mq*2.3+4.)+.16*sqrt(max(0.,1.-dot(mq,mq)))),mm*uMoon.z);col+=vec3(.5,.58,.75)*uMoon.z*(.22*exp(-md*7.)+.05*exp(-md*1.6));
  float sd=length(vW-uSun.xy);vec3 sunc=mix(vec3(1.,.62,.3),vec3(1.,.93,.78),smoothstep(.05,.5,uSun.y));col+=uSun.z*(sunc*smoothstep(.03,.012,sd)*.62+sunc*vec3(1.,.8,.6)*(.45*exp(-sd*10.)+.22*exp(-sd*2.4)));
  /* cloud */
  vec2 cp=vec2(vW.x*.55+uT*.006*(1.+3.*uCloud),vW.y*1.7+vW.x*.1);float cn=fbm(cp*1.9+vec2(0.,uT*.002));float cov=mix(.66,.3,uCloud);float c=smoothstep(cov,cov+.26,cn);
  float cs=fbm3(cp*1.9+vec2(.06,.12));vec3 cc=mix(uCloudDark,uCloudLit,clamp(.5+(cn-cs)*5.,0.,1.));col=mix(col,cc,c*(.42+.5*uCloud));
  /* rainbow: primary, and a faint secondary outside it with the colours reversed */
  float bd=length(vW-uBow.xy);float bk=(bd-uBow.z)/.06;float b1=smoothstep(0.,.15,bk)*smoothstep(1.,.85,bk);float bk2=(bd-uBow.z*1.2)/.075;float b2=smoothstep(0.,.2,bk2)*smoothstep(1.,.8,bk2);
  vec3 bow=spectrum(1.-bk)*b1*.46+spectrum(bk2)*b2*.1;bow*=uBow.w*smoothstep(.03,.3,vW.y);col=1.-(1.-col)*(1.-bow);col+=uBow.w*.03*smoothstep(uBow.z,uBow.z-.25,bd);
  col+=uFlash*vec3(.7,.76,1.)*(.35+.65*cn);
  /* far hills, a line of trees, then the bank */
  float h1=.062+.05*fbm3(vec2(vW.x*.55+3.,.5));col=mix(col,mix(uHor,uLand,.2),smoothstep(h1+.006,h1-.006,vW.y)*.85);
  float tr=fbm3(vec2(vW.x*7.+11.,1.5));float h2=.05+.03*tr+.03*pow(noise(vec2(vW.x*23.,4.)),3.)*smoothstep(.35,.6,tr)+.006*noise(vec2(vW.x*120.,2.));col=mix(col,mix(uHor,uLand,.5+.2*noise(vec2(vW.x*30.,vW.y*60.))),smoothstep(h2+.0025,h2-.0025,vW.y));
  float bt=bankTop(vW.x)+(.003*noise(vec2(vW.x*70.,3.))+.007*pow(noise(vec2(vW.x*300.+uWind*sin(uT+vW.x*9.)*.6,8.)),2.))*smoothstep(0.,.01,vW.y);
  float g=fbm3(vec2(vW.x*30.,vW.y*220.));vec3 grass=uGrass*(.62+.5*g+.3*fbm3(vec2(vW.x*3.,5.)))*(1.-.25*uWet);grass=mix(grass*.3,grass,smoothstep(.002,.02,vW.y))*(.8+.35*smoothstep(.02,.045,vW.y));
  col=mix(col,grass,smoothstep(bt+.0016,bt-.0016,vW.y));
  /* reeds at the water's edge, in clumps */
  float cl=smoothstep(.52,.7,noise(vec2(vW.x*2.6+5.,7.)))*step(.22,abs(vW.x));float rx=vW.x*210.+(vW.y*26.)*(uWind*1.2+.25*sin(uT*.7+vW.x*5.));float rh=hash(vec2(floor(rx),9.));
  float reed=cl*step(.45,rh)*smoothstep(.2,.05,abs(fract(rx)-.5))*smoothstep(.02+rh*.075,.0,vW.y-.002);col=mix(col,uGrass*.55,reed*.9);
  gl_FragColor=vec4(col,1.);}`;
const STRIP_VS = `attribute vec2 aC,aN;attribute float aR,aV,aZ,aK;uniform vec4 uCam;uniform float uPx;varying float vD,vR,vV,vZ,vK;
void main(){float r=aR+uPx*.8;vec2 p=aC+aN*r;vD=sign(aV)*r;vR=aR;vV=abs(aV)-1.;vZ=aZ;vK=aK;gl_Position=vec4((p-uCam.xy)/uCam.zw,0.,1.);}`;
const STRIP_FS = NOISE + `varying float vD,vR,vV,vZ,vK;uniform float uPx,uWet,uFlash,uHazeAmt;uniform vec3 uAmb,uLightCol,uHaze,uShoot;uniform vec2 uL;
void main(){float a=clamp((vR-abs(vD))/uPx+.5,0.,1.);if(a<.01)discard;float nx=clamp(vD/max(vR,1e-5),-1.,1.),nz=sqrt(1.-nx*nx);
  float rid=mix(fbm3(vec2(nx*5.5+vZ*9.,vV*11.)),.45,smoothstep(.012,.003,vR));float fis=smoothstep(.27,.58,rid);float young=smoothstep(.0065,.002,vR);
  vec3 bark=mix(mix(vec3(.16,.135,.105),vec3(.46,.41,.33),fis),vec3(.36,.31,.15),young*.85)*(1.-.3*uWet);vec3 alb=vK>.5?(vK>1.5?vec3(.13,.1,.075):uShoot):bark;
  float dif=max(0.,nx*uL.x+nz*uL.y);float rim=pow(1.-nz,2.)*max(0.,nx*uL.x)*.6;
  vec3 col=alb*(uAmb*(.55+.45*nz)+uLightCol*(dif*(vK>.5?1.:.5+.6*fis)+rim))+uFlash*vec3(.5,.55,.7)*(.3+.7*abs(nx));
  col=mix(col,uHaze,uHazeAmt*(.5-.5*vZ));gl_FragColor=vec4(col*a,a);}`;
const LEAF_VS = `attribute vec2 aQ;attribute vec2 iP;attribute float iA,iF,iG,iS,iSize,iShade,iZ;uniform vec4 uCam;uniform float uPx;varying vec2 vQ;varying float vH,vF,vG,vSh,vZ,vA;
void main(){float len=iSize*iS;float hw=len*.085;float pad=uPx*.8;vec2 l=vec2(aQ.x*len,aQ.y*(hw+pad));float c=cos(iA),s=sin(iA);vec2 p=iP+vec2(l.x*c-l.y*s,l.x*s+l.y*c);
  vQ=vec2(aQ.x,aQ.y*(hw+pad)/max(hw,1e-6));vH=hw/uPx;vF=iF;vG=iG;vSh=iShade;vZ=iZ;vA=iA;gl_Position=vec4((p-uCam.xy)/uCam.zw,0.,iS>.01?1.:0.);}`;
const LEAF_FS = `precision highp float;varying vec2 vQ;varying float vH,vF,vG,vSh,vZ,vA;uniform vec3 uAmb,uLightCol,uHaze,uBackCol;uniform float uBack,uWet,uFlash,uHazeAmt,uGold;
void main(){float u=vQ.x;float w=pow(u,.55)*pow(1.-u,1.05)*2.05;float a=clamp((w-abs(vQ.y))*vH+.5,0.,1.)*min(1.,.45+vH*.8);if(a<.01)discard;
  vec3 up=mix(vec3(.1,.215,.06),vec3(.2,.31,.07),vSh);vec3 lo=vec3(.44,.54,.42);vec3 alb=mix(up,lo,vF)*(.78+.44*fract(vSh*7.3));
  alb=mix(alb,vec3(.62,.5,.1),uGold*fract(vSh*3.7));alb+=.07*smoothstep(.3,0.,abs(vQ.y));alb*=1.-.22*uWet;
  float dif=.5+.5*cos(vA*2.+vSh*6.283);
  vec3 col=alb*(uAmb+uLightCol*(.35+.65*dif))+uBackCol*uBack*(1.-.55*vF)*(.4+.6*vSh)+vG*uLightCol*vec3(.5,.55,.5)*.7+uWet*uLightCol*.05+uFlash*vec3(.4,.45,.55);
  col=mix(col,uHaze,uHazeAmt*(.5-.5*vZ));gl_FragColor=vec4(col*a,a);}`;
const COMP_FS = NOISE + `
varying vec2 vW;varying vec2 vUv;uniform sampler2D uScene;uniform vec4 uCam;uniform float uT,uWind,uRain,uMist,uFlash,uFlow,uGlit;uniform vec3 uWater,uMistCol,uGlitCol;uniform vec4 uRing[8];uniform vec2 uGl;
vec2 uvOf(vec2 w){return (w-uCam.xy)/uCam.zw*.5+.5;}
float streaks(vec2 uv,float sc,float sp){vec2 p=vec2(uv.x*sc+uv.y*sc*.12*(.4+uWind),uv.y);float c=floor(p.x);float h=hash(vec2(c,sc));float y=fract(p.y*(1.3+h)+uT*sp*(.8+h*.5)+h*7.);return step(.45,hash(vec2(c,sc+2.)))*smoothstep(0.,.03,y)*smoothstep(.2,.03,y)*smoothstep(.16,0.,abs(fract(p.x)-.5));}
void main(){vec3 col;float d=-vW.y;
  if(d<=0.)col=texture2D(uScene,vUv).rgb;
  else{float ps=1./(d*3.2+.11);float px=vW.x*ps*1.15,py=ps*4.,t=uT;
    float r1=sin(px*9.+py*1.3+t*.9)+.6*sin(px*17.-py*2.1+t*1.4+1.7)+.4*sin(px*31.+py*5.-t*2.2);float r2=sin(py*6.-t*1.1+sin(px*3.+t*.3)*1.5);
    float n=noise(vec2(px*6.+t*.25,py*9.-t*.5))-.5;float amp=(.0022+.01*uWind+.006*uRain+.004*uFlow)*(.3+d*1.6);
    vec2 off=vec2(r1*.5+n*2.,(r1+r2*1.2+n*2.)*1.9)*amp;float hl=0.;
    for(int i=0;i<8;i++){vec4 R=uRing[i];float age=t-R.y;if(R.w>0.&&age>0.&&age<6.){vec2 q=vec2(vW.x-R.x,(d-R.z)*3.6);float rr=length(q);float fr=age*.07;float ev=exp(-age*.75)*R.w;float wv=sin((rr-fr)*170.)*exp(-pow((rr-fr)*16.,2.))*ev;off+=q/(rr+1e-4)*wv*.01;hl+=wv;}}
    float dimple=uRain*step(.93,noise(vec2(vW.x*90.+floor(t*9.)*7.,d*260.*ps*.2+floor(t*9.)*3.)));hl+=dimple*.6;
    vec2 rw=vec2(vW.x+off.x,max(d+off.y,.0015));vec3 refl=texture2D(uScene,uvOf(rw)).rgb;
    float fres=mix(.9,.52,smoothstep(0.,.5,d));col=mix(uWater,refl,fres)*(.93-.1*smoothstep(0.,.5,d));
    float gx=vW.x-uGl.x;float gp=exp(-gx*gx*(90.+400.*ps*.1))*uGlit*(.5+.5*sin(py*14.-t*1.6+r1*2.))*smoothstep(.0,.05,d);col+=uGlitCol*max(0.,gp)*(.4+.6*abs(r1)*.5);
    col+=hl*.05*(uMistCol+.15);col*=1.-.4*exp(-d*70.);}
  float md=(vW.y-.022)/(d>0.?.11:.07);float m=uMist*exp(-md*md)*(.5+.5*fbm3(vec2(vW.x*1.5-uT*.011,vW.y*8.+uT*.008)));col=mix(col,uMistCol,clamp(m,0.,.86));
  float rn=streaks(vUv,90.,1.9)+.6*streaks(vUv+.37,150.,1.4);col+=rn*uRain*.2*vec3(.72,.8,.9);
  col+=uFlash*vec3(.5,.56,.72)*.45;
  vec2 v=vUv-.5;col*=1.-.26*pow(length(v)*1.3,2.6);col=col*(1.04+.0*col);
  col+=(hash(gl_FragCoord.xy+fract(uT)*61.)-.5)/150.;gl_FragColor=vec4(col,1.);}`;

function prog(vs, fs) { const p = gl.createProgram(); for (const [t, s] of [[gl.VERTEX_SHADER, vs], [gl.FRAGMENT_SHADER, fs]]) { const sh = gl.createShader(t); gl.shaderSource(sh, s); gl.compileShader(sh); if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) console.error('shader: ' + gl.getShaderInfoLog(sh)); gl.attachShader(p, sh); } gl.linkProgram(p); if (!gl.getProgramParameter(p, gl.LINK_STATUS)) console.error('link: ' + gl.getProgramInfoLog(p)); const U = {}, n = gl.getProgramParameter(p, gl.ACTIVE_UNIFORMS); for (let i = 0; i < n; i++) { const u = gl.getActiveUniform(p, i), nm = u.name.replace('[0]', ''); U[nm] = gl.getUniformLocation(p, nm); } const A = {}, na = gl.getProgramParameter(p, gl.ACTIVE_ATTRIBUTES); for (let i = 0; i < na; i++) { const a = gl.getActiveAttrib(p, i); A[a.name] = gl.getAttribLocation(p, a.name); } return { p, U, A }; }
const pSky = prog(QUAD_VS, SKY_FS), pStrip = prog(STRIP_VS, STRIP_FS), pLeaf = prog(LEAF_VS, LEAF_FS), pComp = prog(QUAD_VS, COMP_FS);
const quad = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, quad); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);

/* ─── geometry: branches and shoots as ribbons, three depth layers; leaves as instanced quads ─── */
const layerOf = z => z < -.3 ? 0 : z > .3 ? 2 : 1, strips = [];
sim.Br.forEach((b, i) => strips.push({ kind: b.level === 4 ? 2 : 0, id: i, n: b.K + 1, layer: b.level === 0 || b.level === 4 ? 1 : layerOf(b.z), z: b.z }));
sim.W.forEach((w, i) => strips.push({ kind: 1, id: i, n: sim.N, layer: layerOf(w.z), z: w.z }));
strips.sort((a, b) => a.layer - b.layer || (a.kind === 1) - (b.kind === 1));
let nv = 0, ni = 0; for (const s of strips) { s.v0 = nv; nv += s.n * 2; ni += (s.n - 1) * 6; }
const SV = 8, sdata = new Float32Array(nv * SV), sidx = new Uint16Array(ni), layerIdx = [[0, 0], [0, 0], [0, 0]];
{ let k = 0; for (const s of strips) { const L = layerIdx[s.layer]; if (L[1] === 0) L[0] = k; for (let i = 0; i < s.n - 1; i++) { const a = s.v0 + i * 2; sidx[k++] = a; sidx[k++] = a + 1; sidx[k++] = a + 2; sidx[k++] = a + 1; sidx[k++] = a + 3; sidx[k++] = a + 2; } L[1] = k - L[0]; } }
const sbuf = gl.createBuffer(), ibuf = gl.createBuffer(); gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibuf); gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, sidx, gl.STATIC_DRAW);
function fillStrips() { let o = 0; const N = sim.N;
  for (const s of strips) { const kind = s.kind, isW = kind === 1; let pts, off = 0; if (isW) { off = s.id * N; } else pts = sim.P[s.id]; const g = isW ? sim.wgrow[s.id] : sim.grow[s.id]; let vacc = 0;
    for (let i = 0; i < s.n; i++) { let x, y, xa, ya, xb, yb; const ia = max(0, i - 1), ib = min(s.n - 1, i + 1);
      if (isW) { x = sim.px[off + i]; y = sim.py[off + i]; xa = sim.px[off + ia]; ya = sim.py[off + ia]; xb = sim.px[off + ib]; yb = sim.py[off + ib]; } else { x = pts[i * 2]; y = pts[i * 2 + 1]; xa = pts[ia * 2]; ya = pts[ia * 2 + 1]; xb = pts[ib * 2]; yb = pts[ib * 2 + 1]; }
      let tx = xb - xa, ty = yb - ya; const tl = sqrt(tx * tx + ty * ty) || 1; tx /= tl; ty /= tl; const r = g <= 0 ? 0 : isW ? WL.R_WITHY * lerp(1, .4, i / (s.n - 1)) * (.35 + .65 * g) : sim.radius(s.id, i); if (i > 0) vacc += tl * .5;
      for (let sd = -1; sd <= 1; sd += 2) { sdata[o++] = x; sdata[o++] = y; sdata[o++] = -ty * sd; sdata[o++] = tx * sd; sdata[o++] = g <= 0 ? -1 : r; sdata[o++] = sd * (1 + vacc); sdata[o++] = s.z; sdata[o++] = kind; } } }
  gl.bindBuffer(gl.ARRAY_BUFFER, sbuf); gl.bufferData(gl.ARRAY_BUFFER, sdata, gl.DYNAMIC_DRAW); }
const nl = sim.nl, lstat = new Float32Array(nl * 3), ldyn = new Float32Array(nl * 6), leafLayer = [[0, 0], [0, 0], [0, 0]];
sim.L.forEach((l, i) => { const z = sim.W[l.w].z; lstat[i * 3] = l.size; lstat[i * 3 + 1] = l.shade; lstat[i * 3 + 2] = z; const L = leafLayer[layerOf(z)]; if (L[1] === 0) L[0] = i; L[1] = i + 1 - L[0]; });
const lsbuf = gl.createBuffer(), ldbuf = gl.createBuffer(), lqbuf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, lsbuf); gl.bufferData(gl.ARRAY_BUFFER, lstat, gl.STATIC_DRAW); gl.bindBuffer(gl.ARRAY_BUFFER, lqbuf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([0, -1, 1, -1, 0, 1, 1, 1]), gl.STATIC_DRAW);
function fillLeaves() { const { lx, ly, la, lface, lglint, lscale, lstate } = sim; for (let i = 0, o = 0; i < nl; i++) { const on = lstate[i] !== 0; ldyn[o++] = lx[i]; ldyn[o++] = ly[i]; ldyn[o++] = la[i]; ldyn[o++] = lface[i]; ldyn[o++] = lglint[i]; ldyn[o++] = on ? (lstate[i] === 2 ? 1 : lscale[i]) : 0; } gl.bindBuffer(gl.ARRAY_BUFFER, ldbuf); gl.bufferData(gl.ARRAY_BUFFER, ldyn, gl.DYNAMIC_DRAW); }

/* ─── frame buffer for the scene above the water ─── */
let fbo = gl.createFramebuffer(), tex = gl.createTexture(), CW = 0, CH = 0, scale = 1, cam = [0, 0, 1, 1], pxW = 1, cssW = 1, cssH = 1, dpr = 1;
function fit() { const r = stage.getBoundingClientRect(); cssW = max(1, r.width); cssH = max(1, r.height); dpr = min(window.devicePixelRatio || 1, small ? 1.5 : 2) * scale; CW = max(2, Math.round(cssW * dpr)); CH = max(2, Math.round(cssH * dpr)); cv.width = CW; cv.height = CH; const od = min(window.devicePixelRatio || 1, 2); ov.width = Math.round(cssW * od); ov.height = Math.round(cssH * od);
  gl.bindTexture(gl.TEXTURE_2D, tex); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, CW, CH, 0, gl.RGB, gl.UNSIGNED_BYTE, null); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  gl.bindFramebuffer(gl.FRAMEBUFFER, fbo); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, tex, 0); gl.bindFramebuffer(gl.FRAMEBUFFER, null);
  const A = cssW / cssH, halfH = A < 1.1 ? .86 : .78, halfW = halfH * A, yc = A < 1.1 ? .36 : .3; cam = [A < 1.1 ? .03 : .2 * halfW, yc, halfW, halfH]; pxW = 2 * halfH / CH; dirty = true; }
let dirty = true; new ResizeObserver(fit).observe(stage);

/* ─── light: one table for the sky, the tree and the mist, from the beat ─── */
const PAL = { night: { zen: [.02, .034, .078], mid: [.036, .06, .12], hor: [.075, .11, .175] }, dawn: { zen: [.2, .25, .4], mid: [.6, .52, .56], hor: [.99, .74, .5] }, dusk: { zen: [.15, .17, .34], mid: [.56, .38, .46], hor: [.97, .58, .34] }, day: { zen: [.3, .5, .74], mid: [.56, .72, .85], hor: [.84, .89, .88] }, storm: { zen: [.13, .15, .18], mid: [.24, .26, .29], hor: [.36, .38, .4] } };
const mix3 = (a, b, t) => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)], add3 = (...v) => { const r = [0, 0, 0]; for (let i = 0; i < v.length; i += 2) { r[0] += v[i][0] * v[i + 1]; r[1] += v[i][1] * v[i + 1]; r[2] += v[i][2] * v[i + 1]; } return r; };
function envAt(beat, o) { o = o || {}; const s = o.sun !== undefined ? o.sun : WL.sunAt(beat), eve = o.eve !== undefined ? o.eve : sstep(205, 250, beat), r = o.rain !== undefined ? o.rain : WL.rainAt(beat), bow = o.sun !== undefined ? 0 : WL.rainbowAt(beat);
  const night = 1 - sstep(.03, .3, s), day = sstep(.3, .72, s), tw = max(0, 1 - night - day), T = { zen: mix3(PAL.dawn.zen, PAL.dusk.zen, eve), mid: mix3(PAL.dawn.mid, PAL.dusk.mid, eve), hor: mix3(PAL.dawn.hor, PAL.dusk.hor, eve) }, st = r * .88, E = {};
  for (const k of ['zen', 'mid', 'hor']) E[k] = mix3(add3(PAL.night[k], night, T[k], tw, PAL.day[k], day), PAL.storm[k], st);
  const warm = mix3([1, .74, .5], [1, .6, .36], eve), dim = 1 - .62 * r;
  E.light = add3([.22, .27, .38], night, warm, tw * .8, [1, .97, .9], day * .95).map(v => v * dim); E.amb = mix3(add3([.055, .075, .12], night, [.2, .19, .25], tw, [.4, .47, .55], day), [.2, .21, .23], r * .7);
  let lx = night * (eve > .5 ? .45 : -.4) + tw * lerp(.8, -.8, eve) + day * .3, lz = night * .8 + tw * .3 + day * .9; const ll = sqrt(lx * lx + lz * lz) || 1; E.L = [lx / ll, lz / ll];
  E.back = (tw * .5 + day * .1) * dim; E.backCol = mix3([.66, .7, .12], [.8, .6, .1], eve); E.gold = sstep(330, 372, beat) * .0;
  E.s = s; E.eve = eve; E.rain = r; E.bow = bow; E.night = night; E.day = day; E.tw = tw;
  E.mist = clamp(.2 * night + .82 * tw * (1 - .35 * eve) + .1 * day + .5 * sstep(262, 272, beat) * (1 - sstep(292, 312, beat)) + .2 * r, 0, .92); E.mistCol = mix3(add3(E.hor, .7, E.amb, .5, E.light, .12), [1, 1, 1], .06);
  E.stars = pow(night, 1.6) * (1 - r); E.cloud = clamp(.2 + .72 * sstep(.02, .6, r) + .1 * tw - .1 * night, 0, 1); E.cloudLit = add3(E.hor, .5, E.light, .45, [.1, .1, .12], 1); E.cloudDark = mix3(add3(E.zen, .6, E.amb, .5), [.08, .09, .11], st);
  const hw = cam[2], cx = cam[0]; E.glowX = cx + hw * lerp(.6, -.62, eve); E.glow = tw * 1.0 * dim; E.glowCol = mix3([.9, .5, .25], [.95, .38, .16], eve);
  E.sun = [cx + hw * .58 + s * .25, -.07 + s * 2.2, (1 - eve) * sstep(.035, .1, s) * (1 - sstep(.45, .58, s)) * (1 - r)]; E.moon = eve > .5 ? [cx + hw * .52, .66 + .18 * night, night * (1 - r)] : [cx - hw * .5, .98 - .12 * (1 - night), sstep(.2, .8, night)];
  E.land = add3([.07, .11, .08], 1).map((v, i) => v * (E.amb[i] * 1.5 + E.light[i] * .55)); E.grass = [.17, .235, .095].map((v, i) => v * (E.amb[i] * 1.25 + E.light[i] * .75));
  E.water = add3(E.zen, .22, [.012, .03, .028], 1, E.amb, .1); E.haze = add3(E.hor, .55, E.mid, .35); E.hazeAmt = .16 + .3 * E.mist + .2 * r;
  E.glit = (E.sun[2] * 1.2 + E.moon[2] * .5); E.glitX = E.sun[2] > E.moon[2] * .4 ? E.sun[0] : E.moon[0]; E.glitCol = E.sun[2] > E.moon[2] * .4 ? [1, .7, .4] : [.5, .56, .7];
  E.wet = clamp(r * 1.2 + .6 * sstep(248, 262, beat) * (1 - sstep(280, 320, beat)), 0, 1);
  return E; }

/* ─── state ─── */
let mode = 'poster', beat = 170, t = 0, last = 0, acc = 0, flash = 0, flow = 0, annotate = false, tlIdx = 0, onScreen = true, slow = 0, frames = 0, lastSec = null, costs = [], drawCalls = 0, manual = null;
const rings = [], drops = [], glints = [], marks = [], motes = [], bolts = []; let ringK = 0, creakK = 0;
const birds = { m: { at: 0, in: 0, open: 0, flick: 0 }, f: { at: 0, in: 0, open: 0, flick: 0 }, p: { at: 0, in: 0, open: 0, crest: 0 } }; let lyric = { line: -1, word: -1 }, seedPos = null;
const POSTER = { beat: 170, env: { sun: .27, eve: 0, rain: 0 }, wind: .2 };
function addRing(x, d, s) { rings[ringK++ % 8] = [x, t, d, s]; }
function resetTransient() { rings.length = 0; drops.length = 0; glints.length = 0; marks.length = 0; motes.length = 0; bolts.length = 0; flash = 0; flow = 0; for (const k in birds) { birds[k].in = 0; birds[k].open = 0; } lyric = { line: -1, word: -1 }; showLyric(); }
function seekVisual(b) { sim.seek(b); tlIdx = 0; while (tlIdx < TL.length && TL[tlIdx].b < b) tlIdx++; resetTransient(); if (b >= 302) { birds.m.in = birds.f.in = 1; } if (b >= 310) birds.p.in = 1; if (b > 329) for (let i = 0; i < 26; i++) spawnMote(true); lastSec = null; }

/* what the score does, shown: called once for each event as its moment arrives */
function onEvent(e) {
  switch (e.t) {
    case 'creak': { const bi = sim.creak(e.vel, creakK++), p = sim.P[bi]; marks.push({ x: p[4], y: p[5], t, kind: 'creak' }); break; }
    case 'cavit': { const lv = floor(rv() * 3), cand = []; sim.Br.forEach((b, i) => { if (b.level <= 1 && sim.grow[i] > .3) cand.push(i); }); if (!cand.length) break; const bi = cand[floor(rv() * cand.length)], b = sim.Br[bi], k = floor(rv() * b.K), p = sim.P[bi], f = rv(); glints.push({ x: lerp(p[k * 2], p[k * 2 + 2], f), y: lerp(p[k * 2 + 1], p[k * 2 + 3], f), t, v: e.vel }); break; }
    case 'drip': { for (let i = 0; i < e.cnt; i++) { let x, y, tries = 0; do { const w = floor(rv() * sim.nw), j = w * sim.N + sim.N - 1 - floor(rv() * 3); x = sim.px[j]; y = sim.py[j]; } while (y < .08 && ++tries < 6); drops.push({ x, y, vy: 0, t0: t + rv() * .4 + i * .08 }); } break; }
    case 'water': flow = max(flow, min(1, e.vel * 9)); break;
    case 'rupture': { flash = 1; const x0 = cam[0] + (rv() - .3) * cam[2] * .8, pts = [[x0, cam[1] + cam[3] + .05]]; let x = x0, y = pts[0][1]; const tx = .04, ty = .7; while (y > ty) { y -= .035 + rv() * .04; x += (tx - x) * .12 + (rv() - .5) * .07; pts.push([x, y]); } bolts.push({ pts, t, a: 1 }); break; }
    case 'robin': if (e.action === 'land') { birds.m.at = t; birds.f.at = t + .55; birds.m.in = birds.f.in = .001; } break;
    case 'parrot': if (e.action === 'land') { birds.p.at = t; birds.p.in = .001; } break;
    case 'robinNote': { const b = e.female ? birds.f : birds.m; b.open = max(b.open, e.dur + .06); if (e.phrase !== true || rv() < .2) b.flick = 1; break; }
    case 'syll': { birds.p.open = e.dur * BEAT * .8; birds.p.crest = 1; const L = WL.LYRIC_LINES; for (let li = 0; li < L.length; li++) for (let wi = 0; wi < L[li].length; wi++) if (L[li][wi].idx === e.idx) { lyric = { line: li, word: wi, until: t + e.dur * BEAT + 1.6 }; showLyric(); } break; }
  }
}
function showLyric() { const el = $('lyric'); if (lyric.line < 0) { el.style.opacity = 0; return; } el.innerHTML = WL.LYRIC_LINES[lyric.line].map((w, i) => '<span class="' + (i === lyric.word ? 'now' : i < lyric.word ? 'sung' : '') + '">' + w.text.replace('-', '') + (/-$/.test(w.text) ? '' : ' ') + '</span>').join(''); el.style.opacity = 1; }
function spawnMote(any) { const w = floor(rv() * sim.nw), j = w * sim.N + floor(rv() * sim.N); motes.push({ x: any ? cam[0] + (rv() * 2 - 1) * cam[2] : sim.px[j], y: any ? .1 + rv() * .8 : sim.py[j], vx: 0, vy: 0, ph: rv() * TAU, r: .7 + rv() * 1.1, life: any ? rv() * 14 : 14 }); }

/* ─── drawing ─── */
const X = x => (x - cam[0]) / cam[2] * .5 * ov.width + ov.width / 2, Y = y => ov.height / 2 - (y - cam[1]) / cam[3] * .5 * ov.height;
function u3(p, n, v) { gl.uniform3f(p.U[n], v[0], v[1], v[2]); }
function drawGL(E) {
  drawCalls = 0; const wl = CH * (.5 + .5 * (0 - cam[1]) / cam[3]) | 0;          /* pixel row of the waterline, from the bottom */
  gl.bindFramebuffer(gl.FRAMEBUFFER, fbo); gl.viewport(0, 0, CW, CH); gl.enable(gl.SCISSOR_TEST); gl.scissor(0, max(0, wl - 3), CW, CH); gl.disable(gl.BLEND);
  let p = pSky; gl.useProgram(p.p); gl.bindBuffer(gl.ARRAY_BUFFER, quad); gl.enableVertexAttribArray(p.A.aP); gl.vertexAttribPointer(p.A.aP, 2, gl.FLOAT, false, 0, 0);
  gl.uniform4f(p.U.uCam, cam[0], cam[1], cam[2], cam[3]); gl.uniform1f(p.U.uT, t); gl.uniform1f(p.U.uStars, E.stars); gl.uniform1f(p.U.uCloud, E.cloud); gl.uniform1f(p.U.uFlash, flash); gl.uniform1f(p.U.uWind, sim.U); gl.uniform1f(p.U.uWet, E.wet);
  u3(p, 'uZen', E.zen); u3(p, 'uMid', E.mid); u3(p, 'uHor', E.hor); u3(p, 'uGlowCol', E.glowCol); u3(p, 'uSun', E.sun); u3(p, 'uMoon', E.moon); u3(p, 'uCloudLit', E.cloudLit); u3(p, 'uCloudDark', E.cloudDark); u3(p, 'uLand', E.land); u3(p, 'uGrass', E.grass);
  gl.uniform4f(p.U.uGlow, E.glowX, E.glow, 0, 0); gl.uniform4f(p.U.uBow, cam[0] - cam[2] * .12, -.42, 1.12, E.bow);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); drawCalls++;
  gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
  const S = pStrip, Lf = pLeaf;
  gl.useProgram(S.p); gl.uniform4f(S.U.uCam, cam[0], cam[1], cam[2], cam[3]); gl.uniform1f(S.U.uPx, pxW); gl.uniform1f(S.U.uWet, E.wet); gl.uniform1f(S.U.uFlash, flash); gl.uniform1f(S.U.uHazeAmt, E.hazeAmt); u3(S, 'uAmb', E.amb); u3(S, 'uLightCol', E.light); u3(S, 'uHaze', E.haze); gl.uniform3f(S.U.uShoot, .5, .43, .15); gl.uniform2f(S.U.uL, E.L[0], E.L[1]);
  gl.useProgram(Lf.p); gl.uniform4f(Lf.U.uCam, cam[0], cam[1], cam[2], cam[3]); gl.uniform1f(Lf.U.uPx, pxW); gl.uniform1f(Lf.U.uWet, E.wet); gl.uniform1f(Lf.U.uFlash, flash); gl.uniform1f(Lf.U.uHazeAmt, E.hazeAmt); gl.uniform1f(Lf.U.uBack, E.back); gl.uniform1f(Lf.U.uGold, E.gold); u3(Lf, 'uAmb', E.amb); u3(Lf, 'uLightCol', E.light); u3(Lf, 'uHaze', E.haze); u3(Lf, 'uBackCol', E.backCol);
  const F = 4;
  for (let L = 0; L < 3; L++) {
    if (layerIdx[L][1]) { gl.useProgram(S.p); gl.bindBuffer(gl.ARRAY_BUFFER, sbuf); gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibuf); const st = SV * F; for (const [a, n, off] of [['aC', 2, 0], ['aN', 2, 2], ['aR', 1, 4], ['aV', 1, 5], ['aZ', 1, 6], ['aK', 1, 7]]) { gl.enableVertexAttribArray(S.A[a]); gl.vertexAttribPointer(S.A[a], n, gl.FLOAT, false, st, off * F); inst.vertexAttribDivisorANGLE(S.A[a], 0); } gl.drawElements(gl.TRIANGLES, layerIdx[L][1], gl.UNSIGNED_SHORT, layerIdx[L][0] * 2); drawCalls++; }
    if (leafLayer[L][1]) { gl.useProgram(Lf.p); const b0 = leafLayer[L][0]; gl.bindBuffer(gl.ARRAY_BUFFER, lqbuf); gl.enableVertexAttribArray(Lf.A.aQ); gl.vertexAttribPointer(Lf.A.aQ, 2, gl.FLOAT, false, 0, 0); inst.vertexAttribDivisorANGLE(Lf.A.aQ, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, ldbuf); for (const [a, n, off] of [['iP', 2, 0], ['iA', 1, 2], ['iF', 1, 3], ['iG', 1, 4], ['iS', 1, 5]]) { gl.enableVertexAttribArray(Lf.A[a]); gl.vertexAttribPointer(Lf.A[a], n, gl.FLOAT, false, 6 * F, (b0 * 6 + off) * F); inst.vertexAttribDivisorANGLE(Lf.A[a], 1); }
      gl.bindBuffer(gl.ARRAY_BUFFER, lsbuf); for (const [a, off] of [['iSize', 0], ['iShade', 1], ['iZ', 2]]) { gl.enableVertexAttribArray(Lf.A[a]); gl.vertexAttribPointer(Lf.A[a], 1, gl.FLOAT, false, 3 * F, (b0 * 3 + off) * F); inst.vertexAttribDivisorANGLE(Lf.A[a], 1); }
      inst.drawArraysInstancedANGLE(gl.TRIANGLE_STRIP, 0, 4, leafLayer[L][1]); drawCalls++; for (const a in Lf.A) inst.vertexAttribDivisorANGLE(Lf.A[a], 0); }
  }
  gl.disable(gl.BLEND); gl.disable(gl.SCISSOR_TEST); gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.viewport(0, 0, CW, CH);
  p = pComp; gl.useProgram(p.p); gl.bindBuffer(gl.ARRAY_BUFFER, quad); gl.enableVertexAttribArray(p.A.aP); gl.vertexAttribPointer(p.A.aP, 2, gl.FLOAT, false, 0, 0); gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, tex); gl.uniform1i(p.U.uScene, 0);
  gl.uniform4f(p.U.uCam, cam[0], cam[1], cam[2], cam[3]); gl.uniform1f(p.U.uT, t); gl.uniform1f(p.U.uWind, min(1.5, sim.U)); gl.uniform1f(p.U.uRain, E.rain); gl.uniform1f(p.U.uMist, E.mist); gl.uniform1f(p.U.uFlash, flash); gl.uniform1f(p.U.uFlow, flow); gl.uniform1f(p.U.uGlit, E.glit); u3(p, 'uWater', E.water); u3(p, 'uMistCol', E.mistCol); u3(p, 'uGlitCol', E.glitCol); gl.uniform2f(p.U.uGl, E.glitX, 0);
  const R = new Float32Array(32); for (let i = 0; i < 8; i++) { const r = rings[i]; if (r) { R[i * 4] = r[0]; R[i * 4 + 1] = r[1]; R[i * 4 + 2] = r[2]; R[i * 4 + 3] = r[3]; } } gl.uniform4fv(p.U.uRing, R);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); drawCalls++;
}
function robin(x, y, s, dir, fem, b, a, flying) { const c = BC; c.save(); c.translate(x, y); c.scale(dir * s, s); c.globalAlpha = a; c.rotate(b.open > 0 ? -.16 : -.05);
  c.fillStyle = fem ? '#6b5c44' : '#5a4a33'; c.save(); c.translate(-5, -.5); c.rotate(-.3 + b.flick * .5); c.beginPath(); c.moveTo(0, 0); c.lineTo(-7.5, -1); c.lineTo(-8.2, .6); c.lineTo(-7, 2); c.lineTo(0, 1.6); c.fill(); c.restore();
  if (flying) { const wa = sin(t * 26) * .7; c.fillStyle = '#5e4f3a'; c.save(); c.rotate(wa); c.beginPath(); c.ellipse(-1, -3, 8, 3, -.3, 0, TAU); c.fill(); c.restore(); }
  c.fillStyle = fem ? '#76664c' : '#66553b'; c.beginPath(); c.ellipse(0, 0, 6.2, 4.7, 0, 0, TAU); c.fill();
  c.fillStyle = '#d8d2c2'; c.beginPath(); c.ellipse(.6, 2.3, 4.2, 2.3, .1, 0, TAU); c.fill();
  c.fillStyle = fem ? '#c9823f' : '#dd6a26'; c.beginPath(); c.ellipse(2.4, .2, 3.6, 3.5, .2, 0, TAU); c.fill();
  const hy = -3.2 + (b.open > 0 ? sin(t * 30) * .35 : 0); c.fillStyle = fem ? '#70604a' : '#5f4e36'; c.beginPath(); c.arc(4.6, hy, 3.3, 0, TAU); c.fill(); c.fillStyle = fem ? '#c9823f' : '#dd6a26'; c.beginPath(); c.arc(5.5, hy + .8, 2.2, 0, TAU); c.fill();
  c.fillStyle = '#12100c'; c.beginPath(); c.arc(5.9, hy - .7, .8, 0, TAU); c.fill(); c.fillStyle = 'rgba(255,255,250,.8)'; c.beginPath(); c.arc(6.15, hy - .95, .26, 0, TAU); c.fill();
  const op = b.open > 0 ? .5 + .3 * sin(t * 40) : 0; c.fillStyle = '#2e2412'; c.beginPath(); c.moveTo(7.4, hy - .2 - op); c.lineTo(10.6, hy - .1 - op * 1.6); c.lineTo(7.4, hy + .5); c.fill(); c.beginPath(); c.moveTo(7.4, hy + .3 + op * .5); c.lineTo(10, hy + .7 + op); c.lineTo(7.4, hy + .9); c.fill();
  if (!flying) { c.strokeStyle = '#3d2d18'; c.lineWidth = .6; c.beginPath(); c.moveTo(-1, 4.4); c.lineTo(-1, 7); c.moveTo(1.2, 4.4); c.lineTo(1.2, 7); c.stroke(); } c.restore(); }
function parrot(x, y, s, dir, b, a, flying) { const c = BC; c.save(); c.translate(x, y); c.scale(dir * s, s); c.globalAlpha = a; c.rotate(b.open > 0 ? -.12 + sin(t * 3) * .04 : -.04);
  c.save(); c.translate(-6.5, 1.5); c.rotate(.42 + sin(t * 1.5) * .03); c.fillStyle = '#1f7d36'; c.beginPath(); c.moveTo(0, -2); c.lineTo(-15, -1.6); c.lineTo(-17, .4); c.lineTo(-15, 2.4); c.lineTo(0, 2.4); c.fill(); c.fillStyle = '#2a55b8'; c.beginPath(); c.moveTo(-11, -1.7); c.lineTo(-15, -1.6); c.lineTo(-17, .4); c.lineTo(-15, 2.4); c.lineTo(-11, 2.4); c.fill(); c.restore();
  if (flying) { c.save(); c.translate(-1, -2); c.rotate(sin(t * 19) * .8); c.fillStyle = '#1c7a33'; c.beginPath(); c.ellipse(0, -5, 12, 4.6, -.2, 0, TAU); c.fill(); c.restore(); }
  const g = c.createLinearGradient(-9, -8, 9, 8); g.addColorStop(0, '#2c9a40'); g.addColorStop(.5, '#3fb24c'); g.addColorStop(1, '#23863a'); c.fillStyle = g; c.beginPath(); c.ellipse(0, 0, 9.6, 6.9, -.35, 0, TAU); c.fill();
  c.fillStyle = 'rgba(160,205,70,.5)'; c.beginPath(); c.ellipse(2, 2.2, 5.6, 3.6, -.3, 0, TAU); c.fill(); c.strokeStyle = 'rgba(20,70,30,.45)'; c.lineWidth = .6; c.beginPath(); c.moveTo(-6, -1); c.quadraticCurveTo(-1, 3, 4, .5); c.stroke();
  const hx = 7, hy = -6.4 + (b.open > 0 ? sin(t * 9) * .5 : 0); c.fillStyle = '#35a747'; c.beginPath(); c.arc(hx, hy, 5, 0, TAU); c.fill(); c.fillStyle = '#cf3323'; c.beginPath(); c.arc(hx + .6, hy - 1.7, 3.3, PI * 1.05, TAU * .93); c.fill();
  c.beginPath(); c.moveTo(hx - 1, hy - 4.2); c.lineTo(hx + 1, hy - 4.6 - b.crest * 3.4); c.lineTo(hx + 3, hy - 3.4); c.fill();
  c.fillStyle = '#ecd84a'; c.beginPath(); c.arc(hx + 2.2, hy - .3, 1.7, 0, TAU); c.fill(); c.fillStyle = '#0c0a06'; c.beginPath(); c.arc(hx + 2.2, hy - .3, 1, 0, TAU); c.fill(); c.fillStyle = 'rgba(255,255,250,.8)'; c.beginPath(); c.arc(hx + 2.5, hy - .65, .3, 0, TAU); c.fill();
  const bo = b.open > 0 ? 1.1 + .5 * sin(t * 17) : 0, bx = hx + 3.9, by = hy + 1; c.fillStyle = '#1a1510'; c.beginPath(); c.moveTo(bx, by - 1.6 - bo * .3); c.quadraticCurveTo(bx + 5.4, by - 2.2 - bo * .3, bx + 3.9, by + 1.3 - bo * .2); c.lineTo(bx, by + .4); c.fill(); c.fillStyle = '#2a2219'; c.beginPath(); c.moveTo(bx, by + .5 + bo * .4); c.quadraticCurveTo(bx + 3.6, by + 2.9 + bo, bx + 2.4, by + .9 + bo * .5); c.lineTo(bx, by + .5); c.fill();
  if (!flying) { c.strokeStyle = '#3a342a'; c.lineWidth = .9; c.beginPath(); c.moveTo(-1.5, 6.6); c.lineTo(-1.5, 9.4); c.moveTo(1.6, 6.6); c.lineTo(1.6, 9.4); c.stroke(); } c.restore(); }
const bcv = document.createElement('canvas'), BC = bcv.getContext('2d');
function bird(which, from, lum, dt, u) { const b = birds[which], isP = which === 'p'; if (b.in <= 0 || t < b.at) return; if (b.in < 1) b.in = min(1, b.in + dt * (isP ? .3 : .35)); b.open = max(0, b.open - dt); if (b.flick !== undefined) b.flick *= exp(-dt * 6); if (b.crest !== undefined) b.crest *= exp(-dt * 2.2);
  const pp = sim.perch(isP ? 'parrot' : which === 'm' ? 'male' : 'female'), e = b.in < .5 ? 2 * b.in * b.in : 1 - pow(-2 * b.in + 2, 2) / 2, fly = e < .93, sx = from[0], sy = from[1], ax = (sx + pp[0]) / 2, ay = max(sy, pp[1]) + .2;
  const x = fly ? (1 - e) * (1 - e) * sx + 2 * (1 - e) * e * ax + e * e * pp[0] : pp[0], y = fly ? (1 - e) * (1 - e) * sy + 2 * (1 - e) * e * ay + e * e * pp[1] : pp[1], s = u * (isP ? .0034 : .0029), dir = isP ? (pp[0] > 0 ? -1 : 1) : which === 'f' ? -1 : 1, a = min(1, b.in * 4);
  /* drawn on a small canvas of its own so that it can be darkened with the light, and mirrored in the water */
  const S = Math.ceil(s * 64); if (bcv.width !== S) { bcv.width = bcv.height = S; } BC.setTransform(1, 0, 0, 1, 0, 0); BC.globalCompositeOperation = 'source-over'; BC.globalAlpha = 1; BC.clearRect(0, 0, S, S);
  if (isP) parrot(S / 2, S / 2, s, dir, b, 1, fly); else robin(S / 2, S / 2, s, dir, which === 'f', b, 1, fly);
  BC.setTransform(1, 0, 0, 1, 0, 0); BC.globalCompositeOperation = 'source-atop'; BC.globalAlpha = 1; BC.fillStyle = `rgba(10,14,26,${(1 - lum).toFixed(3)})`; BC.fillRect(0, 0, S, S);
  const foot = (isP ? 9.4 : 7) * s, px = X(x) - S / 2, py = Y(y) - foot - S / 2; o2.globalAlpha = a; o2.drawImage(bcv, px, py);
  if (y < .75) { const wy = Y(0); o2.save(); o2.globalAlpha = a * .3; o2.translate(0, 2 * wy); o2.scale(1, -1); o2.drawImage(bcv, px + sin(t * 1.3 + y * 20) * 1.5, py); o2.restore(); } o2.globalAlpha = 1; }
function drawOverlay(E, dt) {
  const c = o2, w = ov.width, h = ov.height, u = h / cam[3] / 2; c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, w, h); const wy = Y(0), lum = clamp(.06 + E.amb[1] * 1.15 + E.light[1] * .55, .15, 1);
  /* the seed, on its tuft of down */
  if (mode !== 'poster' && beat < 30) { const k = clamp(beat / 8, 0, 1), e = 1 - pow(1 - k, 2.2), x = lerp(cam[0] + cam[2] * .5, 0, e) + sin(beat * 1.3) * .03 * (1 - k), y = lerp(cam[1] + cam[3] * .95, BANK + .004, e) + sin(beat * 2.1) * .012 * (1 - k), a = 1 - sstep(14, 28, beat); c.save(); c.translate(X(x), Y(y)); c.rotate(sin(beat * .9) * .5 * (1 - k)); c.globalAlpha = a * .9; c.strokeStyle = 'rgba(232,236,240,.55)'; c.lineWidth = max(.5, u * .0007); for (let i = 0; i < 13; i++) { const an = -PI / 2 + (i - 6) * .2; c.beginPath(); c.moveTo(0, 0); c.lineTo(cos(an) * u * .017, sin(an) * u * .017); c.stroke(); } c.fillStyle = '#cdbf9c'; c.beginPath(); c.ellipse(0, u * .002, u * .0016, u * .0034, 0, 0, TAU); c.fill(); c.restore(); }
  /* lightning */
  for (let i = bolts.length - 1; i >= 0; i--) { const b = bolts[i], age = t - b.t; if (age > .55) { bolts.splice(i, 1); continue; } const a = (age < .08 ? 1 : exp(-(age - .08) * 9)) * (.75 + .25 * sin(age * 90)) * (b.a || 1); c.save(); c.lineJoin = 'round'; c.lineCap = 'round'; c.globalCompositeOperation = 'lighter'; for (const [lw, col] of [[u * .02, `rgba(150,170,255,${.16 * a})`], [u * .007, `rgba(190,205,255,${.4 * a})`], [max(1.2, u * .0022), `rgba(245,247,255,${a})`]]) { c.strokeStyle = col; c.lineWidth = lw; c.beginPath(); b.pts.forEach((p, k) => k ? c.lineTo(X(p[0]), Y(p[1])) : c.moveTo(X(p[0]), Y(p[1]))); c.stroke(); } c.restore(); }
  /* drops from the leaf tips; each one that reaches the water leaves a ring */
  c.fillStyle = `rgba(${200 * lum + 40 | 0},${215 * lum + 30 | 0},${230 * lum + 25 | 0},.8)`; for (let i = drops.length - 1; i >= 0; i--) { const d = drops[i]; if (t < d.t0) continue; d.vy += .98 * dt; d.y -= d.vy * dt; if (d.y <= .004) { addRing(d.x, .03 + rv() * .2, .9); drops.splice(i, 1); continue; } c.beginPath(); c.ellipse(X(d.x), Y(d.y), max(.8, u * .0016), max(1.2, u * .0016 + d.vy * u * .006), 0, 0, TAU); c.fill(); }
  /* cavitation: a point of light in the wood */
  for (let i = glints.length - 1; i >= 0; i--) { const g = glints[i], age = t - g.t; if (age > .5) { glints.splice(i, 1); continue; } const a = exp(-age * 9), r = u * (.004 + .012 * age); c.save(); c.globalCompositeOperation = 'lighter'; const gr = c.createRadialGradient(X(g.x), Y(g.y), 0, X(g.x), Y(g.y), r * 3); gr.addColorStop(0, `rgba(215,235,255,${.95 * a})`); gr.addColorStop(.3, `rgba(150,200,255,${.35 * a})`); gr.addColorStop(1, 'rgba(120,170,255,0)'); c.fillStyle = gr; c.beginPath(); c.arc(X(g.x), Y(g.y), r * 3, 0, TAU); c.fill(); c.restore();
    if (annotate) { c.strokeStyle = `rgba(224,174,53,${a})`; c.lineWidth = 1; c.beginPath(); c.arc(X(g.x), Y(g.y), u * (.01 + .05 * age), 0, TAU); c.stroke(); } }
  if (annotate) for (let i = marks.length - 1; i >= 0; i--) { const m = marks[i], age = t - m.t; if (age > 1.6) { marks.splice(i, 1); continue; } c.strokeStyle = `rgba(224,174,53,${.8 * (1 - age / 1.6)})`; c.lineWidth = 1; for (let k = 0; k < 2; k++) { c.beginPath(); c.arc(X(m.x), Y(m.y), u * (.02 + .012 * k + .01 * age), -.6, .6); c.stroke(); c.beginPath(); c.arc(X(m.x), Y(m.y), u * (.02 + .012 * k + .01 * age), PI - .6, PI + .6); c.stroke(); } } else marks.length = 0;
  /* seed down on the evening air */
  if (mode !== 'poster' && beat > 326 && beat < 372 && motes.length < 34 && rv() < dt * 2.2 * (beat < 352 ? 1 : .2)) spawnMote(false);
  for (let i = motes.length - 1; i >= 0; i--) { const m = motes[i]; m.life -= dt; if (m.life <= 0 || abs(m.x - cam[0]) > cam[2] + .1) { motes.splice(i, 1); continue; } const wv = sim.windAt(m.x, m.y, sim.t, sim.U + .12); m.vx += (wv * .35 - m.vx) * dt * 1.5; m.vy += (.012 * sin(t * .7 + m.ph) + .006 - m.vy) * dt; m.x += m.vx * dt; m.y += m.vy * dt; if (m.y < .01) m.y = .01; const a = min(1, m.life / 3) * min(1, (14 - m.life) * 2 + .2) * (.35 + .45 * E.tw + .2 * E.day); c.fillStyle = `rgba(255,${228 + 20 * E.night | 0},${190 + 50 * E.night | 0},${a * .55})`; c.beginPath(); c.arc(X(m.x), Y(m.y), m.r * u * .0016 + .4, 0, TAU); c.fill(); if (m.y < .5) { c.globalAlpha = .25; c.beginPath(); c.arc(X(m.x), Y(-m.y), m.r * u * .0016 + .4, 0, TAU); c.fill(); c.globalAlpha = 1; } }
  /* birds, dimmed with the light, and their reflections */
  { const top = cam[1] + cam[3], bl = lum; bird('m', [cam[0] - cam[2] - .1, top - .35], bl, dt, u); bird('f', [cam[0] + cam[2] + .1, top - .45], bl, dt, u); bird('p', [cam[0] + cam[2] * .5, top + .12], bl, dt, u); }
}

/* ─── page furniture ─── */
const total = END_BEATS * BEAT, fmt = s => floor(s / 60) + ':' + String(floor(s % 60)).padStart(2, '0');
const names = $('names'); SECTIONS.forEach((s, i) => { const li = document.createElement('li'); li.style.flex = (s.end - s.start + 1) + ' 0 0'; const b = document.createElement('button'); b.type = 'button'; b.textContent = ({ 'Canopy unfolds': 'Canopy', 'The wind arrives': 'Wind' })[s.name] || s.name; b.title = 'Play from ' + s.name; b.onclick = () => start(s.start); li.appendChild(b); names.appendChild(li); });
const NOTES = {
  'Seed': 'A willow seed is very small and travels on a tuft of down. It lives only a few days unless it lands on wet ground.',
  'Root': 'Willows root easily, even from a cut stem, and the roots grow towards water.',
  'Sapwood': 'Water is pulled up through the wood under tension. When a thread of it breaks, the vessel fills with vapour and the break makes a click (Milburn and Johnson, 1966). In this piece the clicks are placed by the score; each one shows as a point of light in the wood.',
  'Canopy unfolds': 'Where a branch divides, the cross-sections of the parts add up to that of the whole (Leonardo’s rule). The radii of this tree are set that way. Its leaves are narrow and pointed, dark above and pale beneath.',
  'The wind arrives': 'A hanging shoot swings like a pendulum: the longer it is, the slower it swings. The push of the wind grows with the square of its speed.',
  'Leaf song': '',
  'Storm': 'Leaves and shoots stream with the wind and so present less of themselves to it (Vogel, 1989). Thick limbs cannot do that. They bend a little, and creak.',
  'Delta': 'Lightning. In this piece the tree loses the last of its leaves at the strike.',
  'After rain': 'Drops gather at the tips of the leaves and fall. A drop that carries air under the water rings at a pitch set by the size of the bubble (Minnaert, 1933).',
  'Reflection': 'Water reflects more at a glancing angle, so the far water is the better mirror. Two robins arrive, then a parrot.',
  'Catkin': 'Willows flower in catkins. The seed is shed on white down and drifts.',
  'Stillness': 'One leaf.' };
function note() { const el = $('note'); if (!annotate) { el.hidden = true; return; } el.hidden = false; const s = mode === 'poster' ? null : WL.gS(floor(beat)); let txt = s ? NOTES[s.name] : 'Annotations will appear here as the piece plays.';
  if (s && s.name === 'Leaf song' || (s && (s.name === 'The wind arrives' || s.name === 'Storm') && annotate)) { const c = sim.cv(), base = s.name === 'Leaf song' ? 'Each leaf keeps a count of the wind’s push on it and turns over when the count reaches a fixed amount. This tree has ' + sim.nl.toLocaleString('en-GB') + ' leaves. ' : NOTES[s.name] + ' '; txt = base + (c ? 'Spread of the time between turns (standard deviation over mean), measured over the last ' + c.n + ' turns: ' + c.cv.toFixed(2) + '. Candidate value under test: 0.16.' : 'Too few leaf turns yet to measure their spread.'); }
  if (el.textContent !== txt) el.textContent = txt; }
function ui() { const b = clamp(mode === 'poster' ? 0 : beat, 0, END_BEATS), s = WL.gS(floor(b)); $('fill').style.width = (b / END_BEATS * 100).toFixed(2) + '%'; $('clock').textContent = fmt(b * BEAT) + ' / ' + fmt(total); $('prog').setAttribute('aria-valuenow', Math.round(b / END_BEATS * 100));
  if (mode !== 'poster' && s !== lastSec) { lastSec = s; [...names.children].forEach((li, i) => li.classList.toggle('on', SECTIONS[i] === s)); const mv = $('mv'); mv.textContent = s.label; mv.classList.add('show'); clearTimeout(ui.t); ui.t = setTimeout(() => mv.classList.remove('show'), 4200); $('now').textContent = s.name; }
  if (lyric.line >= 0 && t > lyric.until) { lyric.line = -1; showLyric(); } }
function setPlayLabel() { const p = $('play'); p.textContent = mode === 'playing' ? 'Pause' : mode === 'paused' ? 'Resume' : mode === 'ended' ? 'Play again' : 'Play'; p.setAttribute('aria-pressed', mode === 'playing' ? 'true' : 'false'); stage.classList.toggle('idle', mode === 'poster'); }
function start(from) { from = from || 0; stage.classList.add('dip'); const ok = player.start(from); manual = ok ? null : { b: from, on: true }; setTimeout(() => { mode = 'playing'; beat = from; seekVisual(from); setPlayLabel(); stage.classList.remove('dip'); }, 380); mode = 'starting'; setPlayLabel(); $('play').textContent = 'Pause'; }
function toggle() { if (mode === 'poster' || mode === 'ended') start(0); else if (mode === 'playing') { player.pause(); if (manual) manual.on = false; mode = 'paused'; setPlayLabel(); } else if (mode === 'paused') { player.resume(); if (manual) manual.on = true; mode = 'playing'; setPlayLabel(); } }
$('play').onclick = toggle; cv.onclick = toggle; $('again').onclick = () => start(0);
$('ann').onclick = () => { annotate = !annotate; $('ann').setAttribute('aria-pressed', annotate ? 'true' : 'false'); note(); };
$('mixb').onclick = () => { const m = $('mixer'); m.hidden = !m.hidden; $('mixb').setAttribute('aria-expanded', m.hidden ? 'false' : 'true'); };
for (const k of ['reverb', 'wind', 'leaf', 'wood', 'water']) { const el = $('m-' + k); el.value = WL.DEFAULT_MIX[k]; el.oninput = () => player.setMix(k, +el.value); }
const sheet = $('sheet'); $('about').onclick = () => { sheet.hidden = false; $('close').focus(); }; $('close').onclick = () => { sheet.hidden = true; $('about').focus(); }; sheet.onclick = e => { if (e.target === sheet) $('close').click(); }; addEventListener('keydown', e => { if (e.key === 'Escape' && !sheet.hidden) $('close').click(); });
new IntersectionObserver(es => { onScreen = es[0].isIntersecting; }).observe(stage);

/* ─── the loop ─── */
function frame(now) {
  requestAnimationFrame(frame); let dt = min(.1, (now - last) / 1000); last = now; if (document.hidden || !onScreen || CW < 4) return;
  if (still) { frame.k = (frame.k || 0) + dt; if (frame.k < .5 && !dirty) return; dt = 0; frame.k = 0; }
  const c0 = performance.now(); t += dt;
  if (mode === 'playing' || mode === 'paused') { if (manual) { if (manual.on) manual.b += dt / BEAT; beat = manual.b; } else { const b = player.beat(); if (b !== null) beat = max(0, b); } if (beat >= END_BEATS + 3 && mode === 'playing') { mode = 'ended'; player.stop(); setPlayLabel(); } }
  const P = mode === 'poster' || mode === 'starting', b = P ? POSTER.beat : min(beat, END_BEATS + 3), E = envAt(b, P ? POSTER.env : null);
  if (mode === 'playing') { while (tlIdx < TL.length && TL[tlIdx].b <= beat) onEvent(TL[tlIdx++]); }
  if (!still && mode !== 'paused') { acc += dt; let n = 0; while (acc >= 1 / 60 && n < 3) { sim.step(1 / 60, b, P ? POSTER.wind : undefined); acc -= 1 / 60; n++; } if (acc > .1) acc = 0; }
  else if (still && frame.sb !== floor(b / 4)) { frame.sb = floor(b / 4); sim.seek(b); }
  for (const l of sim.landed) addRing(l[0], .02 + rv() * .12, l[2] ? 1.6 : .5); sim.landed.length = 0;
  flash *= exp(-dt * 7); flow *= exp(-dt * .5);
  if (mode === 'playing' && beat > 229 && beat < 247 && !still) { const k = floor((beat - 229) / 4.6); if (frame.sheet !== k) { frame.sheet = k; if (k > 0) flash = max(flash, .3 + .1 * k); } }
  fillStrips(); fillLeaves(); drawGL(E); drawOverlay(E, mode === 'paused' ? 0 : dt); ui(); if ((frames & 31) === 0) note(); dirty = false;
  const cost = performance.now() - c0; costs[frames % 300] = cost; frames++;
  /* if frames are slow, draw fewer pixels */
  if (dt > .034) slow++; else slow = max(0, slow - 1); if (slow > 90 && scale > .6) { scale *= .8; slow = 0; fit(); }
}
fit(); seekVisual(POSTER.beat); setPlayLabel(); ui(); requestAnimationFrame(tm => { last = tm; frame(tm); });
window.WILLOW_PAGE = { sim, player, get beat() { return beat; }, get mode() { return mode; }, get drawCalls() { return drawCalls; }, costs, envAt, start, quality,
  /* for tests: show a given beat without sound */
  show(b, settle) { player.stop(true); mode = 'paused'; manual = { b, on: false }; beat = b; seekVisual(b); for (let i = 0; i < (settle || 0); i++) { sim.step(1 / 60, b); t += 1 / 60; } mode = 'paused'; setPlayLabel(); lastSec = null; dirty = true; },
  run(b) { player.stop(true); manual = { b, on: true }; beat = b; seekVisual(b); mode = 'playing'; setPlayLabel(); }, fire: onEvent, setAnnotate(v) { annotate = v; note(); } };
})();
