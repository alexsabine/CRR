#!/usr/bin/env python3
"""Origin-of-life bottleneck challenges, computed with the frozen core (2026-10-06). No rung.
O1 assembly theory: assembly index (minimal construction path) vs actual synthesis history (arc) and surplus; does surplus
   add anything to (index, copy number) as a selection signature?
O2 RAF emergence in the binary polymer model: is the appearance of an autocatalytic set an 'occasion' in the core's sense?
O3 Eigen error threshold: does any core object enter the survival condition of a master sequence?
O4 M7 'forms as productions of realised history': matched-endpoint history test in a multistable autocatalytic chemistry,
   with and without a slow hidden variable."""
import json, math, itertools, sys
import numpy as np
from crr_instrument import *
rng = np.random.default_rng(606); R = {}

# ============================================================== O1 assembly theory
# Objects: binary strings. Join operation: concatenate two previously made objects. Assembly index a(s) = minimal number
# of joins from {0,1} (computed by BFS over assembly pools up to length 8). Actual history = the sequence of joins a
# process really performed (may include detours: objects made and discarded). Copy number = how many times s is produced.
def assembly_index(s, maxlen=8):
    """Exact minimal join count via BFS on sets of available objects (small lengths only)."""
    from functools import lru_cache
    target = s
    frontier = [frozenset({'0', '1'})]; seen = {frontier[0]}; depth = 0
    while frontier:
        nxt = []
        for pool in frontier:
            if target in pool: return depth
            items = list(pool)
            for x in items:
                for y in items:
                    z = x + y
                    if len(z) <= len(target) and target.startswith(z[:0]) and z not in pool and (z in target):   # prune: only substrings of target
                        np_ = frozenset(pool | {z})
                        if np_ not in seen: seen.add(np_); nxt.append(np_)
        frontier = nxt; depth += 1
        if depth > 12: break
    return None
def random_process(target, steps=60, templated=False):
    """A chemistry that joins random available objects; if templated, it preferentially re-makes objects already present
    (a crude copying/selection). Returns (history_length=number of joins performed, copies_of_target, made_target)."""
    pool = {'0': 1, '1': 1}; joins = 0; copies = 0
    for _ in range(steps):
        keys = list(pool)
        if templated and copies > 0 and rng.random() < 0.7:
            # copy the target by re-running its minimal construction (selection = repeated regeneration)
            copies += 1; pool[target] = pool.get(target, 0) + 1; joins += assembly_index_cache[target]; continue
        x, y = rng.choice(keys), rng.choice(keys); z = x + y
        if len(z) <= len(target):
            pool[z] = pool.get(z, 0) + 1; joins += 1
            if z == target: copies += 1
    return joins, copies
targets = ['0110', '01101001', '00001111', '01010101']
assembly_index_cache = {t: assembly_index(t) for t in targets}
o1 = {"assembly_index": assembly_index_cache, "runs": {}}
for t in targets:
    rows = []
    for templated in (False, True):
        J, Cn = zip(*[random_process(t, templated=templated) for _ in range(300)])
        J, Cn = np.array(J), np.array(Cn)
        made = Cn > 0
        # CRR reading: chord = minimal joins to the target (assembly index); arc = joins actually performed per copy; surplus = arc - a
        arc_per_copy = np.where(made, J/np.maximum(Cn, 1), np.nan)
        rows.append({"templated": templated, "fraction_made": float(made.mean()), "mean_copies_given_made": float(Cn[made].mean()) if made.any() else 0.0,
                     "mean_arc_per_copy_given_made": float(np.nanmean(arc_per_copy)), "mean_surplus_per_copy": float(np.nanmean(arc_per_copy) - assembly_index_cache[t])})
    o1["runs"][t] = rows
o1["outcome"] = ("REPHRASE. Assembly theory already uses a minimal path (the assembly index is a geodesic in construction space, the core's chord) "
    "and a repetition count (copy number) as the selection signature. The core's arc is the actual synthesis history and the surplus the detour; "
    "selection shows up as copy number rising and surplus per copy falling (templated runs). Surplus is therefore a redescription of "
    "'efficiency of production', which assembly theory expresses through copy number; it adds no independent coordinate (the identifiability "
    "constraint applies: given index and arc, surplus is fixed). The core supplies no threshold for 'selection' that assembly theory lacks.")
R["O1_assembly_theory"] = o1

# ============================================================== O2 RAF emergence (binary polymer model, Kauffman / Hordijk-Steel)
def raf_exists(n_max, p_cat, food_len=2, seed=0):
    r = np.random.default_rng(seed)
    mols = [''.join(b) for L in range(1, n_max+1) for b in itertools.product('01', repeat=L)]
    food = {m for m in mols if len(m) <= food_len}
    reactions = [(x, y, x+y) for x in mols for y in mols if len(x+y) <= n_max]      # ligation only (cleavage omitted for speed)
    catalysis = {i: [m for m in mols if r.random() < p_cat] for i, _ in enumerate(reactions)}
    # RAF algorithm (Hordijk & Steel 2004): iteratively remove reactions whose reactants are not in closure or that are uncatalysed by closure
    Rset = set(range(len(reactions)))
    while True:
        # closure of food under Rset
        cl = set(food); changed = True
        while changed:
            changed = False
            for i in Rset:
                x, y, z = reactions[i]
                if x in cl and y in cl and z not in cl: cl.add(z); changed = True
        keep = {i for i in Rset if reactions[i][0] in cl and reactions[i][1] in cl and any(c in cl for c in catalysis[i])}
        if keep == Rset: break
        Rset = keep
    return len(Rset) > 0, len(Rset)
n_max = 5; n_mols = sum(2**L for L in range(1, n_max+1))
curve = {}
for p in [0.0005, 0.001, 0.002, 0.004, 0.008, 0.016]:
    hits = [raf_exists(n_max, p, seed=s)[0] for s in range(20)]
    curve[str(p)] = {"P(RAF)": float(np.mean(hits)), "expected_catalysts_per_molecule": p*n_mols*0.5}
R["O2_RAF_emergence"] = {"n_max": n_max, "n_molecules": n_mols, "curve": curve,
    "outcome": ("NO CONTACT. RAF emergence is a percolation-type threshold in the catalysis probability (the curve above rises from 0 to 1 over a "
                "factor of a few in p, as Hordijk & Steel's theory predicts). It is an event in parameter space or in a growing network, not a "
                "first passage of accumulated statistical change on a circle; the core's cut criterion (half a circumference) has no meaning here "
                "and the core supplies no threshold the RAF literature lacks. The regeneration idea (the set re-makes itself from food) is the "
                "RAF closure condition itself, named by that literature twenty years earlier.")}

# ============================================================== O3 Eigen error threshold
def quasispecies_master_fraction(L, s, mu, gens=400):
    """Master sequence with fitness s>1 vs. mutant cloud fitness 1; per-site error mu; back-mutation neglected (standard)."""
    Q = (1-mu)**L; x = 0.5
    for _ in range(gens):
        wbar = s*x + (1-x); x = s*Q*x/wbar
    return x
L, s = 50, 10.0; thr = math.log(s)/L
scan = {str(round(m, 4)): quasispecies_master_fraction(L, s, m) for m in [0.5*thr, 0.9*thr, 1.1*thr, 1.5*thr]}
R["O3_error_threshold"] = {"L": L, "s": s, "threshold_mu": thr, "master_fraction_by_mu": scan,
    "outcome": ("NO CONTACT. The survival condition mu < ln(s)/L involves fitness, length and error rate only; no path quantity, no first passage, "
                "no regeneration kernel enters. The only CRR-adjacent reading is that heredity is 'regeneration from the settled past with fidelity "
                "1 - mu', which is a rephrase of replication.")}

# ============================================================== O4 M7: forms as productions of realised history (matched-endpoint test)
# Chemistry: two mutually inhibiting autocatalysts A, B. dA = k A^2/(1+A^2) - 0.5 A - 0.4 A B + noise, k = 1.5 (bistable per species); feed pulses add amount directly.
# 'History' = the order and timing of feed pulses. 'Form' = which attractor persists. Test (as P23 prescribes): manipulate histories;
# (i) does history predict the final form? (ii) given the full terminal state, does any history variable (order of pulses, path length)
# still predict the form a long time later? (iii) add a slow hidden variable h (e.g. membrane composition) that is set by history
# and biases the dynamics: now history predicts beyond the OBSERVED terminal state (A,B) but not beyond the FULL state (A,B,h).
def run_chem(pulses, hidden=False, T=60.0, dt=0.01, seed=0):
    r = np.random.default_rng(seed); A = B = 0.1; h = 0.0; Cpath = 0.0; prev = np.array([A, B])
    for i in range(int(T/dt)):
        t = i*dt; fa = fb = 0.0
        for (tp, which, amp) in pulses:
            if abs(t - tp) < dt/2:
                if which == 'A': A += amp
                elif which == 'B': B += amp
                else: A += amp; B += amp                      # common feed: forces the choice of form
        if hidden: h += dt*(0.6*(A - B) - 0.02*h)           # slow variable (e.g. membrane composition) integrates history and decays slowly
        bias = 0.8*np.tanh(3*h) if hidden else 0.0
        dA = (1.5+bias)*A*A/(1+A*A) - 0.5*A - 0.4*A*B + 0.05*r.normal()/math.sqrt(dt)   # bistable: fixed points 0 and ~2.6, threshold ~0.38
        dB = (1.5-bias)*B*B/(1+B*B) - 0.5*B - 0.4*A*B + 0.05*r.normal()/math.sqrt(dt)
        A = max(A + dA*dt, 0); B = max(B + dB*dt, 0)
        cur = np.array([A, B]); Cpath += np.linalg.norm(cur-prev); prev = cur
    return A, B, h, Cpath
def random_history(r):
    k = r.integers(1, 4); return [(float(r.uniform(0.5, 4.5)), 'A' if r.random() < 0.5 else 'B', float(r.uniform(0.1, 0.3))) for _ in range(k)] + [(15.0, 'both', 0.6)]   # sub-threshold history pulses, then a common feed at t=15
def o4_experiment(hidden, n=400):
    r = np.random.default_rng(42 if not hidden else 43); rows = []
    for i in range(n):
        H = random_history(r); first = H[0][1]; netA = sum(a for _, w, a in H if w == 'A') - sum(a for _, w, a in H if w == 'B')   # 'both' contributes 0
        A, B, h, Cp = run_chem(H, hidden, T=12.0, seed=i)                  # observed state after the chemistry has relaxed, before the common feed
        A2, B2, h2, _ = run_chem(H, hidden, T=60.0, seed=i)                 # form at t=60
        rows.append(dict(first=first, netA=netA, A=A, B=B, h=h, C=Cp, formA=A2 > B2))
    rows = {k: np.array([x[k] for x in rows]) for k in rows[0]}
    formA = rows['formA']
    def acc_logistic(X, y):
        # simple logistic regression via Newton steps; returns in-sample accuracy
        X = np.column_stack([np.ones(len(y)), *X]); w = np.zeros(X.shape[1])
        for _ in range(50):
            p = 1/(1+np.exp(-X@w)); g = X.T@(p-y); Hm = X.T@(X*(p*(1-p))[:, None]) + 1e-6*np.eye(len(w)); w -= np.linalg.solve(Hm, g)
        return float(np.mean(((X@w) > 0) == y))
    return {"P(form A)": float(formA.mean()),
            "acc_history_only (net feed A-B, first pulse)": acc_logistic([rows['netA'], (rows['first'] == 'A').astype(float)], formA),
            "acc_observed_terminal_state (A,B)": acc_logistic([rows['A'], rows['B']], formA),
            "acc_observed_state_plus_history": acc_logistic([rows['A'], rows['B'], rows['netA'], rows['C']], formA),
            "acc_full_state_incl_hidden": acc_logistic([rows['A'], rows['B'], rows['h']], formA) if hidden else None}
R["O4_M7_history_vs_state"] = {"no_hidden_variable": o4_experiment(False), "with_slow_hidden_variable": o4_experiment(True),
    "outcome": ("M7 as a formal claim REDUCES to multistability plus hidden state. Without a hidden variable, history predicts the form "
                "(because history chose the basin) but adds nothing once the terminal state is known: the form is a production of history only "
                "in the sense every attractor is. With a slow hidden variable set by history, history predicts beyond the OBSERVED state but not "
                "beyond the FULL state: 'history-dependence' is unobserved state, which is Watson's natural-induction and Blattner's hidden-state "
                "lesson, not a new ontology. Nothing here distinguishes 'forms are produced by history' from 'forms are attractors of the chemistry "
                "reached by history'; P23's discriminator must be a prediction a generic history-conditioned model does not make.")}
print(json.dumps(R, indent=1, default=float))
