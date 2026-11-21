/* The sky, the birds, the reeds, the sound and the controls. The flock itself is in the model above. */
(function () {
'use strict';
const M = window.MURMUR, $ = id => document.getElementById(id);
const canvas = $('sky');
const gl = canvas.getContext('webgl2', { antialias: true, alpha: false, powerPreference: 'high-performance' });
if (!gl) { canvas.style.display = 'none'; $('fail').style.display = 'block'; return; }
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
const small = Math.min(innerWidth, innerHeight) < 620 || (matchMedia('(pointer: coarse)').matches && innerWidth < 900);
const NMAX = small ? 1500 : ((navigator.hardwareConcurrency || 4) >= 8 ? 7000 : 5000);
const S = M.makeFlock(NMAX, { seed: 7 + (Date.now() % 97) });
const SPAN = 0.78;                                             /* drawn wingspan in metres: about twice life */

/* ─── shaders ─── */
function prog(vs, fs) { const p = gl.createProgram(); for (const [t, src] of [[gl.VERTEX_SHADER, vs], [gl.FRAGMENT_SHADER, fs]]) { const s = gl.createShader(t); gl.shaderSource(s, '#version 300 es\nprecision highp float;\n' + src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) console.error(gl.getShaderInfoLog(s)); gl.attachShader(p, s); }
  gl.linkProgram(p); if (!gl.getProgramParameter(p, gl.LINK_STATUS)) console.error(gl.getProgramInfoLog(p)); const u = {}; const n = gl.getProgramParameter(p, gl.ACTIVE_UNIFORMS); for (let i = 0; i < n; i++) { const a = gl.getActiveUniform(p, i); u[a.name] = gl.getUniformLocation(p, a.name); } return { p, u }; }

const SKY_V = `layout(location=0) in vec2 aP;out vec2 vUv;void main(){vUv=aP*.5+.5;gl_Position=vec4(aP,0.,1.);}`;
const SKY_F = `in vec2 vUv;out vec4 o;
uniform vec3 uFwd,uRight,uUp,uSun;uniform vec2 uTan;uniform float uT,uHy,uWind,uCamH;uniform sampler2D uRefl;
float h1(vec2 p){p=fract(p*vec2(123.34,456.21));p+=dot(p,p+45.32);return fract(p.x*p.y);}
float n2(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h1(i),h1(i+vec2(1,0)),f.x),mix(h1(i+vec2(0,1)),h1(i+vec2(1,1)),f.x),f.y);}
float fbm(vec2 p){float a=.5,s=0.;for(int i=0;i<5;i++){s+=a*n2(p);p=p*2.03+vec2(17.3,9.1);a*=.5;}return s;}
/* the dusk sky along a direction. The sun has just set, a little left of centre. Colour comes from how much air the light has crossed:
   deep blue overhead where the path is short, through pale green-grey, to peach and ember at the horizon toward the sun. */
vec3 sky(vec3 d){
  float e=clamp(d.y,0.,1.);
  vec2 sh=normalize(uSun.xz);float mu=dot(normalize(d.xz+vec2(1e-5)),sh),toward=.5+.5*mu;toward*=toward;
  float g=max(dot(d,uSun),0.);
  vec3 zen=vec3(.085,.15,.30),upper=vec3(.21,.33,.50),band=vec3(.56,.63,.63),peach=vec3(.98,.70,.46),ember=vec3(.97,.43,.20),mauve=vec3(.46,.41,.52);
  vec3 c=mix(zen,upper,exp(-e*3.4));
  c=mix(c,band,exp(-e*6.));
  c=mix(c,mauve,exp(-e*11.)*(1.-toward)*.55);
  c=mix(c,peach,exp(-e*13.)*(.22+.78*toward));
  c=mix(c,ember,exp(-e*40.)*(.12+.88*toward*toward));
  c+=vec3(1.,.52,.2)*pow(g,26.)*.30*exp(-e*5.)+vec3(1.,.82,.5)*pow(g,260.)*.5;
  /* high thin cloud, lit from below where it is near the sun */
  if(d.y>.015){vec2 q=d.xz/(d.y+.14);q=vec2(q.x*sh.y-q.y*sh.x,dot(q,sh));
    float n=fbm(q*vec2(.22,1.4)+vec2(uT*.006*(1.+uWind*4.),2.7));float dens=smoothstep(.46,.72,n)*smoothstep(.015,.09,d.y)*smoothstep(.8,.3,d.y);
    float lit=toward*exp(-e*4.5);vec3 cc=mix(vec3(.25,.26,.36),vec3(1.,.55,.34),lit);cc=mix(cc,c,.25);
    c=mix(c,cc,dens*.62);c+=vec3(1.,.6,.35)*dens*lit*smoothstep(.62,.5,n)*.10;}
  /* the far shore: a line of trees */
  float az=atan(d.x,-d.z);float ht=.007+.010*n2(vec2(az*9.,3.))+.006*n2(vec2(az*38.,7.))+.003*n2(vec2(az*150.,1.));
  vec3 tree=mix(vec3(.035,.045,.07),vec3(.16,.10,.09),toward*.5);
  c=mix(tree,c,smoothstep(ht-.0012,ht+.0012,d.y));
  return c;}
void main(){
  vec2 ndc=vUv*2.-1.;vec3 d=normalize(uFwd+ndc.x*uTan.x*uRight+ndc.y*uTan.y*uUp);vec3 col;
  if(d.y>=0.)col=sky(d);
  else{float t=uCamH/(-d.y);vec2 w=d.xz*t;
    /* still water with a slow ripple: it mirrors the sky, stretches what it mirrors, and shows its own dark body where we look down into it */
    vec2 gr=vec2(n2(w*1.3+vec2(uT*.35,0.))-.5,n2(w*1.3+vec2(31.,-uT*.3))-.5)+.7*vec2(n2(w*.21+uT*.08)-.5,n2(w*.21+vec2(7.,-uT*.07))-.5);
    float amp=(.018+.05*uWind)*(.35+.65*min(1.,14./t));
    vec3 rd=normalize(vec3(d.x+gr.x*amp,-d.y+abs(gr.y)*amp*1.6+.002,d.z));
    vec3 rc=sky(rd);
    float F=.03+.97*pow(1.+d.y,5.);
    col=mix(vec3(.018,.03,.045),rc*.93,F);
    vec2 ruv=vec2(vUv.x+gr.x*amp*.5,2.*uHy-vUv.y+gr.y*amp*1.2);
    if(ruv.y<1.){float a=texture(uRefl,ruv).a;col*=1.-.82*a*F;}
    float bank=smoothstep(8.5,6.,t+2.5*n2(vec2(w.x*.35,3.))+.5*n2(vec2(w.x*2.,9.)));col=mix(col,vec3(.018,.017,.02),bank);}
  vec2 v=vUv-.5;col*=1.-.22*dot(v,v);
  col+=(h1(gl_FragCoord.xy+fract(uT)*61.)-.5)/255.*1.6;
  o=vec4(col,1.);}`;

const BIRD_V = `layout(location=0) in vec3 aV;layout(location=1) in float aW;layout(location=2) in vec3 iP;layout(location=3) in vec3 iH;layout(location=4) in vec3 iR;
uniform mat4 uVP;uniform vec3 uCam;uniform float uFocal,uMinPx;out float vA;
void main(){vec3 f=normalize(iH),r0=normalize(cross(f,vec3(0.,1.,0.))),u0=cross(r0,f);float cr=cos(iR.x),sr=sin(iR.x);vec3 r=r0*cr+u0*sr,u=u0*cr-r0*sr;
  /* the wing beat: the wing swings about the body, the tip furthest */
  float th=(sin(iR.y)*.85+.12)*aW;vec3 v=aV;v.y+=abs(aV.z)*sin(th);v.z*=cos(th);
  float dist=length(iP-uCam),px=iR.z*uFocal/dist,s=1.,a=1.;if(px<uMinPx){s=uMinPx/px;a=1./(s*s);}
  vec3 wp=iP+iR.z*s*(f*v.x+u*v.y+r*v.z);gl_Position=uVP*vec4(wp,1.);vA=a*mix(1.,.8,clamp((dist-110.)/160.,0.,1.));}`;
const BIRD_F = `in float vA;out vec4 o;uniform vec3 uCol;uniform float uOp;void main(){float a=vA*uOp;o=vec4(uCol*a,a);}`;

const REED_V = `layout(location=0) in vec2 aT;layout(location=1) in vec3 iB;layout(location=2) in vec3 iD;layout(location=3) in vec3 iC;layout(location=4) in vec4 iW;
uniform mat4 uVP;uniform vec3 uCam;uniform float uT,uWind;out vec2 vS;out float vK;
void main(){float t=aT.x;vec3 c=iB+iD*t+iC*t*t;float hgt=max(c.y,0.)/2.2;
  float sw=(sin(uT*1.1+c.x*.7+iB.z*.4)*.6+sin(uT*.43+iB.x*1.3)*.4+sin(uT*2.3+iW.z)*.15)*(.035+.16*uWind)+uWind*.22;c.x+=sw*hgt*hgt;c.z+=sw*.3*hgt*hgt;
  vec3 tan=normalize(iD+2.*t*iC),side=normalize(cross(tan,c-uCam));
  float w=mix(iW.x,iW.y,t);if(iW.w>.5)w=iW.x*pow(sin(3.14159*clamp(t*.96+.02,0.,1.)),.6);
  c+=side*aT.y*w;gl_Position=uVP*vec4(c,1.);vS=vec2(aT.y,t);vK=iW.w;}`;
const REED_F = `in vec2 vS;in float vK;out vec4 o;float h1(vec2 p){p=fract(p*vec2(123.34,456.21));p+=dot(p,p+45.32);return fract(p.x*p.y);}
void main(){float a=1.;vec3 c=vec3(.016,.016,.020);
  if(vK>.5){float e=abs(vS.x);float fz=h1(floor(vec2(vS.y*46.,vS.x*5.+7.)));a=(1.-smoothstep(.35+.5*fz,1.,e))*.94;c=mix(c,vec3(.17,.095,.06),smoothstep(.25,1.,e)*.8);}
  o=vec4(c*a,a);}`;

const skyP = prog(SKY_V, SKY_F), birdP = prog(BIRD_V, BIRD_F), reedP = prog(REED_V, REED_F);

/* ─── geometry ─── */
const quad = gl.createVertexArray(); gl.bindVertexArray(quad); { const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW); gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0); }

/* a starling from above: short tail, pointed triangular wings. x forward, y up, z to the right; the fourth number says how much the point beats. */
function birdMesh() { const v = []; const tri = (...p) => p.forEach(q => v.push(q[0], q[1], q[2], q[3] || 0));
  const N = [.36, 0, 0], SL = [.10, 0, -.07], SR = [.10, 0, .07], HL = [-.20, 0, -.045], HR = [-.20, 0, .045], TL = [-.42, 0, -.075], TR = [-.42, 0, .075], TM = [-.37, 0, 0];
  tri(N, SL, SR); tri(SL, HL, HR); tri(SL, HR, SR); tri(HL, TL, TM); tri(HL, TM, HR); tri(HR, TM, TR);
  tri(N, [.05, .07, 0], [.05, -.08, 0]); tri([.05, .07, 0], [-.3, 0, 0], [.05, -.08, 0]);
  for (const s of [-1, 1]) { const RF = [.15, 0, s * .06], RB = [-.11, 0, s * .05], W = [.13, 0, s * .27, .5], T = [-.09, 0, s * .52, 1], TMd = [-.16, 0, s * .24, .45]; tri(RF, W, RB); tri(RB, W, TMd); tri(W, T, TMd); }
  return new Float32Array(v); }
const birdVerts = birdMesh(), birdVAO = gl.createVertexArray(), inst = new Float32Array((NMAX + 1) * 9), instBuf = gl.createBuffer();
gl.bindVertexArray(birdVAO); { const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, birdVerts, gl.STATIC_DRAW); gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 16, 0); gl.enableVertexAttribArray(1); gl.vertexAttribPointer(1, 1, gl.FLOAT, false, 16, 12);
  gl.bindBuffer(gl.ARRAY_BUFFER, instBuf); gl.bufferData(gl.ARRAY_BUFFER, inst.byteLength, gl.DYNAMIC_DRAW); for (let a = 0; a < 3; a++) { gl.enableVertexAttribArray(2 + a); gl.vertexAttribPointer(2 + a, 3, gl.FLOAT, false, 36, a * 12); gl.vertexAttribDivisor(2 + a, 1); } }

/* reeds: stems, leaves and seed heads, all the same bent ribbon drawn many times */
const SEG = 9, reedVAO = gl.createVertexArray(), reedBuf = gl.createBuffer(); let reedCount = 0;
gl.bindVertexArray(reedVAO); { const s = []; for (let i = 0; i <= SEG; i++) s.push(i / SEG, -1, i / SEG, 1); const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(s), gl.STATIC_DRAW); gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
  gl.bindBuffer(gl.ARRAY_BUFFER, reedBuf); const off = [0, 12, 24, 36], sz = [3, 3, 3, 4]; for (let a = 0; a < 4; a++) { gl.enableVertexAttribArray(1 + a); gl.vertexAttribPointer(1 + a, sz[a], gl.FLOAT, false, 52, off[a]); gl.vertexAttribDivisor(1 + a, 1); } }
function plantReeds(halfFov) { let s = 12345; const r = () => (s = (s * 16807) % 2147483647) / 2147483647, d = [];
  const rib = (b, dir, c, w0, w1, ph, kind) => d.push(b[0], b[1], b[2], dir[0], dir[1], dir[2], c[0], c[1], c[2], w0, w1, ph, kind);
  const span = halfFov + .2, count = Math.round((small ? 110 : 200) * span / .6);
  for (let i = 0; i < count; i++) { const az = (r() * 2 - 1) * span, a = Math.min(1, Math.abs(az) / halfFov), dist = 5.5 + r() * r() * 9;
    /* tall at the sides, low in the middle, so the reeds frame the water */
    const clump = .5 + .5 * Math.sin(az * 23 + 1.3) * Math.sin(az * 7.1), top = (-7.5 + 11 * Math.pow(a, 1.8) + clump * 2.4 - r() * 4) * Math.PI / 180;
    const h = Math.max(.45, 1.7 - .12 + dist * Math.tan(top)), base = [Math.sin(az) * dist, .12, -Math.cos(az) * dist], lean = (r() - .5) * .2, bend = (r() - .35) * .24, ph = r() * 6.28;
    rib(base, [lean * h, h, (r() - .5) * .1 * h], [bend * h * .5, -Math.abs(bend) * h * .08, 0], .0075, .003, ph, 0);
    const at = t => [base[0] + lean * h * t + bend * h * .5 * t * t, base[1] + h * t - Math.abs(bend) * h * .08 * t * t, base[2]];
    const nl = 1 + Math.floor(r() * 3); for (let k = 0; k < nl; k++) { const t = .3 + r() * .55, p = at(t), sd = r() < .5 ? -1 : 1, len = .22 + r() * .3, up = .55 + r() * .6; rib(p, [sd * len * Math.cos(up), len * Math.sin(up), (r() - .5) * .2], [sd * len * .3, -len * (.15 + r() * .35), 0], .0095, .0008, ph, 0); }
    if (r() < .7) { const p = at(1), sd = bend >= 0 ? 1 : -1, len = .2 + r() * .16; rib(p, [sd * len * .18 + lean * len, len, 0], [sd * len * .3, -len * .22, 0], .016 + r() * .012, 0, ph, 1); } }
  reedCount = d.length / 13; gl.bindBuffer(gl.ARRAY_BUFFER, reedBuf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(d), gl.STATIC_DRAW); }

/* the flock is drawn once, small, into a texture so the water can mirror it */
const refl = { fb: gl.createFramebuffer(), tex: gl.createTexture(), w: 0, h: 0 };
gl.bindTexture(gl.TEXTURE_2D, refl.tex); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);

/* ─── the camera: someone standing on the bank ─── */
const cam = { pos: [0, 1.7, 0], yaw: 0, tyaw: 0, pitch: .17, tanX: .53, tanY: .3, fwd: [0, 0, -1], right: [1, 0, 0], up: [0, 1, 0], vp: new Float32Array(16), focal: 900, hy: .2 };
const SUN = (() => { const v = [-.36, -.035, -1], l = Math.hypot(v[0], v[1], v[2]); return v.map(x => x / l); })();
let dpr = 1, quality = 1;
function size() { const w = canvas.clientWidth, h = canvas.clientHeight; if (!w || !h) return; dpr = Math.min(devicePixelRatio || 1, small ? 1.5 : 2) * quality;
  const W = Math.max(2, Math.round(w * dpr)), H = Math.max(2, Math.round(h * dpr)); if (canvas.width !== W || canvas.height !== H) { canvas.width = W; canvas.height = H; }
  const asp = W / H, k = Math.max(0, Math.min(1, (asp - .8) / (1.6 - .8))); cam.tanX = .41 + .12 * k; cam.tanY = cam.tanX / asp; cam.pitch = Math.atan((.4 + .2 * k) * cam.tanY); cam.focal = W / 2 / cam.tanX;
  const rw = Math.max(2, W >> 1), rh = Math.max(2, H >> 1); if (rw !== refl.w || rh !== refl.h) { refl.w = rw; refl.h = rh; gl.bindTexture(gl.TEXTURE_2D, refl.tex); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, rw, rh, 0, gl.RGBA, gl.UNSIGNED_BYTE, null); gl.bindFramebuffer(gl.FRAMEBUFFER, refl.fb); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, refl.tex, 0); gl.bindFramebuffer(gl.FRAMEBUFFER, null); }
  const hf = Math.atan(cam.tanX); if (size.hf !== hf) { size.hf = hf; plantReeds(hf + .09); } }
function aim() { const cy = Math.cos(cam.yaw), sy = Math.sin(cam.yaw), cp = Math.cos(cam.pitch), sp = Math.sin(cam.pitch);
  const f = cam.fwd = [sy * cp, sp, -cy * cp], r = cam.right = [cy, 0, sy], u = cam.up = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]];
  const p = cam.pos, n = .5, fa = 3000, m = cam.vp, tx = -(r[0] * p[0] + r[1] * p[1] + r[2] * p[2]), ty = -(u[0] * p[0] + u[1] * p[1] + u[2] * p[2]), tz = (f[0] * p[0] + f[1] * p[1] + f[2] * p[2]);
  /* projection times view, written out. View rows are right, up, -forward. */
  const a = 1 / cam.tanX, b = 1 / cam.tanY, c = (fa + n) / (n - fa), dd = 2 * fa * n / (n - fa);
  m[0] = a * r[0]; m[4] = a * r[1]; m[8] = a * r[2]; m[12] = a * tx;
  m[1] = b * u[0]; m[5] = b * u[1]; m[9] = b * u[2]; m[13] = b * ty;
  m[2] = -c * f[0]; m[6] = -c * f[1]; m[10] = -c * f[2]; m[14] = c * tz + dd;
  m[3] = f[0]; m[7] = f[1]; m[11] = f[2]; m[15] = -tz;
  cam.hy = .5 + .5 * (-f[1] / (cam.tanY * u[1])); }

/* ─── drawing ─── */
let tDraw = 0;
function fillInstances() { const n = S.n; let o = 0; for (let i = 0; i < n; i++) { inst[o++] = S.px[i]; inst[o++] = S.py[i]; inst[o++] = S.pz[i]; inst[o++] = S.hx[i]; inst[o++] = S.hy[i]; inst[o++] = S.hz[i]; inst[o++] = S.roll[i]; inst[o++] = S.ph[i]; inst[o++] = SPAN; }
  const F = S.falcon; let m = n; if (F.on) { const v = Math.hypot(F.vx, F.vy, F.vz) || 1; inst[o++] = F.x; inst[o++] = F.y; inst[o++] = F.z; inst[o++] = F.vx / v; inst[o++] = F.vy / v; inst[o++] = F.vz / v; inst[o++] = 0; inst[o++] = F.t * 28; inst[o++] = 2.4; m++; }
  gl.bindBuffer(gl.ARRAY_BUFFER, instBuf); gl.bufferSubData(gl.ARRAY_BUFFER, 0, inst, 0, m * 9); return m; }
function drawBirds(m, op, minPx, focal) { gl.useProgram(birdP.p); gl.uniformMatrix4fv(birdP.u.uVP, false, cam.vp); gl.uniform3fv(birdP.u.uCam, cam.pos); gl.uniform1f(birdP.u.uFocal, focal); gl.uniform1f(birdP.u.uMinPx, minPx); gl.uniform3f(birdP.u.uCol, .035, .04, .058); gl.uniform1f(birdP.u.uOp, op);
  gl.bindVertexArray(birdVAO); gl.drawArraysInstanced(gl.TRIANGLES, 0, birdVerts.length / 4, m); }
function draw() { size(); cam.yaw += (cam.tyaw - cam.yaw) * .06; aim(); const W = canvas.width, H = canvas.height, m = fillInstances();
  gl.disable(gl.DEPTH_TEST); gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
  gl.bindFramebuffer(gl.FRAMEBUFFER, refl.fb); gl.viewport(0, 0, refl.w, refl.h); gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT); drawBirds(m, .9, 2.2, cam.focal * refl.w / W);
  gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.viewport(0, 0, W, H); gl.disable(gl.BLEND);
  gl.useProgram(skyP.p); gl.uniform3fv(skyP.u.uFwd, cam.fwd); gl.uniform3fv(skyP.u.uRight, cam.right); gl.uniform3fv(skyP.u.uUp, cam.up); gl.uniform3fv(skyP.u.uSun, SUN); gl.uniform2f(skyP.u.uTan, cam.tanX, cam.tanY);
  gl.uniform1f(skyP.u.uT, tDraw); gl.uniform1f(skyP.u.uHy, cam.hy); gl.uniform1f(skyP.u.uWind, S.P.wind); gl.uniform1f(skyP.u.uCamH, cam.pos[1]); gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, refl.tex); gl.uniform1i(skyP.u.uRefl, 0);
  gl.bindVertexArray(quad); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  gl.enable(gl.BLEND); drawBirds(m, .88, 1.5, cam.focal);
  gl.useProgram(reedP.p); gl.uniformMatrix4fv(reedP.u.uVP, false, cam.vp); gl.uniform3fv(reedP.u.uCam, cam.pos); gl.uniform1f(reedP.u.uT, tDraw); gl.uniform1f(reedP.u.uWind, S.P.wind);
  gl.bindVertexArray(reedVAO); gl.drawArraysInstanced(gl.TRIANGLE_STRIP, 0, (SEG + 1) * 2, reedCount); gl.bindVertexArray(null); }

/* ─── sound: the starling voice from the old Song of the Starlings page, kept as it was ─── */
const { max, min, abs, pow, exp, floor, random, sin, PI } = Math;
let ac = null, noiseBuf = null, voiceGain = null, natureGain = null, outGain = null, windNoise = null, soundOn = false, singers = 0, offTimer = 0;
const MAX_SINGERS = small ? 6 : 12, canPan = typeof StereoPannerNode !== 'undefined';
function connectVoice(node, pan) { if (canPan && pan) { const p = ac.createStereoPanner(); p.pan.value = max(-1, min(1, pan)); node.connect(p); p.connect(voiceGain); setTimeout(() => { try { p.disconnect(); } catch (e) {} }, 4000); } else node.connect(voiceGain); }
/*AUDIO_PORT*/
function initAudio() { if (ac) return; ac = new (window.AudioContext || window.webkitAudioContext)(); noiseBuf = createNoiseBuf(ac);
  const comp = ac.createDynamicsCompressor(); comp.threshold.value = -12; comp.knee.value = 12; comp.ratio.value = 3; comp.attack.value = .005; comp.release.value = .25;
  natureGain = ac.createGain(); natureGain.gain.value = .6 * .4; voiceGain = ac.createGain(); voiceGain.gain.value = .75 * .5;
  const dry = ac.createGain(), wet = ac.createGain(), rev = createReverb(ac), mix = .7; dry.gain.value = 1 - mix * .35; wet.gain.value = mix;
  outGain = ac.createGain(); outGain.gain.value = 0;
  natureGain.connect(comp); voiceGain.connect(comp); comp.connect(dry); comp.connect(rev); rev.connect(wet); dry.connect(outGain); wet.connect(outGain); outGain.connect(ac.destination);
  windNoise = { gain: ac.createGain(), filter: ac.createBiquadFilter() }; windNoise.gain.gain.value = 0; windNoise.filter.type = 'lowpass'; windNoise.filter.frequency.value = 400; windNoise.filter.Q.value = .8;
  const ns = ac.createBufferSource(); ns.buffer = noiseBuf; ns.loop = true; ns.connect(windNoise.filter); windNoise.filter.connect(windNoise.gain); windNoise.gain.connect(natureGain); ns.start(); }
function setSound(on) { soundOn = on; $('snd').setAttribute('aria-pressed', on ? 'true' : 'false'); clearTimeout(offTimer);
  if (on) { initAudio(); const go = () => { const t = ac.currentTime; outGain.gain.cancelScheduledValues(t); outGain.gain.setTargetAtTime(1, t, .25); }; if (ac.state !== 'running') ac.resume().then(go, () => {}); else go(); }
  else if (ac) { const t = ac.currentTime; outGain.gain.cancelScheduledValues(t); outGain.gain.setTargetAtTime(0, t, .07); offTimer = setTimeout(() => { if (!soundOn && ac.state === 'running') ac.suspend(); }, 700); } }
function sing(hold, fn) { if (singers >= MAX_SINGERS) return; singers++; try { fn(); } catch (e) {} setTimeout(() => { singers = max(0, singers - 1); }, hold * 1000); }
let turnNow = 0, fearNow = 0;
function panOf(i) { const dx = S.px[i] - cam.pos[0], dz = S.pz[i] - cam.pos[2], x = dx * cam.right[0] + dz * cam.right[2], z = dx * cam.fwd[0] + dz * cam.fwd[2]; return max(-1, min(1, x / (z * cam.tanX + 1e-3))) * .8; }
function audioTick(dt) { if (!ac || !soundOn || ac.state !== 'running') return; const now = ac.currentTime, sun = .3, alarm = S.falcon.on && fearNow > .004, bird = () => floor(random() * S.n);
  if (alarm && random() < (5 + 60 * fearNow) * dt) { const i = bird(), type = random() < .4 ? 'squeal' : random() < .7 ? 'chatter' : 'click'; sing(.12 + random() * .2, () => playDualSyrinx(.18 + random() * .1, now, type, floor(random() * 5) + 10, .2, i, panOf(i))); }
  /* in flight: short contact calls, more of them while the flock is turning hard */
  if (random() < (1.6 + 6 * min(1, turnNow)) * dt) { const i = bird(); sing(.25 + random(), () => playDualSyrinx(.08 + sun * .08, now, 'contact', floor(random() * 10), S.pol, i, panOf(i))); }
  if (!alarm && random() < .45 * dt) { const i = bird(); sing(.5 + random() * 1.5, () => playStarlingPhrase(.1 + sun * .1, now, 2 + floor(random() * 2), 'song', i, panOf(i))); }
  /* birds already down in the reeds: whole phrases of whistles, warbles and clicks */
  if (!alarm && random() < .32 * dt) { const i = floor(random() * 250), len = 3 + floor(random() * 6); sing(1.2 + len * .2, () => playStarlingPhrase((.12 + sun * .15) * .8, now, len, random() < .3 ? 'settle' : 'song', i, (random() * 2 - 1) * .8)); }
  const blow = min(1, S.P.wind * .8 + turnNow * .35 + fearNow * 4); windNoise.gain.gain.setTargetAtTime(.04 + .5 * S.P.wind + .16 * min(1, turnNow) + min(.2, fearNow * 3), now, .5); windNoise.filter.frequency.setTargetAtTime(300 + blow * 1400, now, .4); }

/* ─── the loop ─── */
let paused = still, visible = true, last = 0, acc = 0, slow = 0, fast = 0, kps = 0, shown = 0, corr = { ratio: 0 }, corrAt = 0, group = { share: 1 }, frames = 0;
if ('IntersectionObserver' in window) new IntersectionObserver(e => { visible = e[0].isIntersecting; }, { threshold: .02 }).observe(canvas);
document.addEventListener('visibilitychange', () => { if (ac && soundOn) { if (document.hidden) ac.suspend(); else ac.resume(); } last = 0; });
function advance(sec) { const st = Math.round(sec * 60); for (let i = 0; i < st; i++) M.step(S, 1 / 60); }
function sample() { const n = S.n, st = Math.max(1, Math.floor(n / 300)); let u = 0, f = 0, c = 0; for (let i = 0; i < n; i += st) { u += Math.hypot(S.ux[i], S.uy[i], S.uz[i]); f += S.thr[i]; c++; } turnNow = u / c; fearNow = f / c; }
function readout(now) { if (now - shown < 400) return; shown = now; group = M.largestGroup(S); if (now - corrAt > 1500) { corrAt = now; corr = M.correlation(S, 320, true); }
  $('r1').textContent = S.pol.toFixed(2); $('r2').textContent = Math.round(group.share * 100) + '% of birds';
  $('r3').textContent = corr.L ? Math.round(corr.ratio * 100) + '% of its width' : '–'; $('r4').textContent = S.P.rule ? kps.toFixed(1) + ' times a second, each bird' : 'at every instant'; $('r5').textContent = String(S.n); }
function frame(now) { requestAnimationFrame(frame); if (document.hidden || !visible) { last = 0; return; }
  const dt = last ? Math.min(.1, (now - last) / 1000) : 1 / 60; last = now; frames++;
  if (!paused) { acc += dt; let steps = 0; while (acc >= 1 / 60 && steps < 2) { M.step(S, 1 / 60); acc -= 1 / 60; steps++; kps += (S.commits * 60 / S.n - kps) * .05; } if (acc > 1 / 30) acc = 0; tDraw += dt; sample(); audioTick(dt);
    /* if frames are slow, fly fewer birds, then draw fewer pixels */
    if (dt > .03) slow++; else if (dt < .02) fast++; if (frames % 150 === 0) { if (slow > 90 && frames > 200) { if (S.n > 700) setCount(Math.round(S.n * .72)); else if (quality > .6) quality *= .8; } slow = fast = 0; } }
  draw(); readout(now); if (!S.falcon.on && $('falcon').disabled) $('falcon').disabled = false; }
function setCount(n) { S.n = Math.max(300, Math.min(S.nMax, n)); M.buildGrid(S); const k = Math.min(S.P.k, M.KMAX); for (let i = 0; i < S.n; i++) M.knn(S, i, k); M.measure(S); }

/* ─── controls ─── */
$('snd').onclick = () => setSound(!soundOn);
$('falcon').onclick = () => { if (M.sendFalcon(S, [95, 46, 75])) { $('falcon').disabled = true; if (paused) setPaused(false); if (ac && soundOn) { const t = ac.currentTime; playFalconCry(.9, t + .2); playFalconCry(.7, t + 1.3); } } };
$('kn').oninput = e => { S.P.k = +e.target.value; $('knv').textContent = e.target.value; };
$('wind').oninput = e => { S.P.wind = +e.target.value; };
$('plain').onclick = () => { S.P.rule = !S.P.rule; $('plain').setAttribute('aria-pressed', S.P.rule ? 'false' : 'true'); if (S.P.rule) for (let i = 0; i < S.n; i++) S.C[i] = Math.random() * S.P.Cstar; };
function setPaused(p) { paused = p; $('pause').setAttribute('aria-pressed', p ? 'true' : 'false'); $('pause').textContent = p ? 'Paused' : 'Pause'; last = 0; }
$('pause').onclick = () => setPaused(!paused);
canvas.addEventListener('pointermove', e => { const r = canvas.getBoundingClientRect(); cam.tyaw = ((e.clientX - r.left) / r.width - .5) * .16; });
canvas.addEventListener('pointerleave', () => { cam.tyaw = 0; });
addEventListener('resize', () => { size(); if (paused) draw(); });

advance(still ? 6 : 1.5); setPaused(still); sample();
window.MURMURATION = { S, cam, advance, draw, setPaused, setCount, state: () => ({ n: S.n, pol: S.pol, share: M.largestGroup(S).share, falcon: S.falcon.on, paused, frames, reeds: reedCount, sound: soundOn, ac: ac ? ac.state : 'none', singers }), sing: () => ({ playDualSyrinx, playStarlingPhrase, playFalconCry }) };
requestAnimationFrame(frame);
})();
