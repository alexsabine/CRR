(function () {
'use strict';
const M = window.MYC, P = M.P, $ = id => document.getElementById(id), qs = new URLSearchParams(location.search);
const still = matchMedia('(prefers-reduced-motion: reduce)').matches, small = Math.min(innerWidth, innerHeight) < 600;
const DPR = Math.min(devicePixelRatio || 1, small ? 1.5 : 2), DPS = 0.5;            /* days of the fungus per second of yours: a setting */
let qual = +qs.get('q') || 1; const lockQ = qs.has('q');
const S = { mode: +qs.get('mode') || 0, tool: 'wood', hold: qs.has('hold') || still, time: 0, hand: [10, 10], hover: null, seed: (+qs.get('seed')) || (Math.floor(Math.random() * 1e6) + 1) };
let W = null, series = [], marks = [], effPo = [], lastSample = -1, netDirty = true, netT = 9, simAcc = 0;

/* ---------- the camera: above the soil, tilted a little. The same sums are in the shader. ---------- */
const CAM = { C: [10, -5.8, 27.5], T: [10, 9.7, 0], foc: 3, voff: 0, asp: 1 };
{ const f = [CAM.T[0] - CAM.C[0], CAM.T[1] - CAM.C[1], CAM.T[2] - CAM.C[2]], l = Math.hypot(f[0], f[1], f[2]); CAM.F = f.map(v => v / l); CAM.R = [1, 0, 0]; CAM.U = [0, -CAM.F[2], CAM.F[1]]; }
function camFit(asp) { CAM.asp = asp; let mx = 0, lo = 1e9, hi = -1e9; for (const p of [[-0.4, -0.5], [20.4, -0.5], [-0.4, 20.5], [20.4, 20.5]]) { const d = [p[0] - CAM.C[0], p[1] - CAM.C[1], -CAM.C[2]], w = d[0] * CAM.F[0] + d[1] * CAM.F[1] + d[2] * CAM.F[2], x = d[0] / w / asp, y = (d[1] * CAM.U[1] + d[2] * CAM.U[2]) / w; mx = Math.max(mx, Math.abs(x)); lo = Math.min(lo, y); hi = Math.max(hi, y); }
  CAM.foc = Math.min(1 / mx, 2 / (hi - lo)); CAM.voff = CAM.foc * (hi + lo) / 2; }
function project(x, y, z) { const d0 = x - CAM.C[0], d1 = y - CAM.C[1], d2 = (z || 0) - CAM.C[2], w = d0 * CAM.F[0] + d1 * CAM.F[1] + d2 * CAM.F[2]; return [(d0 / w * CAM.foc / CAM.asp + 1) / 2, 1 - ((d1 * CAM.U[1] + d2 * CAM.U[2]) / w * CAM.foc - CAM.voff + 1) / 2]; }
function unproject(u, v) { const qx = (u * 2 - 1) * CAM.asp, qy = (1 - v * 2) + CAM.voff, d = [CAM.F[0] * CAM.foc + qx, CAM.F[1] * CAM.foc + CAM.U[1] * qy, CAM.F[2] * CAM.foc + CAM.U[2] * qy], t = -CAM.C[2] / d[2]; return [CAM.C[0] + d[0] * t, CAM.C[1] + d[1] * t]; }

/* ---------- WebGL: one full-screen pass ---------- */
const cv = $('floor'), ov = $('over'), ox = ov.getContext('2d');
const gl = qs.has('nogl') ? null : cv.getContext('webgl', { alpha: false, antialias: false, powerPreference: 'high-performance' }) || cv.getContext('experimental-webgl', { alpha: false });
const VS = `attribute vec2 aQ; varying vec2 vQ; void main(){ vQ=aQ; gl_Position=vec4(aQ,0.,1.); }`;
const FS = `
#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
#else
precision mediump float;
#endif
varying vec2 vQ; uniform sampler2D uNet; uniform vec3 uC,uF,uR,uU; uniform float uAsp,uFoc,uVoff,uTime,uWet,uMode,uDof,uFocT,uTx;
uniform vec4 uB1[6],uB2[6],uL1[8],uL2[8],uM1[12],uM2[12]; uniform int uNB,uNL,uNM;
const vec3 L=vec3(-0.449,-0.379,0.809); const vec3 KEY=vec3(1.62,1.48,1.24); const vec3 AMB=vec3(0.15,0.18,0.23);
float hash(vec2 p){ p=fract(p*vec2(123.34,456.21)); p+=dot(p,p+45.32); return fract(p.x*p.y); }
float vnoise(vec2 p){ vec2 i=floor(p), f=fract(p); f=f*f*(3.-2.*f); return mix(mix(hash(i),hash(i+vec2(1.,0.)),f.x), mix(hash(i+vec2(0.,1.)),hash(i+vec2(1.,1.)),f.x), f.y); }
float fbm(vec2 p){ float a=.5,s=0.; for(int i=0;i<4;i++){ s+=a*vnoise(p); p=p*2.03+vec2(17.1,9.2); a*=.5; } return s; }
vec3 tone(vec3 x){ x=max(x,0.); x=(x*(2.51*x+0.03))/(x*(2.43*x+0.59)+0.14); return pow(clamp(x,0.,1.),vec3(1./2.2)); }
float soilH(vec2 g,float det){ return 0.55*vnoise(g*1.1)+0.3*vnoise(g*3.7+5.)+det*(0.17*vnoise(g*11.+2.)+0.10*vnoise(g*29.)); }
float fil(vec2 g){ return pow(1.-abs(2.*vnoise(g*23.+3.)-1.),9.)+0.7*pow(1.-abs(2.*vnoise(g*49.-7.)-1.),9.); }
/* a leaf lying flat: q along the midrib from -1 to 1; returns how far inside the edge */
float leafD(vec2 q,float w){ float x=clamp(q.x,-1.,1.); return w*pow(max(1.-x*x,0.),0.7)*(1.+0.28*x)-abs(q.y); }
vec3 leafC(vec2 q,float d,vec3 base,float seed){ float rib=smoothstep(0.03,0.,abs(q.y))*0.45, vein=smoothstep(0.8,1.,sin((q.x-abs(q.y)*1.5)*21.+seed*6.))*0.22*smoothstep(0.,0.12,d);
  vec3 c=base*(0.62+0.7*vnoise(q*6.+seed*31.)); c*=1.-rib-vein; c*=0.7+0.3*smoothstep(0.,0.16,d); return c*(1.+0.35*q.y*sign(seed-0.5)); }
float cells(vec2 p){ vec2 i=floor(p), f=fract(p); float d1=9., d2=9.; for(int a=-1;a<=1;a++) for(int b=-1;b<=1;b++){ vec2 q=vec2(float(a),float(b)); vec2 o=vec2(hash(i+q),hash(i+q+17.3)); float dd=length(q+o-f); if(dd<d1){ d2=d1; d1=dd; } else if(dd<d2) d2=dd; } return d2-d1; }
float sdBox(vec2 p,vec2 b){ vec2 q=abs(p)-b; return length(max(q,0.))+min(max(q.x,q.y),0.); }
void main(){
  vec3 d=normalize(uF*uFoc+uR*(vQ.x*uAsp)+uU*(vQ.y+uVoff));
  float tG=-uC.z/d.z; vec2 g=uC.xy+d.xy*tG;
  float blur=clamp(abs(tG-uFocT)/uFocT*uDof,0.,1.), det=1.-blur;
  /* soil */
  float e=0.04, h0=soilH(g,det), hx=soilH(g+vec2(e,0.),det), hy=soilH(g+vec2(0.,e),det);
  vec3 n=normalize(vec3(-(hx-h0)/e*0.19,-(hy-h0)/e*0.19,1.));
  vec3 alb=mix(vec3(0.011,0.008,0.006),vec3(0.046,0.031,0.020),fbm(g*0.5+3.))*(0.5+1.0*h0);
  float crumb=cells(g*3.7+vec2(vnoise(g*2.),vnoise(g*2.+9.))*0.6); alb*=0.55+0.45*mix(1.,smoothstep(0.,0.2,crumb),det);
  alb=mix(alb,vec3(0.13,0.11,0.09),smoothstep(0.93,0.99,vnoise(g*17.+11.))*det*0.4);
  float flat_=0.;
  /* old leaves, long dead: at most one to a square, most squares empty */
  { vec2 id=floor(g/3.3); float hh=hash(id+7.); if(hh<0.44){ vec2 c=(id+0.5+0.3*(vec2(hash(id+1.3),hash(id+2.9))-0.5))*3.3; float a=hash(id+4.1)*6.283, Ln=0.75+0.6*hash(id+5.5);
      vec2 q=vec2(dot(g-c,vec2(cos(a),sin(a))),dot(g-c,vec2(-sin(a),cos(a))))/Ln; float dd=leafD(q,0.36+0.14*hash(id+6.))-0.05*vnoise(q*8.+hh*9.);
      float holes=smoothstep(0.26,0.40,vnoise(q*4.6+hh*20.)+0.55*smoothstep(0.,0.2,dd)-0.3*step(0.22,hh));
      float al=smoothstep(0.,0.03+0.12*blur,dd)*holes; vec3 lc=leafC(q,dd,mix(mix(vec3(0.030,0.019,0.011),vec3(0.088,0.050,0.020),hash(id+9.)),vec3(0.13,0.105,0.07),step(0.86,hash(id+3.))),hh);
      alb*=1.-0.5*smoothstep(-0.16,0.,dd)*(1.-al); alb=mix(alb,lc,al*0.94); flat_=max(flat_,al); } }
  /* fresh litter: food */
  for(int i=0;i<8;i++){ if(i>=uNL) break; vec4 a=uL1[i], b=uL2[i]; vec2 r=g-a.xy; if(dot(r,r)>a.w*a.w*1.5) continue;
    vec2 q=vec2(dot(r,vec2(cos(a.z),sin(a.z))),dot(r,vec2(-sin(a.z),cos(a.z))))/a.w; float dd=leafD(q,0.5), al=smoothstep(0.,0.03+0.1*blur,dd);
    vec3 lc=leafC(q,dd,mix(vec3(0.46,0.27,0.05),vec3(0.30,0.16,0.04),b.z),b.z); lc=mix(lc,vec3(0.11,0.07,0.04)*(0.6+0.8*vnoise(q*9.)),b.y);
    float wn=fbm(q*3.+b.z*9.); lc=mix(lc,vec3(0.58,0.58,0.52)*(0.7+0.5*fil(q*0.6)),smoothstep(0.1,-0.1,wn-b.x*0.7)*0.6);
    alb*=1.-0.45*smoothstep(-0.16,0.,dd)*(1.-al); alb=mix(alb,lc,al); flat_=max(flat_,al); }
  alb*=mix(1.,0.6,uWet*(1.-0.5*flat_));
  n=normalize(mix(n,vec3(0.,0.,1.),flat_*0.6));
  /* shade thrown on the soil by wood and by fruit bodies */
  float shd=1., ao=1.;
  for(int i=0;i<6;i++){ if(i>=uNB) break; vec4 a=uB1[i], b=uB2[i]; float c=cos(a.z), s=sin(a.z); vec2 r=g-a.xy, gs=r+L.xy/L.z*b.z*0.5;
    float sd=sdBox(vec2(r.x*c+r.y*s,-r.x*s+r.y*c),b.xy), ss=sdBox(vec2(gs.x*c+gs.y*s,-gs.x*s+gs.y*c),b.xy);
    ao*=1.-0.55*exp(-max(sd,0.)/0.28); shd*=1.-0.72*smoothstep(0.45*b.z+0.16,0.45*b.z-0.12,ss); }
  for(int i=0;i<12;i++){ if(i>=uNM) break; vec4 m=uM1[i]; float H=(0.28+0.95*m.z)*(1.-0.4*uM2[i].y), rc=0.11+0.34*m.z; vec2 c=vec2(m.x+m.w*H,m.y)-L.xy/L.z*H;
    shd*=1.-0.6*smoothstep(rc*1.3,rc*0.45,length(g-c)); ao*=1.-0.4*smoothstep(0.16,0.02,length(g-m.xy)); }
  float pool=0.66+0.5*smoothstep(22.,2.,length(g-vec2(6.5,7.5)));
  vec3 key=KEY*pool;
  vec3 col=alb*(AMB*(0.7+0.3*n.z)*ao+key*max(dot(n,L),0.)*shd);
  col+=key*shd*pow(max(dot(n,normalize(L-d)),0.),26.)*uWet*0.05*(1.-flat_);
  /* the fungus, from a picture of its strands: r fine threads, g cords, b what is being shown */
  vec2 uv=g/20.; float inb=step(0.,uv.x)*step(uv.x,1.)*step(0.,uv.y)*step(uv.y,1.), lb=blur*2.6;
  vec4 n0=texture2D(uNet,uv,lb-0.4)*inb, n1=texture2D(uNet,uv,lb+1.7)*inb, n2=texture2D(uNet,uv,lb+3.4)*inb;
  float te=uTx*(1.5+blur*4.);
  float cgx=texture2D(uNet,uv+vec2(te,0.),lb+0.7).g-texture2D(uNet,uv-vec2(te,0.),lb+0.7).g, cgy=texture2D(uNet,uv+vec2(0.,te),lb+0.7).g-texture2D(uNet,uv-vec2(0.,te),lb+0.7).g;
  float cst=texture2D(uNet,uv+L.xy*0.0042,lb+1.1).g*inb;
  col*=1.-0.55*smoothstep(0.05,0.6,cst)*(1.-smoothstep(0.2,0.7,n0.g));
  vec3 nh=normalize(vec3(-cgx*2.4,-cgy*2.4,1.));
  float dim=uMode<0.5?1.:(uMode<1.5?0.34:0.5);
  float lift=min(exp2(max(lb-0.4,0.)*0.45),1.6); float body=smoothstep(0.14,0.66,n0.g*mix(1.,lift,0.5)), fine=smoothstep(0.07,0.8,n0.r*lift)*0.74, age=smoothstep(0.2,0.75,n1.g*1.7);
  vec3 cordC=mix(vec3(0.80,0.80,0.75),vec3(0.76,0.65,0.43),age)*(AMB*1.2+key*shd*(0.32+0.68*max(dot(nh,L),0.)));
  cordC+=key*shd*pow(max(dot(nh,normalize(L+vec3(0.,-0.3,0.95))),0.),28.)*(0.10+0.3*uWet)*body;
  vec3 fineC=vec3(0.70,0.72,0.72)*(AMB+key*shd*0.85);
  float fz=clamp(n2.r*3.2+n1.g*1.1+n1.r*0.8,0.,1.)*det;
  vec3 web=vec3(0.58,0.60,0.60)*(AMB+key*shd*0.75);
  col=mix(col,web*dim,clamp(fil(g)*fz*0.6+(n1.r*0.4+n1.g*0.3)*0.14,0.,0.6));
  col=mix(col,fineC*dim,fine*(1.-body));
  col=mix(col,cordC*dim,body);
  if(uMode>0.5){ vec3 oc=uMode<1.5?vec3(1.0,0.66,0.16):vec3(0.35,1.0,0.80); col+=oc*(n0.b*1.5+n1.b*0.55)*0.8; }
  /* wood */
  float tHit=1e9;
  for(int i=0;i<6;i++){ if(i>=uNB) break; vec4 a=uB1[i], b=uB2[i]; float c=cos(a.z), s=sin(a.z);
    vec3 ro=vec3((uC.x-a.x)*c+(uC.y-a.y)*s,-(uC.x-a.x)*s+(uC.y-a.y)*c,uC.z), rd=vec3(d.x*c+d.y*s,-d.x*s+d.y*c,d.z)+1e-6;
    vec3 t1=(vec3(-b.x,-b.y,0.)-ro)/rd, t2=(vec3(b.x,b.y,b.z)-ro)/rd, tn=min(t1,t2), tf=max(t1,t2); float tN=max(max(tn.x,tn.y),tn.z), tF=min(min(tf.x,tf.y),tf.z), ch=tF-tN;
    if(ch>0.){ vec3 p=ro+rd*tN, N; vec2 w; float top=step(tn.x,tn.z)*step(tn.y,tn.z), sx=step(tn.y,tn.x)*(1.-top);
      float de=min(b.x-abs(p.x),b.y-abs(p.y)); vec3 wood; float wn, seed=a.x*1.7+a.y*0.9;
      if(top>0.5){ N=vec3(0.,0.,1.); float gr=fbm(vec2(p.x*1.4,p.y*8.)+seed); wood=mix(vec3(0.36,0.22,0.10),vec3(0.60,0.42,0.22),gr)*(0.92+0.08*sin(p.y*70.+gr*9.)); wood*=0.72+0.28*smoothstep(0.,0.1,de); wn=fbm(p.xy*2.6+seed)+0.16*smoothstep(0.,0.5,de); }
      else { vec2 nl=sx>0.5?vec2(-sign(rd.x),0.):vec2(0.,-sign(rd.y)); N=vec3(nl.x*c-nl.y*s,nl.x*s+nl.y*c,0.); float al_=sx>0.5?p.y:p.x; float rings=fbm(vec2(al_*5.,p.z*5.)+seed);
        wood=mix(vec3(0.13,0.08,0.045),vec3(0.34,0.22,0.11),rings)*(0.5+0.5*smoothstep(0.,b.z*0.7,p.z)); wn=fbm(vec2(al_,p.z)*2.6+seed+5.)+0.25*(p.z/b.z); }
      wood*=mix(1.,0.5,b.w)*mix(1.,0.7,uWet);
      vec3 myc=vec3(0.70,0.70,0.64)*(0.78+0.3*fil(p.xy*1.3+p.z)); wood=mix(wood,myc*dim+(1.-dim)*wood*0.3,smoothstep(0.12,-0.12,wn-a.w*1.15)*0.92);
      vec3 bc=wood*(AMB*(0.55+0.45*N.z)+key*max(dot(N,L),0.));
      float al=smoothstep(0.,0.07+blur*0.3,ch); col=mix(col,bc,al); if(al>0.5) tHit=min(tHit,tN); } }
  /* fruit bodies: a stem and a cap */
  for(int i=0;i<12;i++){ if(i>=uNM) break; vec4 m=uM1[i], m2=uM2[i]; float sz=m.z, H=(0.28+0.95*sz)*(1.-0.4*m2.y), rc=0.11+0.34*sz, rs=0.04+0.035*sz, rz=rc*mix(0.95,0.42,smoothstep(0.3,1.,sz))*(1.-0.3*m2.y);
    vec3 ro=vec3(uC.x-m.x-m.w*uC.z,uC.y-m.y,uC.z), rd=vec3(d.x-m.w*d.z,d.y,d.z);
    float A=dot(rd.xy,rd.xy), B=dot(ro.xy,rd.xy), Cq=dot(ro.xy,ro.xy)-rs*rs, hq=B*B-A*Cq;
    if(hq>0.){ float t=(-B-sqrt(hq))/A, z=ro.z+rd.z*t; if(z>0.&&z<H&&t<tHit){ vec2 nn=(ro.xy+rd.xy*t)/rs; vec3 N=vec3(nn,0.);
        vec3 sc=mix(vec3(0.80,0.74,0.56),vec3(0.42,0.30,0.16),m2.y)*(0.7+0.3*z/H); vec3 c=sc*(AMB*0.8+key*(0.2+0.8*max(dot(N,L),0.))*(0.45+0.55*smoothstep(H,H-rc*1.6,z)*0.+0.55*step(z,H-rc*0.9)));
        col=mix(col,c,smoothstep(0.,rs*0.5+blur*0.05,sqrt(hq)/A)); } }
    vec3 sv=vec3(1./rc,1./rc,1./rz), o2=(ro-vec3(0.,0.,H))*sv, d2=rd*sv; float a2=dot(d2,d2), b2=dot(o2,d2), c2=dot(o2,o2)-1., h2=b2*b2-a2*c2;
    if(h2>0.){ float t=(-b2-sqrt(h2))/a2; vec3 p=o2+d2*t; if(p.z>-0.3&&t<tHit){ vec3 N=normalize(p*sv); float rr=length(p.xy);
        vec3 cc=mix(vec3(0.36,0.13,0.03),vec3(0.66,0.43,0.10),smoothstep(0.05,0.9,rr)); cc=mix(cc,cc.grb*vec3(1.1,0.9,1.),0.25*(m2.x-0.5)); cc*=0.85+0.3*vnoise(p.xy*5.+m.x); cc=mix(cc,vec3(0.16,0.09,0.04),m2.y*0.8);
        vec3 V=-d; float df=max((dot(N,L)+0.25)/1.25,0.); vec3 c=cc*(AMB*(0.6+0.4*N.z)+key*df)+key*pow(max(dot(N,normalize(L+V)),0.),36.)*(0.06+0.2*uWet)*(1.-m2.y)+cc*key*0.22*pow(1.-max(dot(N,V),0.),2.);
        col=mix(col,c,smoothstep(0.,rc*0.3+blur*0.08,sqrt(h2)/a2)); } } }
  col*=1.-0.3*dot(vQ,vQ);
  gl_FragColor=vec4(tone(col*1.05)+(hash(gl_FragCoord.xy+uTime)-0.5)/255.,1.);
}`;
let prog = null, uni = {}, netTex = null, NET = small ? 1024 : 2048; const netCv = document.createElement('canvas'), netCx = netCv.getContext('2d');
function initGL() { const p = gl.createProgram(); [[gl.VERTEX_SHADER, VS], [gl.FRAGMENT_SHADER, FS]].forEach(([t, src]) => { const s = gl.createShader(t); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) console.error('shader: ' + gl.getShaderInfoLog(s)); gl.attachShader(p, s); });
  gl.linkProgram(p); if (!gl.getProgramParameter(p, gl.LINK_STATUS)) console.error('link: ' + gl.getProgramInfoLog(p)); prog = p; gl.useProgram(p);
  const q = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, q); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW); const a = gl.getAttribLocation(p, 'aQ'); gl.enableVertexAttribArray(a); gl.vertexAttribPointer(a, 2, gl.FLOAT, false, 0, 0);
  NET = Math.min(NET, gl.getParameter(gl.MAX_TEXTURE_SIZE)); netTex = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, netTex); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); }
const U = n => (n in uni ? uni[n] : (uni[n] = gl.getUniformLocation(prog, n)));
function setNet(n) { NET = n; netCv.width = netCv.height = n; fuzz = null; netDirty = true; netT = 9; }

/* ---------- the picture of the strands, redrawn a few times a second ---------- */
let fuzz = null, qref = 8;
const cordW = n => 0.026 * Math.sqrt(n);                                        /* cm: one hypha-strand to a millimetre cord */
function trace(c, e, k) { const q = e.pts; c.moveTo(q[0] * k, q[1] * k); for (let i = 2; i < q.length; i += 2) c.lineTo(q[i] * k, q[i + 1] * k); }
function drawNet() { const c = netCx, T = NET, k = T / P.W, E = W.edges; c.globalCompositeOperation = 'source-over'; c.fillStyle = '#000'; c.fillRect(0, 0, T, T); c.globalCompositeOperation = 'lighter'; c.lineCap = 'round'; c.lineJoin = 'round';
  if (!fuzz) { fuzz = document.createElement('canvas'); const r = Math.ceil(0.55 * k); fuzz.width = fuzz.height = 2 * r; const f = fuzz.getContext('2d'), gr = f.createRadialGradient(r, r, 0, r, r, r); gr.addColorStop(0, 'rgba(255,0,0,.11)'); gr.addColorStop(0.5, 'rgba(255,0,0,.05)'); gr.addColorStop(1, 'rgba(255,0,0,0)'); f.fillStyle = gr; f.fillRect(0, 0, 2 * r, 2 * r); }
  const lev = []; c.strokeStyle = 'rgba(255,0,0,.92)'; c.lineWidth = Math.max(1.25, 0.017 * k); c.beginPath();
  for (const e of E) { if (!e.alive) continue; trace(c, e, k); if (e.n > 1) (lev[e.n] || (lev[e.n] = [])).push(e); } c.stroke();
  c.strokeStyle = 'rgb(0,255,0)'; for (let n = 2; n < lev.length; n++) { if (!lev[n]) continue; c.lineWidth = Math.max(1.6, cordW(n) * k); c.beginPath(); for (const e of lev[n]) trace(c, e, k); c.stroke(); }
  const fr = fuzz.width / 2; for (const t of W.tips) if (t.alive && t.v > 0.02) c.drawImage(fuzz, t.x * k - fr, t.y * k - fr);
  for (const b of W.blocks) if (b.state === 'source' || b.state === 'col') { const s = (b.hw + 0.5) / 0.55 * (b.state === 'col' ? 0.7 : 1); c.drawImage(fuzz, (b.x - 0.55 * s) * k, (b.y - 0.55 * s) * k, 2 * fr * s, 2 * fr * s); }
  if (S.mode === 1) { let qm = 0; const bk = []; for (const e of E) { if (!e.alive) continue; const aq = Math.abs(e.Q); if (aq > qm) qm = aq; if (aq < 0.08) continue; const i = Math.min(4, Math.floor(Math.pow(Math.min(1, aq / qref), 0.55) * 5)), w = e.n < 3 ? 0 : e.n < 9 ? 1 : 2, j = i * 3 + w; (bk[j] || (bk[j] = [])).push(e); } qref += (Math.max(6, qm) - qref) * 0.2;
    for (let j = 0; j < 15; j++) { if (!bk[j]) continue; const i = (j / 3) | 0, w = j % 3; c.strokeStyle = 'rgba(0,0,255,' + (0.14 + 0.2 * i).toFixed(2) + ')'; c.lineWidth = Math.max(1.6, cordW([1.5, 5, 14][w]) * k * 1.25); c.beginPath(); for (const e of bk[j]) trace(c, e, k); c.stroke(); } }
  else if (S.mode === 2) { const bk = []; for (const e of E) { if (!e.alive || e.cU <= 0.02) continue; const i = Math.min(3, Math.floor(e.cU / P.Ub * 4)); (bk[i] || (bk[i] = [])).push(e); }
    for (let i = 0; i < 4; i++) { if (!bk[i]) continue; c.strokeStyle = 'rgba(0,0,255,' + (0.12 + 0.17 * i).toFixed(2) + ')'; c.lineWidth = Math.max(1.6, 0.03 * k); c.beginPath(); for (const e of bk[i]) trace(c, e, k); c.stroke(); } }
  if (gl) { gl.bindTexture(gl.TEXTURE_2D, netTex); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, netCv); gl.generateMipmap(gl.TEXTURE_2D); } }

/* ---------- sizes ---------- */
const c2 = { tip: $('tip'), chart: $('chart') }, x2 = {}; for (const k in c2) x2[k] = c2[k].getContext('2d');
let vw = 1, vh = 1;
function fit() { const r = cv.getBoundingClientRect(); vw = r.width; vh = r.height; camFit(vw / Math.max(1, vh)); cv.width = Math.max(2, Math.round(vw * DPR * qual)); cv.height = Math.max(2, Math.round(vh * DPR * qual)); ov.width = Math.round(vw * DPR); ov.height = Math.round(vh * DPR);
  for (const k in c2) { const b = c2[k].getBoundingClientRect(); c2[k].width = Math.round(b.width * DPR); c2[k].height = Math.round(b.height * DPR); } chartDirty = true; placeHand(); }
function placeHand() { const p = project(S.hand[0], S.hand[1], 0), b = $('hand'); b.style.left = (p[0] * 100) + '%'; b.style.top = (p[1] * 100) + '%'; }

/* ---------- draw the soil ---------- */
const fB1 = new Float32Array(24), fB2 = new Float32Array(24), fL1 = new Float32Array(32), fL2 = new Float32Array(32), fM1 = new Float32Array(48), fM2 = new Float32Array(48);
let drawCalls = 0;
function drawGL() { if (!gl) return; gl.viewport(0, 0, cv.width, cv.height);
  const wood = W.blocks.filter(b => b.kind === 'wood').sort((a, b) => b.y - a.y).slice(0, 6), lit = W.blocks.filter(b => b.kind === 'litter').slice(0, 8), fr = W.fruits.slice().sort((a, b) => b.y - a.y).slice(0, 12);
  wood.forEach((b, i) => { const white = b.state === 'new' ? 0 : b.state === 'col' ? 0.12 + 0.5 * b.col / b.colNeed : b.state === 'source' ? 0.5 : 0.36; fB1.set([b.x, b.y, b.rot, white], i * 4); fB2.set([b.hw, b.hh, 0.62 + 0.3 * b.seed, b.state === 'spent' ? 0.85 : b.state === 'source' ? 0.2 + 0.5 * (1 - b.S / b.S0) : 0], i * 4); });
  lit.forEach((b, i) => { fL1.set([b.x, b.y, b.rot, b.hw * 1.25], i * 4); fL2.set([b.state === 'new' ? 0 : b.state === 'col' ? 0.3 : b.state === 'source' ? 0.6 : 0.25, b.state === 'spent' ? 0.85 : b.state === 'source' ? 0.5 * (1 - b.S / b.S0) : 0, b.seed, 0], i * 4); });
  fr.forEach((f, i) => { fM1.set([f.x, f.y, Math.max(0.04, f.size), f.lean], i * 4); fM2.set([f.hue, f.state === 2 ? Math.min(1, (W.t - f.tM - P.fruitLife) / 4) : 0, 0, 0], i * 4); });
  gl.uniform4fv(U('uB1'), fB1); gl.uniform4fv(U('uB2'), fB2); gl.uniform4fv(U('uL1'), fL1); gl.uniform4fv(U('uL2'), fL2); gl.uniform4fv(U('uM1'), fM1); gl.uniform4fv(U('uM2'), fM2); gl.uniform1i(U('uNB'), wood.length); gl.uniform1i(U('uNL'), lit.length); gl.uniform1i(U('uNM'), fr.length);
  gl.uniform3fv(U('uC'), CAM.C); gl.uniform3fv(U('uF'), CAM.F); gl.uniform3fv(U('uR'), CAM.R); gl.uniform3fv(U('uU'), CAM.U); gl.uniform1f(U('uAsp'), CAM.asp); gl.uniform1f(U('uFoc'), CAM.foc); gl.uniform1f(U('uVoff'), CAM.voff);
  gl.uniform1f(U('uTime'), still ? 0 : S.time % 10); gl.uniform1f(U('uWet'), M.sm(0.15, 0.95, W.moisture)); gl.uniform1f(U('uMode'), S.mode); gl.uniform1f(U('uDof'), 5); gl.uniform1f(U('uFocT'), Math.hypot(CAM.C[0] - 10, CAM.C[1] - 8.6, CAM.C[2])); gl.uniform1f(U('uTx'), 1 / NET);
  gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, netTex); gl.uniform1i(U('uNet'), 0); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); drawCalls++; }

/* ---------- what is laid over the picture: moving food, the counts, your hand ---------- */
const flashes = []; let logSeen = 0;
function along(e, f) { const q = e.pts, n = q.length / 2 - 1, x = Math.max(0, Math.min(0.9999, f)) * n, i = Math.floor(x), t = x - i; return [q[2 * i] + (q[2 * i + 2] - q[2 * i]) * t, q[2 * i + 1] + (q[2 * i + 3] - q[2 * i + 1]) * t]; }
function drawOver(dt) { const c = ox, w = ov.width, h = ov.height, u = DPR; c.clearRect(0, 0, w, h); const px = (x, y, z) => { const p = project(x, y, z); return [p[0] * w, p[1] * h]; };
  if (!gl) { c.fillStyle = '#17110c'; c.fillRect(0, 0, w, h); c.lineCap = 'round'; const sc = w / 24;
    for (const b of W.blocks) { const col = b.kind === 'litter' ? '#7a5a1c' : b.state === 'new' ? '#6b4a26' : '#8d7a5e'; c.fillStyle = col; c.beginPath(); for (let i = 0; i < 4; i++) { const sx = (i === 0 || i === 3 ? -1 : 1) * b.hw, sy = (i < 2 ? -1 : 1) * b.hh, p = px(b.x + sx * Math.cos(b.rot) - sy * Math.sin(b.rot), b.y + sx * Math.sin(b.rot) + sy * Math.cos(b.rot), 0); if (i) c.lineTo(p[0], p[1]); else c.moveTo(p[0], p[1]); } c.fill(); }
    const lev = []; for (const e of W.edges) if (e.alive) { const j = Math.min(5, Math.floor(Math.sqrt(e.n))); (lev[j] || (lev[j] = [])).push(e); }
    for (let j = 1; j < lev.length; j++) { if (!lev[j]) continue; c.strokeStyle = j > 1 ? '#efe4c4' : 'rgba(255,253,248,.7)'; c.lineWidth = Math.max(u * 0.8, cordW(j * j) * sc); c.beginPath(); for (const e of lev[j]) { const q = e.pts; for (let i = 0; i < q.length; i += 2) { const p = px(q[i], q[i + 1], 0); if (i) c.lineTo(p[0], p[1]); else c.moveTo(p[0], p[1]); } } c.stroke(); }
    for (const f of W.fruits) { const p = px(f.x, f.y, 0.5); c.fillStyle = '#c98a1e'; c.fillRect(p[0] - 3 * u, p[1] - 3 * u, 6 * u, 6 * u); } }
  if (S.mode === 1) { c.fillStyle = 'rgba(255,214,120,.95)'; const sp = 0.55; let k = 0;                  /* parcels of food moving the way the flow goes */
    for (const e of W.edges) { if (!e.alive) continue; const aq = Math.abs(e.Q); if (aq < 0.25 || e.len < 0.2) continue; if (++k > 1400) break; const vel = Math.min(2.4, 0.5 + 0.9 * aq / e.n), ph = ((S.time * vel * (e.Q > 0 ? 1 : -1) + e.born * 7.3) % sp + sp) % sp, r = (0.8 + 0.22 * Math.sqrt(e.n)) * u;
      for (let s = ph; s < e.len; s += sp) { const g = along(e, s / e.len), p = px(g[0], g[1], 0.02); c.fillRect(p[0] - r, p[1] - r, 2 * r, 2 * r); } } }
  if (S.mode === 2) { c.lineWidth = 1.6 * u; c.lineCap = 'butt';                                         /* a ring at each tip fills as its count builds */
    for (const t of W.tips) { if (!t.alive) continue; const p = px(t.x, t.y, 0.02), r = 5.5 * u; c.strokeStyle = 'rgba(255,253,248,.22)'; c.beginPath(); c.arc(p[0], p[1], r, 0, 6.2832); c.stroke();
      c.strokeStyle = '#e0ae35'; c.beginPath(); c.arc(p[0], p[1], r, -1.5708, -1.5708 + 6.2832 * Math.min(1, t.C / P.Cb)); c.stroke();
      if (t.F > 0.02) { c.strokeStyle = '#7fe0cb'; c.beginPath(); c.arc(p[0], p[1], r * 0.55, -1.5708, -1.5708 + 6.2832 * Math.min(1, t.F / P.Fb)); c.stroke(); } }
    for (const b of W.blocks) { const f = b.state === 'col' ? b.col / b.colNeed : b.state === 'source' && b.kind === 'wood' ? b.cF / P.fruitF : 0; if (f <= 0) continue; const p = px(b.x, b.y, 0.9), r = 11 * u; c.strokeStyle = 'rgba(255,253,248,.25)'; c.beginPath(); c.arc(p[0], p[1], r, 0, 6.2832); c.stroke(); c.strokeStyle = b.state === 'col' ? '#fffdf8' : '#e0ae35'; c.beginPath(); c.arc(p[0], p[1], r, -1.5708, -1.5708 + 6.2832 * Math.min(1, f)); c.stroke(); } }
  const lg = W.log; while (logSeen < W.logN) { const i = lg.length - (W.logN - logSeen); if (i >= 0) flashes.push({ k: lg[i].k, x: lg[i].x, y: lg[i].y, a: 0 }); logSeen++; } if (flashes.length > 60) flashes.splice(0, flashes.length - 60);
  for (let i = flashes.length - 1; i >= 0; i--) { const f = flashes[i]; f.a += dt / 0.9; if (f.a >= 1) { flashes.splice(i, 1); continue; } if (S.mode !== 2 && f.k !== 'x') continue; const p = px(f.x, f.y, 0.02), col = f.k === 'f' ? '127,224,203' : f.k === 'x' ? '255,253,248' : '224,174,53';
    c.strokeStyle = 'rgba(' + col + ',' + (0.8 * (1 - f.a)).toFixed(3) + ')'; c.lineWidth = 1.2 * u; c.beginPath(); c.arc(p[0], p[1], (5 + 12 * f.a) * u, 0, 6.2832); c.stroke(); }
  const hv = S.hover || (document.activeElement === $('hand') ? S.hand : null);
  if (hv) { c.strokeStyle = 'rgba(255,253,248,.55)'; c.lineWidth = u; c.beginPath(); if (S.tool === 'wood') { [[-1.25, -0.85], [1.25, -0.85], [1.25, 0.85], [-1.25, 0.85]].forEach((q, i) => { const p = px(hv[0] + q[0], hv[1] + q[1], 0); if (i) c.lineTo(p[0], p[1]); else c.moveTo(p[0], p[1]); }); c.closePath(); }
    else for (let i = 0; i <= 24; i++) { const a = i / 24 * 6.2832, p = px(hv[0] + 0.45 * Math.cos(a), hv[1] + 0.45 * Math.sin(a), 0); if (i) c.lineTo(p[0], p[1]); else c.moveTo(p[0], p[1]); } c.stroke(); } }

/* ---------- at one tip ---------- */
const TP = { t: null, ves: [], buds: [], scroll: 0, side: -1, lastTC: 0, gone: 0, spawn: 0, pat: [] };
{ const r = M.rng(5); for (let i = 0; i < 16; i++) { const a = r() * 6.2832, d = Math.sqrt(r()); TP.pat.push([Math.cos(a) * d, Math.sin(a) * d]); } }
function pickTip() { let best = null; for (const t of W.tips) if (t.alive && (!best || t.I * (1 + t.C) > best.I * (1 + best.C))) best = t; return best; }
function drawTip(dt) { const c = x2.tip, w = c2.tip.width, h = c2.tip.height, u = DPR; let t = TP.t;
  if (t && !t.alive) { if (t.heir && t.heir.alive) { t = TP.t = t.heir; TP.buds.push({ x: 0.74 * w - h * 0.2, age: 0, side: TP.side }); TP.lastTC = t.tC; } else { TP.gone += dt; if (TP.gone > 0.9) { t = TP.t = null; } } }
  if (!t || (TP.t && !TP.t.alive && TP.gone > 0.9)) { t = TP.t = pickTip(); TP.gone = 0; TP.ves.length = 0; TP.buds.length = 0; if (t) TP.lastTC = t.tC; }
  const live = t && t.alive, cy = 0.47 * h, r = 0.135 * h, xt = 0.74 * w, I = live ? t.I : 0, v = live ? t.v : 0, frac = live ? Math.min(1, t.C / P.Cb) : 0;
  const gbg = c.createLinearGradient(0, 0, w, h); gbg.addColorStop(0, '#062a27'); gbg.addColorStop(1, '#0b3f38'); c.fillStyle = gbg; c.fillRect(0, 0, w, h);
  if (live) { const cr = Math.cos(t.th) * t.my - Math.sin(t.th) * t.mx; if (Math.abs(cr) > 1e-4) TP.side = cr > 0 ? -1 : 1; if (t.tC !== TP.lastTC) { TP.lastTC = t.tC; TP.buds.push({ x: xt - 3.6 * r, age: 0, side: TP.side }); } }
  const sp = still ? 0 : v / P.vmax * 0.1 * w * dt; TP.scroll += sp; const xs = xt - 3.6 * r, ys = cy + TP.side * 0.72 * r;
  const tube = () => { c.beginPath(); c.moveTo(-10, cy - r); c.lineTo(xt - 1.5 * r, cy - r); c.bezierCurveTo(xt - 0.5 * r, cy - r, xt, cy - 0.55 * r, xt, cy); c.bezierCurveTo(xt, cy + 0.55 * r, xt - 0.5 * r, cy + r, xt - 1.5 * r, cy + r); c.lineTo(-10, cy + r); c.closePath(); };
  const bud = (b, lw, col) => { const L = Math.min(1, b.age / 1.3) * 2.3 * r + Math.max(0, b.age - 1.3) * 0.25 * r; c.strokeStyle = col; c.lineWidth = lw; c.lineCap = 'round'; c.beginPath(); c.moveTo(b.x, cy + b.side * 0.4 * r); c.lineTo(b.x + L * 0.5, cy + b.side * (0.4 * r + L)); c.stroke(); };
  const wall = 'rgba(255,253,248,.82)', inner = '#0f4d45';
  for (let i = TP.buds.length - 1; i >= 0; i--) { const b = TP.buds[i]; b.age += dt; b.x -= sp; if (b.x < -4 * r) TP.buds.splice(i, 1); }
  if (live && t.near < P.rs) { const xo = xt + r * 1.1 + (t.near / P.rs) * 0.13 * w; c.strokeStyle = wall; c.lineWidth = 1.7 * r + 2.4 * u; c.lineCap = 'butt'; c.beginPath(); c.moveTo(xo, -5); c.lineTo(xo + 0.05 * w, h + 5); c.stroke(); c.strokeStyle = inner; c.lineWidth = 1.7 * r; c.beginPath(); c.moveTo(xo, -5); c.lineTo(xo + 0.05 * w, h + 5); c.stroke(); }
  for (const b of TP.buds) bud(b, 1.5 * r + 2.4 * u, wall); c.strokeStyle = wall; c.lineWidth = 2.4 * u; tube(); c.stroke(); for (const b of TP.buds) bud(b, 1.5 * r, inner); c.fillStyle = inner; tube(); c.fill();
  c.save(); tube(); c.clip();
  c.strokeStyle = 'rgba(255,253,248,.4)'; c.lineWidth = 1.2 * u; const gap = 0.62 * w; for (let x = ((-TP.scroll) % gap + gap) % gap - gap; x < xt - 4.5 * r; x += gap) { c.beginPath(); c.moveTo(x, cy - r); c.lineTo(x, cy - 0.22 * r); c.moveTo(x, cy + 0.22 * r); c.lineTo(x, cy + r); c.stroke(); c.fillStyle = 'rgba(223,243,230,.10)'; c.beginPath(); c.ellipse(x + 0.2 * w, cy - 0.1 * r, 0.07 * w, 0.55 * r, 0, 0, 6.2832); c.fill(); }
  /* parcels: made behind, carried forward. Their number follows the supply this tip is getting. */
  if (live && !still) { TP.spawn += dt * (5 + 46 * Math.min(1.6, I) / 1.6); const sur = Math.max(0, I - v * P.cLen) / Math.max(I, 1e-6); while (TP.spawn > 1) { TP.spawn -= 1; TP.ves.push({ x: -4, y: (Math.random() * 2 - 1) * 0.72 * r, s: Math.random() < sur, v: (0.28 + 0.14 * Math.random()) * w }); } }
  if (TP.ves.length > 160) TP.ves.splice(0, TP.ves.length - 160);
  for (let i = TP.ves.length - 1; i >= 0; i--) { const p = TP.ves[i], tx = p.s ? xs : xt - 0.8 * r, ty = p.s ? ys - cy : 0; p.x += p.v * dt; const k = M.sm(tx - 2.2 * r, tx, p.x), yy = cy + p.y * (1 - k) + ty * k; if (p.x >= tx) { TP.ves.splice(i, 1); continue; } c.fillStyle = p.s ? 'rgba(224,174,53,.9)' : 'rgba(223,243,230,.75)'; c.fillRect(p.x - 1.1 * u, yy - 1.1 * u, 2.2 * u, 2.2 * u); }
  if (live) { const n = Math.round(frac * 16); c.fillStyle = '#e0ae35'; for (let i = 0; i < n; i++) { const q = TP.pat[i]; c.beginPath(); c.arc(xs + q[0] * 0.5 * r, ys + q[1] * 0.26 * r, 1.7 * u, 0, 6.2832); c.fill(); }
    const pul = still ? 0 : 0.06 * Math.sin(S.time * 5); const g2 = c.createRadialGradient(xt - 0.8 * r, cy, 0, xt - 0.8 * r, cy, 0.62 * r); g2.addColorStop(0, 'rgba(255,246,214,' + (0.5 + 0.5 * Math.min(1, I / 0.8)).toFixed(2) + ')'); g2.addColorStop(0.45 + pul, 'rgba(224,174,53,.55)'); g2.addColorStop(1, 'rgba(224,174,53,0)'); c.fillStyle = g2; c.beginPath(); c.arc(xt - 0.8 * r, cy, 0.62 * r, 0, 6.2832); c.fill(); }
  c.restore();
  /* the count itself, as a line that fills */
  const bx0 = 0.05 * w, bx1 = 0.95 * w, by = h - 9 * u; c.strokeStyle = 'rgba(255,253,248,.25)'; c.lineWidth = u; c.beginPath(); c.moveTo(bx0, by); c.lineTo(bx1, by); c.moveTo(bx1, by - 4 * u); c.lineTo(bx1, by + 4 * u); c.stroke();
  c.strokeStyle = '#e0ae35'; c.lineWidth = 2.6 * u; c.beginPath(); c.moveTo(bx0, by); c.lineTo(bx0 + (bx1 - bx0) * frac, by); c.stroke();
  if (live && t.F > 0.01) { c.strokeStyle = '#7fe0cb'; c.lineWidth = 2 * u; c.beginPath(); c.moveTo(bx0, by - 6 * u); c.lineTo(bx0 + (bx1 - bx0) * Math.min(1, t.F / P.Fb), by - 6 * u); c.stroke(); }
  return live ? t : null; }

/* ---------- the whole net, day by day ---------- */
let chartDirty = true;
function sample() { const s = M.stats(W), wood = W.blocks.filter(b => b.kind === 'wood'); let eff = null, n = 0, sum = 0; for (let i = 1; i < wood.length; i++) if (wood[i].state !== 'new' && wood[0]) { sum += M.efficiency(W, wood[0], wood[i], 1e-6, effPo[i] && effPo[i].length >= W.p.length ? effPo[i] : (effPo[i] = new Float64Array(W.p.length))); n++; } if (n) eff = sum / n;
  series.push({ t: W.t, len: s.len, mat: s.mat, eff }); if (series.length > 720) { series = series.filter((_, i) => i % 2 === 0); } chartDirty = true; return s; }
function drawChart() { const c = x2.chart, w = c2.chart.width, h = c2.chart.height, u = DPR, l = 6 * u, r = w - 6 * u, top = 2 * u, bot = h - 16 * u, rows = [['thread', 'len', ' cm', 0], ['material', 'mat', '', 0], ['economy', 'eff', '%', 1]], rh = (bot - top) / 3; c.clearRect(0, 0, w, h);
  const t1 = Math.max(10, series.length ? series[series.length - 1].t : 0), X = t => l + (r - l) * t / t1; c.font = (11.5 * u) + 'px "IM Fell English SC", Georgia, serif'; c.textBaseline = 'alphabetic';
  rows.forEach((row, j) => { const y0 = top + j * rh + 15 * u, y1 = top + (j + 1) * rh - 5 * u; let mx = 0, last = null; for (const s of series) if (s[row[1]] != null) { mx = Math.max(mx, s[row[1]]); last = s[row[1]]; } mx = mx || 1;
    c.strokeStyle = '#d9cfae'; c.lineWidth = u; c.beginPath(); c.moveTo(l, y1); c.lineTo(r, y1); c.stroke();
    for (const m of marks) { c.strokeStyle = m.k === 'w' ? 'rgba(185,134,25,.7)' : 'rgba(20,32,42,.45)'; c.beginPath(); c.moveTo(X(m.t), y0); c.lineTo(X(m.t), y1); c.stroke(); }
    c.strokeStyle = '#0d7a70'; c.lineWidth = 1.4 * u; c.beginPath(); let pen = false; for (const s of series) { const v = s[row[1]]; if (v == null) { pen = false; continue; } const x = X(s.t), y = y1 - (y1 - y0) * v / mx; if (pen) c.lineTo(x, y); else { c.moveTo(x, y); pen = true; } } c.stroke();
    c.fillStyle = '#b98619'; c.textAlign = 'left'; c.fillText(row[0], l, y0 - 4 * u); c.fillStyle = '#14202a'; c.textAlign = 'right'; c.fillText(last == null ? 'no second piece of wood joined yet' : row[3] ? (last * 100).toFixed(1) + row[2] : Math.round(last).toLocaleString('en-GB') + row[2], r, y0 - 4 * u); });
  c.fillStyle = '#4d5a61'; c.textAlign = 'left'; c.fillText('day 0', l, h - 3 * u); c.textAlign = 'right'; c.fillText('day ' + t1.toFixed(0), r, h - 3 * u); }

/* ---------- words and numbers: every figure is read from the model ---------- */
const N0 = v => Math.round(v).toLocaleString('en-GB'), wetWord = m => m < 0.3 ? 'dry' : m < 0.55 ? 'damp' : m < 0.85 ? 'wet' : 'sodden';
let shown = {};
function readout(tipNow) { const s = M.stats(W); shown = s;
  $('rDay').innerHTML = s.t.toFixed(1) + '<small>one day passes in about ' + (1 / DPS).toFixed(0) + ' seconds</small>';
  $('rLen').innerHTML = N0(s.len) + ' cm<small>' + s.tips + ' growing tip' + (s.tips === 1 ? '' : 's') + '; ' + N0(s.cords) + ' cm is cord of four hyphae or more</small>';
  $('rLoop').innerHTML = N0(s.loops) + '<small>from ' + N0(s.fusions) + ' fusions; a tree would have none</small>';
  $('rFlow').innerHTML = s.qmax.toFixed(1) + '<small>units a day through it; ' + s.deliv.toFixed(1) + ' a day reaching the tips</small>';
  $('rWd').innerHTML = N0(s.withdrawn) + ' cm<small>' + (s.grown > 0 ? Math.round(100 * s.withdrawn / (s.grown + 1e-9)) : 0) + '% of the ' + N0(s.grown) + ' cm grown; ' + N0(s.recycled) + ' units returned</small>';
  $('rFr').innerHTML = s.fruits + '<small>standing now; ' + s.fruitStarts + ' cluster' + (s.fruitStarts === 1 ? '' : 's') + ' started' + (M.moistFruit(W.moisture) <= 0 ? '. Too dry for the count to build' : '') + '</small>';
  $('rCv').innerHTML = s.cvN >= 20 ? 'spread ' + s.cv.toFixed(2) + '<small>standard deviation over mean, measured over ' + N0(s.cvN) + ' intervals averaging ' + s.ivMean.toFixed(1) + ' days. The candidate value 0.159 is a proposal under test, shown only for comparison; nothing is tuned towards it</small>' : '&ndash;<small>fewer than 20 intervals so far (' + s.cvN + ')</small>';
  $('tipP').textContent = tipNow ? 'One tip, much enlarged. Parcels of wall material stream to the bright body at the apex. Those it cannot use gather behind, in gold. At a fixed number a branch begins there and the gathering starts again. This tip is getting ' + tipNow.I.toFixed(2) + ' units a day and growing ' + (tipNow.v * 10).toFixed(1) + ' mm a day.' : 'No tip is growing just now. Put down wood or cut a cord and new tips will start.';
  $('chartP').textContent = 'Material counts every hypha in a cord. Economy asks how well the first block is joined to the others for the material spent: all of it laid as one straight cord would score 100%. Gold lines mark wood put down, dark lines a cut.'; }

/* ---------- your hand ---------- */
let sayT = 0; function say(msg) { const e = $('say'); e.textContent = msg; e.style.display = msg ? 'block' : 'none'; sayT = msg ? 3.2 : 0; }
function actAt(x, y) { if (S.tool === 'wood') { const wood = W.blocks.filter(b => b.kind === 'wood'); if (wood.length >= 6) return say('There is room for six pieces of wood. Begin again for a clear floor.');
    if (M.edge(x, y) < 1.9) return say('Closer to the middle, please.'); if (W.blocks.some(b => Math.hypot(b.x - x, b.y - y) < (b.kind === 'wood' ? 2.7 : 1.5))) return say('Something is already lying there.');
    M.addBlock(W, x, y); marks.push({ t: W.t, k: 'w' }); say(''); } else { if (M.cut(W, x, y, 0.45)) marks.push({ t: W.t, k: 'x' }); } netDirty = true; netT = 9; chartDirty = true; }
const ground = e => { const r = cv.getBoundingClientRect(); return unproject((e.clientX - r.left) / r.width, (e.clientY - r.top) / r.height); };
let down = null;
cv.addEventListener('pointerdown', e => { down = { x: e.clientX, y: e.clientY, t: performance.now(), drag: false, last: ground(e) }; });
cv.addEventListener('pointermove', e => { if (e.pointerType === 'mouse') S.hover = ground(e); if (down && e.pointerType === 'mouse' && S.tool === 'cut' && (e.buttons & 1)) { const g = ground(e); if (Math.hypot(g[0] - down.last[0], g[1] - down.last[1]) > 0.3) { down.drag = true; actAt(g[0], g[1]); down.last = g; } } });
cv.addEventListener('pointerup', e => { if (down && !down.drag && Math.hypot(e.clientX - down.x, e.clientY - down.y) < 10 && performance.now() - down.t < 600) { const g = ground(e); S.hand = g; placeHand(); actAt(g[0], g[1]); } down = null; });
cv.addEventListener('pointerleave', () => { S.hover = null; }); cv.addEventListener('pointercancel', () => { down = null; });
$('hand').addEventListener('keydown', e => { const d = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, 1], ArrowDown: [0, -1] }[e.key]; if (d) { e.preventDefault(); const hx = S.hand[0] + d[0] * 0.5, hy = S.hand[1] + d[1] * 0.5; if (M.edge(hx, hy) > 0.5) S.hand = [hx, hy]; placeHand(); } });
$('hand').addEventListener('click', () => actAt(S.hand[0], S.hand[1]));
document.querySelectorAll('input[name=tool]').forEach(r => r.addEventListener('change', () => { if (r.checked) S.tool = r.value; }));
document.querySelectorAll('input[name=mode]').forEach(r => { if (+r.value === S.mode) r.checked = true; r.addEventListener('change', () => { if (r.checked) { S.mode = +r.value; netDirty = true; netT = 9; } }); });
$('wet').addEventListener('input', e => { W.moisture = +e.target.value; $('wetOut').textContent = wetWord(W.moisture); });
$('hold').addEventListener('click', () => { S.hold = !S.hold; $('hold').setAttribute('aria-pressed', S.hold ? 'true' : 'false'); });
$('again').addEventListener('click', () => begin(Math.floor(Math.random() * 1e6) + 1, still ? 24 : 4));

/* ---------- begin ---------- */
function begin(seed, days) { S.seed = seed; W = M.create({ seed, litter: 6, inoculum: [7.4, 9.4], moisture: +$('wet').value }); W.logN = 0; const push = W.log.push.bind(W.log); W.log.push = function (o) { W.logN++; return push(o); };
  if (!qs.has('bare')) M.addBlock(W, 14.3, 11.6, { rot: -0.45 }); series = []; marks = []; effPo = []; lastSample = -1; logSeen = 0; flashes.length = 0; TP.t = null; simAcc = 0;
  while (W.t < days) { M.step(W); if (W.t - lastSample >= 0.5) { lastSample = W.t; sample(); } } netDirty = true; netT = 9; chartDirty = true; }

/* ---------- loop ---------- */
let last = 0, visible = true, onScreen = true, slowN = 0, slowT = 0, tick = 9, tipNow = null;
function frame(now) { requestAnimationFrame(frame); if (!visible || !onScreen) { last = now; return; }
  const raw = (now - last) / 1000; last = now; const dt = Math.min(0.05, Math.max(0.001, raw)); S.time += dt;
  if (!S.hold) { simAcc += dt * DPS; let g = 0; while (simAcc >= P.dt && g++ < 4) { M.step(W); simAcc -= P.dt; netDirty = true; if (W.t - lastSample >= 0.5) { lastSample = W.t; sample(); } } if (simAcc > 0.1) simAcc = 0; }
  netT += dt; if (netDirty && netT > (qual < 0.8 || small ? 0.2 : 0.11)) { drawNet(); netDirty = false; netT = 0; }
  drawGL(); drawOver(dt); tipNow = drawTip(dt);
  if (sayT > 0) { sayT -= dt; if (sayT <= 0) say(''); }
  tick += dt; if (tick > 0.25) { tick = 0; readout(tipNow); if (chartDirty) { drawChart(); chartDirty = false; } }
  if (!lockQ && raw < 0.5) { slowT += raw; if (++slowN >= 50) { const avg = slowT / slowN; slowN = 0; slowT = 0; if (avg > 0.030 && qual > 0.5) { qual = Math.max(0.5, qual - 0.17); if (qual < 0.7 && NET > 1024) setNet(1024); fit(); } } } }

if (gl) initGL(); else $('nogl').style.display = 'block';
setNet(NET);
if (qs.has('wet')) $('wet').value = qs.get('wet'); $('wetOut').textContent = wetWord(+$('wet').value);
if (S.hold) $('hold').setAttribute('aria-pressed', 'true');
fit(); begin(S.seed, qs.has('t') ? +qs.get('t') : still ? 24 : 4);
document.addEventListener('visibilitychange', () => { visible = !document.hidden; });
if ('IntersectionObserver' in window) new IntersectionObserver(es => { onScreen = es.some(e => e.isIntersecting); }, { rootMargin: '80px' }).observe(document.querySelector('.stage'));
let rz = 0; addEventListener('resize', () => { clearTimeout(rz); rz = setTimeout(fit, 120); });
if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { chartDirty = true; });
requestAnimationFrame(t => { last = t; frame(t); });
window.MYCPAGE = { S, CAM, project, unproject, actAt, fit, get W() { return W; }, get shown() { return shown; }, get series() { return series; }, get qual() { return qual; }, get drawCalls() { return drawCalls; }, get net() { return netCv; }, step(n) { for (let i = 0; i < n; i++) M.step(W); netDirty = true; netT = 9; } };
})();
