"""
S1d -- corrected entrainment comparison.

Bug found in S1: heterogeneity was injected through the Fisher-Rao speed L, which the
A.11 self-fed (convex) clock does not use -- its period is (Omega/a)(1-e^{-1/Omega^2}),
set by the gain a. So every "convex" row of S1 was in fact homogeneous. Here heterogeneity
is injected into the quantity that actually sets each clock's period, per clock type.
"""
import numpy as np, json, sys
def head(s): print("\n"+"="*80+f"\n{s}\n"+"="*80); sys.stdout.flush()

def simulate(N=50, rise='linear', coupling='count', kappa=0.05, hetero=0.0,
             Om=1/np.pi, T=1200.0, dt=1e-2, tau_c=0.3, a0=0.4, seed=0):
    rng = np.random.default_rng(seed)
    Cstar = 1.0/Om
    het = 1.0 + hetero*rng.normal(size=N)
    v0 = np.clip(het, 0.1, None)/(Om*np.pi)        # linear/concave: heterogeneous speed
    a  = a0*np.clip(het, 0.1, None)                # convex: heterogeneous gain (sets its period)
    C = rng.random(N)*Cstar
    boost = np.zeros(N); Rs = []
    nst = int(T/dt); samp = max(1, nst//1500)
    for k in range(nst):
        if rise == 'linear':    rate = v0*(1+boost)
        elif rise == 'convex':  rate = a*np.exp(C*Om)*(1+boost)
        else:                   rate = v0*(1.6-1.2*C*Om)*(1+boost)
        C = C + rate*dt
        fired = C >= Cstar
        nf = int(fired.sum())
        if nf:
            C[fired] = 0.0
            if coupling == 'count':
                C[~fired] = np.minimum(C[~fired] + kappa*nf*Cstar, Cstar)
                ab = C >= Cstar; C[ab] = 0.0
            elif coupling == 'speed':
                boost[~fired] += kappa*nf
        if coupling == 'speed': boost *= np.exp(-dt/tau_c)
        if k % samp == 0: Rs.append(abs(np.exp(2j*np.pi*C*Om).mean()))
    Rs = np.array(Rs)
    return float(Rs[-max(1, len(Rs)//5):].mean())

head("S1d  ENTRAINMENT WITH HETEROGENEITY INJECTED INTO EACH CLOCK'S OWN PERIOD-SETTING TERM\n"
     "     (mean R over 5 seeds; SYNCHRONISED = R>0.85)")
print(f"{'rise':>8} {'coupling':>9} " + "".join(f"{k:>9}" for k in ['k=0.02','k=0.10','k=0.30','k=1.0','k=4.0'])
      + "   (hetero = 10%)"); sys.stdout.flush()
KS = [0.02, 0.10, 0.30, 1.0, 4.0]
rows = []
for rise in ['linear', 'convex', 'concave']:
    for coupling in ['count', 'speed']:
        Rs = []
        for kap in KS:
            r = np.mean([simulate(rise=rise, coupling=coupling, kappa=kap, hetero=0.10, seed=s)
                         for s in range(5)])
            Rs.append(r)
        print(f"{rise:>8} {coupling:>9} " + "".join(f"{r:9.3f}" for r in Rs)); sys.stdout.flush()
        rows.append(dict(rise=rise, coupling=coupling, R=[float(x) for x in Rs]))

head("S1e  same, identical clocks (hetero = 0): isolates absorption from true entrainment")
print(f"{'rise':>8} {'coupling':>9} " + "".join(f"{k:>9}" for k in ['k=0.02','k=0.10','k=0.30','k=1.0','k=4.0']))
sys.stdout.flush()
for rise in ['linear', 'convex', 'concave']:
    for coupling in ['count', 'speed']:
        Rs = [np.mean([simulate(rise=rise, coupling=coupling, kappa=kap, hetero=0.0, seed=s)
                       for s in range(3)]) for kap in KS]
        print(f"{rise:>8} {coupling:>9} " + "".join(f"{r:9.3f}" for r in Rs)); sys.stdout.flush()
        rows.append(dict(rise=rise, coupling=coupling, hetero=0.0, R=[float(x) for x in Rs]))

json.dump(rows, open('/home/user/CRR/crr_v012_validation/results/entrainment2.json', 'w'), indent=1)
print("\nwrote results/entrainment2.json"); sys.stdout.flush()
