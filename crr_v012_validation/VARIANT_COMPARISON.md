# CRR v01.2 against the other variants in this repository

Three variants are compared: **v01.2** (Aug 2026, the paper under review), **CANON**
(`CRR_FINAL_CANONICAL.md`, post-campaign consolidation), and **132** (`132.pdf`, the
132-system empirical paper). Checks in `src/compare_variants.py`.

## 1. What accumulates

| | definition of C | reparameterisation-invariant? | dimensionless? |
|---|---|---|---|
| CANON | ∫(ds/dτ)²dτ — the **energy** functional | **No** | No: [C·Ω] = Length/Time |
| 132 | ∫L dτ, L a "mnemonic entanglement rate", C *declared* dimensionless | — | by stipulation |
| **v01.2** | (1/ε)∫‖ds/dτ‖dτ — **arc length in cells** | **Yes** | **Yes, derived** |

Numerically verified: the same full traverse of the arena taken over 1, 2 and 10 time units
gives CANON's C = 9.87, 4.93, 0.99 but v01.2's C = π, π, π. Since the entire framework says
the cut falls when *the arena is used up*, invariance under how fast you cross it is the
property the theory needs, and only v01.2 has it. **This is v01.2's clearest technical
advance and it repairs a dimensional inconsistency in its predecessor.**

## 2. What the dial is

CANON: Ω = 1/φ_G, the reciprocal closed-geodesic length of a compact connected Lie group
taken as the "memory-bearing manifold". This inherits the Čencov normalisation ambiguity
(the Fisher metric is unique only up to a positive constant), which CANON §1.5 confronts as
a "two-Ω disambiguation" between Ω_geo and Ω_int and resolves by convention.

v01.2: Ω = ε/π, a **ratio of two lengths in the same metric**, hence invariant under
g → c²g (Prop 3(iv), verified). The two-Ω problem does not arise. **Resolved, not conventionalised.**

## 3. Where the factor of 2 between symmetry classes comes from

- CANON (M2): from |Z₂|, the order of the discrete subgroup, φ_{SO(2)}/φ_{Z₂} = 2π/π.
  Requires positing a Lie-group memory manifold.
- v01.2 (Prop 8): the arena is an interval with ends; a trajectory reflecting at both ends
  unfolds onto a circle of circumference 2π, and **two regimes complete one circuit**.

Same number, far cheaper derivation. v01.2 gets the empirically load-bearing 2:1 class ratio
from one-dimensional geometry with no group theory. **Strict improvement.**

## 4. The interval law — v01.2 regresses here

| variant | law | scaling | Z₂ | SO(2) | ratio |
|---|---|---|---|---|---|
| CANON/132 (M1) | CV = Ω/2, from Bernoulli(½), n = 1 at the wall | linear | 0.1592 | 0.0796 | 2.00 |
| v01.2 A.12, mode-on-wall | CV = (π/√6)Ω² | **quadratic** | 0.1300 | 0.0325 | 4.00 |
| v01.2 A.12, multiplier 1 (offered in C3) | CV = (π/√6)Ω | linear | 0.4083 | 0.2041 | 2.00 |
| v01.2 §2.3, quantal overshoot | CV = Ω/2 | linear | 0.1592 | 0.0796 | 2.00 |

v01.2 §2.3 asserts the quantal and Gompertz readings are the same law. They are not: they
differ in the *scaling exponent*. Tested (see `PREREGISTRATION.md`, `results/`): on Class A of
the 132-system dataset the quantal/CANON law wins by ΔAIC = 91 and 116 over the two Gompertz
readings, and the fitted exponent is 0.95 (95% CI [0.72, 1.19]), excluding 2.

**Two independent reasons A.12's calibration is wrong, one internal and one empirical.**
Internal: the hazard e^{C/Ω} e-folds over Ω cells, i.e. over *less than one resolvable cell*
for every Ω in the grammar's own domain Ω < 1 (Prop 7) — a threshold smeared finer than the
system's resolution cannot produce resolvable variability. Empirical: PR-1.

**A.12 is not false, it is misplaced.** A hazard rising in accumulated coherence is a
*senescence* law: it predicts strongly **negatively** skewed intervals (skew −1.1395 exactly,
a reflected Gumbel). Human age-at-death — a terminal, once-only rupture — is negatively skewed
and is the canonical Gompertz application. The cyclic intervals of the 132 dataset (ISI, RR,
Ca²⁺ spikes, somite periods) are positively skewed. **A.12 describes terminal rupture; §2.3
misapplies it to stationary cycling.** Recommended repair: keep A.12 for the once-only case,
restore the quantal overshoot for cycles, and state CV = Ω/2 as v01.2's interval law.

## 5. Scope: a large and mostly healthy retreat

Dropped from CANON in v01.2: the Lie-group CV generalisation (SU(2), SU(3), SO(3)), the α³
fine-structure fixed point (CANON's only T3 result), singular-continuous spectral type, the
Kan-extension uniqueness claim, the 16-nats hypothesis, time-crystal and quantum-computing
readings, dark-energy and gravitational-wave predictions.

This is the right direction — those were the weakest claims and several are relabellings of
standard results — but it is worth naming the cost: **v01.2 discards the programme's only
promoted empirical result and replaces the one surviving quantitative law with a worse one.**
On the tests run here, v01.2's *formalism* is better than CANON's and its *empirical content*
is thinner.

## 6. Genuinely new in v01.2, and worth keeping

1. **Ω_eff = Ω/√(1−f)** (eq. 5, Prop 10) — the dyadic composition law. Parameter-free,
   verified symbolically and by simulation, and the only new *quantitative* claim in the
   paper. Its discriminating prediction (turn-taking leaves the period invariant; a parallel
   traverse shortens it) is confirmed in simulation as a genuine discriminator.
2. **Prop 9** — the clock is Markov, the dial is not; R(Ω) is the Laplace transform of the
   archive's density of states. The explicit counterexample checks out exactly (745 vs 198).
   This is a clean, correct and non-obvious structural result with no predecessor in CANON.
3. **The edge kernel** (Prop 4(iii)) — retention set by precision at encoding and position in
   the regime, with lag contributing nothing. A sharp, falsifiable memory commitment.
4. **The Landauer accounting** (§10.1, A.7) — correct as far as it goes, and it yields a
   scaling the paper does not state: P ≥ (L/π)(1/Ω)k_BT ln 2.
5. **The boundary-impossibility linkage** (Fields–Glazebrook / Winnicott) — an interpretive
   claim, correctly labelled as such.

## 7. Verdict on the comparison

v01.2 is the **best-formed** variant of CRR in this repository and the **least empirically
committed**. Its geometry is invariant where CANON's was convention-dependent, its dial is
well-defined where CANON's needed a disambiguation table, and its 2:1 ratio is derived rather
than posited. Against that, it swapped a law that fits 132 systems for one that does not, and
it did so in an appendix, without noticing.
