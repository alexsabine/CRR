# Pre-registration — testing CRR v01.2 against existing data

**Object of study.** Sabine, A. (2026) *The Paradox That Must Not Be Resolved: Transitional
Space, the Relational Weave, and a Temporal Grammar for Finite Systems*, v01.2, August 2026.

**Registered by.** Claude (Opus 5), acting as analyst, at the author's request.
**Registered on.** 2026-08-28, before any analysis script in `src/analyse_*.py` existed.
**Audit trail.** This file is committed in its own commit. `git log` shows it precedes every
analysis script. Results are binding in whichever direction they fall and stay committed.

This follows the epistemic protocol already in this repository
(`CRR_FINAL_CANONICAL.md` §0, PART III): every claim starts at T0; T3 requires a
pre-registered prediction confirmed on data not used to construct it; honest negatives are
permanent; sympathy with the framework is not evidence.

---

## 0. Disclosure of blinding status

Full egress is blocked in this environment, so no new data could be fetched. All tests below
use data **already present in this repository**:

| Dataset | Source | n | Blinding |
|---|---|---|---|
| D1 | 132 oscillatory systems, `132.pdf` Table 8 / `crr-cv-predictions/data/cv_predictions_132.csv` | 132 | **Not blind.** The analyst read Table 8 while extracting it. |
| D2 | PLV-CV by band, PhysioNet EEGBCI, `132.pdf` Table 2 | 109 | Not blind. |
| D3 | Amplitude-envelope CV by band × age, MPI-LEMON, `132.pdf` Table 3 | 189 | Not blind. |
| D4 | Eyes-closed/eyes-open CV, MPI-LEMON pilot, `132.pdf` Table 4 | 19 | Not blind. |

**Mitigation, and its limits.** Every prediction below is *analytically forced and
parameter-free*: each is a closed-form function of Ω with no fitted quantity, derived in
`src/derive_cv.py` from the text of v01.2 alone. Having seen the outcome column cannot move a
number that has no freedom in it. What non-blindness *does* cost is the choice of test — which
subset, which statistic — so those are fixed here, in advance, and not revised afterwards.
Tests marked **[EXPLORATORY]** were formulated after the analyst had seen the relevant rows and
are reported as hypothesis-generating only; they are re-registered in §7 for future data.

No prediction below is downgraded, re-specified or dropped after seeing a result.

---

## 1. The quantity at issue

v01.2 gives a deterministic cut, eq. (2): δ(now) when C·Ω = 1. Real inter-event intervals
scatter. v01.2 offers **two incompatible accounts of that scatter and asserts they are the
same one** (§2.3: "Read as a hazard on the current regime, an exponential of the same form as
the kernel gives the interval law — Gompertz").

**Route A — Appendix A.12, soft threshold.** Hazard h(C) = φ₀e^{C/Ω}, C rising at unit rate.
Intervals are Gompertz with shape η = φ₀Ω, scale Ω. A.12 fixes φ₀ by putting the mode on the
wall: φ₀ = e^{−1/Ω²}/Ω, i.e. **η = e^{−1/Ω²}**, leaving no free parameter.
Writing T = Ω·(ln(1/η) + ln E) with E ~ Exp(1) (exact), so T is a shifted reflected Gumbel:

- mean → 1/Ω − γΩ, sd → (π/√6)·Ω,
- **CV_A(Ω) → (π/√6)·Ω² = 1.28255 Ω²**  — *quadratic* in Ω,
- **skew(T) = −1.1395** — *negatively* skewed, exactly, for every Ω in the small-η regime.

**Route A′ — A.12 with the alternative multiplier v01.2 itself offers.** C3 says: "identifying
the multiplier on C with 1/Ω is a modelling choice, and one e-fold per resolvable step would
give a multiplier of 1 instead." Taking h(C) = φ₀e^{C} with the mode on the wall gives
η = e^{−1/Ω} and **CV_A′(Ω) = (π/√6)·Ω = 1.28255 Ω** — *linear* in Ω.

**Route B — §2.3, quantal overshoot.** "Evidence arrives in quanta … so the threshold is
crossed with a modest overshoot." One quantum, Bernoulli(½) sufficient statistic at the wall,
n = 1: sd = ½ cell absolute, mean count 1/Ω cells, so **CV_B(Ω) = Ω/2** — *linear* in Ω.
This is identical to the earlier canonical variant's M1 result.

**Ω by symmetry class** (unchanged between variants; v01.2 derives the factor 2 geometrically
in Prop 8 — two arc traversals complete the circle — where the earlier variant got it from
|Z₂| in a Lie group): Ω_{Z₂} = 1/π, Ω_{SO(2)} = 1/2π, Ω_{Z₃} = 1/3π.

### Point predictions (no free parameters)

| | Z₂ (Ω=1/π) | SO(2) (Ω=1/2π) | ratio Z₂:SO(2) | skew |
|---|---|---|---|---|
| **A** CV = 1.28255 Ω² | 0.12996 | 0.03249 | 4.00 | −1.14 |
| **A′** CV = 1.28255 Ω | 0.40826 | 0.20413 | 2.00 | −1.14 |
| **B** CV = Ω/2 | 0.15915 | 0.07958 | 2.00 | n/a |

---

## 2. PR-1 — Which interval law? (D1, Class A only)

**Rationale for the subset.** v01.2 and the earlier variant agree that the bare geometric
prediction applies only to autonomous, unregulated oscillators. The 132-system dataset's own
pre-registered three-class scheme calls these **Class A** (n = 45); Class B is expected below
baseline and Class C above it, so neither can adjudicate an absolute-value test. The primary
test is therefore Class A only. Class B/C are reported but are not the test.

**PR-1.1 (class ratio).** median CV(Z₂, A) / median CV(SO(2), A).
- A predicts 4.00; A′ and B predict 2.00.
- *Decision rule*: bootstrap 95% CI (10⁵ resamples) on the ratio. A model is rejected if its
  point prediction lies outside that CI.

**PR-1.2 (absolute location).** median CV within each (class A × symmetry) cell against the
three point predictions above.
- *Decision rule*: a model is rejected for a cell if the prediction lies outside the
  bootstrap 95% CI of that cell's median.

**PR-1.3 (model comparison).** Fit nothing. Score each of A, A′, B as a zero-parameter model
of log CV with a single shared, *estimated* residual scale (1 nuisance parameter each, so AIC
is comparable), over Class A systems with symmetry in {Z₂, SO(2)}.
- *Decision rule*: report ΔAIC. ΔAIC > 10 against a model is treated as decisive.

**PR-1.4 (scaling exponent).** Regress log CV on log Ω over Class A.
- A predicts slope 2, A′ and B predict slope 1.
- *Decision rule*: report the slope and its 95% CI; reject an exponent outside it.

**Prior stated commitment.** The analyst's derivation (`src/derive_cv.py`, committed with this
file) already shows on internal grounds that Route A must fail: its hazard e^{C/Ω} e-folds over
Ω cells, i.e. over **less than one resolvable cell for every Ω in the grammar's stated domain
Ω < 1** (Prop 7). A threshold smeared finer than the system's own resolution cannot generate
resolvable interval variability. PR-1 is the empirical check on an internal argument already
made. If PR-1 instead favours A, the internal argument is wrong and will be withdrawn.

## 3. PR-2 — Interval skew (D1 is insufficient; stated as a criterion)

Route A and A′ both predict inter-rupture intervals with **skew = −1.1395** (reflected Gumbel),
independent of Ω. Route B predicts scatter with no committed skew.

**Prediction.** Empirical inter-event interval distributions for the cyclic oscillators of D1
(neuronal ISI, cardiac RR, calcium spikes, segmentation clock) are, as a matter of standard
published morphology, **positively** skewed with a long right tail.
- *Decision rule*: if the standard morphology is positive skew, Routes A and A′ are rejected
  as accounts of **cyclic** rupture. Separately, if human age-at-death — a **terminal**,
  once-only rupture — is negatively skewed, Route A is *supported* for that case.
- *Interpretation fixed in advance*: a split verdict here means A.12 is a senescence law
  misapplied in §2.3 to stationary cycling, not a false law.

## 4. PR-3 — The developmental Ω schedule (D3)

v01.2 §6: "development is Ω falling"; A.6(iii) assumes "a schedule in which Ωₖ decreases with
k"; §3.4: "Any developmental process described as annealing is therefore a process in which Ω
decreases with age."

Under the surviving interval law (whichever of A/A′/B wins PR-1, all monotone increasing in Ω),
**CV is monotone increasing in Ω**, so:

**Prediction.** In MPI-LEMON (D3), amplitude-envelope CV in the **old** group should be **lower
than or equal to** the young group in **every** band.
- *Decision rule*: sign test over the 5 bands. The prediction requires ≥ 4/5 effects negative
  (Cohen's d < 0). It fails if ≥ 3/5 are positive.
- *Scope stated in advance*: v01.2's schedule is argued for childhood. D3 contrasts young
  adults with old adults. A failure therefore refutes only the **strong lifespan-monotone**
  reading (which §3.4 and A.6(iii) do assert), not the childhood claim, and will be reported
  at exactly that strength.

## 5. PR-4 — Precision lowers Ω (D4)

v01.2 §6: "the brakes are precision, and precision is what lowers Ω."
Opening the eyes raises sensory precision.

**Prediction.** CV falls from eyes-closed to eyes-open in precision-modulated (Z₂) bands and
not in local-circuit (SO(2)) bands.
- *Decision rule*: 4/4 Z₂ bands with d > 0 (CV decreasing) and |d| for the SO(2) band below
  the smallest Z₂ effect.
- **Non-independence declared**: this same prediction was made and reported in `132.pdf` §4.2.1.
  It is scored here as a *consistency* check of v01.2 with an already-published result, **not**
  as new confirmatory evidence, and cannot promote any claim above T2.

## 6. PR-5 — Holding raises effective Ω  [EXPLORATORY]

v01.2 eq. (5) and Prop 10(i): a partner taking fraction f of a shared turn-taking traverse
leaves the individual's kernel as flat as a solitary kernel at **Ω_eff = Ω/√(1−f)**, with the
**regime duration π/L unchanged**.

Combined with the surviving interval law CV = Ω/2, this predicts for a *dyadic, turn-taking*
system, measured on the individual's own contribution:

  **CV_dyad / CV_solitary = (1−f)^{−1/2}**,  bounded in [1, √2] for f ∈ [0, ½].

For a balanced two-party exchange (f = ½): **CV = (1/π)/2 × √2 = 0.22508**.

**Test.** D1 contains dyadic turn-taking systems. Compare their CV against both the solitary
Z₂ baseline 0.15915 and the held prediction 0.22508.
- *Decision rule*: the held prediction is preferred if it is closer in log ratio for a majority
  of the dyadic systems.
- **[EXPLORATORY]** — the analyst had seen these rows before formulating the test. Reported as
  hypothesis-generating only, at T1, and re-registered in §7.

## 7. Registered for future data (genuinely blind, not tested here)

- **F1.** In turn-taking dyads with independently measured turn-share f, individual inter-turn
  interval CV scales as (1−f)^{−1/2} while the *joint* cycle period is invariant in f.
  Falsified if the period shortens with f (that is Prop 10(ii), the parallel traverse, which
  v01.2 says would break the framework).
- **F2.** Still face: on withdrawal of the partner (f: ½ → 0), the infant's interval CV falls
  by a factor √2 ≈ 1.414 within one regime, while the cycle *period* is unchanged.
- **F3.** Timing beats fidelity: manipulating an artificial partner's response latency moves
  the still-face signature more than manipulating response fidelity (v01.2 §12, D.7(iv)).
- **F4.** Landauer power: at fixed Fisher–Rao speed L, a system's minimum dissipated power
  scales as P ≥ (L/π)(1/Ω) k_BT ln 2 — inversely with the dial. Rigid systems cost more per
  unit time than plastic ones of the same speed.
- **F5.** Gompertz over-determination: for any terminal-rupture process fitted as h(t)=a e^{bt},
  Ω̂ = 1/√(−ln(a/b)) computed from the *shape* must agree with Ω̂ computed from the *CV* of the
  same intervals via the surviving interval law. The two routes coincide only at
  Ω* = √6/(2π) = 0.38986; agreement elsewhere falsifies one of them.

## 8. What would falsify v01.2's empirical content outright

If PR-1 rejects **all three** of A, A′ and B, then v01.2 has no surviving account of interval
variability and its only quantitative contact with data is lost. That is the framework-level
falsifier and it is registered as such.
