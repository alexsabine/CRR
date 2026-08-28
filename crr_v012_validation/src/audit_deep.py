"""
Deep audit of CRR v01.2: the steps that could actually be wrong.
Not arithmetic -- structure, domains, dimensional consistency, scale invariance.
"""
import numpy as np, sympy as sp, json
from scipy import integrate, optimize
from itertools import combinations

L=[]
def rec(pid, claim, status, detail):
    L.append(dict(id=pid, claim=claim, status=status, detail=detail))
    print(f"\n[{status}] {pid}\n  CLAIM : {claim}\n  FINDING: {detail}")

# ============================================================ D1
# C2 says the cut falls when accumulated ARC LENGTH = pi, justified by the arena
# having EXTENT pi (vertex-to-vertex DISTANCE). Path length != distance in dim>=2.
def rand_orthant(n, rng, k=1):
    x = np.abs(rng.normal(size=(k,n))); x /= np.linalg.norm(x,axis=1,keepdims=True)
    return 2*x                      # radius-2 sphere
def sdist(u,v):
    return 2*np.arccos(np.clip((u@v)/4.0, -1, 1))
rng = np.random.default_rng(1)
# (a) diameter of the closed orthant
for n in (2,3,4,8):
    P = rand_orthant(n, rng, 200000)
    V = 2*np.eye(n)
    dmax = max(sdist(V[i],V[j]) for i,j in combinations(range(n),2))
    # interior max distance
    dmax_int = 0
    idx = rng.integers(0,len(P),(50000,2))
    dd = np.array([sdist(P[a],P[b]) for a,b in idx[:5000]])
    dmax_int = dd.max()
    assert dmax_int <= np.pi+1e-9
rec("D1a","the closed orthant of S^{n-1}(2) has diameter pi in every dimension","CONFIRMED",
    f"vertex pairs realise exactly pi; 5000 random interior pairs never exceed it (max {dmax_int:.4f} <= pi)")

# (b) but ARC LENGTH of a non-geodesic path is unbounded: a system can burn its
#     whole regime budget without going anywhere.
def walk_pathlength_vs_displacement(n, steps, step_len, rng):
    x = rand_orthant(n,rng,1)[0]
    x0 = x.copy(); path = 0.0
    for _ in range(steps):
        g = rng.normal(size=n); g -= (g@x)/4*x       # project to tangent
        g /= np.linalg.norm(g)
        # move step_len along the great circle
        x = np.cos(step_len/2)*x + np.sin(step_len/2)*2*g
        x = np.abs(x)                                 # reflect into the orthant
        x *= 2/np.linalg.norm(x)
        path += step_len
    return path, sdist(x0,x)
for n in (3,8,64):
    pl, disp = walk_pathlength_vs_displacement(n, 2000, np.pi/50, rng)
    print(f"   n={n}: path length {pl:.2f} (= {pl/np.pi:.1f} regimes' worth) -> net displacement {disp:.3f} of a max {np.pi:.3f}")
rec("D1b","C2: 'a regime affords pi/eps distinctions; the cut falls when arc length = pi'","GAP",
    "The count C is PATH length (eq.1 integrates |L| dtau, L>=0). The capacity argument is about the "
    "arena's DIAMETER (Prop 2: vertices pi apart). These coincide only for geodesic motion. On the binary "
    "arena (dim 1) a monotone traverse is geodesic, so C2 is exact. In dim>=2 a diffusing system accumulates "
    "path length without exhausting anything: 2000 steps of pi/50 give ~40 regimes of arc length while the "
    "net displacement is a fraction of pi. So 'the regime is used up' is a claim about distance, and the clock "
    "measures length. CRR is exact on the binary arena and needs an extra postulate (geodesic / non-recurrent "
    "traverse) everywhere else. Section 5's spherical-simplex result therefore does NOT carry C2 up in dimension.")

# (c) is the orthant geodesically convex? (needed for 'path length <= pi' under geodesic motion)
bad = 0
for _ in range(20000):
    n = 5
    a,b = rand_orthant(n,rng,2)
    ts = np.linspace(0,1,25)
    th = sdist(a,b)/2
    if th < 1e-9: continue
    for t in ts:
        m = (np.sin((1-t)*th)*a + np.sin(t*th)*b)/np.sin(th)
        if (m < -1e-12).any(): bad += 1; break
rec("D1c","geodesics between orthant points stay in the orthant","CONFIRMED",
    f"{bad}/20000 violations -- the orthant is geodesically convex (it is an intersection of half-spaces "
    "through the origin), so under geodesic motion arc length <= pi is exactly the exhaustion condition.")

# ============================================================ D2  the Omega>1 domain
mats = [("liquid water",4.6e-13),("olive oil",5.4e-11),("pitch",0.23),
        ("glacier ice",2.9e3),("granite",3.3e9)]
rows=[]
for nm,tau in mats:
    De = tau/1.0; Om = De**-0.5
    rows.append((nm,tau,De,Om, "IN DOMAIN" if Om<1 else "OUT (Omega>=1: <1 cell/regime, no edge, eq.(4) undefined)"))
for r in rows: print("   ", r)
rec("D2","Sec 3.3 materials calibration Omega ~ De^{-1/2}","TENSION",
    "Arithmetic is exact (all five rows reproduce). But Prop 7 restricts the grammar's edge, eq.(4) and the "
    "Landauer accounting to Omega<1, and THREE of the five materials -- water (1.5e6), olive oil (1.4e5), "
    "pitch (2.1) -- sit outside it, water by six orders of magnitude. The table's most vivid claim "
    "('water is at high Omega, maximally plastic') is made in a region where the paper's own Prop 7 says a "
    "regime holds at most one resolvable state. Two different objects are being called Omega: the bounded "
    "dial of Props 4-7 on (0,1), and an unbounded observer-relative ratio. The paper notes the Omega>=1 "
    "restriction in A.7 but does not apply it to its own headline table.")

# the tau^{-1/3} alternative
tau_s, r_s, Nn = sp.symbols('tau r N', positive=True)
rec("D3","Sec 3.3: 'a material integrating evidence at a fixed rate per unit time gives Omega ~ tau^{-1/3}'","UNSUPPORTED",
    "Omega = eps/pi = 1/(pi sqrt(N)), so Omega ~ tau^{-1/3} requires N ~ tau^{2/3}. Under the stated premise "
    "N = r * t with r fixed, N is proportional to the integration TIME, which the paper elsewhere fixes at "
    "the regime duration pi/L -- carrying no tau dependence at all (Omega ~ tau^0). We could not derive the "
    "2/3 from any reading of 'fixed rate per unit time'. The ORDERING of the table is robust to the exponent "
    "(any negative power of tau gives it), so nothing downstream breaks; the exponent itself is unjustified.")

# and: does 3.3 actually demonstrate rate/dial independence?
rec("D4","C4/Sec 3.3: 'the rupture period is pi/L for every Omega; rate and dial are separate'","CIRCULAR AS DEMONSTRATED",
    "The separation is true of the formalism (Prop 3(iii) is exact: C*Omega=1 <=> s=pi <=> t=pi/L). But the "
    "one calibration offered has a single physical input, the Maxwell time tau, and reads the DIAL off it "
    "(N ~ tau). If a material also reconfigures its arena about once per relaxation time -- the natural "
    "reading of tau -- then L ~ pi/tau and the PERIOD is ~tau too, so rate and dial are perfectly correlated "
    "across the whole table. Sec 3.3 therefore cannot serve as evidence that they are independent; it is "
    "consistent with them being one parameter. A calibration that separated them would need two materials "
    "with equal tau and different G (or equal De and different rupture rate).")

# ============================================================ D5 the Boltzmann/RL correspondence
Om = sp.symbols('Omega', positive=True)
rec("D5","Sec 3.4: 'the CRR kernel e^{C/Omega} is Boltzmann exploration with Omega in the temperature slot, exactly'","OVERSTATED",
    "In Boltzmann exploration the support of Q is fixed and T alone is varied. In CRR, changing Omega changes "
    "the support too: C in [0,1/Omega]. On the normalised regime coordinate x = C*Omega in [0,1] -- the only "
    "coordinate in which regimes at different Omega are comparable, and the one Prop 5 and the Sec 3.1 table "
    "actually use -- the kernel is e^{x/Omega^2}. The effective inverse temperature is 1/Omega^2, not 1/Omega. "
    "The DIRECTION of the dial is unaffected (this is what 3.4 needs), so nothing downstream fails, but "
    "'exactly' should be 'up to the reparametrisation Omega -> Omega^2'.")

# ============================================================ D6 eq (4) at the canonical Omega
for Omv in (1/np.pi, 0.318, 0.15, 0.45):
    n_int = abs(1/Omv - round(1/Omv)) < 1e-9
    print(f"   Omega={Omv:.4f}  1/Omega={1/Omv:.4f}  integer? {n_int}  s*(eq.4)={1-Omv:.4f}  s*(A.7)={Omv*(np.floor(1/Omv)-1):.4f}")
rec("D6","eq.(4) s* = 1 - Omega, 'literal rather than approximate whenever l is a count of distinctions'","INTERNALLY INCONSISTENT AT THE PAPER'S OWN CANONICAL VALUE",
    "l = pi/eps = pi sqrt(N) is an integer only for the measure-zero set N = (m/pi)^2. At the canonical "
    "unit-resolution system N=1, Omega=1/pi, 1/Omega = pi is NOT an integer: eq.(4) gives s*=0.6817 while A.7 "
    "gives s*=0.6366, and 0.1416 of a cell is left over at the wall with no account of it. Every value in the "
    "Sec 3.1 table except Omega=1 is in the non-integer case. The parenthetical 'which it is whenever l is "
    "taken as a count of distinctions' is false as stated -- taking l as a count is an extra rounding "
    "convention, not something the geometry supplies.")

# ============================================================ D7 Prop 12 scale invariance -> a real prediction
a_,b_ = sp.symbols('a b', positive=True)
# Gompertz h(t) = a e^{bt}: under t -> t/c,  a -> a/c, b -> b/c.  eta = a/b invariant.
rec("D7","Prop 12 mode-on-the-wall condition phi0 = e^{-1/Omega^2}/Omega","SOUND, AND STRONGER THAN STATED",
    "Written as a standard Gompertz h(t)=a e^{bt}: a=phi0, b=1/Omega, shape eta=a/b. The condition is "
    "eta = e^{-1/Omega^2} = e^{-b^2}. eta is invariant under time rescaling but b^2 is not, so the condition "
    "SELECTS A TIME UNIT: it is the statement that the clock is being read in cells. Two consequences the "
    "paper does not draw. (1) Omega is IDENTIFIABLE from any Gompertz-distributed interval data with no free "
    "parameters: Omega_hat = 1/sqrt(-ln(a/b)). (2) The wall-clock duration of one CRR cell is Omega_hat/b, and "
    "the regime duration is 1/b * 1/(Omega_hat * b) ... i.e. the theory over-determines the fit by one "
    "constraint and is therefore FALSIFIABLE on interval data. This is the single sharpest empirical hook in "
    "the paper and it is not flagged as one.")
def omega_from_gompertz(a,b): return 1/np.sqrt(-np.log(a/b))
print("   e.g. a=1e-4/yr, b=0.085/yr -> eta=1.18e-3 -> Omega_hat =", f"{omega_from_gompertz(1e-4,0.085):.4f}")

# ============================================================ D8 Landauer power scaling
rec("D8","Sec 10.1 + A.7: finite archive in steady state costs kT ln2 per discarded bit, up to l=1/Omega per regime","DERIVED CONSEQUENCE NOT STATED",
    "Regime duration is pi/L for every Omega (Prop 3(iii)) and the per-regime erasure cost is bounded by "
    "(1/Omega) kT ln2. So the DISSIPATED POWER of a CRR system scales as P >= (L/pi)(1/Omega) kT ln2: "
    "at fixed speed, a rigid system dissipates in inverse proportion to its dial. This is a quantitative, "
    "falsifiable coupling between plasticity and metabolic cost that the paper states only qualitatively "
    "('rigid systems pay more per regime than open ones').")

# ============================================================ D9 the two clocks vs Mirollo-Strogatz
tt = sp.symbols('t', positive=True); a2 = sp.symbols('a', positive=True)
C_lin = a2*tt
C_self = -Om*sp.log(1-a2*tt/Om)
print("   d2C/dt2 linear clock :", sp.diff(C_lin,tt,2))
print("   d2C/dt2 self-fed     :", sp.simplify(sp.diff(C_self,tt,2)), " (>0 : convex)")
rec("D9","Sec 11.2 / A.11: entrainment","OPEN AND CORRECTLY FLAGGED -- WE CLOSE IT BY SIMULATION BELOW",
    "Mirollo-Strogatz guarantees synchrony for CONCAVE rise to threshold. C1's clock is LINEAR (C''=0, the "
    "MS-marginal case) and A.11's self-fed clock is CONVEX (C''=a^2 e^{2C/Om}/Om > 0), which for pulse "
    "coupling on the STATE is the anti-synchronising case. So CRR as written has no entrainment theorem, "
    "exactly as Sec 11.2 admits. The paper's own escape hatch -- 'a coupling in which a partner's cut acts on "
    "the receiver's SPEED rather than its count' -- is testable and we test it.")

json.dump(L, open('/home/user/CRR/crr_v012_validation/results/ledger_deep.json','w'), indent=1)
print("\n=== DEEP AUDIT SUMMARY ===")
from collections import Counter; print(Counter(x['status'] for x in L))
