# Score for "More Than One Ruler": the sort plays itself. Each swap plucks the note of the child who moves down the line (E minor pentatonic, tall = high);
# a swap that sets the neighbours' score back adds a low muted note beneath it. When the line is in order it is played once, bottom to top.
import numpy as np, wave, json, os, subprocess
S=os.path.dirname(os.path.abspath(__file__)); SR=44100; BPM=72; BT=60/BPM; BAR=4*BT; rng=np.random.default_rng(16)
TM=json.load(open(S+'/timing.json')); TOTAL=TM['total']; M=json.load(open(S+'/maths.json')); N_=json.load(open(S+'/script.json')); idx={}; k=0
for c in N_: idx[c['id']]=k; k+=len(c['text'])
cue=lambda s,i: TM['cues'][idx[s]+i][0]; CE=lambda s,i: TM['cues'][idx[s]+i][1]
total=int((TOTAL+6)*SR); L=np.zeros(total); R=np.zeros(total)
def put(sig,t,pan=0.,gain=1.):
    i=int(t*SR); j=min(total,i+len(sig)); a=(pan+1)*np.pi/4
    if j>i and i>=0: L[i:j]+=sig[:j-i]*np.cos(a)*gain; R[i:j]+=sig[:j-i]*np.sin(a)*gain
m2f=lambda m:440*2**((m-69)/12)
def env(n,a,r): e=np.ones(n); a=max(1,min(a,n//2)); r=max(1,min(r,n//2)); e[:a]=np.sin(np.linspace(0,np.pi/2,a))**2; e[-r:]*=np.cos(np.linspace(0,np.pi/2,r))**2; return e
def string(m,dur,bright=.5):
    f=m2f(m); P=max(2,int(round(SR/f))); n=int(dur*SR); buf=rng.uniform(-1,1,P); buf=np.convolve(buf,np.ones(5)/5,'same')*(1-bright)+buf*bright; out=np.empty(n); k=0; g=.9972 if f<200 else .9958 if f<500 else .993
    while k<n:
        q=min(P,n-k); out[k:k+q]=buf[:q]; buf=g*.5*(buf+np.roll(buf,1)); k+=q
    return out*env(n,30,int(.25*SR))
def pad(ch,t,dur,vol):
    n=int(dur*SR); tt=np.arange(n)/SR; e=env(n,int(1.6*SR),int(2.2*SR))
    for k,m in enumerate(ch):
        f=m2f(m); s=sum(np.sin(2*np.pi*f*h*tt*(1+.0012*(k-1))+h*k)*h**-2.0 for h in range(1,7)); put(s*e*(.8+.2*np.sin(2*np.pi*.11*tt+k))*vol,t,(-.4,0,.4)[k%3])

import sys; sys.argv=['x']; sys.path.insert(0,S); import film7 as F
PENT=[52,55,57,59,62,64,67,69,71,74,76,79]                      # E minor pentatonic, low to high
def sea(t0,dur,vol,period=7.5):                                 # the sea: filtered noise that swells and falls back
    n=int(dur*SR); t=np.arange(n)/SR; X=np.fft.rfft(rng.normal(0,1,n)); f=np.fft.rfftfreq(n,1/SR); X*=np.exp(-((np.log(np.maximum(f,1))-np.log(520))/1.0)**2); x=np.fft.irfft(X,n); x/=np.abs(x).max()
    sw=(.35+.65*np.maximum(0,np.sin(2*np.pi*t/period))**2)*(.8+.2*np.sin(2*np.pi*t/(period*2.7)+1)); e=env(n,int(2.5*SR),int(3*SR)); put(x*sw*e*vol,t0,-.25); put(np.roll(x,3301)*np.roll(sw,int(.6*SR))*e*vol,t0,.25)
c=cue; CE=F.CE; w2=c('w2',0); w3=c('w3',0); h1=c('h1',0); p1=c('p1',0); s1=c('s1',0); c1=c('c1',0); w4=c('w4',0); w5=c('w5',0); w6=c('w6',0)
sea(c('w1',0)-2.5, c('r2',0)-c('w1',0)+3.0, .050); sea(w6-1.5, TOTAL-w6+1.5, .050)
for q,m in enumerate([64,71,76]): put(string(m,5.,.35)*.14,1.4+q*BT,(-.3,0,.3)[q])
ks=F.beach_model(); MEM=[]
for k,(tk,i,j,dur) in enumerate(ks):
    m=PENT[2+((i*2+k)%7)]; put(string(m,2.6,.5)*.19,tk,-.6+1.2*i/5)
    if len(MEM)<7: MEM.append(m)
while len(MEM)<7: MEM.append(PENT[2+len(MEM)])
for k,m in enumerate(MEM): put(string(m,3.2,.4)*.15,c('w3',1)+.3+k*.35,-.4+.8*k/6)
def chord(ch,t,dur,vol): pad(ch,t,dur+1.5,vol)
def walk(notes,t0,t1,vol,pan0=-.3,pan1=.3,dur=3.2,bright=.4):
    for k,m in enumerate(notes): put(string(m,dur,bright)*vol,t0+(t1-t0)*k/max(1,len(notes)-1),pan0+(pan1-pan0)*k/max(1,len(notes)-1))
def tap(t,vol,pan=0.): n=int(.05*SR); tt=np.arange(n)/SR; put((rng.uniform(-1,1,n)*np.exp(-tt*90)+.6*np.sin(2*np.pi*240*tt)*np.exp(-tt*60))*vol,t,pan)
# the house: outside, a held chord; inside, the same notes moving
chord([40,47,52,59],h1-.5,c('h1',1)-h1,.016); walk([52,59,64,59,52,59,64,67],c('h1',1)+.4,c('h1',2)-.4,.11); chord([43,50,55,59],c('h1',1)-.5,p1-c('h1',1),.016)
# the jigsaw: wood taps as pieces move; the seven notes as the bright pieces come together; two notes change places
for k in range(10): tap(p1+.6+k*.55+.1*np.sin(k*3.1),.06,-.5+k*.1)
chord([36,43,48,55],p1-.5,c('p1',2)-p1,.015); walk(MEM,c('p1',2)+3.0,c('p1',2)+7.3,.15)
for k in range(7): tap(c('p1',2)+3.1+k*4.3/6,.05,-.3+k*.1)
x_=CE('p1',2)-3.0; put(string(MEM[2]+12,2.6,.45)*.13,x_,-.2); put(string(MEM[5]+12,2.6,.45)*.13,x_+.9,.2)
chord([40,47,52,55],c('p1',2)-.5,s1-c('p1',2),.016); walk([64,62,59,57],c('p1',3)+3.0,c('p1',3)+4.4,.12,.3,-.3); walk([57,59,62,64],c('p1',3)+5.6,c('p1',3)+7.0,.12,-.3,.3)
# a day, a year, a life; then the stories
chord([40,47,52,59,64],s1-.5,c('s1',2)-s1,.016); put(string(64,4.,.4)*.14,s1+2.6,0.); walk([64,66,67,71,74,76,79],s1+3.2,s1+7.2,.10)
walk([52,59,64,67,71,76,71,67,64,59,52],c('s1',1)+4.0,c('s1',1)+8.5,.10)
chord([43,50,55,59,62],c('s1',2)-.5,c('s1',3)-c('s1',2),.016); u0=c('s1',2)+2.2
for q,m in ((.12,59),(.5,52),(.88,64)): put(string(m,4.5,.45)*.16,u0+6.8*q,0.)
walk([76,74,71,69,67,64,62,59,57,55,52],CE('s1',2)-7.2,CE('s1',2)-1.2,.10,.4,0.)
chord([36,43,48,52,55],c('s1',3)-.5,c('s1',4)-c('s1',3),.016); put(string(40,1.6,.2)*.16,c('s1',3)+1.6,-.4)
for k,m in enumerate(MEM): put(string(m,3.2,.4)*.14,c('s1',3)+7.1+k*.5,-.3+.1*k)
chord([40,47,52,59,64],c('s1',4)-.5,c1-c('s1',4),.017); put(string(MEM[0],4.,.4)*.14,c('s1',4)+.6,-.3); walk(MEM,c('s1',4)+2.2,c('s1',4)+3.6,.11)
# the wall: each stone laid is a low note; when one falls there is a lower one; then seven in a row
chord([40,47,52],c1-.5,c('c1',1)-c1,.016); t=c('c1',1)+.2; k=0
while t<c('c1',3)-.6: put(string([40,43,45,47,50,52,55][(k*3)%7],2.2,.3)*.12,t,-.6+1.2*((k*5)%9)/8); tap(t,.035,-.6+1.2*((k*5)%9)/8); k+=1; t+=.62
for k in range(5): put(string(33,2.4,.15)*.14,c('c1',2)+1.2+k*1.5,0.)
chord([36,43,48,52],c('c1',1)-.5,c('c1',3)-c('c1',1),.016); chord([40,47,52,59,64],c('c1',3)-.5,w4-c('c1',3),.018)
for i in range(7): put(string(MEM[i],4.,.45)*.14,c('c1',3)+1.0+i*.3,-.6+.2*i)
# the trap, the ruler, the night and the morning, as before
t=w4+.3; lap=0
while t<c('w4',3)-1.5:
    step=max(.16,.34-.012*lap)
    for k,o in enumerate(F.ORD_A): put(string(MEM[o],.9,.25)*(.12-.003*min(lap,20)),t+k*step,0.)
    t+=7*step+.25; lap+=1
pad([40,47,52],w4-.5,c('w4',3)-w4+1.,.018)
g0=c('w4',3)+1.0; g1=CE('w4',3)-2.2
for k,m in enumerate([52,55,57,59,62,64,67,71]): put(string(m,3.4,.4)*.13,g0+(g1-g0)*k/7,-.3+.6*k/7)
pad([45,52,57,60],c('w4',3)-.5,w5-c('w4',3)+1.,.016)
def tick(t,vol): n=int(.05*SR); tt=np.arange(n)/SR; put(np.sin(2*np.pi*1900*tt)*np.exp(-tt*120)*vol,t,.15)
tt_=w5+.4; k=0
while tt_<w5+9.5: tick(tt_,.05*max(0,1-(tt_-w5)/9.5)); k+=1; tt_+=.75 if tt_<w5+3.4 else float(np.random.default_rng(k).uniform(.2,1.4))
r2=np.random.default_rng(31); t=w5+3.6
while t<c('w5',2)-.5: m=MEM[r2.integers(7)]+12*int(r2.integers(-1,2)); put(string(m,3.6,.3)*.11,t,float(r2.uniform(-.7,.7))); t+=float(r2.uniform(.45,1.4))
for i in range(6): put(string(64+12*(i%2),4.5,.35)*.10,c('w5',1)+1.2+i*.25,-.6+1.2*i/5)
for k,o in enumerate(F.ORD_B): put(string(MEM[o]+12,3.,.45)*.14,c('w5',2)+4.2+k*2.4/7,-.2+.4*k/6)
pad([40,47,54,59],w5-.5,c('k1',0)-w5+1.,.016)
for q,m in enumerate([64,71,76]): put(string(m,5.,.4)*.15,w6+.4+q*BT,(-.3,0,.3)[q])
for k in range(6): tap(c('w6',1)+.4+k*.3,.05,-.4+k*.15)
put(string(MEM[0],5.,.45)*.16,c('w6',1)+5.4,0.); walk(MEM,c('w6',2)+.4,c('w6',2)+3.4,.12)
for q,m in enumerate([40,52,59,64]): put(string(m,7.,.4)*.15,CE('w6',2)+.8+q*.05,(-.3,-.1,.1,.3)[q])
# ---- the added scenes ----
q1=c("q1",0); a1=c("a1",0); m1=c("m1",0); k1=c("k1",0); f1=c("f1",0); lerp=lambda a_,b_,u_: a_+(b_-a_)*u_
def noise(t0,dur,vol,lo,hi,pan=0.):
    n=int(dur*SR); X=np.fft.rfft(rng.normal(0,1,n)); f=np.fft.rfftfreq(n,1/SR); X*=((f>lo)&(f<hi)); x=np.fft.irfft(X,n); x/=np.abs(x).max(); put(x*env(n,int(1.5*SR),int(2*SR))*vol,t0,pan)
# the second jigsaw: each piece laid is a note, gold high and blue low; then a rush of many puzzles; then two players, left and right
chord([40,47,52,55],q1-.5,c('q1',2)-q1,.015)
seq=F.M2['keep'][0]['seq']; t0=c('q1',2)+2.6; t1=CE('q1',2)+.6
for k,(cell,col) in enumerate(seq): put(string(PENT[(4+cell%5) if col else (cell%4)],2.4,.45)*.12,t0+(t1-t0)*k/24,-.4+.8*(cell%6)/5); tap(t0+(t1-t0)*k/24,.03)
chord([43,50,55,59],c('q1',2)-.5,c('q1',3)-c('q1',2),.015)
for k in range(48): put(string(PENT[(k*5)%12],1.2,.4)*.06,c('q1',3)+.6+k*5.9/48,-.7+1.4*((k*7)%12)/11)
chord([36,43,48,52,55],c('q1',3)-.5,c('q1',4)-c('q1',3),.015); seq=F.M2['keep'][1]['seq']; t0=c('q1',4)+.6; t1=CE('q1',4)-1.5
for k,(cell,col) in enumerate(seq): put(string(PENT[(4+cell%5) if col else (cell%4)],2.4,.45)*.12,t0+(t1-t0)*k/24,-.6 if k%2==0 else .6)
chord([40,47,52,59],c('q1',4)-.5,s1-c('q1',4),.016)
# told and told again: one phrase, six times, a little smoother each time; then many lines falling into one; then three chords; then a rising step
ph=[64,67,62,69,59,64]
for i in range(6):
    for k,m in enumerate(ph): put(string(m+int(round((1-i/5)*[0,1,-2,2,-1,0][k])),1.8,.4)*.10,a1+1.6+i*1.3+k*.16,-.6+1.2*i/5)
chord([40,47,52,55],a1-.5,c('a1',1)-a1,.015)
r3=np.random.default_rng(8)
for k in range(60): u=k/59; put(string(int(round(lerp(float(r3.integers(52,84)),64,u))),1.6,.35)*.06,c('a1',1)+.4+6.6*u,float(r3.uniform(-.7,.7))*(1-u))
chord([36,43,48,55],c('a1',1)-.5,c('a1',2)-c('a1',1),.015)
for g,ch in enumerate(([40,47,52],[40,47,52,59,64],[52,59,64,71])): chord(ch,c('a1',2)+3.2+g*1.3,5.,.013)
chord([43,50,55,59],c('a1',2)-.5,c('a1',3)-c('a1',2),.012)
for i,m in enumerate([52,55,57,59,62,64]): put(string(m,3.,.45)*.14,c('a1',3)+1.2+i*(CE('a1',3)+1.-c('a1',3)-1.2)/5,-.5+.2*i); tap(c('a1',3)+1.2+i*(CE('a1',3)+1.-c('a1',3)-1.2)/5,.05)
chord([40,47,52,59],c('a1',3)-.5,c1-c('a1',3),.016)
# the second trap: a phrase that answers itself, quieter each time; then a pendulum of two notes
for d_ in range(5):
    for k,m in enumerate([64,71,67]): put(string(m+12*(d_%2),2.,.35)*(.12*.62**d_),m1+.8+d_*1.2+k*.18,(-.5,.5)[d_%2])
chord([38,45,50,57],m1-.5,c('m1',1)-m1,.015); chord([40,47,52],c('m1',1)-.5,c('m1',2)-c('m1',1),.015)
for q in range(9): tap(c('m1',1)+1.5+q*.61,.04)
chord([45,52,57,60],c('m1',2)-.5,c('l1',0)-c('m1',2),.015)
tt=c('m1',2)+5.
while tt<CE('m1',2): ph_=np.sin((tt-c('m1',2))*1.6); put(string(59 if ph_<0 else 64,1.6,.4)*.09,tt,.6*ph_); tt+=.98
# the cinema: a storm on the screen (low noise, a few rolls of thunder), the projector's whirr when the child looks round; then the beach, and a giggle
noise(k1-.5,c('k1',1)-k1+1.5,.05,60,500); noise(c('k1',2)-.5,c('pl',0)-c('k1',2),.035,60,400); noise(c('k2',0)-.5,2.5,.03,60,400)
for th in (k1+3.2,k1+7.0,c('k1',2)+1.5): noise(th,2.6,.08,30,120)
chord([38,45,50,53],k1-.5,c('k1',1)-k1,.016)
tt=c('k1',1)+.8
while tt<c('k1',2)+.2: tick(tt,.018); tt+=1/12.
noise(c('k1',1)+.6,c('k1',2)-c('k1',1),.012,800,3000); chord([45,52,57,64],c('k1',1)+.6,c('k1',2)-c('k1',1)-1.,.012)
chord([40,47,52,59],c('k1',2)-.5,c('pl',0)-c('k1',2)-1.,.014); chord([40,47,52,59],c('k2',0)-.5,c('k2',1)-c('k2',0),.014)
sea(c('k2',1)-1.,f1-c('k2',1)+.5,.045); gt=c('k2',1)+5.6
for k in range(26): put(string(76+[0,3,5,7,3,5,8,12][k%8],.5,.6)*.10,gt+k*.13+.03*np.sin(k*2.2),-.2+.4*(k%2))
for k in range(12): put(string(76+[0,3,5,7,3,5][k%6],.5,.6)*.07,gt+5.+k*.14,.2)
chord([40,47,52,59,64],c('k2',2)-.5,f1-c('k2',2),.018); put(string(64,5.,.45)*.14,CE('k2',2)-5.2,-.4); put(string(71,5.,.45)*.14,CE('k2',2)-2.6,.4)
# the fourth wall: the whirr again; a single plain note; three notes for three cuts; then two notes together
tt=f1+.4
while tt<c('f1',1)-.4: tick(tt,.016); tt+=1/12.
noise(f1,c('f1',1)-f1,.012,800,3000); chord([40,47,52],f1-.5,c('f1',1)-f1,.014); put(string(52,6.,.3)*.13,c('f1',1)+.6,0.)
chord([36,43,48,52],c('f1',1)-.5,c('f1',2)-c('f1',1),.014); chord([40,47,52,55],c('f1',2)-.5,c('f1',3)-c('f1',2),.015)
for i,m in enumerate([59,62,64]): put(string(m,4.,.45)*.14,c('f1',2)+5.4+i*2.2,-.5+.5*i)
chord([40,47,52,59,64],c('f1',3)-.5,w6-c('f1',3),.018); put(string(64,6.,.45)*.15,c('f1',3)+2.2,-.3); put(string(71,6.,.45)*.15,c('f1',3)+2.2,.3)
# ---- in action, on action ----
r1=c('r1',0); r2=c('r2',0); SL=F.SLOW[:,0]
noise(r1-.5,c('w3',0)-r1+.5,.022,2200,7500,-.1)
tt=r1+.3; k=0
while tt<c('w3',0)-.6:
    fi=F.simf(tt); tap(tt,.05*(1.1-SL[fi]),-.2+.1*np.sin(k)); put(string(40+(k%2)*7,1.,.2)*.05,tt,0.); k+=1; tt+=.42/(SL[fi]/.6)
chord([40,47,52,59],r1-.5,c('w3',0)-r1,.014); walk([64,67,71],c('r1',1)+1.6,c('r1',1)+2.6,.10)
chord([40,47,52,55,59],r2-.5,c('r2',2)-r2,.017); put(string(76,5.,.4)*.12,r2+1.,0.)
for k in range(7): put(string(MEM[k],3.,.4)*.10,c('r2',1)+.6+k*.6,-.5+k*.15)
tt=c('r2',2)
while tt<c('r2',3)-.6: tap(tt,.04,-.6); put(string(52+(int(tt*3)%3)*3,.8,.3)*.06,tt,-.6); tt+=.45
chord([52,59,64],c('r2',2)-.3,c('r2',3)-c('r2',2),.014)
noise(c('r2',3)-.5,c('h1',0)-c('r2',3)+.4,.018,90,700,0.); chord([40,47,54,59,64],c('r2',3)-.5,c('h1',0)-c('r2',3),.016)
for i,m in enumerate([64,71,76]): put(string(m,4.,.4)*.12,c('r2',4)+i*.7,-.3+.3*i)
# ---- the loud world ----
l1=c('l1',0)
for i in range(36): put(string(PENT[3+(i*5)%8],1.6,.45)*.06,l1+1.2+i*.12,-.7+1.4*(i%12)/11)
chord([40,47,52,59,64],l1-.5,c('l1',1)-l1,.017)
for k in range(10): walk([64,67,64],c('l1',1)+.4+k*.62,c('l1',1)+.8+k*.62,.05)
for k in range(14): tick(c('l1',1)+3.+k*.25,.02)
put(string(28,3.,.15)*.20,F.CE('l1',1)-3.,0.); put(string(35,3.,.15)*.16,F.CE('l1',1)-3.,0.)
chord([38,45,50],c('l1',2)-.4,c('l1',3)-c('l1',2),.010)
def pop(t,vol,pan): n=int(.06*SR); tt_=np.arange(n)/SR; f=1300+500*rng.random(); put(np.sin(2*np.pi*f*tt_*(1+2*tt_))*np.exp(-tt_*55)*vol,t,pan)
tt=c('l1',3)
while tt<F.CE('l1',4)+.4:
    u=(tt-c('l1',3))/(F.CE('l1',4)-c('l1',3)); pop(tt,.05,float(rng.uniform(-.8,.8))); put(string(PENT[int(rng.integers(12))]+12,.6,.6)*.04,tt+.03,float(rng.uniform(-.8,.8))); tt+=max(.06,.42-.36*u)
noise(c('l1',3),F.CE('l1',4)+.4-c('l1',3),.02,300,4000)
put(string(64,4.,.45)*.13,c('l1',4)+.9,0.)
# ---- Plato ----
pl=c('pl',0)
for k in range(90): tap(pl+k*.11+.05*np.sin(k*7.1),.03*float(rng.random()),-.5)
chord([33,40,45],pl-.5,c('pl',1)-pl,.016); walk([52,55,57,59,62,64,67],pl+7.,F.CE('pl',0)-.2,.10); chord([52,59,64,71,76],F.CE('pl',0)-1.,2.6,.02)
chord([40,47,52,59],c('pl',1)-.4,c('pl',2)-c('pl',1),.014)
for k in range(40): put(string(PENT[6+int(rng.integers(6))]+12,1.4,.55)*.035,c('pl',1)+k*.13,float(rng.uniform(-.8,.8)))
for i in range(6):
    for q in range(3): put(string(MEM[(i+q)%7]+12-q*2,2.,.45)*.06,c('pl',1)+1.+i*.35+q*.2,-.6+.24*i)
chord([40,47,52,55],c('pl',2)-.4,c('k2',0)-c('pl',2)-.6,.015); u0=c('pl',2)+2.; u1=F.CE('pl',2)+.4
for k in range(7): put(string(MEM[k],3.,.45)*.13,u0+(u1-u0)*k/6,-.5+k/6)
def room(x):
    y=x.copy()
    for dl,g in ((.031,.22),(.047,.17),(.083,.12),(.139,.08)): dd=int(dl*SR); y[dd:]+=x[:-dd]*g
    return y
L=room(L); R=room(R); mx=max(np.abs(L).max(),np.abs(R).max()); st=np.stack([L,R],1)/mx*.85; n=int(TOTAL*SR); st=st[:n]; st[-int(3*SR):]*=np.linspace(1,0,int(3*SR))[:,None]
w=wave.open(S+'/song.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes()); w.close(); print('song',round(n/SR,1))
