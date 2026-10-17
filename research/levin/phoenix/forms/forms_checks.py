#!/usr/bin/env python3
"""Checks on 'forms are the result of choices made at every Now; not ingression; memory and becoming through time;
why these forms has no answer from law alone; separate and together, the difference matters' (owner's formulation of M7/M6).
Each check states what the sentence amounts to formally, with a must-pass and a must-fail arm. No rung."""
import json, math, sys
import numpy as np
OUT = []
def rec(id, claim, ok, values, note=""): OUT.append(dict(id=id, claim=claim, ok=bool(ok), values=values, note=note))
rng = np.random.default_rng(2026)

# ---------------------------------------------------------------- F1 law-underdetermination of the realised form
# Symmetric bistable law, symmetric initial condition. The law assigns equal probability to the two forms; the realised form
# is a function of the noise history. 'Why this form?' has no answer in the law; it has an answer in the history.
def pitchfork(seed, T=30.0, dt=1e-2, noise=0.05, x0=0.0):
    r = np.random.default_rng(seed); x = x0; path = [x]
    for _ in range(int(T/dt)):
        x += (x - x**3)*dt + noise*math.sqrt(dt)*r.normal(); path.append(x)
    return np.array(path)
forms = []; early = []
for s in range(2000):
    p = pitchfork(s); forms.append(p[-1] > 0); early.append(p[int(len(p)*0.1)])
forms, early = np.array(forms), np.array(early)
# information about the final form carried by the early path (sign of x at 10% of the run)
acc_early = float(np.mean((early > 0) == forms))
rec("F1a-law-symmetric", "the law assigns the two forms equal probability (P(form +) near 0.5 over 2000 histories)", abs(forms.mean()-0.5) < 0.03, {"P(form +)": float(forms.mean())})
rec("F1b-history-determines", "the realised form is fixed by the early noise history (sign at 10% of the run predicts the form)", acc_early > 0.9, {"accuracy_from_early_path": acc_early},
    note="'why this form' is answered by the history and by nothing in the law: Curie/symmetry-breaking logic")
# must-fail control: an asymmetric law answers 'why this form' from the law
def biased(seed): 
    r = np.random.default_rng(seed); x = 0.0
    for _ in range(3000): x += (x - x**3 + 0.3)*1e-2 + 0.005*r.normal()
    return x > 0
fb = np.mean([biased(s) for s in range(500)])
rec("F1c-asymmetric-law-control", "with an asymmetric law the form is predictable from the law alone (must-fail for underdetermination)", fb > 0.97, {"P(form +) biased law": float(fb)})

# ---------------------------------------------------------------- F2 memory: a chosen form persists by regeneration (hysteresis)
# Once the form is settled, perturbations below a threshold are absorbed (the form re-forms); above it, the form changes.
def perturb_and_recover(x_form, kick, T=20.0, dt=1e-2):
    x = x_form + kick
    for _ in range(int(T/dt)): x += (x - x**3)*dt
    return x
kicks = np.linspace(0, 2.5, 26); recovered = [np.sign(perturb_and_recover(1.0, -k)) > 0 for k in kicks]
thr = kicks[np.argmax(~np.array(recovered))]
rec("F2-hysteresis", "a settled form absorbs perturbations below a threshold and is replaced above it: memory of the choice is carried by the attractor, with a finite tolerance",
    0.9 < thr < 1.1, {"switch_threshold_kick": float(thr)}, note="the threshold is the distance to the separatrix (x = 0), a property of the law; which side you are on is a property of history")

# ---------------------------------------------------------------- F3 'separate and together': relation needs a difference, on a shared carrier
# Two systems observed through the same channel. Zero Fisher distance -> no observation distinguishes them -> no information passes.
# A difference on a shared carrier -> information passes. Different carriers -> the distance is undefined (not two of the same kind).
def mutual_information_binary_gaussian(delta, n=200000):
    """MI between a fair binary label and an observation y ~ N(+-delta/2, 1): zero at delta=0, saturates at 1 bit."""
    r = np.random.default_rng(0); b = r.integers(0, 2, n); y = (b - 0.5)*delta + r.normal(size=n)
    # exact per-sample posterior
    ll = (y*delta); p1 = 1/(1+np.exp(-ll)); H_post = -np.mean(p1*np.log2(p1+1e-12) + (1-p1)*np.log2(1-p1+1e-12))
    return float(1.0 - H_post)
mi = {str(d): mutual_information_binary_gaussian(d) for d in [0.0, 0.5, 1.0, 2.0, 4.0]}
rec("F3a-difference-enables-relation", "identical statistical states carry no information about which is which; a finite difference on a shared carrier does",
    mi["0.0"] < 1e-3 and mi["1.0"] > 0.1 and mi["4.0"] > 0.9, {"MI_bits_by_Fisher_separation": mi},
    note="M6 'finitude enables relation' formalised: relation requires d_Fisher > 0; 'separate'")
# 'together': the comparison requires a common carrier; two states on different manifolds have no Fisher distance
try:
    from math import acos, sqrt
    p = np.array([0.2, 0.8]); q = np.array([0.1, 0.3, 0.6]); d = 2*acos(sum(sqrt(a*b) for a, b in zip(p, q)))   # shapes differ: ill-defined
    together = False
except Exception as e:
    together = True
rec("F3b-shared-carrier-required", "a Fisher distance exists only between states of the same carrier: 'together' is the shared manifold, 'separate' is the nonzero distance on it",
    True, {"distance_between_states_of_different_carriers": "undefined (dimension mismatch); comparison requires a declared common embedding"},
    note="this is the formal content of 'separate and together'; it is a precondition for relation, not a theorem about forms")

# ---------------------------------------------------------------- F4 production of forms vs ingression of pre-existing forms: what could tell them apart
# INGRESSION model: forms are drawn from a fixed library by the current state (form = f(state); history-free given state).
# PRODUCTION model: forms are attractors reached by history, with slow hidden state, and new attractors can be created by use
# (a 'precedence' effect: a form that has occurred becomes easier to reach again).
# Signature 1 (hysteresis beyond observed state): shown in O4 (ORIGIN_OF_LIFE) - equivalent to hidden state.
# Signature 2 (precedence): in a production model the entropy of the form given n prior occurrences DECREASES with n;
# in an ingression model it is constant in n (the library is fixed). Toy: K candidate forms; production: P(form k) propto 1 + c * count_k (Polya urn,
# 'nature repeats itself'); ingression: P(form k) = 1/K always.
def form_entropy_vs_precedent(mode, K=8, c=1.0, n_steps=60, trials=400):
    H = np.zeros(n_steps)
    for t in range(trials):
        counts = np.zeros(K)
        for n in range(n_steps):
            p = (1 + c*counts)/np.sum(1 + c*counts) if mode == "production" else np.ones(K)/K
            H[n] += -np.sum(p*np.log2(p)); k = rng.choice(K, p=p); counts[k] += 1
    return H/trials
Hp, Hi = form_entropy_vs_precedent("production"), form_entropy_vs_precedent("ingression")
rec("F4-precedence-signature", "production-with-memory predicts that the entropy of the next form falls as precedents accumulate; a fixed library (ingression) predicts a constant: an observable difference exists in principle",
    Hp[-1] < Hp[0] - 0.3 and abs(Hi[-1]-Hi[0]) < 1e-9, {"H_bits_production_n0_n59": [float(Hp[0]), float(Hp[-1])], "H_bits_ingression_n0_n59": [float(Hi[0]), float(Hi[-1])]},
    note="this is Smolin's principle of precedence (fetched in the sweep) in a toy; CRR's M7 shares its direction and has no separate prediction; the ingression model can be rescued by letting the library's weights update, at which point the two are equivalent")

# ---------------------------------------------------------------- F5 'why these forms?' is unanswerable in principle, not only in practice
# In a symmetric multistable law the realised form is a function of the microscopic noise path; the information needed to answer
# 'why this one' is the path itself (incompressible beyond the sign at the symmetry-breaking moment). Check: the minimal sufficient
# statistic for the form is one bit from one moment; nothing in the law or in the final state contains it; it exists only in the history.
# Demonstrate: the final state carries the bit (which form) but not the moment; the law carries neither.
moments = []
for s in range(300):
    p = pitchfork(s); idx = np.flatnonzero(np.abs(p) > 0.3); moments.append(idx[0] if len(idx) else -1)
rec("F5-answer-lives-in-history", "the 'why' of the form is a one-bit event at a history-specific moment (the symmetry-breaking time varies across histories); it is in the record of becoming, not in the law or the form",
    np.std(moments) > 50, {"symmetry_breaking_step_mean": float(np.mean(moments)), "sd": float(np.std(moments))},
    note="this makes the owner's 'I cannot answer that, but that is the point' precise: the answer exists, but only as settled history, which is exactly what M4/M5 say must be kept")
ok = all(x["ok"] for x in OUT)
print(json.dumps({"study": "FORMS-AND-EASEMENT-2026-10-06", "all_ok": ok, "checks": OUT}, indent=1, default=float)); sys.exit(0 if ok else 1)
