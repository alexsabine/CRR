# "The Wall and the Beach". Usage: film6.py <t0> <t1>. Line, traces and ruler sweep are read from maths.json (our own simulation); study figures are from the DG ruler note.
import numpy as np, json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from multiprocessing import Pool
S=os.path.dirname(os.path.abspath(__file__)); FD='/tmp/claude-0/-home-user/1edd5cc0-6987-5771-b57b-68d2ef3dbc39/scratchpad/clips/package/files/'
IT=lambda s: ImageFont.truetype(FD+'im-fell-english-latin-400-italic.woff',int(s)); RG=lambda s: ImageFont.truetype(FD+'im-fell-english-latin-400-normal.woff',int(s))
W,H,FPS,Q=1280,720,24,2
INK=(20,32,42); PAPER=(255,253,248); GOLD=(232,180,60); DGOLD=(176,128,20); VIR=(13,122,112); WARM=(200,72,44); HAIR=(217,207,174); SOFT=(84,90,94)
TM=json.load(open(S+'/timing.json')); CUES=TM['cues']; TOTAL=TM['total']; N_=json.load(open(S+'/script.json')); BASE={}; k_=0
for ch in N_: BASE[ch['id']]=k_; k_+=len(ch['text'])
cue=lambda sec,i: CUES[BASE[sec]+i][0]; CE=lambda sec,i: CUES[BASE[sec]+i][1]
ez=lambda u: (lambda v: v*v*(3-2*v))(min(1.,max(0.,u))); lerp=lambda a,b,u: a+(b-a)*u
def ramp(t,a,b): return ez((t-a)/(b-a)) if b>a else float(t>=a)
def win(t,a,b,f=.6): return ramp(t,a,a+f)*(1-ramp(t,b-f,b))
M=json.load(open(S+'/maths.json'))
_PP=None
def canvas():
    global _PP
    if _PP is None:
        yy,xx=np.mgrid[0:H*Q,0:W*Q].astype(np.float32); v=1-.10*(((xx/(W*Q)-.5)**2+(yy/(H*Q)-.5)**2)*1.6); g=np.random.default_rng(2).normal(0,1.6,(H*Q,W*Q,1)).astype(np.float32)
        _PP=Image.fromarray(np.clip(np.array(PAPER,np.float32)[None,None,:]*v[:,:,None]+g,0,255).astype(np.uint8))
    return _PP.copy()
D=lambda im: ImageDraw.Draw(im,'RGBA'); fin=lambda im: im.resize((W,H),Image.LANCZOS).convert('RGB')
A_=lambda a: int(255*min(1,max(0,a)))
def ln(d,pts,col,a=1.,w=4):
    if a>.02 and len(pts)>1: d.line([(x*Q,y*Q) for x,y in pts],fill=col+(A_(a),),width=max(1,int(round(w*Q))),joint='curve')
def pg(d,pts,col,a=1.):
    if a>.01: d.polygon([(x*Q,y*Q) for x,y in pts],fill=col+(A_(a),))
def dot(d,x,y,r,col,a=1.):
    if a>.02: d.ellipse([(x-r)*Q,(y-r)*Q,(x+r)*Q,(y+r)*Q],fill=col+(A_(a),))
def rect(d,x0,y0,x1,y1,col,a=1.,r=0,outline=None,w=2):
    if a>.02: d.rounded_rectangle([x0*Q,y0*Q,x1*Q,y1*Q],radius=r*Q,fill=(col+(A_(a),)) if col else None,outline=(outline+(A_(a),)) if outline else None,width=int(w*Q))
def tx(d,x,y,s,size,col=INK,a=1.,anchor='la',f=IT):
    if a>.02: d.multiline_text((x*Q,y*Q),s,font=f(size*Q),fill=col+(A_(a),),anchor=anchor,align='center' if anchor[0]=='m' else 'left',spacing=6*Q)
NUM=lambda s: ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf',int(s))
def note(d,s,a=1.): tx(d,40,560,s,21,SOFT,a,'ld')
def cite(d,s,a=1.): tx(d,W-40,560,s,21,SOFT,a,'rd')

NIGHT=(18,24,38); PALE=(241,223,174); SEA=(60,128,132); SAND=(236,214,160)
_PH=None
def photo(zoom=1.,cx=.5,cy=.5,warm=0.,grey=0.):
    """The owner's photograph (children softened), cropped to the screen's shape; zoom about a point given as a fraction of the frame."""
    global _PH
    if _PH is None: _PH=Image.open(S+'/wall-soft.jpg').convert('RGB').crop((0,180,1436,988))
    w,h=_PH.size; vw=w/zoom; vh=h/zoom; x0=min(max(cx*w-vw/2,0),w-vw); y0=min(max(cy*h-vh/2,0),h-vh)
    im=_PH.transform((W*Q,H*Q),Image.EXTENT,(x0,y0,x0+vw,y0+vh),Image.BICUBIC)
    if grey>0 or warm>0:
        a=np.asarray(im,np.float32); g=a.mean(2,keepdims=True); a=a+(g-a)*grey; a=a*(1-warm)+a*np.array([1.10,1.0,.84],np.float32)*warm; im=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
    return im,(x0,y0,vw,vh)
def P(pt,view):
    """A point given in the photograph's own pixels, as a place on the screen."""
    x0,y0,vw,vh=view; return ((pt[0]-x0)/vw*W,(pt[1]-180-y0)/vh*H)
def tab(d,x,y,s,size=26,a=1.,col=INK,f=IT,anchor='la',pad=11):
    if a<=.02: return
    b=d.textbbox((x*Q,y*Q),s,font=f(size*Q),anchor=anchor,spacing=6*Q); p=pad*Q
    d.rectangle([b[0]-p+3*Q,b[1]-p+4*Q,b[2]+p+3*Q,b[3]+p+4*Q],fill=(20,14,8,int(60*a))); d.rectangle([b[0]-p,b[1]-p,b[2]+p,b[3]+p],fill=PAPER+(int(244*a),)); d.rectangle([b[0]-p,b[3]+p-3*Q,b[2]+p,b[3]+p],fill=GOLD+(A_(a),))
    d.multiline_text((x*Q,y*Q),s,font=f(size*Q),fill=col+(A_(a),),anchor=anchor,spacing=6*Q)
def arrow(d,p,q,col,a=1.,w=3.5,u=1.,head=13):
    if a<=.02 or u<=0: return
    p=np.array(p,float); q=np.array(q,float); e=p+(q-p)*min(1.,u); v=q-p; v/=max(1e-6,np.linalg.norm(v)); pv=np.array([-v[1],v[0]]); ln(d,[tuple(p),tuple(e-v*head*.5)],col,a,w)
    pg(d,[tuple(e),tuple(e-v*head+pv*head*.5),tuple(e-v*head-pv*head*.5)],col,a)
DOTS=[(968,338),(1016,392),(1086,366),(1104,452),(1190,506),(1052,528),(1256,566)]      # seven moments, placed on the sand of the photograph
ORD_A=[0,1,2,3,5,4,6]; ORD_B=[2,0,1,5,3,6,4]
def spark(d,x,y,r,a=1.,col=GOLD):
    if a<=.02: return
    dot(d,x,y,r*2.6,col,a*.22); dot(d,x,y,r*1.5,col,a*.5); dot(d,x,y,r,(255,246,214),a)
def thread(d,pts,u,col,a=1.,w=3):
    if a<=.02 or u<=0 or len(pts)<2: return
    L_=(len(pts)-1)*min(1.,u); out=[pts[0]]
    for k in range(1,len(pts)):
        if L_>=k: out.append(pts[k])
        elif L_>k-1: f=L_-(k-1); out.append((lerp(pts[k-1][0],pts[k][0],f),lerp(pts[k-1][1],pts[k][1],f)))
    ln(d,out,col,a,w)
def kid(d,x,y,s,col,a=1.,lean=0.):
    if a<=.02: return
    dot(d,x+2,y+2,s*.34,(60,50,30),a*.12); body=[(x-s*.26,y),(x-s*.30+lean*4,y-s*.52),(x-s*.16+lean*7,y-s*.70),(x+s*.16+lean*7,y-s*.70),(x+s*.30+lean*4,y-s*.52),(x+s*.26,y)]
    pg(d,body,col,a); dot(d,x+lean*9,y-s*.88,s*.19,col,a); dot(d,x+lean*9-s*.05,y-s*.93,s*.07,tuple(min(255,int(c+(255-c)*.4)) for c in col),a*.6)
KC=[(60,104,204),(200,72,44),(13,122,112),(176,128,20),(90,96,110),(150,70,120)]
# ---------------- scenes ----------------
def sc_title(t):
    im=canvas(); d=D(im); a=win(t,.8,cue('w1',0)-.5,.9); tx(d,W/2,236,'The Wall and the Beach',66,INK,a,'ma',RG); ln(d,[(W/2-150,326),(W/2+150,326)],GOLD,a,2.5); tx(d,W/2,342,'on doing, remembering and dreaming',28,SOFT,a,'ma'); return fin(im)
def sc_wall1(t):
    c0=cue('w1',0); u=ramp(t,c0-.6,cue('w2',0)); im,v=photo(1.+.07*u,.56,.5); d=D(im)
    tab(d,44,54,'looking on',30,ramp(t,cue('w1',1)-.2,cue('w1',1)+.6)); tab(d,44,112,'all of it at once, and out of reach',22,ramp(t,cue('w1',1)+2.6,cue('w1',1)+3.4),SOFT)
    f=1-ramp(t,c0-.6,c0+.5)
    if f>.01: d.rectangle([0,0,W*Q,H*Q],fill=PAPER+(A_(f),))
    return fin(im)
KICKS=None
def beach_model():
    """The game on the sand, worked out once: a ball passed between six children, with a spark left at each kick."""
    global KICKS
    if KICKS is None:
        r=np.random.default_rng(4); t0=cue('w2',0)+.6; t1=cue('r1',0)-.9; ks=[]; who=0; t=t0+.7
        while t<t1-1.2: nxt=int((who+r.integers(1,5))%6); dur=float(r.uniform(.95,1.45)); ks.append((t,who,nxt,dur)); who=nxt; t+=dur
        KICKS=ks
    return KICKS
def kx(i,t): return 170+i*178+10*np.sin(t*1.3+i*2.1)
def sc_beach(t):
    im=canvas(); d=D(im); c0=cue('w2',0); a=ramp(t,c0-.5,c0+.5)*(1-ramp(t,cue('r1',0)-1.1,cue('r1',0)-.4)); hz=232; gy=470
    pg(d,[(0,0),(W,0),(W,hz),(0,hz)],(232,238,236),a*.9)
    for k in range(7):                                                     # the sea: bands that slide and swell
        y=hz+8+k*20; pts=[(x,y+5*np.sin(x*.012+t*(1.1+.12*k)+k*1.7)+2.5*np.sin(x*.031-t*1.7+k)) for x in range(0,W+20,20)]; pg(d,pts+[(W,y+34),(0,y+34)],tuple(int(lerp(c,p,.18*k)) for c,p in zip(SEA,(214,232,226))),a*.92)
    sy=hz+150; shore=[(x,sy+7*np.sin(x*.008+t*.9)+4*np.sin(x*.021-t*1.3)) for x in range(0,W+20,20)]; pg(d,shore+[(W,600),(0,600)],SAND,a); ln(d,shore,(255,253,244),a*.9,3)
    ks=beach_model(); bx,by=kx(0,t),gy-14; sparks=[]
    for (tk,i,j,dur) in ks:
        if t>=tk: sparks.append((kx(i,tk)+24,gy+10+12*((i*37)%5-2),t-tk))
        if tk<=t<tk+dur: u=(t-tk)/dur; bx=lerp(kx(i,tk)+20,kx(j,tk+dur)-20,u); by=gy-14-150*4*u*(1-u)*min(1.,abs(j-i)/2.2+.35)
        elif t>=tk+dur: bx,by=kx(j,t)-20,gy-14
    for (x,y,age) in sparks: spark(d,x,y,5.5,a*(.55+.45*np.exp(-age*.6)))
    for i in range(6):
        act=max([np.exp(-abs(t-tk)*5) for (tk,ii,jj,du) in ks if ii==i]+[0]); kid(d,kx(i,t),gy+6*np.sin(i*1.7),96+8*((i*5)%3),KC[i],a,lean=.5*act+.12*np.sin(t*2+i))
    dot(d,bx+3,gy+4,11,(60,50,30),a*.13*max(.3,1-(gy-by)/170)); dot(d,bx,by,13,(250,246,238),a); d.ellipse([(bx-13)*Q,(by-13)*Q,(bx+13)*Q,(by+13)*Q],outline=INK+(A_(a),),width=int(2*Q)); dot(d,bx-4,by-4,4,WARM,a)
    tab(d,44,54,'in it',30,a*ramp(t,cue('w2',1)-.2,cue('w2',1)+.6)); tab(d,44,112,'no view of the whole, and everything within reach',22,a*ramp(t,cue('w2',1)+5.4,cue('w2',1)+6.2),SOFT)
    tab(d,44,160,'nobody here knows how the day will end',22,a*ramp(t,cue('w2',2)+.2,cue('w2',2)+1.),SOFT)
    return fin(im)

WOODC=None
def wood():
    """A table top: long grain drawn from stretched noise, a little darker toward the edges."""
    global WOODC
    if WOODC is None:
        r=np.random.default_rng(12); h,w=H*Q//4,W*Q//64; n=r.normal(0,1,(h,w)).astype(np.float32); g=np.asarray(Image.fromarray(n).resize((W*Q,H*Q),Image.BICUBIC)); f=r.normal(0,1,(H*Q//2,W*Q//2)).astype(np.float32); f=np.asarray(Image.fromarray(f).resize((W*Q,H*Q),Image.BILINEAR))
        yy,xx=np.mgrid[0:H*Q,0:W*Q].astype(np.float32); band=np.sin(yy*.011+g*1.6)*.5+.5; v=1-.30*(((xx/(W*Q)-.5)**2+(yy/(H*Q)-.5)**2)*2.0)
        base=np.array([150,104,62],np.float32)[None,None,:]*(0.78+.24*band[:,:,None]+.05*g[:,:,None]+.02*f[:,:,None]); WOODC=Image.fromarray(np.clip(base*v[:,:,None],0,255).astype(np.uint8))
    return WOODC.copy()
import jig as JG
_PC={}; _SRC=None
def piece(k,scale,ang,tint=None):
    key=(k,round(scale,3),tint)
    if key not in _PC:
        if 'raw' not in _PC: _PC['raw']=[Image.open(f'{S}/jig/{i:02d}.png').convert('RGBA') for i in range(24)]
        p=_PC['raw'][k]
        if tint is not None: a_=np.asarray(p,np.float32).copy(); g_=a_[:,:,:3].mean(2,keepdims=True); a_[:,:,:3]=np.clip((a_[:,:,:3]*.35+g_*.65)*np.array(tint,np.float32),0,255); p=Image.fromarray(a_.astype(np.uint8),'RGBA')
        _PC[key]=p.resize((max(2,int(p.width*scale*Q)),max(2,int(p.height*scale*Q))),Image.LANCZOS)
    p=_PC[key]
    return p.rotate(ang,Image.BICUBIC,expand=True) if abs(ang)>.3 else p
def put_piece(im,k,cx,cy,ang,scale,a=1.,lift=0.,tint=None):
    if a<=.02: return
    p=piece(k,scale,ang,tint); al=p.getchannel('A'); sh=Image.new('RGBA',p.size,(20,12,6,0)); sh.putalpha(al.point(lambda v:int(v*.42*a))); off=int((5+16*lift)*Q); x=int(cx*Q-p.width/2); y=int(cy*Q-p.height/2)
    im.paste(sh,(x+off,y+off),sh.filter(ImageFilter.GaussianBlur(3+8*lift)))
    if a<.99: p=p.copy(); p.putalpha(al.point(lambda v:int(v*a)))
    im.paste(p,(x,y),p)
def home(k,ox,oy,sc): i,j=k%6,k//6; return (ox+(i+.5)*200*sc,oy+(j+.5)*200*sc)
SCAT=None
def scatter():
    global SCAT
    if SCAT is None: r=np.random.default_rng(21); SCAT=[(r.uniform(90,720),r.uniform(120,520),r.uniform(-70,70)) for _ in range(24)]
    return SCAT
def lid(im,d,x,y,w,a=1.,lab=True):
    """The box lid: the whole picture, with a rim."""
    global _SRC
    if a<=.02: return
    if _SRC is None: _SRC=Image.open(S+'/wall-soft.jpg').convert('RGB').crop((118,180,1318,980))
    h=int(w*2/3); sh=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh).rectangle([(x-4)*Q,(y+2)*Q,(x+w+22)*Q,(y+h+26)*Q],fill=(20,12,6,int(120*a))); im.paste(sh,(0,0),sh.filter(ImageFilter.GaussianBlur(10*Q//2)))
    d.rectangle([(x-12)*Q,(y-12)*Q,(x+w+12)*Q,(y+h+12)*Q],fill=(246,240,226,A_(a))); pic=_SRC.resize((w*Q,h*Q),Image.LANCZOS)
    if a<.99: m=Image.new('L',pic.size,int(255*a)); im.paste(pic,(x*Q,y*Q),m)
    else: im.paste(pic,(x*Q,y*Q))
    d.rectangle([(x-12)*Q,(y-12)*Q,(x+w+12)*Q,(y+h+12)*Q],outline=(120,84,50,A_(a)),width=int(2*Q))
def sc_wall2(t):
    c=[cue('w3',i) for i in range(2)]; u=ramp(t,c[0]-.6,cue('r2',0)); im,v=photo(1.12+.10*u,.74,.46,grey=.35*ramp(t,c[0],c[0]+3)); d=D(im); a=1-ramp(t,cue('r2',0)-1.1,cue('r2',0)-.4)
    pts=[P(p,v) for p in DOTS]
    for k,p in enumerate(pts): spark(d,p[0],p[1],6.5,a*ramp(t,c[1]+.3+k*.35,c[1]+.7+k*.35))
    tab(d,44,54,'looking back',30,a*ramp(t,c[0]+2.6,c[0]+3.4))
    g=a*ramp(t,c[1]+3.4,c[1]+4.2)
    if g>.02:
        y=556; d.rectangle([40*Q,(y-44)*Q,1240*Q,(y+30)*Q],fill=PAPER+(int(236*g),)); arrow(d,(70,y),(1200,y),INK,g,3,ramp(t,c[1]+3.6,c[1]+6.0)); tx(d,1206,y-30,'time',22,SOFT,g,'rs')
        ln(d,[(300,y-10),(300,y+10)],DGOLD,g,3); ln(d,[(640,y-10),(640,y+10)],DGOLD,g,3); ln(d,[(300,y),(640,y)],GOLD,g,7); tx(d,470,y-34,'the day on the beach',22,DGOLD,g,'ma')
        k=ramp(t,c[1]+8.0,c[1]+8.8); dot(d,1010,y,8,WARM,g*k); tx(d,1010,y-34,'now, on the wall',22,WARM,g*k,'ma'); arrow(d,(990,y-58),(660,y-58),WARM,g*ramp(t,c[1]+10.,c[1]+10.6)*.9,2.4,ramp(t,c[1]+10.,c[1]+11.6))
    return fin(im)
def bighouse(d,x,y,a,inside,t,dim=1.):
    if a<=.02: return
    w,h=380,220; A=a*dim
    if inside:
        d.rectangle([x*Q,y*Q,(x+w)*Q,(y+h)*Q],fill=(250,246,234,A_(A)),outline=INK+(A_(A),),width=int(3*Q)); cxp=x+170+80*np.sin(t*1.2)
        d.rectangle([(x+250)*Q,(y+30)*Q,(x+340)*Q,(y+110)*Q],fill=(214,226,232,A_(A)),outline=INK+(A_(A),),width=int(2*Q)); ln(d,[(x+295,y+30),(x+295,y+110)],INK,A,2); ln(d,[(x+250,y+70),(x+340,y+70)],INK,A,2)
        pg(d,[(cxp,y+h-6),(cxp,y+h-62),(cxp+10,y+h-62),(cxp+10,y+h-108),(cxp+20,y+h-108),(cxp+20,y+h-62),(cxp+56,y+h-62),(cxp+56,y+h-6),(cxp+46,y+h-6),(cxp+46,y+h-48),(cxp+10,y+h-48),(cxp+10,y+h-6)],DGOLD,A)
        kid(d,cxp-52,y+h-6,150,(60,104,204),A,lean=.2)
    else:
        pg(d,[(x,y),(x+w,y),(x+w,y+h),(x,y+h)],(232,226,208),A); pg(d,[(x-26,y),(x+w/2,y-120),(x+w+26,y)],WARM,A*.92); ln(d,[(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)],INK,A,3); ln(d,[(x-26,y),(x+w/2,y-120),(x+w+26,y)],INK,A,3)
        d.rectangle([(x+52)*Q,(y+52)*Q,(x+152)*Q,(y+142)*Q],fill=(214,226,232,A_(A)),outline=INK+(A_(A),),width=int(2.4*Q)); cxp=x+74; pg(d,[(cxp,y+140),(cxp,y+112),(cxp+5,y+112),(cxp+5,y+90),(cxp+11,y+90),(cxp+11,y+112),(cxp+30,y+112),(cxp+30,y+140)],DGOLD,A*.4)
        d.rectangle([(x+236)*Q,(y+92)*Q,(x+302)*Q,(y+h)*Q],fill=(120,84,50,A_(A)),outline=INK+(A_(A),),width=int(2.4*Q)); pg(d,[(x+250,y-70),(x+250,y-150),(x+290,y-150),(x+290,y-40)],(170,90,70),A); kid(d,x+w+92,y+h,150,(60,104,204),A)
def sc_house(t):
    im=canvas(); d=D(im); c=[cue('h1',i) for i in range(3)]; a=ramp(t,c[0]-.5,c[0]+.5)*(1-ramp(t,cue('p1',0)-1.1,cue('p1',0)-.4)); both=ramp(t,c[2]-.2,c[2]+.6)
    o=ramp(t,c[0]-.2,c[0]+.8); i_=ramp(t,c[1]-.3,c[1]+.6); x1=lerp(430,720,i_)
    tx(d,48,56,'Outside and inside',33,INK,a,'ls')
    bighouse(d,lerp(-420,84,i_) ,290,a*i_,True,t); bighouse(d,x1,290,a*o,False,t,dim=1.)
    tx(d,x1+190,532,'outside: the whole shape',25,WARM,a*o,'ma'); tx(d,x1+190,566,'you cannot move the chair',22,SOFT,a*ramp(t,CE('h1',0)-2.,CE('h1',0)-1.2),'ma')
    tx(d,274,532,'inside: you can move the chair',25,VIR,a*i_,'ma'); tx(d,274,566,'you have lost the shape',22,SOFT,a*ramp(t,CE('h1',1)-1.6,CE('h1',1)-.8),'ma')
    tx(d,W/2,118,'nobody gets both at once',30,DGOLD,a*both,'ma',RG)
    return fin(im)
def sc_puzzle(t):
    im=wood(); d=D(im); c=[cue('p1',i) for i in range(4)]; a=ramp(t,c[0]-.5,c[0]+.5); out=1-ramp(t,cue('q1',0)-1.1,cue('q1',0)-.4); sc_=.34; ox,oy=120,170; SC=scatter()
    hand=ramp(t,CE('p1',0)-3.0,CE('p1',0)-2.0)*(1-ramp(t,c[2]-.6,c[2])); K=4
    asm=ramp(t,c[2]+3.0,c[2]+7.5); alt=ramp(t,CE('p1',2)-3.2,CE('p1',2)-1.0); bright=[2,4,9,15,17,22,10]; swap={9:10,10:9,2:17,17:2}
    for k in range(24):
        sx,sy,sa=SC[k]; hx,hy=home(k,ox,oy,sc_); u=ez(asm) if k in bright else 0.; x,y,an=lerp(sx,hx,u),lerp(sy,hy,u),sa*(1-u)
        if k in swap and alt>0: tx_,ty_=home(swap[k],ox,oy,sc_); lf=np.sin(np.pi*alt); x,y=lerp(x,tx_,ez(alt)),lerp(y,ty_,ez(alt))-34*lf
        if k==K and hand>0: x,y,an=lerp(x,560,ez(hand)),lerp(y,300,ez(hand)),an*(1-ez(hand)); put_piece(im,k,x,y,an,lerp(sc_,.86,ez(hand)),a*out,lift=ez(hand)); continue
        put_piece(im,k,x,y,an,sc_,a*out*(1. if (k in bright or asm<.05) else lerp(1.,.45,ramp(t,c[2],c[2]+2))))
        if k in bright and c[2]<t and asm<1: gx,gy=x,y; dot(d,gx,gy,40,GOLD,a*out*.20*ramp(t,c[2]+.6,c[2]+1.8)*(1-asm))
    lid(im,d,860,150,330,a*out*ramp(t,c[0]+2.6,c[0]+3.6))
    tab(d,860,400,'the lid: the whole picture',22,a*out*ramp(t,c[0]+3.4,c[0]+4.2),INK); tab(d,440,480,'in your hand: one piece',22,a*out*hand,INK)
    tab(d,44,54,'living is the pieces',28,a*out*win(t,c[1]-.1,c[2]-.3,.5),VIR); tab(d,860,96,'remembering is the lid',28,a*out*ramp(t,c[1]+1.9,c[1]+2.6),WARM,anchor='la')
    tab(d,44,54,'made again from a few bright pieces',26,a*out*win(t,c[2]+2.6,c[3]-.3,.6),INK); tab(d,44,104,'and a little different each time',22,a*out*win(t,CE('p1',2)-3.2,c[3]-.3,.6),SOFT)
    if a*out*win(t,c[2]+3.4,c[3]-.4,.6)>.02: tab(d,W-44,560,'memory is rebuilt, not replayed · Schacter & Addis, 2007',19,a*out*win(t,c[2]+3.4,c[3]-.4,.6),SOFT,anchor='rd')
    k=ramp(t,c[3]-.2,c[3]+.6)*out
    if k>.02:
        x0,y0=44,150; d.rectangle([x0*Q,y0*Q,(x0+520)*Q,(y0+214)*Q],fill=PAPER+(int(250*k),)); d.rectangle([x0*Q,(y0+210)*Q,(x0+520)*Q,(y0+214)*Q],fill=GOLD+(A_(k),))
        q1=ramp(t,c[3]+3.,c[3]+3.8); q2=ramp(t,c[3]+5.6,c[3]+6.4)
        tx(d,x0+26,y0+26,'understood backwards',34,VIR,k*q1,'la',RG); arrow(d,(x0+478,y0+92),(x0+30,y0+92),VIR,k*q1,3.5,ramp(t,c[3]+3.2,c[3]+4.4))
        tx(d,x0+26,y0+108,'lived forwards',34,WARM,k*q2,'la',RG); arrow(d,(x0+30,y0+172),(x0+478,y0+172),WARM,k*q2,3.5,ramp(t,c[3]+5.8,c[3]+7.))
        tx(d,x0+26,y0+184,'Kierkegaard, Journals, 1843',18,SOFT,k,'la')
    f=1-ramp(t,c[0]-.5,c[0]+.4)
    if f>.01: d.rectangle([0,0,W*Q,H*Q],fill=PAPER+(A_(f),))
    if out<.99: d.rectangle([0,0,W*Q,H*Q],fill=PAPER+(A_(1-out),))
    return fin(im)
def sc_story(t):
    im=canvas(); d=D(im); c=[cue('s1',i) for i in range(5)]; a=ramp(t,c[0]-.5,c[0]+.5)*(1-ramp(t,cue('a1',0)-1.1,cue('a1',0)-.4))
    # 0. a day is one piece; so is a year; so is a life
    s0=a*(1-ramp(t,c[1]-.6,c[1])); z1=ramp(t,c[0]+3.0,c[0]+4.6); z2=ramp(t,c[0]+5.6,c[0]+7.4)
    if s0>.02:
        tx(d,48,56,'Step further back',33,INK,s0,'ls'); y=320
        spark(d,lerp(W/2,300,ez(z1)),y,lerp(16,5,ez(z1)),s0*(1-.0*z1)); tx(d,W/2,y+40,'a day',26,DGOLD,s0*(1-ramp(z1,0,.3)),'ma')
        if z1>0:
            for k in range(52): x=300+k*13*ez(z1); spark(d,x,lerp(y,y,1),lerp(5,2.2,ez(z2)),s0*z1*(1 if k else 0)) if z2<.02 else None
            tx(d,300+26*13,y+40,'a year',26,DGOLD,s0*ramp(z1,.6,1.)*(1-ramp(z2,0,.3)),'ma')
        if z2>0:
            pts=[(120+k*13.4,y+70*np.sin(k*.09)*ez(z2)-40*np.sin(k*.031+1)*ez(z2)) for k in range(80)]; ln(d,pts,GOLD,s0*z2,3)
            for k in range(0,80,1): dot(d,pts[k][0],pts[k][1],2.6,DGOLD,s0*z2)
            tx(d,W/2,y+130,'a life',26,DGOLD,s0*ramp(z2,.6,1.),'ma')
    # 1. from inside, the next thing; from outside, a shape
    s1_=a*win(t,c[1]-.1,c[2]-.3,.6)
    if s1_>.02:
        tx(d,48,56,'A life, from inside and from outside',33,INK,s1_,'ls'); u=ramp(t,c[1]+.4,c[1]+3.4)
        kid(d,250,430,110,(60,104,204),s1_); arrow(d,(300,372),(300+150*u,372),VIR,s1_,4,1.); tx(d,300,452,'inside: the next thing to do',23,VIR,s1_,'ma')
        v=ramp(t,c[1]+4.0,c[1]+8.5); cx,cy,R_=860,330,150; n=int(90*v); pts=[(cx-R_*np.cos(q),cy-R_*np.sin(q)*.9) for q in np.linspace(0,2*np.pi*v,max(2,n))]; ln(d,pts,WARM,s1_,4)
        for q in np.linspace(0,2*np.pi*v,max(2,int(14*v))): dot(d,cx-R_*np.cos(q),cy-R_*np.sin(q)*.9,5,GOLD,s1_)
        tx(d,cx,cy+R_+26,'outside: a shape, told as a story',23,WARM,s1_*ramp(v,.3,.5),'ma')
    # 2. Campbell and Murdock
    s2=a*win(t,c[2]-.1,c[3]-.3,.6)
    if s2>.02:
        tx(d,48,56,'The shape, told as a story',33,INK,s2,'ls'); cx,cy,R_=330,340,150; u=ramp(t,c[2]+2.2,c[2]+9.0)
        pts=[(cx+R_*np.sin(q),cy-R_*np.cos(q)) for q in np.linspace(0,2*np.pi*u,max(2,int(100*u)))]; ln(d,pts,WARM,s2,4); dot(d,cx,cy-R_,9,INK,s2)
        for q,lab,an in ((.12,'leave home','ls'),(.5,'be tested','ma'),(.88,'come back changed','rs')):
            x,y=cx+R_*np.sin(2*np.pi*q),cy-R_*np.cos(2*np.pi*q); k=ramp(u,q-.06,q+.02); dot(d,x,y,7,GOLD,s2*k); tx(d,x+(16 if an=='ls' else -16 if an=='rs' else 0),y+(18 if an=='ma' else -10),lab,22,INK,s2*k,an)
        tx(d,cx,cy-12,'the hero’s journey',25,WARM,s2*ramp(u,.05,.2),'ma'); tx(d,cx,cy+22,'Campbell, 1949',18,SOFT,s2*ramp(u,.05,.2),'ma')
        w_=ramp(t,CE('s1',2)-7.2,CE('s1',2)-1.0); cx2=900; pts=[(cx2+(R_-110*q/(2.5*2*np.pi))*np.sin(q),cy-(R_-110*q/(2.5*2*np.pi))*np.cos(q)) for q in np.linspace(0,2.5*2*np.pi*w_,max(2,int(160*w_)))]; ln(d,pts,VIR,s2,4)
        if w_>0: dot(d,pts[-1][0],pts[-1][1],7,GOLD,s2)
        tx(d,cx2,cy+R_+20,'the heroine’s journey: also a return',25,VIR,s2*ramp(w_,.2,.4),'ma'); tx(d,cx2,cy+R_+54,'Murdock, 1990',18,SOFT,s2*ramp(w_,.2,.4),'ma')
    # 3. Le Guin: not a spear, a bag
    s3=a*win(t,c[3]-.1,c[4]-.3,.6)
    if s3>.02:
        tx(d,48,56,'Not a spear. A bag.',33,INK,s3,'ls'); sp=1-ramp(t,c[3]+4.2,c[3]+5.4)
        ln(d,[(170,470),(430,210)],INK,s3*lerp(.25,1,sp),5); pg(d,[(430,210),(398,222),(418,242)],INK,s3*lerp(.25,1,sp)); tx(d,300,500,'a spear',24,SOFT,s3*lerp(.4,1,sp),'ma')
        b=ramp(t,c[3]+5.0,c[3]+6.2); bx,by=lerp(700,760,ez(ramp(t,CE('s1',3)-4.4,CE('s1',3)-2.2))),330
        bag=[(bx-70,by-60),(bx-88,by+10),(bx-60,by+74),(bx+60,by+74),(bx+88,by+10),(bx+70,by-60)]; pg(d,bag,(196,150,96),s3*b); ln(d,bag+[bag[0]],INK,s3*b,3); ln(d,[(bx-70,by-60),(bx-30,by-118),(bx+30,by-118),(bx+70,by-60)],INK,s3*b,3)
        for k in range(7): q=ramp(t,c[3]+6.6+k*.5,c[3]+7.4+k*.5); spark(d,bx-48+k*16+6*np.sin(k*2.1),lerp(by-190,by+20+18*np.sin(k*1.7),ez(q)),6,s3*q)
        tx(d,bx,by+100,'something to carry things home in',24,DGOLD,s3*b,'ma')
        g=ramp(t,CE('s1',3)-4.4,CE('s1',3)-3.4); kid(d,560,470,120,(60,104,204),s3*g); kid(d,990,470,120,(13,122,112),s3*g); tx(d,bx,by+134,'and to someone else',24,VIR,s3*ramp(t,CE('s1',3)-2.6,CE('s1',3)-1.8),'ma')
        cite(d,'Ursula K. Le Guin, “The Carrier Bag Theory of Fiction”, 1986',s3*b)
    # 4. the small self holds the piece; the large self is the picture
    s4=a*ramp(t,c[4]-.1,c[4]+.6)
    if s4>.02:
        tx(d,48,56,'Two selves',33,INK,s4,'ls'); put_piece(im,4,300,330,-8,.8,s4,lift=.6); tx(d,300,490,'the small self holds the piece',25,VIR,s4,'ma')
        lg=ramp(t,c[4]+2.0,c[4]+3.0); lid(im,d,700,190,420,s4*lg); tx(d,910,500,'the large self is the picture',25,WARM,s4*lg,'ma')
        tx(d,W/2,560,'we are both, and we mostly forget the second',23,SOFT,s4*ramp(t,c[4]+5.0,c[4]+5.8),'ma')
    return fin(im)
STN=None
def stones():
    """A wall in courses. Each stone is laid in turn; a few fall and are laid again."""
    global STN
    if STN is None:
        r=np.random.default_rng(8); out=[]; y=470; k=0
        for row in range(8):
            x=150+(34 if row%2 else 0)
            while x<1110: w=float(r.uniform(58,104)); out.append((x,y-row*46,w,k,float(r.uniform(.86,1.)))); x+=w+4; k+=1
        STN=out
    return STN
def sc_built(t):
    c=[cue('c1',i) for i in range(4)]; e0=ramp(t,cue('c1',1)-1.0,cue('c1',1)-.2); a=1-ramp(t,cue('w4',0)-1.1,cue('w4',0)-.4)
    if e0<1:
        u=ramp(t,c[0]-.6,c[1]); im,v=photo(1.0+1.7*ez(ramp(t,c[0]+.5,c[0]+5.5)),.97,.99); d=D(im); tab(d,44,54,'the wall they are leaning on',28,ramp(t,c[0]+3.0,c[0]+3.8)*(1-e0)); tab(d,44,108,'somebody built it',24,ramp(t,c[0]+5.2,c[0]+6.0)*(1-e0),SOFT)
        f=1-ramp(t,c[0]-.6,c[0]+.4)
        if f>.01: d.rectangle([0,0,W*Q,H*Q],fill=PAPER+(A_(f),))
        if e0>0: d.rectangle([0,0,W*Q,H*Q],fill=PAPER+(A_(e0),))
        return fin(im)
    im=canvas(); d=D(im); ST=stones(); n=len(ST); laid=n*.72*ramp(t,c[1]-.2,c[3]+4.0)+2; s2=ramp(t,c[2]-.2,c[2]+.6); s3=ramp(t,c[3]-.2,c[3]+.6)
    tx(d,48,56,'Ever building',33,INK,a*(1-s3),'ls'); ln(d,[(110,518),(1170,518)],INK,a*.4,1.6)
    for (x,y,w,k,sh) in ST:
        if k>laid+10: continue
        q=min(1.,max(0.,laid-k)); old=min(1.,max(0.,(laid-k)/(n*.4))); fall=0.
        if s2>0 and k%13==5 and k<laid-6: ph=((t-c[2])*.35+k*.37)%1; fall=np.sin(np.pi*ph)**2 if ph<1 else 0
        if q<=0:
            if k<laid+10: d.rectangle([x*Q,(y-42)*Q,(x+w)*Q,y*Q],outline=(150,144,130,A_(a*.5*(1-(k-laid)/10))),width=int(1.2*Q))      # the courses not yet laid
            continue
        yy=y-(1-ez(q))*60+fall*40; col=tuple(int(lerp(c_,p_,old*.45)) for c_,p_ in zip((206,192,160),(236,230,214))); rect(d,x,yy-42,x+w,yy,tuple(int(v*sh) for v in col),a*(1-.5*fall),2,(120,108,90),1.4)
        spark(d,x+w/2,yy-21,3.6,a*lerp(1.,.28,old)*(1-fall))
    kx_=150+((laid*37)%900); kid(d,kx_,516,70,(60,104,204),a*(1-s3)*.9,lean=.2); kid(d,kx_+70,516,64,(200,72,44),a*(1-s3)*.9,lean=-.2)
    fo=1-ramp(t,c[2]-1.4,c[2]-.6); tx(d,48,96,'the lower stones: people we will never meet',22,SOFT,a*ramp(t,c[1]+2.2,c[1]+3.0)*fo,'ls'); tx(d,48,126,'the outlines above: people who will never meet us',22,SOFT,a*ramp(t,c[1]+7.2,c[1]+8.0)*fo,'ls')
    if s2*(1-s3)*a>.02: tab(d,48,112,'ever building, ever falling',34,s2*(1-s3)*a,WARM,RG); tab(d,48,170,'William Blake, Milton',19,s2*(1-s3)*a,SOFT)
    if s3*a>.02:
        d.rectangle([0,0,W*Q,H*Q],fill=PAPER+(int(228*s3*a),)); tx(d,W/2,130,'re-member',64,INK,s3*a,'ma',RG); tx(d,W/2,214,'to put the members back together',26,SOFT,s3*a*ramp(t,c[3]+3.2,c[3]+4.0),'ma')
        for i in range(7):
            x=250+i*130; g=ramp(t,c[3]+1.0+i*.3,c[3]+1.8+i*.3); kid(d,x,470,104+6*((i*5)%3),KC[i%6],s3*a*g)
            if i: ln(d,[(x-96,412),(x-34,412)],INK,s3*a*g*.7,2.4)
        pos=250+780*(((t-c[3])*.16)%1); spark(d,pos,340+10*np.sin(pos*.05),8,s3*a*ramp(t,c[3]+4.0,c[3]+5.0)); tx(d,W/2,520,'nobody does that alone',26,DGOLD,s3*a*ramp(t,CE('c1',3)-1.6,CE('c1',3)-.8),'ma')
    return fin(im)
PS=M['passes']; LX=lambda p: np.log(p)/np.log(4000)
def chart(d,x,y,w,h,a,dark=False):
    ink=PALE if dark else INK; soft=(150,160,170) if dark else SOFT; hair=(60,70,88) if dark else HAIR
    X=lambda p: x+w*LX(p); Y=lambda e: y+h-h*min(e,1.5)/1.5
    ln(d,[(x,y),(x,y+h),(x+w,y+h)],ink,a*.7,1.6)
    for p in (1,10,100,1000,4000): ln(d,[(X(p),y+h),(X(p),y+h+6)],ink,a*.7,1.4); tx(d,X(p),y+h+10,format(p,','),17,soft,a,'ma',NUM)
    tx(d,x+w/2,y+h+36,'times it has gone over its own day',20,soft,a,'ma'); tx(d,x-12,y-8,'mistakes',20,soft,a,'rs')
    ln(d,[(x,Y(1.)),(x+w,Y(1.))],soft,a*.8,1.2); tx(d,x+w*.40,Y(1.)-6,'knowing nothing',18,soft,a,'ms')
    return X,Y
def curve(d,X,Y,vals,u,col,a,w=4.2):
    n=max(2,int(len(PS)*u)); ln(d,[(X(PS[i]),Y(vals[i])) for i in range(n)],col,a,w)
    return X(PS[n-1]),Y(vals[n-1])
def sc_trap(t):
    im=canvas(); d=D(im); c=[cue('w4',i) for i in range(4)]; a=ramp(t,c[0]-.5,c[0]+.5)*(1-ramp(t,cue('m1',0)-1.1,cue('m1',0)-.4)); r_=ramp(t,c[3]-.5,c[3]+.3); a1=a*(1-r_)
    tx(d,48,56,'Rehearsing one day, over and over',33,INK,a1,'ls')
    px,py,pw,ph=60,150,330,330
    if a1>.02:
        d.rectangle([px*Q,py*Q,(px+pw)*Q,(py+ph)*Q],fill=(250,246,234,A_(a1)),outline=HAIR+(A_(a1),),width=int(1.4*Q))
        pts=[(px+30+(p[0]-950)*.86,py+40+(p[1]-330)*1.02) for p in DOTS]; lap=((t-c[0])*.42)%1; n_=int((t-c[0])*.42)
        thread(d,[pts[k] for k in ORD_A],1.,GOLD,a1*.35,2.4); thread(d,[pts[k] for k in ORD_A],lap,DGOLD,a1,4)
        for p in pts: spark(d,p[0],p[1],5.5,a1)
        tx(d,px,py+ph+12,'the same join, every time',21,SOFT,a1,'la'); tx(d,px+pw,py+ph+12,'%d times'%max(0,n_),21,DGOLD,a1*ramp(t,c[0]+2,c[0]+3),'ra',NUM)
        X,Y=chart(d,520,150,690,330,a1); u=ramp(t,c[1]-.2,c[1]+6.5)
        if u>0:
            ex,ey=curve(d,X,Y,M['awake']['seen'],u,VIR,a1); tx(d,ex+10 if ex<1090 else ex-10,ey-16,'on the day you have',20,VIR,a1*ramp(u,.25,.4),'ls' if ex<1090 else 'rs')
            ex,ey=curve(d,X,Y,M['awake']['new'],u,WARM,a1); tx(d,ex-10,ey-14,'on a new day',20,WARM,a1*ramp(u,.5,.65),'rs')
        y_=a1*ramp(t,c[1]+7.2,c[1]+8.); tx(d,865,172,'very good at being who you were yesterday',25,WARM,y_,'ma')
        g=ramp(t,c[2]+.2,c[2]+1.)*a1
        if g>.02: d.rectangle([520*Q,150*Q,1210*Q,356*Q],fill=PAPER+(int(252*g),)); tx(d,865,186,'When a measure becomes a target,\nit ceases to be a good measure.',33,INK,g,'ma',RG); tx(d,865,296,'Marilyn Strathern, 1997, after Charles Goodhart, 1975',19,SOFT,g,'ma')
        note(d,'illustration: our own simulation',a1*ramp(t,c[1],c[1]+.8))
    # the ruler itself has changed: the same wall, a child who grows, and the measure they carry
    a2=a*r_
    if a2>.02:
        tx(d,48,56,'How the world looked',33,INK,a2,'ls'); gr=ez(ramp(t,c[3]+1.0,CE('w4',3)-2.2)); gy=470; ln(d,[(120,gy),(1160,gy)],INK,a2*.5,1.6)
        pg(d,[(560,gy),(560,gy-150),(900,gy-150),(900,gy)],(214,206,190),a2); ln(d,[(560,gy),(560,gy-150),(900,gy-150),(900,gy)],INK,a2,2.2)
        for k in range(1,6): ln(d,[(560,gy-25*k),(900,gy-25*k)],(150,144,130),a2*.6,1)
        hs=lerp(96,236,gr); kid(d,430,gy,hs,(60,104,204),a2)
        ux=lerp(26,64,gr); x=960; rect(d,x-6,gy-320,x+28,gy,GOLD,a2,2,DGOLD,1.4)                       # the ruler: its unit is the child's own hand-span
        k=0
        while k*ux<=320: ln(d,[(x-6,gy-k*ux),(x+(16 if k%2==0 else 8),gy-k*ux)],INK,a2*.85,1.4); k+=1
        tx(d,48,104,'the wall is %d of your own hand-spans high'%round(150/ux),25,DGOLD,a2,'ls',NUM)
        tx(d,x+44,gy-250,'the wall has\nnot changed',22,SOFT,a2*ramp(gr,.5,.7),'la'); tx(d,x+44,gy-180,'the ruler has',22,WARM,a2*ramp(gr,.75,.95),'la')
        tx(d,430,gy+16,'five' if gr<.5 else 'now',22,SOFT,a2,'ma')
    return fin(im)
def sc_night(t):
    im=Image.new('RGB',(W*Q,H*Q),NIGHT); d=D(im); c=[cue('w5',i) for i in range(4)]; a=ramp(t,c[0]-.5,c[0]+.6)*(1-ramp(t,cue('k1',0)-1.1,cue('k1',0)-.4))
    r=np.random.default_rng(9)
    for k in range(90): x,y=r.uniform(0,W),r.uniform(0,420); dot(d,x,y,r.uniform(.5,1.5),PALE,a*(.25+.3*np.sin(t*r.uniform(.5,2)+k)**2))
    tx(d,48,56,'At night',33,PALE,a,'ls')
    # 1. the clock stops mattering; the ball rolls uphill; the sea is in the wrong place
    s1=a*(1-ramp(t,c[1]-.7,c[1]-.1))
    if s1>.02:
        cx,cy,R_=250,310,104; d.ellipse([(cx-R_)*Q,(cy-R_)*Q,(cx+R_)*Q,(cy+R_)*Q],outline=PALE+(A_(s1*.9),),width=int(2.4*Q))
        for k in range(12): an=k*np.pi/6; ln(d,[(cx+np.cos(an)*(R_-12),cy+np.sin(an)*(R_-12)),(cx+np.cos(an)*(R_-3),cy+np.sin(an)*(R_-3))],PALE,s1*.8,2)
        go=ramp(t,c[0]+3.4,c[0]+7.5); h1=-1.1+t*.9+go*go*9*np.sin(t*1.7); h2=.6-t*.35-go*go*7*np.cos(t*1.1); fa=1-.85*go
        ln(d,[(cx,cy),(cx+np.cos(h1)*78+go*60*np.sin(t),cy+np.sin(h1)*78-go*90)],PALE,s1*fa,3.2); ln(d,[(cx,cy),(cx+np.cos(h2)*52-go*70,cy+np.sin(h2)*52-go*50*np.cos(t))],PALE,s1*fa,4.2); dot(d,cx,cy,4,PALE,s1)
        tx(d,cx,cy+R_+16,'no clock',22,(170,178,190),s1*go,'ma')
        sa=s1*ramp(t,c[0]+7.6,c[0]+8.4); ln(d,[(520,470),(860,320)],PALE,sa*.7,2.4); uu=((t-c[0])*.22)%1; dot(d,lerp(540,840,uu),lerp(446,314,uu)-2,13,(250,246,238),sa); dot(d,lerp(540,840,uu)-4,lerp(446,314,uu)-6,4,WARM,sa)
        wa=s1*ramp(t,c[0]+9.6,c[0]+10.4)
        for k in range(4): y=100+k*14; ln(d,[(x,y+5*np.sin(x*.02+t*1.4+k)) for x in range(470,1230,14)],SEA,wa*.85,2.6)
        tx(d,960,470,'nobody minds',24,(170,178,190),s1*ramp(t,CE('w5',0)-1.6,CE('w5',0)-.8),'ma')
    # 2. everyone in the dream is made by you: six figures, one colour
    s2=a*win(t,c[1]-.2,c[2]-.2,.6)
    if s2>.02:
        gy=440; ln(d,[(120,gy+2),(1160,gy+2)],PALE,s2*.3,1.4)
        for i in range(6):
            x=210+i*172+12*np.sin(t*.9+i*1.9); one=ez(ramp(t,c[1]+1.2+i*.25,c[1]+2.4+i*.25)); col=tuple(int(lerp(p,q,one)) for p,q in zip(KC[i],GOLD)); dot(d,x,gy-52,56,GOLD,s2*.10*one); kid(d,x,gy,100+8*((i*5)%3),col,s2,lean=.15*np.sin(t*1.4+i))
        tx(d,W/2,gy+34,'all of them are you',26,GOLD,s2*ramp(t,c[1]+3.4,c[1]+4.2),'ma')
    # 3. the dots are shaken and joined again: yesterday, transformed
    s3=a*win(t,c[2]-.2,c[3]-.2,.6)
    if s3>.02:
        px,py=150,170; base=[(px+(p[0]-950)*1.0,py+(p[1]-330)*1.05) for p in DOTS]; rr=np.random.default_rng(77); new=[(px+560+rr.uniform(0,330),py+rr.uniform(0,260)) for _ in DOTS]
        sh=ramp(t,c[2]+.4,c[2]+4.2); f=ez(sh); wob=np.sin(np.pi*sh)*26; pts=[(lerp(p[0],q[0],f)+wob*np.sin(t*7+k*2.1),lerp(p[1],q[1],f)+wob*np.cos(t*6+k*1.3)) for k,(p,q) in enumerate(zip(base,new))]
        thread(d,[base[k] for k in ORD_A],1.,PALE,s3*.28,2.2); 
        for p in base: dot(d,p[0],p[1],4,PALE,s3*.3)
        tx(d,px+150,py+300,'yesterday',23,(170,178,190),s3,'ma')
        j=ramp(t,c[2]+4.2,c[2]+6.6); thread(d,[pts[k] for k in ORD_B],j,GOLD,s3,3.4)
        for p in pts: spark(d,p[0],p[1],6.5,s3)
        tx(d,px+725,py+300,'yesterday, transformed',23,GOLD,s3*ramp(j,.6,.9),'ma'); arrow(d,(px+330,py+130),(px+520,py+130),PALE,s3*.6,2.6,ramp(t,c[2]+1.,c[2]+3.))
    # 4. the hypothesis, and the arithmetic
    s4=a*ramp(t,c[3]-.2,c[3]+.6)
    if s4>.02:
        X,Y=chart(d,300,150,720,320,s4,dark=True); u=ramp(t,c[3]+2.0,c[3]+9.0)
        ex,ey=curve(d,X,Y,M['awake']['new'],1.,WARM,s4*.55,3); tx(d,ex-8,ey-12,'awake only, on a new day',19,WARM,s4*.8,'rs')
        if u>0:
            ex,ey=curve(d,X,Y,M['dream']['seen'],u,(90,190,176),s4); tx(d,ex-8,ey+26,'with dreams, on the day you have',19,(90,190,176),s4*ramp(u,.7,.9),'rs')
            ex,ey=curve(d,X,Y,M['dream']['new'],u,GOLD,s4); tx(d,ex-8,ey-12,'with dreams, on a new day',19,GOLD,s4*ramp(u,.7,.9),'rs')
        tx(d,48,560,'the idea: Hoel, 2021, after Crick & Mitchison, 1983, and Hobson & Friston, 2012 · the arithmetic: Bishop, 1995 · the curves: our own simulation',19,(170,178,190),s4*ramp(t,c[3]+8.,c[3]+9.),'ls')
    return fin(im)

M2=json.load(open(S+'/maths2.json')); WARMT=(1.34,1.04,.56); COOLT=(.62,.9,1.34)
def mosaic(d,x,y,w,grid,a=1.,n=24,seq=None):
    """A lid painted piece by piece: 6 by 4 squares, gold or blue."""
    cw=w/6; ch=cw*200/200*(2/3)*1.0
    cells=[(k,c) for k,c in (seq[:n] if seq is not None else enumerate(grid))]
    for k,c in cells: i_,j_=k%6,k//6; d.rectangle([(x+i_*cw)*Q,(y+j_*ch)*Q,(x+(i_+1)*cw)*Q-1,(y+(j_+1)*ch)*Q-1],fill=((224,172,70) if c else (70,120,190))+(A_(a),))
def sc_second(t):
    im=wood(); d=D(im); c=[cue('q1',i) for i in range(5)]; a=ramp(t,c[0]-.5,c[0]+.4); out=1-ramp(t,cue('s1',0)-1.1,cue('s1',0)-.4); A=a*out
    s0=A*(1-ramp(t,c[1]-.6,c[1])); lid(im,d,470,170,340,s0); tab(d,470,440,'the lid: printed before you opened the box',24,s0*ramp(t,c[0]+2.6,c[0]+3.4),INK)
    s1=A*win(t,c[1]-.1,c[2]-.4,.6)
    if s1>.02:
        fr=sc_beach(cue('w2',1)+1.5+((t-c[1])*.9)%9).resize((520*Q,292*Q),Image.LANCZOS); d.rectangle([(380-12)*Q,(150-12)*Q,(900+12)*Q,(442+12)*Q],fill=(246,240,226,A_(s1))); m=Image.new('L',fr.size,A_(s1)); im.paste(fr,(380*Q,150*Q),m); d=D(im)
        tab(d,380,476,'every piece you lay changes the pieces that are left',24,s1*ramp(t,c[1]+3.,c[1]+3.8),INK)
    def board(run,u,al,who=False):
        seq=M2['keep'][run]['seq']; n=int(len(seq)*min(1.,u)); sc_=.36; ox,oy=110,150
        d.rectangle([(ox-8)*Q,(oy-8)*Q,(ox+6*200*sc_+8)*Q,(oy+4*200*sc_+8)*Q],outline=(246,240,226,A_(al*.5)),width=int(1.5*Q))
        for q,(k,col) in enumerate(seq[:n+1]):
            f=1. if q<n else (len(seq)*min(1.,u))%1; hx,hy=home(k,ox,oy,sc_); sx=(-80 if (who and q%2) else 640) if True else 0; x=lerp(640 if not who else (60 if q%2==0 else 620),hx,ez(f)); y=lerp(600,hy,ez(f))
            put_piece(im,k,x,y,(1-ez(f))*40,sc_,al,lift=(1-ez(f)),tint=WARMT if col else COOLT)
        return seq,n
    s2=A*win(t,c[2]-.1,c[3]-.4,.6)
    if s2>.02:
        u=ramp(t,c[2]+2.6,CE('q1',2)+.6); seq,n=board(0,u,s2); d=D(im)
        d.rectangle([(820-12)*Q,(170-12)*Q,(1160+12)*Q,(397+12)*Q],fill=(246,240,226,A_(s2))); d.rectangle([820*Q,170*Q,1160*Q,397*Q],fill=(232,226,208,A_(s2))); mosaic(d,820,170,340,None,s2,n,seq)
        tab(d,820,430,'the lid: blank, and painted as you go',24,s2*ramp(t,c[2]+2.,c[2]+2.8),INK)
    s3=A*win(t,c[3]-.1,c[4]-.4,.6)
    if s3>.02:
        d.rectangle([60*Q,120*Q,1220*Q,520*Q],fill=PAPER+(int(244*s3),)); nshow=int(48*ramp(t,c[3]+.6,c[3]+6.5))
        for q in range(nshow): gx=90+(q%12)*78; gy=150+(q//12)*62; mosaic(d,gx,gy,66,M2['keep'][q]['grid'],s3)
        z=ramp(t,c[3]+6.2,c[3]+7.2); tx(d,90,418,'%d of 1,000 came out different'%M2['distinct'],40,INK,s3*z,'la',RG); tx(d,90,474,'the same pieces, the same rule, laid in a different order',22,SOFT,s3*z,'la'); tx(d,1190,488,'illustration: our own simulation',19,SOFT,s3,'ra')
    s4=A*ramp(t,c[4]-.1,c[4]+.6)
    if s4>.02:
        u=ramp(t,c[4]+.6,CE('q1',4)-1.5); seq,n=board(1,u,s4,who=True); d=D(im); kid(d,640,420,150,(60,104,204),s4,lean=-.15); kid(d,790,420,150,(200,72,44),s4,lean=.15)
        tab(d,620,470,'found, and made, and not alone',28,s4*ramp(t,CE('q1',4)-5.,CE('q1',4)-4.2),INK); tab(d,W-44,560,'second-order: the player is part of the puzzle · after von Foerster',19,s4*ramp(t,c[4]+2.,c[4]+2.8),SOFT,anchor='rd')
    f=1-ramp(t,c[0]-.5,c[0]+.4)
    if f>.01: D(im).rectangle([0,0,W*Q,H*Q],fill=PAPER+(A_(f),))
    if out<.99: D(im).rectangle([0,0,W*Q,H*Q],fill=PAPER+(A_(1-out),))
    return fin(im)
def pebble(d,cx,cy,r,rough,key,col,a):
    rr=np.random.default_rng(key); pts=[(cx+np.cos(q)*r*(1+rough*rr.uniform(-.5,.5)),cy+np.sin(q)*r*.8*(1+rough*rr.uniform(-.5,.5))) for q in np.linspace(0,2*np.pi,22,endpoint=False)]; pg(d,pts,col,a); ln(d,pts+[pts[0]],INK,a,2.2)
def sc_arch(t):
    im=canvas(); d=D(im); c=[cue('a1',i) for i in range(4)]; a=ramp(t,c[0]-.5,c[0]+.5)*(1-ramp(t,cue('c1',0)-1.2,cue('c1',0)-.6))
    s0=a*(1-ramp(t,c[1]-.6,c[1]))
    if s0>.02:
        tx(d,48,56,'Told, and told again',33,INK,s0,'ls')
        for i in range(6):
            g=ramp(t,c[0]+1.6+i*1.3,c[0]+2.4+i*1.3); x=170+i*188; kid(d,x,470,104,KC[i],s0*g); pebble(d,x,300,44,.9*(1-i/5)**1.3,40+i,(214,196,150),s0*g)
            if i: arrow(d,(x-140,300),(x-62,300),SOFT,s0*g,2.4)
        tx(d,170,220,'as first told',21,SOFT,s0*ramp(t,c[0]+2.,c[0]+2.8),'ma'); tx(d,170+5*188,220,'as it reached us',21,SOFT,s0*ramp(t,c[0]+8.6,c[0]+9.4),'ma')
    s1=a*win(t,c[1]-.1,c[2]-.4,.6)
    if s1>.02:
        tx(d,48,56,'What ten thousand choices leave',33,INK,s1,'ls'); n=int(420*ramp(t,c[1]+.3,c[1]+7.0)); r=np.random.default_rng(5)
        for q in range(420):
            y0=r.uniform(170,520); ph=r.uniform(0,6.28); w_=r.uniform(.5,1.)
            if q<n: ln(d,[(120+x*26,lerp(y0,340+60*np.sin(x*.21)+18*np.sin(x*.5+ph)*(1-x/40)*w_,ez(min(1,x/14)))) for x in range(41)],INK,s1*.07,1.6)
        tx(d,W/2,548,'the lid, worn smooth by hands',26,DGOLD,s1*ramp(t,c[1]+6.2,c[1]+7.),'ma')
    s2=a*win(t,c[2]-.1,c[3]-.4,.6)
    if s2>.02:
        tx(d,48,56,'A partnership across time',33,INK,s2,'ls')
        for g_,(x0,lab,al,ol) in enumerate(((160,'the dead',.28,False),(520,'the living',1.,False),(880,'those to be born',.9,True))):
            k=ramp(t,c[2]+3.2+g_*1.3,c[2]+4.+g_*1.3)
            for i in range(3):
                x=x0+i*92; 
                if ol: d.ellipse([(x-20)*Q,(410-104)*Q,(x+20)*Q,(410-64)*Q],outline=INK+(A_(s2*k*.6),),width=int(1.6*Q)); ln(d,[(x-28,410),(x-32,410-56),(x-16,410-66),(x+16,410-66),(x+32,410-56),(x+28,410),(x-28,410)],INK,s2*k*.6,1.6)
                else: kid(d,x,410,108,KC[(i+g_*2)%6],s2*k*al)
            tx(d,x0+92,430,lab,24,INK,s2*k,'ma')
        ln(d,[(150,350),(1130,350)],GOLD,s2*ramp(t,c[2]+6.6,c[2]+7.6),3)
        tx(d,160,500,'“those who are living, those who are dead,\nand those who are to be born”',24,INK,s2*ramp(t,c[2]+1.,c[2]+1.8),'la'); tx(d,160,566,'Edmund Burke, 1790',18,SOFT,s2*ramp(t,c[2]+1.,c[2]+1.8),'la')
        tx(d,1120,500,'“the democracy of the dead”',24,INK,s2*ramp(t,CE('a1',2)-3.4,CE('a1',2)-2.6),'ra'); tx(d,1120,538,'G. K. Chesterton, 1908',18,SOFT,s2*ramp(t,CE('a1',2)-3.4,CE('a1',2)-2.6),'ra')
    s3=a*ramp(t,c[3]-.1,c[3]+.6)
    if s3>.02:
        tx(d,48,56,'A ratchet',33,INK,s3,'ls'); u=ramp(t,c[3]+1.2,CE('a1',3)+1.0)*5
        for i in range(6):
            x=180+i*160; y=500-i*52; g=min(1.,max(0.,u-i+1)); ln(d,[(x,y),(x+160,y)],INK,s3*g,3); ln(d,[(x,y),(x,y+52)],INK,s3*g*(1 if i else 0),3)
            if g>0: kid(d,x+80,y,84,KC[i],s3*g*(1. if i>=int(u) else .35)); spark(d,x+80,y-110,5.5,s3*g*(1. if i>=int(u) else .3))
        tx(d,W/2,560,'each generation starts where the last one stopped',24,DGOLD,s3*ramp(t,c[3]+3.6,c[3]+4.4),'ma'); cite(d,'the ratchet effect: Tomasello, 1999',s3*ramp(t,c[3]+1.,c[3]+1.8))
    return fin(im)
def sc_meta(t):
    global _SRC
    im=canvas(); d=D(im); c=[cue('m1',i) for i in range(3)]; a=ramp(t,c[0]-.5,c[0]+.5)*(1-ramp(t,cue('l1',0)-1.1,cue('l1',0)-.4))
    s0=a*(1-ramp(t,c[1]-.6,c[1]))
    if s0>.02:
        tx(d,48,56,'A second trap',33,INK,s0,'ls')
        if _SRC is None: _SRC=Image.open(S+'/wall-soft.jpg').convert('RGB').crop((118,180,1318,980))
        zz=1+.25*ramp(t,c[0],c[1]); x,y,w=330,120,int(620*zz); x=int(640-w/2); y=int(330-w/3)
        for depth in range(6):
            h=int(w*2/3); 
            if w<30: break
            d.rectangle([(x-8)*Q,(y-8)*Q,(x+w+8)*Q,(y+h+8)*Q],fill=(246,240,226,A_(s0)),outline=(120,84,50,A_(s0)),width=int(1.6*Q)); pic=_SRC.resize((w*Q,h*Q),Image.BILINEAR); im.paste(pic,(x*Q,y*Q),Image.new('L',pic.size,A_(s0))); d=D(im)
            x=x+int(w*.50); y=y+int(h*.10); w=int(w*.44)
        tab(d,48,96,'a picture of the lid, on the lid',24,s0*ramp(t,c[0]+4.6,c[0]+5.4),SOFT)
    s1=a*win(t,c[1]-.1,c[2]-.4,.6)
    if s1>.02:
        tx(d,48,56,'Too much looking back',33,INK,s1,'ls'); kid(d,300,470,170,(60,104,204),s1); n_=int(9*ramp(t,c[1]+1.5,c[1]+7.))
        for q in range(n_): rect(d,380+q*54,470-150-q*4,380+q*54+46,470,(232,226,208),s1,2,(120,108,90),1.4); tx(d,380+q*54+23,470-80,'then',15,SOFT,s1,'ma')
        arrow(d,(300,250),(170,250),VIR,s1*ramp(t,c[1]+7.,c[1]+7.8),4); tx(d,160,214,'the way on',22,VIR,s1*ramp(t,c[1]+7.,c[1]+7.8),'ma')
        tx(d,W/2,540,'to live at all, something has to be forgotten',27,WARM,s1*ramp(t,CE('m1',1)-3.4,CE('m1',1)-2.6),'ma'); tx(d,48,96,'after Nietzsche, On the Uses and Disadvantages of History for Life, 1874',20,SOFT,s1*ramp(t,c[1]+.6,c[1]+1.4),'ls')
    s2=a*ramp(t,c[2]-.1,c[2]+.6)
    if s2>.02:
        tx(d,48,56,'One step outside',33,INK,s2,'ls')
        for i in range(4):
            g=ramp(t,c[2]+.8+i*1.1,c[2]+1.6+i*1.1); x=250+i*230; sc_=150-i*22; kid(d,x,470,sc_,KC[i],s2*g); d.rectangle([(x-130+i*14)*Q,(470-sc_-60)*Q,(x+70-i*4)*Q,(470+16)*Q],outline=INK+(A_(s2*g*.55),),width=int(1.6*Q))
            if i: tx(d,x-10,470-sc_-70,'watching',19,SOFT,s2*g,'ma')
        ph=np.sin((t-c[2])*1.6); px_=640+260*ph; ln(d,[(640,96),(px_,170)],INK,s2*ramp(t,c[2]+5.,c[2]+5.8),2); dot(d,px_,170,9,GOLD,s2*ramp(t,c[2]+5.,c[2]+5.8))
        tx(d,330,150,'irony',27,SOFT,s2*ramp(t,CE('m1',2)-4.6,CE('m1',2)-3.8),'ma'); tx(d,950,150,'wanting to mean it',27,WARM,s2*ramp(t,CE('m1',2)-2.6,CE('m1',2)-1.8),'ma')
        cite(d,'Vermeulen & van den Akker, “Notes on metamodernism”, 2010',s2*ramp(t,c[2]+4.,c[2]+4.8))
    return fin(im)
def heads(d,y,n,r,a,child=None,turn=0.):
    for i in range(n):
        x=W*(i+.5)/n+18*np.sin(i*2.3); rr=r*(.9+.12*np.sin(i*1.7)); col=(16,19,30)
        if child is not None and i==child: rr=r*.72; 
        pg(d,[(x-rr*1.5,y+rr*2.6),(x-rr*1.3,y+rr*1.1),(x-rr*.5,y+rr*.75),(x+rr*.5,y+rr*.75),(x+rr*1.3,y+rr*1.1),(x+rr*1.5,y+rr*2.6)],col,a); dot(d,x+ (turn*rr*.25 if i==child else 0),y,rr,col,a); d.arc([(x-rr)*Q,(y-rr)*Q,(x+rr)*Q,(y+rr)*Q],200,340,fill=(96,112,150,A_(a*.8)),width=int(2*Q))
        if child is not None and i==child: d.ellipse([(x-rr)*Q,(y-rr)*Q,(x+rr)*Q,(y+rr)*Q],outline=GOLD+(A_(a*.8),),width=int(1.6*Q))
def storm(im,d,x0,y0,x1,y1,t,calm=0.,a=1.):
    d.rectangle([x0*Q,y0*Q,x1*Q,y1*Q],fill=(26,36,58,A_(a))); h=y1-y0; fl=max(0.,np.sin(t*2.3)*np.sin(t*5.1)-.72)*3.2*(1-calm)
    if fl>0: d.rectangle([x0*Q,y0*Q,x1*Q,(y0+h*.55)*Q],fill=(200,210,235,A_(a*min(.8,fl))))
    for k in range(7):
        y=y0+h*.42+k*h*.085; amp=(16-k)*(1-.6*calm); pts=[(x,y+amp*np.sin(x*.018+t*(2.2-.2*k)+k*1.9)+amp*.5*np.sin(x*.043-t*2.6+k)) for x in range(int(x0),int(x1)+12,12)]; pg(d,pts+[(x1,y1),(x0,y1)],tuple(int(lerp(c_,p_,k/7)) for c_,p_ in zip((70,96,130),(18,30,54))),a)
    r=np.random.default_rng(int(t*24))
    for _ in range(int(60*(1-calm))): x=r.uniform(x0,x1-20); y=r.uniform(y0,y1-30); ln(d,[(x,y),(x+10,y+26)],(190,200,220),a*.35,1)
    bx=lerp(x0+120,x1-160,(t*.05)%1); by=y0+h*.47+10*np.sin(t*2.1); pg(d,[(bx-34,by),(bx+34,by),(bx+24,by+14),(bx-24,by+14)],(12,14,20),a); ln(d,[(bx,by),(bx,by-44)],(12,14,20),a,2.4); pg(d,[(bx+2,by-42),(bx+30,by-8),(bx+2,by-8)],(210,200,180),a*.9)
def cinema(t,calm=0.,turn=0.,screen=None,show=1.):
    im=Image.new('RGB',(W*Q,H*Q),(7,8,13)); d=D(im); x0,y0,x1,y1=250,70,1030,400
    if screen is None: storm(im,d,x0,y0,x1,y1,t,calm)
    else: im.paste(screen.resize(((x1-x0)*Q,(y1-y0)*Q),Image.LANCZOS),(x0*Q,y0*Q)); d=D(im)
    fl=.85+.15*np.sin(t*31)*np.sin(t*7.3)                                         # the beam: a cone of light from behind, with dust in it
    for (px,py) in ((x0,y0),(x1,y0)): pg(d,[(640,-420),(px,py),(px+(x1-x0 if px==x0 else 0)-( x1-x0 if px==x1 else 0),py)],(255,244,214),0) 
    pg(d,[(600,-60),(680,-60),(x1,y0),(x1,y1),(x0,y1),(x0,y0)],(255,244,214),.085*fl); pg(d,[(620,-60),(660,-60),(x1-120,y0),(x0+120,y0)],(255,244,214),.07*fl)
    for k in range(1,7): d.rectangle([(x0-k*16)*Q,(y0-k*12)*Q,(x1+k*16)*Q,(y1+k*14)*Q],outline=(70,84,120,int(26/k)),width=int(14*Q))
    r=np.random.default_rng(3)
    for k in range(70): u=r.uniform(.15,1.); xx=lerp(640,r.uniform(x0,x1),u)+6*np.sin(t*.6+k); yy=lerp(-60,r.uniform(y0,y1),u)+4*np.cos(t*.5+k*2); dot(d,xx,yy,r.uniform(.6,1.6),(255,246,220),.5*(.5+.5*np.sin(t*1.3+k*1.7))*fl)
    glow=Image.new('RGB',im.size,(0,0,0)); gd=ImageDraw.Draw(glow); gd.rectangle([(x0-10)*Q,(y0-10)*Q,(x1+10)*Q,(y1+10)*Q],fill=(46,54,78)); im=Image.composite(im,Image.blend(im,glow.filter(ImageFilter.GaussianBlur(60)),.5),Image.new('L',im.size,150)) if False else im
    d=D(im); heads(d,500,9,30,1.); heads(d,585,7,42,1.,child=3,turn=turn)
    return im,d
def booth(t):
    im=Image.new('RGB',(W*Q,H*Q),(6,6,10)); d=D(im); cx,cy=640,250; fl=.85+.15*np.sin(t*31)*np.sin(t*7.3)
    pg(d,[(cx-18,cy),(cx+18,cy),(W+200,H+60),(-200,H+60)],(255,240,200),.10*fl); pg(d,[(cx-8,cy),(cx+8,cy),(W*.72,H+60),(W*.28,H+60)],(255,244,214),.10*fl)
    r=np.random.default_rng(3)
    for k in range(110): u=r.uniform(.1,1.)**.7; xx=lerp(cx,r.uniform(-100,W+100),u)+8*np.sin(t*.6+k); yy=lerp(cy,H+40,u)+5*np.cos(t*.5+k*2); dot(d,xx,yy,r.uniform(.8,2.4)*(.4+u),(255,246,220),.55*(.5+.5*np.sin(t*1.1+k*1.7))*fl)
    d.rectangle([(cx-170)*Q,(cy-70)*Q,(cx+170)*Q,(cy+80)*Q],fill=(20,20,26,255)); d.rectangle([(cx-60)*Q,(cy-34)*Q,(cx+60)*Q,(cy+34)*Q],fill=(34,34,42,255))
    for sx in (-96,96):
        rx,ry=cx+sx,cy-132; d.ellipse([(rx-72)*Q,(ry-72)*Q,(rx+72)*Q,(ry+72)*Q],fill=(24,24,30,255),outline=(70,66,60,255),width=int(3*Q))
        for q in range(6): an=t*(2.4 if sx<0 else -2.4)+q*np.pi/3; ln(d,[(rx,ry),(rx+np.cos(an)*66,ry+np.sin(an)*66)],(70,66,60),1.,3)
        dot(d,rx,ry,10,(70,66,60),1.)
    ln(d,[(cx-96,cy-60),(cx-30,cy-30),(cx+30,cy-30),(cx+96,cy-60)],(60,52,40),1.,5)
    for rad,al in ((120,.10),(70,.18),(40,.35),(22,.8),(12,1.)): dot(d,cx,cy,rad*(1+.04*np.sin(t*23)),(255,244,214),al*fl)
    return im,d
def tickle(d,t,a,x=640,y=470):
    w=np.sin(t*17)*.6; kid(d,x-70,y,150,(60,104,204),a,lean=.35); kid(d,x+70,y+4*np.sin(t*21),150,(200,72,44),a,lean=.25*np.sin(t*13))
    ln(d,[(x-40,y-70),(x+30+6*w,y-58+6*w)],(60,104,204),a,6)
    for k in range(5): an=-1.2+k*.5+w*.3; spark(d,x+70+np.cos(an)*(96+10*np.sin(t*9+k)),y-120+np.sin(an)*60-20,4.5,a*(.5+.5*np.sin(t*11+k)))
def sc_cinema(t):
    c=[cue('k1',0),cue('k1',1),cue('k1',2),cue('k2',0),cue('k2',1),cue('k2',2)]; a_in=ramp(t,c[0]-.5,c[0]+.5); out=1-ramp(t,cue('f1',0)-1.1,cue('f1',0)-.4)
    rev=ramp(t,c[1]+.6,c[1]+1.4)*(1-ramp(t,c[2]-.2,c[2]+.6))
    if t<c[4]-.5:
        if rev>.5: im,d=booth(t); tab(d,44,54,'a lamp, a strip of film, dust in the beam',26,ramp(t,c[1]+3.2,c[1]+4.),INK); tab(d,44,108,'only a picture',24,ramp(t,CE('k1',1)-3.,CE('k1',1)-2.2),SOFT)
        else:
            calm=ramp(t,c[2],c[3]+2); turn=-ramp(t,c[1]-.2,c[1]+.6)*(1-ramp(t,c[2]-.2,c[2]+.6)); scr=None
            if t>c[3]+1.5: scr=sc_beach(cue('w2',1)+1.+((t-c[3])*.9)%9)
            im,d=cinema(t,calm,turn,scr); tab(d,44,40,'at the cinema',26,ramp(t,c[0]+.4,c[0]+1.2)*(1-ramp(t,c[1]-.5,c[1])),INK)
            tab(d,44,40,'the people on the screen cannot see you',24,ramp(t,CE('k2',0)-4.,CE('k2',0)-3.2),INK)
        sw=1-abs(2*ramp(t,c[1]+.6,c[1]+1.4)-1); sw=max(sw,1-abs(2*ramp(t,c[2]-.2,c[2]+.6)-1))
        if sw>.02: D(im).rectangle([0,0,W*Q,H*Q],fill=(6,6,10,A_(sw)))
        f=1-a_in
        if f>.01: D(im).rectangle([0,0,W*Q,H*Q],fill=NIGHT+(A_(f),))
        return fin(im)
    # on the beach, the others can surprise you
    im=canvas(); d=D(im); a=ramp(t,c[4]-.5,c[4]+.4)*out; hz=232
    pg(d,[(0,0),(W,0),(W,hz),(0,hz)],(232,238,236),a*.9)
    for k in range(7): y=hz+8+k*20; pts=[(x,y+5*np.sin(x*.012+t*(1.1+.12*k)+k*1.7)) for x in range(0,W+20,20)]; pg(d,pts+[(W,y+34),(0,y+34)],tuple(int(lerp(c_,p_,.18*k)) for c_,p_ in zip(SEA,(214,232,226))),a*.92)
    pg(d,[(0,hz+150),(W,hz+150),(W,600),(0,600)],SAND,a)
    s5=ramp(t,c[5]-.3,c[5]+.5); tk=ramp(t,c[4]+5.6,c[4]+6.4)
    tickle(d,t if tk>0 else 0,a*(1-.0*s5),x=lerp(640,330,ez(s5)))
    tab(d,44,54,'they can surprise you',28,a*ramp(t,c[4]+3.2,c[4]+4.)*(1-s5),INK); tab(d,44,110,'you cannot tickle yourself',26,a*ramp(t,c[4]+7.6,c[4]+8.4)*(1-s5),WARM)
    tab(d,W-44,560,'Blakemore, Wolpert & Frith, Nature Neuroscience, 1998',19,a*ramp(t,c[4]+8.,c[4]+8.8)*(1-s5),SOFT,anchor='rd')
    if s5*a>.02:
        tab(d,640,150,'a tickle is evidence',34,a*s5,INK,RG); r1=ramp(t,CE('k2',2)-5.2,CE('k2',2)-4.2); r2=ramp(t,CE('k2',2)-2.6,CE('k2',2)-1.6)
        arrow(d,(720,330),(1040,330),WARM,a*s5*r1,4,r1); tab(d,760,268,'you are real because they are',24,a*s5*r1,WARM); arrow(d,(1040,400),(720,400),VIR,a*s5*r2,4,r2); tab(d,760,424,'they are real because you are',24,a*s5*r2,VIR)
        tab(d,W-44,560,'“All real living is meeting.” Martin Buber, 1923',20,a*s5*r2,SOFT,anchor='rd')
    return fin(im)
_CUTS=None
def sc_fourth(t):
    global _CUTS
    c=[cue('f1',i) for i in range(4)]; a=ramp(t,c[0]-.5,c[0]+.5); out=1-ramp(t,cue('w6',0)-1.2,cue('w6',0)-.5)
    if t<c[1]-.4:
        im,d=booth(t); tab(d,44,54,'this voice is not a person',30,ramp(t,c[0]+3.4,c[0]+4.2),INK); tab(d,44,112,'this film was put together with a machine',24,ramp(t,c[0]+5.8,c[0]+6.6),SOFT); tab(d,44,160,'it has read a great deal about beaches. It has never been cold.',22,ramp(t,CE('f1',0)-3.6,CE('f1',0)-2.8),SOFT)
        f=1-a
        if f>.01: D(im).rectangle([0,0,W*Q,H*Q],fill=PAPER+(A_(f),))
        return fin(im)
    im=Image.new('RGB',(W*Q,H*Q),NIGHT); d=D(im); s1=win(t,c[1]-.4,c[2]-.4,.6)
    if s1>.02:
        lid(im,d,430,150,420,s1); d=D(im); tab(d,430,470,'all lid',34,s1*ramp(t,c[1]+.6,c[1]+1.4),INK,RG); tx(d,640,560,'a film telling you to go and play, written with something that cannot go down to the sand',21,(170,178,190),s1*ramp(t,c[1]+3.,c[1]+3.8),'ma')
    s2=win(t,c[2]-.4,c[3]-.3,.6)
    if s2>.02:
        if _CUTS is None: _CUTS=[Image.open(S+f'/cut{i}.jpg').convert('RGB') for i in (1,2,3)]
        notes=('“needs to be even clearer”','“it feels like it is too fast”','“we need some more elegance”')
        for i,(th,nt) in enumerate(zip(_CUTS,notes)):
            g=ramp(t,c[2]+5.4+i*2.2,c[2]+6.2+i*2.2)*s2; x=80+i*390; y=170; w_=340; h_=int(w_*9/16)
            if g>.02:
                d.rectangle([(x-8)*Q,(y-8)*Q,(x+w_+8)*Q,(y+h_+8)*Q],fill=(246,240,226,A_(g))); im.paste(th.resize((w_*Q,h_*Q),Image.LANCZOS),(x*Q,y*Q),Image.new('L',(w_*Q,h_*Q),A_(g))); d=D(im)
                tx(d,x,y+h_+22,('first','second','third')[i]+' cut',22,PALE,g,'la'); tx(d,x,y+h_+56,nt,24,GOLD,g*ramp(t,c[2]+6.4+i*2.2,c[2]+7.+i*2.2),'la')
        tx(d,80,96,'The film is not the machine’s',33,PALE,s2,'ls'); tx(d,80,520,'the notes are his',20,(170,178,190),s2*ramp(t,CE('f1',2)-2.,CE('f1',2)-1.2),'la')
    s3=ramp(t,c[3]-.3,c[3]+.5)*out
    if s3>.02:
        kid(d,520,440,170,(60,104,204),s3); 
        for rad,al in ((90,.10),(52,.2),(30,.4),(16,.9)): dot(d,770,330,rad*(1+.04*np.sin(t*9)),(255,244,214),al*s3)
        ln(d,[(600,330),(700,330)],GOLD,s3,3); tx(d,640,150,'It took two.',64,PALE,s3*ramp(t,c[3]+2.2,c[3]+3.),'ma',RG)
    if out<.99: D(im).rectangle([0,0,W*Q,H*Q],fill=NIGHT+(A_(1-out),))
    return fin(im)
def sc_dawn(t):
    c=[cue('w6',i) for i in range(3)]; s1=ramp(t,c[1]-.6,c[1]+.3); s2=ramp(t,c[2]+2.2,c[2]+4.0)
    if s1<=0:
        u=ramp(t,c[0]-.6,c[1]); im,v=photo(1.02+.10*ez(u),.80,.44,warm=.55); d=D(im); f=1-ramp(t,c[0]-.6,c[0]+.6)
        if f>.01: d.rectangle([0,0,W*Q,H*Q],fill=NIGHT+(A_(f),))
        tab(d,44,60,'somewhere again',32,ramp(t,c[0]+.4,c[0]+1.2)); tab(d,44,118,'not everywhere, not nowhere, and not quite where you were',22,ramp(t,c[0]+2.8,c[0]+3.6),SOFT)
        return fin(im)
    if s2<1:
        im=wood(); d=D(im); SC=scatter(); sh=ramp(t,c[1]+.2,c[1]+2.0); hd=ez(ramp(t,c[1]+5.2,c[1]+6.6)); zm=ez(ramp(t,c[2]+.2,c[2]+3.6)); K=10
        lid(im,d,int(lerp(860,1320,ez(sh))),150,330,1.)
        for k in range(24):
            if k==K: continue
            sx,sy,sa=SC[k]; put_piece(im,k,sx,sy,sa,.34,1.-.7*zm)
        sx,sy,sa=SC[K]; put_piece(im,K,lerp(sx,W/2,hd),lerp(sy,330,hd),sa*(1-hd),lerp(.34,lerp(.9,5.2,zm),hd),1.,lift=hd*(1-zm))
        tab(d,44,54,'the lid is on the shelf',26,ramp(t,c[1]+2.0,c[1]+2.8)*(1-zm),SOFT); tab(d,44,104,'one piece is in your hand',28,ramp(t,c[1]+6.2,c[1]+7.0)*(1-zm),INK)
        f=1-ramp(t,c[1]-.6,c[1]+.3); 
        if s2>0: 
            im2,v=photo(1.5,.80,.44,warm=.55); im=Image.blend(im,im2,s2); d=D(im)
        tab(d,44,60,'Go down again.',44,ramp(t,c[2]+3.0,c[2]+3.8),INK,RG)
        return fin(im)
    u=ramp(t,c[2]+4.0,TOTAL); im,v=photo(1.5+.25*ez(u),.80,.44,warm=.55); d=D(im); tab(d,44,60,'Go down again.',44,1.,INK,RG); k=ramp(t,CE('w6',2)+1.,CE('w6',2)+2.); tab(d,44,134,'Photograph and film: Alexander Sabine',19,k,SOFT)
    return fin(im)

# ================= particles: in action, and on action =================
import cv2
_SD=np.load(S+'/sand.npz'); SF=_SD['frames']; SSH=_SD['shade']; SJ=json.load(open(S+'/sand.json')); FEET=np.array(SJ['feet']); SLOW=np.array(SJ['slow']); SWX,SWY,SSEA=1600,900,210
SIM0=cue('r1',0)-.5
def simf(t): return int(np.clip((t-SIM0)*24,0,len(SF)-1))
def swave(ts): return SSEA+40*max(0.,np.sin(2*np.pi*ts/7.3))**1.4+7*np.sin(2*np.pi*ts/2.9)
def sproj(pts,cam,m,ow,oh):
    cx,cy,s=cam; sc=ow/(W*Q); X=(pts[:,0]-cx)*s*Q*sc+ow/2; Y=(pts[:,1]-cy)*s*Q*sc+oh/2
    if m>0:
        th=np.radians(14); vx=pts[:,0]-800.; vy=pts[:,1]-1350.; vz=-520.
        vf=np.maximum(-vy*np.cos(th)-vz*np.sin(th),1.); vu=-vy*np.sin(th)+vz*np.cos(th)
        px=ow/2+620*Q*sc*vx/vf; py=200*Q*sc-620*Q*sc*vu/vf; X=X+(px-X)*m; Y=Y+(py-Y)*m
    return X,Y
def _splat(X,Y,w,ow,oh,sig):
    m=np.zeros((oh,ow),np.float32); ix=np.rint(X).astype(np.int32); iy=np.rint(Y).astype(np.int32); ok=(ix>=0)&(ix<ow)&(iy>=0)&(iy<oh)
    np.add.at(m,(iy[ok],ix[ok]),w[ok]); return cv2.GaussianBlur(m,(0,0),max(.6,sig))
def topkid(dr,x,y,hd,r,col,a=1.):
    """A child seen from above: shadow, shoulders, head, in screen pixels."""
    c,s_=np.cos(hd),np.sin(hd); A=A_(a)
    def el(cx,cy,rx,ry,fill):
        pts=[(cx+rx*np.cos(q)*c-ry*np.sin(q)*(-s_)*-1+0, cy+rx*np.cos(q)*s_+ry*np.sin(q)*c) for q in np.linspace(0,2*np.pi,24)]; dr.polygon(pts,fill=fill)
    el(x+r*.35,y+r*.45,r*.62,r*1.0,(60,44,24,int(A*.30))); el(x,y,r*.55,r*.95,col+(A,)); dr.ellipse([x-r*.36,y-r*.36,x+r*.36,y+r*.36],fill=tuple(min(255,int(v*1.12)) for v in col)+(A,))
def sandframe(t,fi,cam,m=0.,memory=0.,ow=W*Q,oh=H*Q,trails=0.,ghost=None,walkers=True,vign=0.,glowk=1.):
    P=SF[fi,:,:2]; sp=SF[fi,:,2]; sh_=SSH
    if m>0: P=np.vstack([P,P+[SWX,0.],P-[SWX,0.]]); sp=np.concatenate([sp,sp*0,sp*0]); sh_=np.concatenate([SSH,SSH,SSH])
    sc=ow/(W*Q); X,Y=sproj(P,cam,m,ow,oh)
    s_eff=cam[2]*(1-m)+ .62*m; sig=max(.8,s_eff*Q*sc*R0g*.5)
    img=np.empty((oh,ow,3),np.float32); img[:]=np.array([206,180,128],np.float32)
    yy=np.linspace(0,1,oh,dtype=np.float32)[:,None,None]; img*=(.94+.08*yy)
    one=np.ones(len(P),np.float32); norm=2*np.pi*sig*sig
    cnt=_splat(X,Y,one,ow,oh,sig); body=np.clip((cnt*norm-.35)/.4,0,1); shd=np.clip((_splat(X+sig*.7,Y+sig*1.0,one,ow,oh,sig*1.15)*norm*1.3-.3)/.5,0,1)
    shv=_splat(X,Y,sh_,ow,oh,sig)/np.maximum(cnt,1e-6); g1=np.array([244,228,186],np.float32); g2=np.array([222,192,134],np.float32)
    gc=g1[None,None,:]*(1-shv[:,:,None])+g2[None,None,:]*shv[:,:,None]; light=np.clip(_splat(X-sig*.5,Y-sig*.6,one,ow,oh,sig*.55)*2*np.pi*(sig*.55)**2-.5,0,1)
    img*=(1-.30*shd[:,:,None]); img=img*(1-body[:,:,None])+gc*body[:,:,None]; img+=light[:,:,None]*np.array([16,14,10],np.float32)
    if glowk>0:
        gs=sig*2.4; gl=np.clip(_splat(X,Y,np.minimum(sp/3.,1.).astype(np.float32),ow,oh,gs)*2*np.pi*gs*gs,0,1.4); img+=gl[:,:,None]*np.array([90,62,10],np.float32)*glowk
    if memory>0:
        gy_=img.mean(2,keepdims=True); img=img+(gy_*np.array([1.10,1.0,.84],np.float32)-img)*(.75*memory)
    if vign>0:
        Y2,X2=np.mgrid[0:oh,0:ow].astype(np.float32); r2=((X2/ow-.5)**2+(Y2/oh-.5)**2)*2.2; img*=(1-vign*np.clip(r2,0,1)**1.3)[:,:,None]
    im=Image.fromarray(np.clip(img,0,255).astype(np.uint8)); dr=ImageDraw.Draw(im,'RGBA')
    ts=(fi/24.); xs=np.arange(-40,SWX+81,40.) if m<=0 else np.arange(-4000,SWX+4001,40.)
    wl=np.stack([xs,[swave(ts)+6*np.sin(x*.011+ts*1.3) for x in xs]],1); far=np.stack([xs[::-1],np.full(len(xs),-6000.)],1)
    sx,sy=sproj(np.vstack([wl,far]),cam,m,ow,oh); seacol=tuple(int(v*(1-.25*memory)+v*.0) for v in (72,140,146))
    dr.polygon(list(zip(sx,sy)),fill=seacol+(int(205),)); dr.line(list(zip(sx[:len(xs)],sy[:len(xs)])),fill=(255,253,246,int(230*(1-.4*memory))),width=int(4*Q*sc))
    rr=np.random.default_rng(int(ts*6))
    for _ in range(40):
        u=rr.uniform(0,1); x=rr.uniform(0,SWX); y=swave(ts)-rr.uniform(4,140); px,py=sproj(np.array([[x,y]]),cam,m,ow,oh); dr.ellipse([px[0]-2*Q*sc,py[0]-1*Q*sc,px[0]+2*Q*sc,py[0]+1*Q*sc],fill=(255,255,255,int(110*(1-memory*.6))))
    if m>.02:
        hx,hy=sproj(np.array([[x_,-60000.] for x_ in (-20000.,800.,20000.)]),cam,m,ow,oh); hz=float(hy[1])
        sky=Image.new('RGBA',(ow,max(1,int(hz))),(0,0,0,0)); sd=ImageDraw.Draw(sky)
        for k in range(0,max(1,int(hz)),4): f=k/max(1,hz); sd.rectangle([0,k,ow,k+4],fill=(int(lerp(150,236,f)),int(lerp(176,226,f)),int(lerp(206,206,f)),int(255*min(1,m*1.6))))
        im.paste(sky,(0,0),sky); dr=ImageDraw.Draw(im,'RGBA')
    if trails>0:
        for w,col in ((0,(60,104,204)),(1,(13,122,112)),(2,(200,72,44))):
            n=max(2,int(len(FEET)*min(1.,trails))); tx_,ty_=sproj(FEET[:n,w],cam,m,ow,oh); dr.line(list(zip(tx_,ty_)),fill=GOLD+(230,),width=int(3.2*Q*sc)); dr.line(list(zip(tx_,ty_)),fill=col+(150,),width=int(1.2*Q*sc))
    if walkers:
        for w in range(3):
            p=FEET[fi,w]; q=FEET[max(0,fi-6),w]; hd=np.arctan2(p[1]-q[1],p[0]-q[0])+np.pi/2; px,py=sproj(p[None,:],cam,m,ow,oh)
            topkid(dr,float(px[0]),float(py[0]),hd,RFg*cam[2]*Q*sc,KC[[0,2,1][w]])
    if ghost is not None:
        gx,gy,ga=ghost; px,py=sproj(np.array([[gx,gy]]),cam,m,ow,oh); r=RFg*cam[2]*Q*sc*1.05
        for q in np.linspace(0,2*np.pi,18,endpoint=False): dr.arc([px[0]-r,py[0]-r,px[0]+r,py[0]+r],np.degrees(q),np.degrees(q)+11,fill=(255,253,246,A_(ga)),width=int(2.4*Q*sc))
    return im
R0g=6.2; RFg=30.
def follow(fi):
    lo=max(0,fi-30); p=FEET[lo:fi+1,0].mean(0); s=2.35; hw=W/2/s; hh=H/2/s
    return (float(np.clip(p[0],hw,SWX-hw)),float(np.clip(p[1],300,SWY-hh)),s)
def sc_rin(t):
    c=[cue('r1',i) for i in range(2)]; fi=simf(t); im=sandframe(t,fi,follow(fi),vign=.55); d=D(im)
    a=ramp(t,c[0]-.6,c[0]+.4); out=1-ramp(t,cue('w3',0)-1.1,cue('w3',0)-.4)
    tab(d,44,54,'reflection-in-action',32,ramp(t,c[0]+.6,c[0]+1.4),INK,RG); tab(d,44,116,'thinking while doing, from inside the thing you are changing',22,ramp(t,c[0]+5.2,c[0]+6.),SOFT)
    sl=float(SLOW[fi,0]); k=ramp(t,c[1]-.2,c[1]+.6)
    if k>.02:
        x0,y0=W-300,52; d.rectangle([(x0-14)*Q,(y0-14)*Q,(x0+256)*Q,(y0+66)*Q],fill=PAPER+(int(232*k),)); tx(d,x0,y0,'your pace',20,SOFT,k,'la'); rect(d,x0,y0+26,x0+240,y0+40,HAIR,k,2); rect(d,x0,y0+26,x0+240*(sl-.45)/.25,y0+40,VIR,k,2)
        tx(d,x0+240,y0+46,'slower where the sand is deep',16,SOFT,k*ramp(t,c[1]+1.2,c[1]+2.),'ra')
    tab(d,44,166,'the sand pushes back',24,ramp(t,c[1]+1.6,c[1]+2.4),VIR); tab(d,44,214,'nobody here can see the whole beach',22,ramp(t,c[1]+3.8,c[1]+4.6),SOFT); tab(d,44,256,'everybody here can change it',22,ramp(t,CE('r1',1)-2.2,CE('r1',1)-1.4),SOFT)
    tab(d,W-44,560,'Donald Schön, The Reflective Practitioner, 1983',19,ramp(t,c[0]+1.,c[0]+1.8),SOFT,anchor='rd'); note(d,'the sand: our own particle simulation',ramp(t,c[0]+2.,c[0]+2.8))
    if a<.99: d.rectangle([0,0,W*Q,H*Q],fill=PAPER+(A_(1-a),))
    if out<.99: d.rectangle([0,0,W*Q,H*Q],fill=PAPER+(A_(1-out),))
    return fin(im)
FIT=(800.,450.,.8)
def sc_ron(t):
    c=[cue('r2',i) for i in range(5)]; fF=len(SF)-1; a=ramp(t,c[0]-.6,c[0]+.4); out=1-ramp(t,cue('h1',0)-1.2,cue('h1',0)-.5)
    if c[2]-.4<=t<c[3]-.4:
        k=win(t,c[2]-.4,c[3]-.4,.5); L=sandframe(t,120+int((t-c[2])*24)%(len(SF)-121),follow(120+int((t-c[2])*24)%(len(SF)-121)),ow=W*Q//2,oh=H*Q,vign=.4)
        Rm=sandframe(t,fF,(800.,560.,1.05),memory=1.,ow=W*Q//2,oh=H*Q,trails=1.,walkers=False,glowk=0.)
        im=Image.new('RGB',(W*Q,H*Q)); im.paste(L,(0,0)); im.paste(Rm,(W*Q//2,0)); d=D(im); ln(d,[(W/2,0),(W/2,H)],GOLD,1.,3)
        tab(d,30,54,'in the moment',30,k,VIR,RG); tab(d,30,108,'you can affect the world around you',22,ramp(t,c[2]+2.,c[2]+2.8),INK)
        tab(d,W/2+30,54,'afterwards',30,k,WARM,RG); tab(d,W/2+30,108,'you can only reflect back on it',22,ramp(t,CE('r2',2)-3.,CE('r2',2)-2.2),INK)
        return fin(im)
    m=ez(ramp(t,c[3]-.2,c[3]+3.2)); rise=ez(ramp(t,c[0]-.4,c[0]+3.)); cam=(800.,lerp(520.,450.,rise),lerp(1.15,.8,rise))
    gh=None; gk=ramp(t,c[1]+5.,c[1]+5.6)*(1-ramp(t,c[2]-1.,c[2]-.5))
    if gk>0: u=ramp(t,c[1]+5.,c[2]-.6); gh=(lerp(380,1240,u),620+70*np.sin(u*6),gk)
    im=sandframe(t,fF,cam,m=m,memory=1.,trails=ramp(t,c[1]+.4,c[1]+4.6),ghost=gh,walkers=False,glowk=0.,vign=.25); d=D(im)
    tab(d,44,54,'reflection-on-action',32,ramp(t,c[0]+.8,c[0]+1.6)*(1-ramp(t,c[3]-.6,c[3]-.1)),INK,RG); tab(d,44,116,'thinking it over afterwards, from outside',22,ramp(t,c[0]+3.,c[0]+3.8)*(1-ramp(t,c[1]-.4,c[1])),SOFT)
    tab(d,44,116,'every footprint, every turn',22,ramp(t,c[1]+2.,c[1]+2.8)*(1-ramp(t,c[2]-.8,c[2]-.4)),SOFT); tab(d,44,166,'reach down and push: nothing moves',24,gk,WARM)
    if m>.02:
        pg(d,[(0,H),(0,606),(110,574),(236,560),(330,584),(440,640),(560,H)],(38,42,52),m); kid(d,236,562,96,(30,34,44),m)
        tab(d,44,54,'from the mountain',30,ramp(t,c[3]+2.2,c[3]+3.),INK,RG); tab(d,44,108,'you can see the whole landscape',22,ramp(t,c[3]+3.,c[3]+3.8),SOFT); tab(d,44,150,'you cannot act inside it',22,ramp(t,CE('r2',3)-1.8,CE('r2',3)-1.),WARM)
    k=ramp(t,c[4]-.2,c[4]+.6)
    if k>.02:
        y=640; d.rectangle([600*Q,(y-50)*Q,1250*Q,(y+30)*Q],fill=PAPER+(int(238*k),)); arrow(d,(620,y),(1230,y),INK,k,3,ramp(t,c[4],c[4]+1.6)); ln(d,[(700,y),(900,y)],GOLD,k,7); tx(d,800,y-36,'the day',20,DGOLD,k,'ma'); dot(d,1130,y,8,WARM,k*ramp(t,c[4]+1.,c[4]+1.6)); tx(d,1130,y-36,'now',20,WARM,k*ramp(t,c[4]+1.,c[4]+1.6),'ma')
        tab(d,620,540,'memory is the same · so is time',24,k*ramp(t,c[4]+1.4,c[4]+2.2),INK)
    note(d,'the sand: our own particle simulation',ramp(t,c[0]+1.,c[0]+1.8)*(1-m))
    if a<.99: d.rectangle([0,0,W*Q,H*Q],fill=PAPER+(A_(1-a),))
    if out<.99: d.rectangle([0,0,W*Q,H*Q],fill=PAPER+(A_(1-out),))
    return fin(im)
# ================= Plato, and forgetting =================
def sil(d,x,y,s,col,a,scale_y=1.):
    body=[(x-s*.26,y),(x-s*.30,y-s*.52*scale_y),(x-s*.16,y-s*.70*scale_y),(x+s*.16,y-s*.70*scale_y),(x+s*.30,y-s*.52*scale_y),(x+s*.26,y)]; pg(d,body,col,a); dot(d,x,y-s*.88*scale_y,s*.19,col,a)
def sc_plato(t):
    c=[cue('pl',i) for i in range(3)]; a=ramp(t,c[0]-.5,c[0]+.4); out=1-ramp(t,cue('k2',0)-1.4,cue('k2',0)-.6)
    if t<c[1]-.3:
        im=Image.new('RGB',(W*Q,H*Q),(22,16,12)); d=D(im); fl=.85+.15*np.sin(t*17)*np.sin(t*5.3); climb=ez(ramp(t,c[0]+7.,CE('pl',0)-.2)); sun=ramp(t,c[0]+8.,CE('pl',0)+.2)
        pg(d,[(760,40),(1270,60),(1270,470),(760,470)],(70,44,26),a); 
        for rad,al in ((520,.10),(360,.14),(220,.22),(120,.4)): dot(d,300,470,rad*fl,(255,150,60),al*a*.5)
        for k in range(3): dot(d,300+8*np.sin(t*9+k),456-k*14,26-k*7,(255,190-k*40,80),a*fl)
        ln(d,[(160,486),(940,486)],(96,72,52),a,14)
        for i in range(4):
            px=180+((t*38+i*190)%760); sil(d,px,470,72,KC[i],a); sx=780+(px-180)*.62; sil(d,sx+6*np.sin(t*13),452,170,(14,10,8),a*.85*fl*(1 if sx<1240 else 0))
        pg(d,[(0,0),(330,0),(250,150),(130,190),(0,170)],(250,236,190),a*(.5+.5*sun)); 
        for rad,al in ((240,.10),(150,.18),(80,.4)): dot(d,150,70,rad,(255,240,200),al*a*(.4+.6*sun))
        heads(d,640,6,34,a,child=1,turn=-ramp(t,c[0]+4.,c[0]+5.))
        if climb>0: x=lerp(300,150,climb); y=lerp(600,150,climb); kid(d,x,y,lerp(90,40,climb),(60,104,204),a)
        if sun>0: d.rectangle([0,0,W*Q,H*Q],fill=(255,244,214,A_(sun*.55)))
        tab(d,44,54,'the cave',30,a*ramp(t,c[0]+1.,c[0]+1.8)*(1-sun),INK,RG); tab(d,W-44,560,'Plato, Republic, book VII',19,a*ramp(t,c[0]+1.,c[0]+1.8),SOFT,anchor='rd')
        if a<.99: d.rectangle([0,0,W*Q,H*Q],fill=(0,0,0,A_(1-a)))
        return fin(im)
    if t<c[2]-.3:
        k=ramp(t,c[1]-.3,c[1]+.4)*(1-ramp(t,c[2]-.9,c[2]-.3)); im=Image.new('RGB',(W*Q,H*Q),(24,30,48)); d=D(im)
        for k2 in range(70): r=np.random.default_rng(k2); dot(d,r.uniform(0,W),r.uniform(0,250),r.uniform(.5,1.4),PALE,k*.5)
        pg(d,[(0,330),(W,310),(W,450),(0,470)],(44,70,104),k)
        for j in range(160): r=np.random.default_rng(1000+j); x=(r.uniform(0,W)+t*r.uniform(30,80))%W; y=r.uniform(330,450); dot(d,x,y,r.uniform(1,2.4),(200,220,255),k*(.3+.4*np.sin(t*3+j)**2))
        pg(d,[(0,470),(W,450),(W,H),(0,H)],(36,40,52),k)
        for i in range(6):
            x=180+i*184; dr_=ramp(t,c[1]+.8+i*.35,c[1]+3.2+i*.35); kid(d,x,520,100,KC[i],k,lean=-.45*np.sin(np.pi*dr_))
            for q in range(3): u=ramp(t,c[1]+1.+i*.35+q*.2,c[1]+3.6+i*.35+q*.2); spark(d,x-16+q*16,lerp(400,440+q*4,ez(u)),5.,k*(1-u))
        tab(d,44,54,'a river of forgetting',30,k*ramp(t,c[1]+.6,c[1]+1.4),INK,RG); tab(d,W-44,560,'Plato, Republic, book X',19,k,SOFT,anchor='rd')
        return fin(im)
    im=canvas(); d=D(im); k=ramp(t,c[2]-.3,c[2]+.4)*out; xs=[150+i*163 for i in range(7)]; ys=[440-30*np.sin(i*.9) for i in range(7)]
    ln(d,list(zip(xs,ys)),HAIR,k,4); u=ramp(t,c[2]+2.,CE('pl',2)+.4)*6; i0=min(6,int(u)); f=u-i0
    for i,(x,y) in enumerate(zip(xs,ys)): spark(d,x,y,7,k*(1. if i<=u else .25))
    kx=lerp(xs[i0],xs[min(6,i0+1)],ez(f)) if i0<6 else xs[6]; ky=lerp(ys[i0],ys[min(6,i0+1)],ez(f)) if i0<6 else ys[6]; kid(d,kx,ky-8,96,(60,104,204),k)
    tab(d,44,54,'the curriculum of being human',30,k*ramp(t,c[2]+1.4,c[2]+2.2),INK,RG); tab(d,44,108,'we forget, so that we can live it',22,k*ramp(t,CE('pl',2)-3.,CE('pl',2)-2.2),SOFT); tab(d,W-44,560,'after Ram Dass',19,k,SOFT,anchor='rd')
    if out<.99: d.rectangle([0,0,W*Q,H*Q],fill=(7,8,13,A_(1-out)))
    return fin(im)
# ================= the loud world =================
SANSB=lambda s: ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',int(s)); SANS=lambda s: ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',int(s))
TITLES=['THE AI THAT WILL REPLACE YOU','SUPERINTELLIGENCE BY 2030?','AI LORE, EXPLAINED','WE ARE NOT READY','THE LAST INVENTION','IT ALREADY KNOWS','THE TRUTH ABOUT AGI','WATCH BEFORE IT IS TOO LATE','THE MACHINE GOD','I ASKED AN AI ABOUT DEATH','THE END OF WORK','NOBODY IS TALKING ABOUT THIS']
CROWD=[(120+(i%12)*94+(47 if (i//12)%2 else 0),250+(i//12)*120) for i in range(36)]
_THUMB=None
def tile(d,im,x,y,w,i,t,a,ours=False):
    global _THUMB
    h=w*9/16; r=np.random.default_rng(i); base=tuple(int(v) for v in r.uniform(40,170,3))
    if ours:
        if _THUMB is None: _THUMB=Image.open(S+'/cut3.jpg').convert('RGB')
        im.paste(_THUMB.resize((int(w*Q),int(h*Q))),(int(x*Q),int(y*Q))); d=D(im); d.rectangle([(x-4)*Q,(y-4)*Q,(x+w+4)*Q,(y+h+4)*Q],outline=GOLD+(A_(a),),width=int(4*Q))
    else:
        d.rectangle([x*Q,y*Q,(x+w)*Q,(y+h)*Q],fill=base+(A_(a),)); d.rectangle([x*Q,(y+h*.55)*Q,(x+w)*Q,(y+h)*Q],fill=(10,10,14,A_(a*.55)))
        import textwrap as _tw; ttl=TITLES[i%len(TITLES)]; d.multiline_text(((x+8)*Q,(y+h*.58)*Q),'\n'.join(_tw.wrap(ttl,15)[:2]),font=SANSB(w*.085*Q),fill=(255,255,255,A_(a)),spacing=2*Q)
        pg(d,[(x+w/2-12,y+h*.25-14),(x+w/2-12,y+h*.25+14),(x+w/2+14,y+h*.25)],(255,255,255),a*.85); d.rectangle([x*Q,(y+h-4)*Q,(x+w*r.uniform(.1,.9))*Q,(y+h)*Q],fill=(220,30,40,A_(a)))
    v=(r.uniform(.2,3.)*(1+(t%9)*.6)) if not ours else 0; lab=('1 view' if ours else ('%.1fM views'%v))
    d.text((x*Q,(y+h+5)*Q),lab,font=SANS(w*.075*Q),fill=(200,200,206,A_(a)))
    if not ours and np.sin(t*3.1+i*1.7)>.85: dot(d,x+w-8,y+8,7,(230,30,40),a)
    return d
def sc_loud(t):
    c=[cue('l1',i) for i in range(5)]; a=ramp(t,c[0]-.5,c[0]+.5)
    if t<c[3]-.3:
        im=canvas(); d=D(im); grey=ramp(t,c[2]-.3,c[2]+.8); dim=1-.75*grey
        lit=[ramp(t,c[0]+1.2+i*.12,c[0]+1.8+i*.12) for i in range(36)]
        for i,(x,y) in enumerate(CROWD):
            for j in (i+1,i+12):
                if j<36 and lit[i]>.5 and lit[j]>.5 and abs(CROWD[j][0]-x)<160: ln(d,[(x,y-60),(CROWD[j][0],CROWD[j][1]-60)],GOLD,a*.35*dim,1.6)
        lp=ramp(t,c[1]+.2,c[1]+1.2)*(1-grey)
        for i,(x,y) in enumerate(CROWD):
            ox=lp*14*np.cos(t*2.2+i); oy=lp*8*np.sin(t*2.2+i); col=tuple(int(lerp(v,150,grey)) for v in KC[i%6]); kid(d,x+ox,y+oy,64,col,a)
            spark(d,x+ox,y+oy-62,4.5,a*lit[i]*dim)
            if lp>.05 and i%3==0: d.arc([(x-30)*Q,(y-40)*Q,(x+30)*Q,(y+6)*Q],20,320,fill=INK+(A_(a*lp*.5),),width=int(1.6*Q))
        gk=ramp(t,c[1]+3.,c[1]+5.)*(1-grey); sp_=lerp(140,44,ez(ramp(t,c[1]+3.,CE('l1',1)-2.)))
        if gk>.02:
            for x in np.arange(40,W,sp_): ln(d,[(x,140),(x,H-60)],(120,120,126),a*gk*.45,1.4)
            for y in np.arange(140,H-60,sp_): ln(d,[(40,y),(W-40,y)],(120,120,126),a*gk*.45,1.4)
        mk=ez(ramp(t,CE('l1',1)-3.4,CE('l1',1)-2.2))*(1-grey)
        if mk>.02:
            x0=lerp(W+20,520,mk); d.rectangle([x0*Q,150*Q,(x0+720)*Q,560*Q],fill=(214,60,52,A_(a*.92))); d.rectangle([(x0+40)*Q,190*Q,(x0+330)*Q,360*Q],fill=(40,70,160,A_(a))); d.rectangle([(x0+360)*Q,300*Q,(x0+680)*Q,520*Q],fill=(240,200,40,A_(a)))
            d.text(((x0+60)*Q,390*Q),'THE MAP',font=SANSB(92*Q),fill=(255,255,255,A_(a)))
        tab(d,44,54,'love matters · kindness matters',28,a*ramp(t,c[0]+4.,c[0]+4.8)*(1-ramp(t,c[1]-.5,c[1])),INK); tab(d,44,106,'nobody is doing it alone',22,a*ramp(t,CE('l1',0)-1.8,CE('l1',0)-1.),SOFT)
        tab(d,44,54,'stuck in our little loops',26,a*ramp(t,c[1]+.4,c[1]+1.2)*(1-grey),INK); tab(d,44,104,'rules and words can hold us too tightly',22,a*ramp(t,c[1]+3.2,c[1]+4.)*(1-grey),SOFT); tab(d,44,148,'the loudest maps crowd out the land',22,mk*a,WARM)
        if grey>.02: d.rectangle([0,0,W*Q,H*Q],fill=(120,120,124,A_(grey*.35))); tab(d,W/2,330,'enough of war · too much suffering',30,grey*ramp(t,c[2]+.6,c[2]+1.4),INK,anchor='ma')
        if a<.99: d.rectangle([0,0,W*Q,H*Q],fill=PAPER+(A_(1-a),))
        return fin(im)
    im=Image.new('RGB',(W*Q,H*Q),(14,14,18)); d=D(im); den=ramp(t,c[3],CE('l1',4)); w=lerp(250,150,den); gap=w*.12; cols=int(W//(w+gap))+1; scroll=max(0.,t-c[3])*lerp(30,140,den)
    hh=w*9/16+28+gap; rows=int(H//hh)+3; i=0
    for r_ in range(rows):
        for q in range(cols):
            x=gap/2+q*(w+gap); y=r_*hh-(scroll%hh); idx=abs(int(r_+scroll//hh)*cols+q)
            if np.random.default_rng(idx).random()<.55+.45*den: d=tile(d,im,x,y,w,idx,t+idx,ramp(t,c[3]+.1*(idx%7),c[3]+.6+.1*(idx%7)))
    ok=ramp(t,c[4]+.6,c[4]+1.4)
    if ok>.02:
        d.rectangle([0,0,W*Q,H*Q],fill=(0,0,0,A_(ok*.55))); d=tile(d,im,W/2-190,H/2-130,380,0,t,ok,ours=True); tab(d,W/2-190,H/2+120,'The Wall and the Beach · this film',22,ok,INK); tab(d,W/2-190,H/2+168,'yes, this film too',22,ramp(t,CE('l1',4)-1.6,CE('l1',4)-.8),WARM)
    end=ramp(t,CE('l1',4)+.4,CE('l1',4)+1.)
    if end>.01: d.rectangle([0,0,W*Q,H*Q],fill=NIGHT+(A_(end),))
    return fin(im)

def programme(t):
    if t<cue('w1',0)-.6: return sc_title(t)
    if t<cue('w2',0)-.5: return sc_wall1(t)
    if t<cue('r1',0)-.4: return sc_beach(t)
    if t<cue('w3',0)-.4: return sc_rin(t)
    if t<cue('r2',0)-.4: return sc_wall2(t)
    if t<cue('h1',0)-.5: return sc_ron(t)
    if t<cue('p1',0)-.5: return sc_house(t)
    if t<cue('q1',0)-.5: return sc_puzzle(t)
    if t<cue('s1',0)-.4: return sc_second(t)
    if t<cue('a1',0)-.5: return sc_story(t)
    if t<cue('c1',0)-.6: return sc_arch(t)
    if t<cue('w4',0)-.4: return sc_built(t)
    if t<cue('m1',0)-.4: return sc_trap(t)
    if t<cue('l1',0)-.4: return sc_meta(t)
    if t<cue('w5',0)-.4: return sc_loud(t)
    if t<cue('k1',0)-.5: return sc_night(t)
    if t<cue('pl',0)-.5: return sc_cinema(t)
    if t<cue('k2',0)-.6: return sc_plato(t)
    if t<cue('f1',0)-.5: return sc_cinema(t)
    if t<cue('w6',0)-.6: return sc_fourth(t)
    return sc_dawn(t)
def one(args):
    i,t,out=args; programme(t).save(f'{out}/{i:05d}.jpg',quality=93)
if __name__=='__main__':
    a=float(sys.argv[1]); b=float(sys.argv[2]); out=S+'/frames'; os.makedirs(out,exist_ok=True); jobs=[(i,i/FPS,out) for i in range(int(a*FPS),int(min(b,TOTAL)*FPS))]
    with Pool(os.cpu_count()) as p: p.map(one,jobs,chunksize=8)
