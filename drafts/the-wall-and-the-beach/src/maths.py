# Our own simulation (illustration). Thirty noisy days, a linear learner, plain gradient descent; "dreams" are jumbled replays (inputs perturbed, remembered answers kept).
import numpy as np, json
d=40; n=30; R=200; noise=0.6; lr=0.02; pts=np.unique(np.round(np.logspace(0,np.log10(4000),70)).astype(int))
def run(sd,seed):
    r=np.random.default_rng(seed); wt=r.normal(0,1,d)/np.sqrt(d); X=r.normal(0,1,(n,d)); y=X@wt+r.normal(0,noise,n); Xt=r.normal(0,1,(3000,d)); yt=Xt@wt; w=np.zeros(d); a=[]; b=[]
    for s in range(1,4001):
        Xb,yb=(np.vstack([X,X+r.normal(0,sd,X.shape)]),np.concatenate([y,y])) if sd>0 else (X,y)
        w-=lr*(Xb.T@(Xb@w-yb))/len(yb)
        if s in pts: a.append(np.mean((X@w-y)**2)); b.append(np.mean((Xt@w-yt)**2))
    return a,b
out={'passes':pts.tolist(),'nothing':1.0}
for k,sd in (('awake',0.),('dream',1.)):
    T=np.array([run(sd,1000+i) for i in range(R)]).mean(0); out[k]={'seen':T[0].round(4).tolist(),'new':T[1].round(4).tolist()}
json.dump(out,open('maths.json','w')); print(len(pts),out['awake']['new'][-1],out['dream']['new'][-1],min(out['awake']['new']))
