"""S6b -- is the canonical dial Omega = 1/pi special? A proper sweep, non-stationary bandit."""
import numpy as np, json, sys
def bandit(sched, n_arms=10, steps=2500, switch=800, seed=0, noise=0.3):
    rng=np.random.default_rng(seed); Q=np.zeros(n_arms); N=np.zeros(n_arms); tot=0.0
    mu=rng.random(n_arms)
    for t in range(steps):
        if t%switch==0 and t>0: mu=rng.random(n_arms)
        Om=sched(t,steps); lam=1/max(Om,1e-3)**2
        z=lam*(Q-Q.max()); z-=z.max(); p=np.exp(z); p/=p.sum()
        a=rng.choice(n_arms,p=p); r=rng.normal(mu[a],noise)
        N[a]+=1; Q[a]+=(r-Q[a])/N[a]; tot+=r
    return tot/steps
S=24
print("S6b  fixed-dial sweep (mean reward over %d seeds, 10-arm bandit, world ruptures every 1000 steps)"%S)
print(f"{'Omega':>8} {'1/Omega^2':>10} {'mean reward':>12} {'sem':>8}"); sys.stdout.flush()
grid=[0.15,0.20,0.25,0.28,1/np.pi,0.35,0.40,0.50,0.65,0.85,1.2,2.0]
res={}
for Om in grid:
    v=np.array([bandit(lambda t,T,o=Om:o,seed=s) for s in range(S)])
    res[round(Om,4)]=(float(v.mean()),float(v.std(ddof=1)/np.sqrt(S)))
    mark=" <- canonical 1/pi" if abs(Om-1/np.pi)<1e-9 else ""
    print(f"{Om:8.4f} {1/Om**2:10.3f} {v.mean():12.4f} {v.std(ddof=1)/np.sqrt(S):8.4f}{mark}"); sys.stdout.flush()
best=max(res,key=lambda k:res[k][0])
print(f"\n  argmax over the grid: Omega = {best}   (canonical 1/pi = {1/np.pi:.4f})")
print("\nS6c  schedules")
scheds={"fixed at the grid optimum": lambda t,T,o=best: o,
        "monotone anneal 1.0->0.15 (Sec 6 / Sec 12 i)": lambda t,T: 1.0*0.15**(t/T),
        "sawtooth: re-open at every rupture (C2)":      lambda t,T: 1.0*0.15**((t%800)/1000),
        "sawtooth with a falling envelope":             lambda t,T: (1.0*0.5**(t/T))*0.3**((t%800)/1000)}
for nm,f in scheds.items():
    v=np.array([bandit(f,seed=s) for s in range(S)])
    print(f"  {nm:46s} {v.mean():.4f} +/- {v.std(ddof=1)/np.sqrt(S):.4f}"); sys.stdout.flush()
json.dump({str(k):v for k,v in res.items()},open('/home/user/CRR/crr_v012_validation/results/dial_sweep.json','w'),indent=1)
