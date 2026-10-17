#!/usr/bin/env python3
"""Frozen-core instrument for bottleneck challenges (2026-10-05).

Implements ONLY what CORE/MATHEMATICS.md defines, on a declared statistical carrier:
  arc C (Fisher-Rao path length / sigma), chord Cstar (geodesic distance / sigma), surplus S = C - Cstar,
  causal first-passage cuts at half-circumference on an intrinsic circle (R2), the R6 dissipation bound.
Causality rule: every quantity at time t uses samples <= t only (Embers finding 01 on the Hilbert-phase cut).
No CRR 'extra term' is invented here; if a challenge needs one, it is written in the challenge file and graded.
"""
import math
import numpy as np

# ---------- carriers: Fisher metrics and geodesic distances ----------
def fisher_length_1d(theta_path, g):
    """Arc length of a 1-parameter path under metric g(theta) (scalar Fisher information)."""
    th = np.asarray(theta_path, float)
    mid = 0.5*(th[1:]+th[:-1]); return float(np.sum(np.sqrt(g(mid))*np.abs(np.diff(th))))

def gaussian_mean_unitcov_length(mu_path):
    """Family N(mu, I): Fisher metric on the mean is Euclidean."""
    mu = np.asarray(mu_path, float); return float(np.sum(np.linalg.norm(np.diff(mu, axis=0), axis=1)))

def gaussian_mean_unitcov_chord(mu0, mu1): return float(np.linalg.norm(np.asarray(mu1)-np.asarray(mu0)))

def poisson_g(lam): return 1.0/np.asarray(lam, float)          # Fisher info of Poisson rate
def poisson_chord(l0, l1): return float(2*abs(math.sqrt(l1)-math.sqrt(l0)))   # Fisher-Rao geodesic for Poisson

def bernoulli_g(p): p = np.asarray(p, float); return 1.0/(p*(1-p))
def bernoulli_chord(p0, p1): return float(2*abs(math.asin(math.sqrt(p1))-math.asin(math.sqrt(p0))))

def gaussian_1d_meanvar_length(mu, sd):
    """Fisher-Rao arc for N(mu, sd^2) along a sampled path: ds^2 = (dmu^2 + 2 dsd^2)/sd^2."""
    mu = np.asarray(mu, float); sd = np.asarray(sd, float); smid = 0.5*(sd[1:]+sd[:-1])
    return float(np.sum(np.sqrt(np.diff(mu)**2 + 2*np.diff(sd)**2)/smid))

def gaussian_1d_meanvar_chord(mu0, sd0, mu1, sd1):
    """Closed form (hyperbolic half-plane with x = mu/sqrt2, y = sd)."""
    x0, x1 = mu0/math.sqrt(2), mu1/math.sqrt(2)
    d = math.acosh(1 + ((x1-x0)**2 + (sd1-sd0)**2)/(2*sd0*sd1)); return float(math.sqrt(2)*d)

# ---------- core quantities ----------
def surplus(C, Cstar, sigma=1.0):
    S = (C - Cstar)/sigma
    if S < -1e-9: raise ValueError("chord exceeds arc: carrier or chord formula inconsistent")
    return max(S, 0.0)

def causal_first_passages(arc_cum, half_circ):
    """R2: t_{n+1} = inf{t > t_n : s_t - s_{t_n} = a}; arc_cum is the signed unwrapped arc, sampled.
    Uses only past samples; returns indices. Interpolation checks the piecewise-linear measured path only."""
    cuts, last = [], arc_cum[0]
    for i in range(1, len(arc_cum)):
        if arc_cum[i] - last >= half_circ:
            cuts.append(i); last = arc_cum[i]
    return cuts

def r6_bound(Q, T, zeta_min, a, B, sigma=1.0):
    """Q T >= zeta_min (a + 2B)^2 = zeta_min sigma^2 (Cstar + S)^2. Returns (lhs, rhs, holds)."""
    rhs = zeta_min*(a + 2*B)**2; return float(Q*T), float(rhs), bool(Q*T >= rhs - 1e-12)

def backtrack(arc_increments):
    inc = np.asarray(arc_increments, float); return float(np.sum(np.maximum(-inc, 0)))

# ---------- native rivals (standard, for the no-CRR reduction) ----------
def thermodynamic_length_bound(L, T, friction=1.0):
    """Salamon-Berry / Sivak-Crooks: excess dissipation >= friction * L^2 / T (linear response)."""
    return friction*L**2/T

def mfpt_resetting_diffusion(x0, D, r):
    """Evans-Majumdar: mean first-passage time to the origin from x0 with Poisson resetting rate r."""
    a0 = math.sqrt(r/D); return (math.exp(a0*x0) - 1)/r

def quadratic_variation(x): return float(np.sum(np.diff(np.asarray(x, float))**2))

if __name__ == "__main__":
    # self-test against CORE numbers
    th = np.linspace(0.1, 0.11, 10001); print("bernoulli +0.01 at 0.1:", fisher_length_1d(th, bernoulli_g))
    print("poisson chord 1->4:", poisson_chord(1, 4), "arc:", fisher_length_1d(np.linspace(1, 4, 100001), poisson_g))
    mu = np.linspace(0, 1, 1001); sd = np.ones_like(mu); print("gauss meanvar arc vs chord:", gaussian_1d_meanvar_length(mu, sd), gaussian_1d_meanvar_chord(0, 1, 1, 1))
