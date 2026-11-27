# A plain check of the "dreams against over-training" idea, in ordinary mathematics.
# A learner sees a few noisy days. It fits them by gradient descent. Two ways of going on:
#   awake only : it keeps training on the same days (its own record is the target)
#   with dreams: between passes it also trains on jumbled replays of those days (inputs perturbed, the remembered answer kept)
# We measure the error on the days themselves (the proxy it can see) and on new days from the same world (what it is for).
import numpy as np, json
rng=np.random.default_rng(11); d=40; n=30; R=200; steps=4000; lr=0.02; noise=0.6
def run(dream_sd, seed):
    r=np.random.default_rng(seed); w_true=r.normal(0,1,d)/np.sqrt(d)
    X=r.normal(0,1,(n,d)); y=X@w_true+r.normal(0,noise,n); Xt=r.normal(0,1,(4000,d)); yt=Xt@w_true
    w=np.zeros(d); tr=[]; te=[]
    for s in range(steps):
        Xb=X; yb=y
        if dream_sd>0: Xb=np.vstack([X, X+r.normal(0,dream_sd,X.shape)]); yb=np.concatenate([y,y])   # one waking pass and one dreamt pass
        w-=lr*(Xb.T@(Xb@w-yb))/len(yb)
        if s in (9,49,199,999,3999): tr.append(float(np.mean((X@w-y)**2))); te.append(float(np.mean((Xt@w-yt)**2)))
    return tr,te
out={}
for name,sd in (('awake only',0.),('with dreams',1.0)):
    T=np.array([run(sd,1000+k) for k in range(R)]); out[name]={'seen':T[:,0].mean(0).round(3).tolist(),'new':T[:,1].mean(0).round(3).tolist()}
    print(name); print('  error on the days it has seen :',out[name]['seen']); print('  error on new days             :',out[name]['new'])
# ridge with the matching penalty: Bishop (1995) says input noise of variance s2 acts like a penalty s2*|w|^2 (here on half the data)
def ridge(seed,lam):
    r=np.random.default_rng(seed); w_true=r.normal(0,1,d)/np.sqrt(d); X=r.normal(0,1,(n,d)); y=X@w_true+r.normal(0,noise,n); Xt=r.normal(0,1,(4000,d)); yt=Xt@w_true
    w=np.linalg.solve(X.T@X/n+lam*np.eye(d),X.T@y/n); return float(np.mean((Xt@w-yt)**2))
out['ridge, matching penalty 0.5']=round(float(np.mean([ridge(1000+k,0.5) for k in range(R)])),3); out['baseline: guess nothing']=round(float(np.mean([np.sum((np.random.default_rng(1000+k).normal(0,1,d)/np.sqrt(d))**2) for k in range(R)])),3)
print('ridge with the matching penalty, error on new days:',out['ridge, matching penalty 0.5']); print('guessing nothing at all, error on new days:',out['baseline: guess nothing'])
out['checkpoints']=[10,50,200,1000,4000]; json.dump(out,open('check.json','w'),indent=1)
