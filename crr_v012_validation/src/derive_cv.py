"""
PURE THEORY. Touches no data.
What interval statistics does CRR v01.2 predict, and how do they differ from the
earlier canonical variant (CV = Omega/2)?
"""
import numpy as np, sympy as sp
from scipy import integrate, optimize, special

print("="*78)
print("ROUTE 1 -- v01.2 Appendix A.12: soft threshold, Gompertz interval law")
print("="*78)
# h(C) = phi0 e^{C/Om}, C grows at unit rate -> Gompertz  h(t)= a e^{bt}, a=phi0, b=1/Om
# shape eta = a/b = phi0*Om ; scale 1/b = Om
# Mode-on-the-wall (A.12): phi0 = e^{-1/Om^2}/Om   <=>   eta = e^{-1/Om^2}
def gompertz_moments(eta, b):
    """mean and sd of Gompertz  S(t)=exp(-eta(e^{bt}-1)),  h=eta*b*e^{bt}"""
    f = lambda t: eta*b*np.exp(b*t)*np.exp(-eta*(np.exp(b*t)-1))
    m1 = integrate.quad(lambda t: t*f(t), 0, 200/b, limit=400)[0]
    m2 = integrate.quad(lambda t: t*t*f(t), 0, 200/b, limit=400)[0]
    return m1, np.sqrt(max(m2-m1**2,0))
def cv_gompertz_v012(Om):
    eta = np.exp(-1/Om**2); b = 1/Om
    m,s = gompertz_moments(eta,b); return s/m, m, s, eta

# analytic small-eta asymptotics: mean ~ (1/b)(ln(1/eta) - gamma), sd ~ (1/b) pi/sqrt6
gam = np.euler_gamma
def cv_asym(Om): return (np.pi/np.sqrt(6))*Om**2 / (1 - gam*Om**2)

print(f"{'Omega':>10} {'1/Omega':>8} {'eta':>12} {'mean':>9} {'sd':>9} {'CV v01.2':>10} {'CV asym':>10} {'CV old=Om/2':>12}")
for Om in [1/np.pi, 1/(2*np.pi), 1/(3*np.pi), 0.5, 0.45, 0.318, 0.15, 0.06]:
    cv,m,s,eta = cv_gompertz_v012(Om)
    print(f"{Om:10.5f} {1/Om:8.4f} {eta:12.3e} {m:9.4f} {s:9.4f} {cv:10.5f} {cv_asym(Om):10.5f} {Om/2:12.5f}")

print("\n  asymptotic law (eta -> 0, i.e. Omega -> 0):")
print("     CV_v01.2  ->  (pi/sqrt6) * Omega^2  =  1.28255 * Omega^2      [QUADRATIC in Omega]")
print("     CV_old    =   0.5       * Omega^1                             [LINEAR   in Omega]")
print(f"  ratio Z2:SO(2)  (Omega = 1/pi vs 1/2pi):")
r012 = cv_gompertz_v012(1/np.pi)[0]/cv_gompertz_v012(1/(2*np.pi))[0]
print(f"     v01.2 : {r012:.4f}   (-> 4 exactly in the small-Omega limit)")
print(f"     old   : {0.5*(1/np.pi)/(0.5/(2*np.pi)):.4f}   (exactly 2)")

print()
print("="*78)
print("ROUTE 2 -- v01.2 Section 2.3: 'evidence arrives in quanta, so the threshold")
print("           is crossed with a modest overshoot'")
print("="*78)
# One quantum of overshoot, Bernoulli(1/2) sufficient statistic at the wall -> sd = 1/2 CELL
# mean count at the cut = C* = 1/Omega cells  =>  CV = (1/2)/(1/Omega) = Omega/2
print("  overshoot ~ one quantum, sd(overshoot) = 1/2 cell (Bernoulli(1/2), n=1)")
print("  mean count at cut     = C* = 1/Omega cells")
print("  CV = (1/2) / (1/Omega) = Omega/2                                [LINEAR   in Omega]")
print("  -> identical to the earlier canonical variant. v01.2 contains BOTH routes and")
print("     Section 2.3 asserts they are the same law ('an exponential of the same form")
print("     as the kernel gives the interval law -- Gompertz'). THEY ARE NOT.")

print()
print("="*78)
print("RECONCILIATION: what eta would the Gompertz need to reproduce CV = Omega/2?")
print("="*78)
def cv_of_eta(eta):
    m,s = gompertz_moments(eta,1.0); return s/m
for Om in [1/np.pi, 1/(2*np.pi)]:
    target = Om/2
    eta_star = optimize.brentq(lambda e: cv_of_eta(e)-target, 1e-12, 0.999999)
    mode_star = np.log(1/eta_star)            # in units of 1/b = Omega ; mode at t=Om ln(1/eta)
    wall = 1/Om                               # C* in cells ; in b-units the wall is at C*=1/Om
    print(f"  Omega={Om:.5f}: need eta = {eta_star:.4e};  mode sits at C = {mode_star:.4f} cells,")
    print(f"                 wall C* = {wall:.4f} cells  ->  mode/wall = {mode_star/wall:.4f}")
    print(f"                 (mode-on-the-wall would need eta = {np.exp(-1/Om**2):.3e})")
print("""
  So the Gompertz CAN reproduce CV = Omega/2, but only with a hazard whose mode sits
  far BEYOND the wall (mode/wall >> 1) -- i.e. a hazard so weak that the regime almost
  never ends by hazard, and the cut is effectively the hard deterministic wall of eq.(2)
  with quantal jitter. That is exactly the Section 2.3 reading. The A.12 mode-on-the-wall
  calibration is therefore NOT the right calibration for CRR: it makes rupture a
  hazard-driven event rather than a capacity-driven one, and changes the scaling law.
""")

print("="*78)
print("PRE-REGISTERED DISCRIMINATOR")
print("="*78)
print("""
  H_old   (canonical CRR, Sabine 132-system paper):  CV = Omega/2
  H_v012A (v01.2 A.12 with mode-on-the-wall)      :  CV = 1.28255 * Omega^2
  H_v012B (v01.2 Sec 2.3 quantal overshoot)       :  CV = Omega/2      == H_old

  Z2 class   Omega = 1/pi   : H_old 0.15915   H_v012A 0.12996
  SO(2) class Omega = 1/2pi : H_old 0.07958   H_v012A 0.03249
  class ratio               : H_old 2.000     H_v012A 4.000 (asymptotically)
""")
