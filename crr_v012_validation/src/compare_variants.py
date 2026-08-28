"""Dimensional and structural comparison of the CRR variants in this repository."""
import sympy as sp
T,Lm = sp.symbols('Time Length', positive=True)   # Length = Fisher-Rao distinguishability units
print("="*80); print("DIMENSIONAL AUDIT OF THE RUPTURE CONDITION C*Omega = 1 IN EACH VARIANT")
print("="*80)
def show(tag, dimC, dimOm):
    prod = sp.simplify(dimC*dimOm)
    print(f"\n  {tag}")
    print(f"    [C]      = {dimC}")
    print(f"    [Omega]  = {dimOm}")
    print(f"    [C*Om]   = {prod}   -> {'DIMENSIONLESS (consistent)' if prod==1 else 'NOT DIMENSIONLESS -- INCONSISTENT'}")

# 1. CRR_FINAL_CANONICAL Sec 1.1 + 1.4:  C = int (ds/dtau)^2 dtau ,  Omega = 1/phi_geodesic
show("CRR_FINAL_CANONICAL (Feb 2026): C = int (ds/dtau)^2 dtau, Omega = 1/phi_G",
     (Lm/T)**2*T, 1/Lm)
# 2. 132.pdf: C = int L dtau with L declared 'dimensionless rate'
show("132.pdf: C = int L dtau, L a 'mnemonic entanglement rate', C declared dimensionless",
     sp.Integer(1), sp.Integer(1))
# 3. v01.2:  C = (1/eps) int |ds/dtau| dtau  (arc length in cells) ,  Omega = eps/pi
show("v01.2: C = (1/eps) int L dtau (arc length in cells), Omega = eps/pi",
     (Lm/T)*T/Lm, Lm/Lm)

print("""
  Reading. The canonical variant's C is the ENERGY functional int (ds/dtau)^2 dtau, not
  arc length. Two consequences it does not note:
    (a) it is NOT reparameterisation invariant -- traversing the same path twice as slowly
        halves C, so 'accumulated coherence' depends on how long you take, not on what you
        distinguished;
    (b) with Omega = 1/phi_G a reciprocal length, C*Omega carries units Length/Time, so the
        rupture condition C*Omega = 1 is dimensionally ill-formed and its numerical content
        depends on the unit of time.
  The 132 paper avoids (b) by declaring C dimensionless, which is a stipulation rather than
  a derivation. v01.2 fixes both: dividing arc length by the resolution eps makes C a genuine
  pure count, and making Omega the RATIO eps/pi makes it invariant under the Cencov
  normalisation g -> c^2 g that the metric leaves free (Prop 3 iv, verified).
  This is the clearest technical advance of v01.2 over its predecessors.""")

print("\n"+"="*80); print("REPARAMETERISATION TEST, NUMERICALLY"); print("="*80)
import numpy as np
from scipy import integrate
# same geodesic path on the Bernoulli arc, traversed at two different speeds
def path(T_total):
    f = lambda t: np.pi*t/T_total                 # s(t), a full traverse of the arena
    sdot = np.pi/T_total
    C_v012 = integrate.quad(lambda t: abs(sdot), 0, T_total)[0]        # /eps later
    C_canon= integrate.quad(lambda t: sdot**2,   0, T_total)[0]
    return C_v012, C_canon
for Tt in [1.0, 2.0, 10.0]:
    a,b = path(Tt)
    print(f"  traverse duration {Tt:5.1f}:  v01.2 arc length = {a:.6f} (pi = {np.pi:.6f})   "
          f"canonical energy = {b:.6f}")
print("  -> v01.2's C is invariant under how fast the arena is crossed; the canonical C is not.")
print("     Since the whole framework says the cut falls when the arena is USED UP, invariance")
print("     is the property it needs. v01.2 has it; its predecessors did not.")
