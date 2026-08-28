"""
S1 -- Does a population of CRR clocks entrain, and under which coupling?

Section 11.2 of v01.2 leaves this open: "the coupling that produces it for a CRR pair
[is left] for further work". We close it numerically. Vectorised.
"""
import numpy as np, json, sys
OUT = {}
def head(s):
    print("\n" + "=" * 80 + f"\n{s}\n" + "=" * 80); sys.stdout.flush()

def simulate(N=50, rise='linear', coupling='count', kappa=0.05, hetero=0.0,
             Om=1/np.pi, T=1200.0, dt=1e-2, tau_c=0.3, a=0.4, seed=0):
    rng = np.random.default_rng(seed)
    Cstar = 1.0/Om
    L = np.clip(1.0 + hetero*rng.normal(size=N), 0.1, None)
    v0 = L/(Om*np.pi)
    C = rng.random(N)*Cstar
    boost = np.zeros(N); Rs = []
    nst = int(T/dt); samp = max(1, nst//1500)
    for k in range(nst):
        if rise == 'linear':    rate = v0*(1+boost)
        elif rise == 'convex':  rate = a*np.exp(C*Om)*(1+boost)      # A.11 self-fed clock
        else:                   rate = v0*(1.6-1.2*C*Om)*(1+boost)   # concave: Mirollo-Strogatz
        C += rate*dt
        fired = C >= Cstar
        nf = int(fired.sum())
        if nf:
            C[fired] = 0.0
            if coupling == 'count':
                C[~fired] = np.minimum(C[~fired] + kappa*nf*Cstar, Cstar)
                ab = C >= Cstar; C[ab] = 0.0                          # absorption
            elif coupling == 'speed':
                boost[~fired] += kappa*nf
        if coupling == 'speed':
            boost *= np.exp(-dt/tau_c)
        if k % samp == 0:
            Rs.append(abs(np.exp(2j*np.pi*C*Om).mean()))
    Rs = np.array(Rs)
    return float(Rs[-max(1, len(Rs)//5):].mean())

head("S1  ENTRAINMENT OF CRR CLOCKS (N=50; R = Kuramoto order parameter of the phase C*Omega)")
print(f"{'rise':>8} {'coupling':>9} {'kappa':>6} {'hetero':>7} {'R_final':>8}   verdict"); sys.stdout.flush()
rows = []
for rise in ['linear', 'convex', 'concave']:
    for coupling, ks in [('none', [0.0]), ('count', [0.02, 0.10, 0.30]), ('speed', [0.2, 1.0, 4.0])]:
        for kap in ks:
            for het in [0.0, 0.10]:
                R = simulate(rise=rise, coupling=coupling, kappa=kap, hetero=het, seed=3)
                v = 'SYNCHRONISED' if R > 0.85 else ('partial' if R > 0.4 else '-')
                print(f"{rise:>8} {coupling:>9} {kap:6.2f} {het:7.2f} {R:8.3f}   {v}"); sys.stdout.flush()
                rows.append(dict(rise=rise, coupling=coupling, kappa=kap, hetero=het, R=R, verdict=v))
OUT['sweep'] = rows

head("S1b  The paper's own claim, checked directly (Sec 11.2): a count-advancing pulse\n"
     "     'locks them only when they begin within one pulse of each other'")
def two(dphi0, kappa, rise='linear', T=600.0, dt=5e-3, Om=1/np.pi):
    Cstar = 1/Om; v = 1/(Om*np.pi); C = np.array([0.0, dphi0*Cstar])
    for _ in range(int(T/dt)):
        rate = v*np.ones(2) if rise == 'linear' else 0.4*np.exp(C*Om)
        C = C + rate*dt
        f = C >= Cstar
        if f.any():
            C[f] = 0.0
            C[~f] = np.minimum(C[~f] + kappa*int(f.sum())*Cstar, Cstar)
            ab = C >= Cstar; C[ab] = 0.0
    d = abs(C[0]-C[1])*Om
    return min(d, 1-d)
offs = [0.02, 0.05, 0.10, 0.20, 0.35, 0.50]
print(f"{'kappa':>7} " + " ".join(f"{d:>7.2f}" for d in offs)); sys.stdout.flush()
lock = {}
for kap in [0.05, 0.10, 0.20, 0.40]:
    r = [two(d, kap) for d in offs]; lock[kap] = r
    print(f"{kap:7.2f} " + " ".join(f"{x:7.4f}" for x in r)); sys.stdout.flush()
print("  entries = final |phase difference| (0 = locked); columns = initial offset")
OUT['two_clock'] = {str(k): v for k, v in lock.items()}

head("S1c  Critical coupling under SPEED coupling (the paper's suggested escape hatch)")
ks = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
print(f"{'hetero':>7} " + "".join(f"{k:>8.2f}" for k in ks)); sys.stdout.flush()
crit = {}
for het in [0.05, 0.10, 0.20]:
    Rs = [simulate(rise='linear', coupling='speed', kappa=k, hetero=het, seed=5) for k in ks]
    print(f"{het:7.2f} " + "".join(f"{r:8.3f}" for r in Rs)); sys.stdout.flush()
    crit[het] = next((k for k, r in zip(ks, Rs) if r > 0.85), None)
print(f"\n  first kappa reaching R>0.85: {crit}")
OUT['critical'] = {str(k): v for k, v in crit.items()}

json.dump(OUT, open('/home/user/CRR/crr_v012_validation/results/entrainment.json', 'w'), indent=1)
print("\nwrote results/entrainment.json"); sys.stdout.flush()
