# CRR v01.2 — mathematical audit, cross-system tests, and pre-registered results

Analyst: Claude (Opus 5). Object of study: Sabine (2026) v01.2, 33 pp.
Everything below is reproducible from `src/`; ledgers in `results/`.
Pre-registration committed at `2ce9bc1`, before any analysis script existed.

---

## Part 1 — Mathematical audit

### 1.1 Appendix A: 42 of 43 checks pass

Every proposition was verified symbolically (sympy) and numerically. **Propositions 1–13 are
all correct as stated.** Every in-text table reproduces:

- Sec 3.1 kernel-entropy table: all six rows to three decimals, including ln 200 = 5.298.
- Sec 8.1 holding table: all four rows (ℓ_eff, Ω_eff, H).
- A.4 ratios e^{1/Ω²}: 2.7, 140, 1.9×10⁴, 2×10¹⁹ — all within 2%.
- A.6 worked example shares 0.27 / 0.81 / 0.9999 — reproduce.
- A.9 counterexample: w = 3.627 (paper 3.63); Z at β=4 gives 745 and 198 — exact.
- A.12 KS statistic: our independent simulation gives D = 0.0020, matching the reported 0.002.
- A.7 Landauer: k_B·310·ln2 = 2.967×10⁻²¹ J. The "≈4% of one ATP hydrolysis" matches the
  in-cell figure (~50 kJ/mol → 3.6%), not the standard-state figure (30.5 kJ/mol → 5.9%).

The single non-pass is a `simplify` limitation on Prop 1(iii), not a mathematical error; the
numerical check of the same identity passes to 10⁻⁸.

**This is an unusually clean piece of arithmetic.** Nothing in Appendix A is wrong.

### 1.2 Where the problems actually are — nine findings

| # | Where | Severity | Finding |
|---|---|---|---|
| **D1** | C2 + §5 | **Gap** | C is *path length*; the capacity argument is about the arena's *diameter*. They coincide only for geodesic motion. Exact on the binary arena (dim 1); in dim ≥ 2 a diffusing system burns ~40 regimes' worth of arc length while its net displacement is a fraction of π (simulated, n = 3, 8, 64). §5's spherical-simplex result therefore does **not** carry C2 up in dimension without an added postulate. The orthant *is* geodesically convex (0/20 000 violations), so a geodesic postulate would repair it exactly. |
| **D2** | §3.3 | Tension | Three of five materials — water (Ω = 1.5×10⁶), olive oil, pitch — sit outside the domain Ω < 1 that Prop 7 requires for the edge, eq. (4) and the Landauer accounting. Water is outside by six orders of magnitude. Two different objects are being called Ω. Repair: the dial is only defined for an observer whose sampling interval is shorter than the fastest relaxation time in view. |
| **D3** | §3.3 | Unsupported | "A material integrating evidence at a fixed rate per unit time gives Ω ∝ τ^{−1/3}" requires N ∝ τ^{2/3}; no reading of the stated premise yields 2/3. The table's *ordering* is exponent-free (Spearman 1.000 across τ^{−1/2}, τ^{−1/3}, τ^{−1}), so nothing downstream breaks. |
| **D4** | C4 + §3.3 | Circular as demonstrated | Rate/dial separation is *true of the formalism* (Prop 3(iii) exact). But §3.3 has one physical input, τ, and reads the dial off it; if a material also reconfigures once per relaxation time then rate and dial are perfectly correlated across the whole table. §3.3 cannot evidence the separation it is offered for. |
| **D5** | §3.4 | Overstated | On the normalised coordinate x = CΩ — the only one in which regimes at different Ω are comparable, and the one Prop 5 and the Sec 3.1 table actually use — the kernel is e^{x/Ω²}. The effective inverse temperature is 1/Ω², not 1/Ω. Direction unaffected; "exactly" should be "up to Ω → Ω²". |
| **D6** | eq. (4) | Internally inconsistent at the paper's own canonical value | ℓ = π√N is an integer only on a measure-zero set. At the canonical N = 1, Ω = 1/π, eq. (4) gives s* = 0.6817 but A.7 gives 0.6366, with 0.1416 of a cell unaccounted for at the wall. Every row of the Sec 3.1 table except Ω = 1 is in the non-integer case. |
| **D7** | A.12 | **Sound and stronger than stated** | As a standard Gompertz h = ae^{bt}: a = φ₀, b = 1/Ω, shape η = a/b. Mode-on-wall ⟺ η = e^{−b²}. η is scale-invariant, b² is not, so the condition *selects a time unit* — it is the statement that the clock is read in cells. Consequence the paper misses: Ω is **identifiable with no free parameter** from any Gompertz interval data, Ω̂ = 1/√(−ln(a/b)). This is the sharpest empirical hook in the paper and it is not flagged as one. |
| **D8** | §10.1 | Derived, unstated | Regime duration is π/L for every Ω, so the dissipation floor is **P ≥ (L/π)(1/Ω)k_BT ln2** — inverse in the dial. The paper states only the per-regime version qualitatively. |
| **D9** | §11.2 | Open, correctly flagged; **now closed** | Neither CRR clock meets Mirollo–Strogatz: C1's is linear (C″ = 0), A.11's is convex (C″ = a²e^{2C/Ω}/Ω > 0). Resolved by simulation in Part 3. |

---

## Part 2 — Pre-registered tests on existing data

Data: 132 oscillatory systems across 20 domains (`132.pdf` Table 8; our independent parse
agrees with the repo CSV on 87/87 name-matched rows at 100% for CV, class and symmetry),
plus PhysioNet EEGBCI (N = 109) and MPI-LEMON (N = 189). **Blinding status is disclosed in
`PREREGISTRATION.md` §0: the analyst had read the outcome columns. Every prediction is
parameter-free, so the point predictions have no freedom to be moved; the choice of test was
fixed in advance and not revised.**

### PR-1 — which interval law? Primary test: Class A (n = 45), the autonomous systems.

| test | result | A: CV = 1.283Ω² | A′: CV = 1.283Ω | B: CV = Ω/2 |
|---|---|---|---|---|
| PR-1.1 class ratio | 1.875, 95% CI [1.500, 2.344] | predicts 4.00 → **REJECTED** | 2.00 → survives | 2.00 → survives |
| PR-1.2 Z₂ median | 0.150 [0.135, 0.188] | 0.130 → **REJECTED** | 0.408 → **REJECTED** | 0.159 → **survives** (obs/pred 0.94) |
| PR-1.2 SO(2) median | 0.080 [0.065, 0.100] | 0.032 → **REJECTED** | 0.204 → **REJECTED** | 0.080 → **survives** (obs/pred 1.01) |
| PR-1.3 AIC | — | ΔAIC **+90.9** | ΔAIC **+116.3** | **best**, σ_log 0.269, log-bias −0.001 |
| PR-1.4 exponent | slope 0.953, CI [0.719, 1.186] | 2 → **REJECTED** | 1 → survives | 1 → survives |

**Verdict.** v01.2's Appendix A.12 calibration is rejected on all four sub-tests. The law that
survives is CV = Ω/2 — which v01.2 has in §2.3 (quantal overshoot) and which is the earlier
canonical variant's M1. Replicates in both EEG datasets: on the Class A bands the quantal law
gives obs/pred of 0.96 and 1.07 (PhysioNet PLV) and 1.14 / 1.42 (LEMON young), against 2.6–3.6
for Route A.

This confirms *empirically* an argument already available *internally*: A.12's hazard e^{C/Ω}
e-folds over Ω cells — **less than one resolvable cell for every Ω < 1**. A threshold smeared
finer than the system's own resolution cannot generate resolvable variability.

### PR-2 — interval skew

Routes A and A′ predict skew = **−1.1395** exactly (reflected Gumbel), for every Ω.
Cyclic interval distributions (ISI, RR, Ca²⁺, somite periods) are positively skewed; human
age-at-death is strongly negatively skewed and is the canonical Gompertz application.
**A.12 is a senescence law that §2.3 misapplies to stationary cycling.** Keep it for terminal
rupture; restore the quantal overshoot for cycles.

### PR-3 — the developmental Ω schedule: **FAILS** (recorded as a binding negative)

§3.4 and A.6(iii) commit to Ω falling monotonically. Under any surviving interval law CV
increases in Ω, so CV should not rise with age. MPI-LEMON, young vs old, 5 bands:

| band | young | old | d | |
|---|---|---|---|---|
| Delta | 0.200 | 0.256 | **+0.46** (p = 0.012) | against |
| Theta | 0.204 | 0.216 | +0.18 | against |
| Alpha | 0.262 | 0.281 | +0.20 | against |
| Beta | 0.163 | 0.160 | −0.06 | as predicted |
| Low γ | 0.113 | 0.117 | +0.14 | against |

1/5 in the predicted direction; the rule required ≥ 4/5. Inverting CV = Ω/2, implied Ω rises
from 0.377 to 0.412 (+9.3%). **The strong lifespan-monotone reading of the annealing schedule
is refuted.** Scope, as registered in advance: this is a young-adult/old-adult contrast, so it
does not touch the childhood claim — but §3.4's "any developmental process described as
annealing is a process in which Ω decreases with age" is stated without an upper age bound,
and at that strength it fails.

### PR-4 — precision lowers Ω: **consistent** (non-independent, capped at T2)

Eyes-closed → eyes-open: CV falls in 4/4 Z₂ bands (d = 0.39–0.65), invariant in SO(2)
(d = 0.005). This is the pattern v01.2 requires. It was, however, already predicted and
reported in `132.pdf` §4.2.1, so it is scored as consistency, not new confirmation.

### PR-5 — holding raises effective Ω: **exploratory, 2/3 favour the correction**

Predicted for a balanced dyad (f = ½): CV = (1/π)/2 × √2 = 0.2251, against the solitary Z₂
baseline 0.1592.

| system | CV | closer to | implied f |
|---|---|---|---|
| Neonatal inter-cry interval | 0.225 | **held** (|log ratio| 0.000) | +0.50 |
| Conversation turn-taking gap | 0.200 | **held** (0.118 vs 0.228) | +0.37 |
| Infant suckling burst | 0.150 | solitary | −0.13 |

The neonatal cry interval lands on the f = ½ prediction to three decimals. **This is the only
place in the analysis where v01.2 beats its predecessor on data.** It is exploratory — the
analyst had seen these rows — and is re-registered as F1/F2 for confirmatory test.

### A qualitative test of the edge kernel (Prop 4(iii))

v01.2 asserts retention depends on precision at encoding and position within the regime, and
that **lag contributes nothing**. Against a century of retention functions (Ebbinghaus through
Rubin & Wenzel's 100+ datasets) showing smooth monotone decline with lag, this predicts
retention should be a **step function across regime boundaries**. Event-boundary effects
(Radvansky & Zacks) do show discrete drops in accessibility at boundaries, so the two
literatures are reconcilable only if CRR regimes are identified with event boundaries — an
operationalisation the paper owes and does not supply. Registered as the decisive test.

---

## Part 3 — Running the grammar in other systems

### S1 — Entrainment: the open question of §11.2, closed

N = 50 pulse-coupled CRR clocks, order parameter R of the phase CΩ.

*Identical clocks:* count coupling gives R = 1.000 for **all three** rise shapes at every
κ ≥ 0.02. This is pure absorption and discriminates nothing — vindicating the paper's caution.

*Heterogeneous clocks (10%, the case Kuramoto addresses), count coupling:*

| rise | κ=0.02 | 0.10 | 0.30 | 1.0 | 4.0 |
|---|---|---|---|---|---|
| concave (L falls toward the cut) | 0.465 | 0.693 | **0.972** | 0.971 | 0.971 |
| linear (C1's clock) | 0.184 | 0.443 | 0.585 | 0.960 | 0.960 |
| convex (A.11's self-fed clock) | 0.133 | 0.320 | 0.427 | 0.955 | 0.955 |

Speed coupling needs κ ≈ 1–4 for every rise shape.

**Answer.** CRR's C1 clock *does* entrain, but needs ≈ 3× the coupling a concave clock needs;
A.11's self-fed clock is no better than linear. Of the two repairs §11.2 offers, the **first**
(speed L falling as the regime nears its cut) is the cheap one and the **second** (coupling on
speed rather than count) is the expensive one. The paper leans on the second.

Direct check of the paper's own claim — "a pulse advancing the receiver's count locks them
only when they begin within one pulse of each other": final |Δφ| is exactly 0 iff the initial
offset ≤ κ, and exactly preserved otherwise. **Confirmed to four decimals.** The phase-response
curve of a linear clock to a state pulse is flat.

### S2 — Holding and the still face

Prop 10 verified by simulation: under **turn-taking** the regime duration is invariant in f
(π/L = 3.1416 at f = 0, 0.3, 0.5, 0.7); under a **parallel** traverse it shortens as (1−f)π/L.
The paper's headline prediction is therefore a genuine discriminator between the two dyadic
architectures, exactly as it claims.

Still face, quantified: withdrawal from f = ½ to f = 0 drops kernel entropy 4.655 → 4.003, so
the effective number of past moments in play falls **105 → 55, a factor 1.92** — while the
cycle period does not change at all. *Possibility space halves; the clock does not move; the
face is still there.* That is a quantitative account of an otherwise purely clinical fact.

### S3 — Development, adversity, therapy

Simulating 8 regimes with a falling Ω schedule reproduces A.6(iii) exactly (the most recent
regime takes ~all the weight at low Ω_t). Inserting one early regime at a precision the life
never reaches again (Ω = 0.06 among 0.12–0.9) gives that regime **≈100% of every
reconstruction at every Ω_t below 1**. The paper's Frankenhuis–Gopnik adversity prediction is
not a conjecture in this framework; it is a theorem.

The clinical corollary is quantitative and the paper does not draw it. Therapy as "a held
raising of Ω_t" (D.4) is bounded by Prop 6(ii): as Ω_t → ∞ each regime contributes exactly its
*mass*. So re-reading cannot delete a peaked regime; **its floor is that regime's share of
lived time** (1/8 = 0.125 here). Traumatic share falls 1.000 → 0.937 → 0.417 → 0.167 as Ω_t
goes 1 → 2 → 5 → 20.

### S4 — Materials

Ordering is exponent-free (Spearman 1.000 across τ^{−1/2}, τ^{−1/3}, τ^{−1}); only the
ordering is used, so D3 costs nothing. But the domain constraint (D2) is real and unstated.

### S5 — Thermodynamics

P ≥ (L/π)(1/Ω)k_BT ln2. At L = 1 s⁻¹ and 310 K this runs from 1.0×10⁻²¹ W at Ω = 0.9 to
9.4×10⁻²⁰ W at Ω = 0.01 — two orders of magnitude of dissipation across two orders of the
dial, at ~10⁻²⁰ W absolute. As the paper says, the magnitude constrains nothing biological.
The **scaling** is the content and it is measurable in neuromorphic substrates.

### S6 — The dial as a continual-learning parameter

10-arm bandit whose reward structure ruptures every 800 steps, 24 seeds:

| schedule | mean reward |
|---|---|
| fixed Ω at the grid optimum (Ω ≈ 0.35) | **0.716 ± 0.015** |
| sawtooth: re-open the dial at every rupture | 0.658 ± 0.009 |
| monotone anneal 1.0 → 0.15 (§6, §12(i), D.7(i)) | 0.635 ± 0.014 |

**v01.2's own design advice is the worst of the three.** A monotone anneal is optimal only if
the world ruptures once; C2 says every finite system ruptures repeatedly, so the schedule
CRR's own axioms imply is sawtooth, not monotone. (The sawtooth–anneal gap is ~1.4 SE and not
individually significant; the fixed-vs-anneal gap is ~4 SE and is.) §6 and §12(i) are
inconsistent with C2 on this point.

The fixed optimum sits at Ω ≈ 0.35, near the canonical 1/π = 0.318. **This is not evidence:**
Ω enters as a temperature on an arbitrary reward scale, so the optimum's location is set by
that scale, not by geometry.

---

## Part 4 — Ledger

**Correct and verified:** Propositions 1–13; every table; the Landauer arithmetic; Prop 9's
Markov/non-Markov split and its counterexample; Prop 10's dyadic algebra; Prop 8's derivation
of the 2:1 class ratio; the reparameterisation-invariance of C and the convention-independence
of Ω (both repairs of earlier variants).

**Needs repair before publication:** D1 (geodesic postulate, or restrict C2 to dim 1);
D2 (state the Ω < 1 domain and apply it to §3.3); D3 (drop the −1/3); D5 (soften "exactly");
D6 (eq. (4) fails at the paper's own canonical Ω); and, most importantly, **§2.3 + A.12**:
the Gompertz and quantal readings are different laws, the data select the quantal one, and the
paper should say so.

**Genuinely new and worth keeping:** Ω_eff = Ω/√(1−f); the Markov-clock/non-Markov-dial
theorem; the edge kernel; P ∝ 1/Ω; the boundary-impossibility linkage.

**Failed:** PR-3, the lifespan-monotone annealing schedule.
