# The sand, as particles (our own simulation, for the picture). Grains push each other apart; a walking child pushes grains aside,
# and is slowed by how much sand is in the way; the sea washes over the top of the beach and slowly smooths what it covers.
import numpy as np, json, sys, os
from scipy.spatial import cKDTree
S=os.path.dirname(os.path.abspath(__file__)); WX,WY=1600,900; SEA0=210; FPS=24; SUB=3; T=float(sys.argv[1]); R0=6.2; RF=30.
rng=np.random.default_rng(4)
xs=np.arange(8,WX-6,18.); ys=np.arange(SEA0-36,WY-4,15.5); X,Y=np.meshgrid(xs,ys)
P=np.stack([X.ravel()+(np.arange(X.size)//len(xs)%2)*9,Y.ravel()],1)+rng.normal(0,3.,(X.size,2)); HOME=P.copy(); V=np.zeros_like(P); N=len(P)
def wave(t): return SEA0+40*np.maximum(0,np.sin(2*np.pi*t/7.3))**1.4+7*np.sin(2*np.pi*t/2.9)
def catmull(W,u):
    W=np.asarray(W,float); n=len(W)-1; u=min(max(u,0.),1.)*n; i=min(int(u),n-1); f=u-i; p0=W[max(i-1,0)]; p1=W[i]; p2=W[i+1]; p3=W[min(i+2,n)]
    return .5*((2*p1)+(-p0+p2)*f+(2*p0-5*p1+4*p2-p3)*f*f+(-p0+3*p1-3*p2+p3)*f**3)
PATHS=[[(170,800),(330,690),(470,560),(610,430),(760,330),(900,300),(1010,380),(1080,520),(1180,640),(1330,700),(1460,600)],
       [(1500,820),(1380,760),(1240,800),(1120,720),(1000,760),(880,700),(800,780)],
       [(260,330),(380,380),(520,330),(640,400),(700,520),(620,640),(520,700)]]
SPD=[.075,.055,.065]; s=[0.,0.,0.]; out=[]; feet=[]; slow=[]
for f in range(int(T*FPS)):
    for k in range(SUB):
        t=(f+k/SUB)/FPS; tree=cKDTree(P); fac=[]
        for w in range(3):
            q=catmull(PATHS[w],s[w]); n=len(tree.query_ball_point(q,RF*1.35)); fk=1/(1+.045*n); fac.append(fk); s[w]=min(1.,s[w]+SPD[w]/FPS/SUB*fk)
            d=P-q; dist=np.hypot(d[:,0],d[:,1])+1e-6; m=dist<RF
            if m.any(): u=d[m]/dist[m,None]; over=(RF-dist[m])[:,None]; P[m]+=u*over*.55; V[m]+=u*over*.09
        pr=tree.query_pairs(2*R0,output_type='ndarray')
        if len(pr):
            a,b=pr[:,0],pr[:,1]; dd=P[a]-P[b]; dist=np.hypot(dd[:,0],dd[:,1])+1e-6; push=((2*R0-dist)/dist*.25)[:,None]*dd
            np.add.at(P,a,push); np.add.at(P,b,-push)
        wl=wave(t); wet=P[:,1]<wl; back=np.cos(2*np.pi*t/7.3)
        V[wet,1]+= -.03*back; P[wet]+=(HOME[wet]-P[wet])*.006
        V*=.80; P+=V; P[:,0]=np.clip(P[:,0],2,WX-2); P[:,1]=np.clip(P[:,1],SEA0-60,WY-2)
    out.append(P.astype(np.float32).copy()); feet.append([catmull(PATHS[w],s[w]).tolist() for w in range(3)]); slow.append(fac)
    sp=np.hypot(V[:,0],V[:,1]); out[-1]=np.concatenate([out[-1],np.minimum(sp,6)[:,None].astype(np.float32)],1)
A=np.stack(out); np.savez_compressed(S+'/sand.npz',frames=A,home=HOME.astype(np.float32),shade=rng.uniform(0,1,N).astype(np.float32))
json.dump({'feet':feet,'slow':slow,'fps':FPS,'N':N,'WX':WX,'WY':WY,'SEA0':SEA0},open(S+'/sand.json','w')); print(A.shape, 'final progress',[round(x,2) for x in s])
