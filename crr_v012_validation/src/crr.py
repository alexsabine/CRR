"""Minimal, faithful implementation of the CRR v01.2 grammar."""
import numpy as np

class CRRClock:
    """C1/C2: C rises at v = L/eps cells per unit time; cut at C = 1/Omega."""
    def __init__(self, Omega, L=1.0, rise='linear', a=1.0, C0=0.0):
        self.Om, self.L, self.rise, self.a = Omega, L, rise, a
        self.C, self.n, self.v0 = C0, 0, L/(Omega*np.pi)   # eps = Omega*pi
        self.v = self.v0
    @property
    def Cstar(self): return 1.0/self.Om
    @property
    def phase(self): return self.C*self.Om            # s in [0,1]
    def rate(self):
        if self.rise == 'linear':  return self.v                     # C1
        if self.rise == 'convex':  return self.a*np.exp(self.C*self.Om)   # A.11 self-fed
        if self.rise == 'concave': return self.v*(1.6 - 1.2*self.phase)   # Mirollo-Strogatz condition
        raise ValueError(self.rise)
    def step(self, dt):
        self.C += self.rate()*dt
        if self.C >= self.Cstar:
            self.C = 0.0; self.n += 1; return True                   # a cut
        return False

def kernel_weight(C, Omega_t): return np.exp(np.clip(C/Omega_t, -700, 700))

def regime_weight(phibar, T, Ok, Ot):
    """Appendix A.2: total weight of a regime in a reconstruction at Ot (log-safe)."""
    x = 1.0/(Ok*Ot)
    return phibar*T*Ok*Ot*np.expm1(x) if x < 700 else np.inf

def log_regime_weight(phibar, T, Ok, Ot):
    x = 1.0/(Ok*Ot)
    return np.log(phibar*T*Ok*Ot) + (x + np.log1p(-np.exp(-x)) if x > 1e-6 else np.log(x))

def shares(phibars, Ts, Oks, Ot):
    lw = np.array([log_regime_weight(p,T,O,Ot) for p,T,O in zip(phibars,Ts,Oks)])
    lw -= lw.max(); w = np.exp(lw); return w/w.sum()

def grid_entropy(Om, B=200):
    x = np.linspace(0,1,B); lam = 1/Om**2
    w = np.exp(lam*(x-1)); w /= w.sum()
    return float(-(w*np.log(np.where(w>0,w,1))).sum())

def order_parameter(phases):
    z = np.exp(2j*np.pi*np.asarray(phases)); return abs(z.mean())
