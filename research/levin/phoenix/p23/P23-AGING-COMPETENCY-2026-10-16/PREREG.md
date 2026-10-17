# P23-AGING-COMPETENCY preregistration (OD-50, 2026-10-16)

**Aim (owner, OD-50).** "The goal here is not to 'prove CRR', but to use CRR to develop Levin's research findings."
The aim is to take the central claim of Pio-Lopez, Hartl & Levin (2025), that ageing in their NCA is a *loss of
goal-directedness*, and turn it into tests whose answers extend their findings, using CRR's rupture–regeneration
framing to choose them. The authors' code is used unchanged (bhartl/muse 9404ec3). The protocol is frozen before the
test seeds. Development used seeds 3000–3049 (`results/dev/`).

**How CRR shaped the questions.**
- CRR treats a life as cycles of rupture (a cut is a first passage) and regeneration. That suggests asking:
  - Does the *capacity to regenerate* after a standard rupture decline with age (Q2), or does the *chance of a
    rupture that cannot be regenerated* stay constant (Q1)?
  - Is organ loss a first passage of lesion size to a critical value (Q2b, Q2c)?
- CRR's coherence (Fisher–Rao change) offers a candidate early-warning signal, set against the classic ones (Q4).
- If loss is a first passage past a critical lesion, repair should be triggered *before* that size is reached
  (Q5).

Each answer is a statement about the authors' model, whatever it says about CRR.

## Development observations (seeds 3000–3049) that fix the predictions

- **Repair by age (20 seeds).** A 1-cell injury at the eye's centre (5,5) is repaired in about 95% of cases at
  every age from 40 to 1,200. A 3-cell eye injury is repaired in under 5% at every age, including 0/9 without
  noise. A 3-cell cheek (face) injury is repaired in 100% at every age.
- **Lesion size (30 seeds, age 300).** One random eye cell injured: eye lost within 300 steps in 7/17 (uninjured
  0/17). Two cells: 16/17. Three to five: all.
- **Survival (50 lifetimes, 2,000 steps).** Age coefficient of the log hazard −0.38 per 1,000 steps [−0.83, +0.05];
  cascade coefficient +0.19 [−0.24, +0.56]. Organs pass through long partly-damaged plateaus (score 0.6–0.8)
  before loss.
- **Early warning (window 20, horizon 100).** Cross-validated AUC: damage + margin 0.936. Adding the CRR arc gives
  +0.006 [+0.003, +0.011]; adding variance and lag-1 autocorrelation gives +0.012 [+0.006, +0.020].
- **Lesion-size-triggered repair (10 seeds, noise 0.125).** Late fitness k = 1: 224.1; k = 2: 220.9;
  k = 3: 216.5; k = 4: 214.2; k = 5: 213.7. About 60–72 cell writes each.

## Test (seeds 4000+), noise 0.125 unless stated

| id | question | design | rule | prediction |
|---|---|---|---|---|
| Q1 | does the hazard of organ loss rise with age (senescence)? | 200 lifetimes (4000–4199), 2,000 steps; discrete-time logistic hazard, event ~ age + organ | senescence if the bootstrap 95% CI of the age coefficient is > 0 | no senescence (CI includes 0 or is negative) |
| Q2 | does repair capacity decline with age? | injuries eye-centre 1 cell (5,5), eye 3 cells, cheek 3 cells (organ-typed) at ages 40, 100, 200, 400, 800, 1,200; seeds 4000–4039 | decline if repaired share young (≤ 100) > mature (≥ 400), Fisher p < 0.05 | no decline for any injury |
| Q2b | is there a critical lesion size? | k = 1, 2, 3, 4 random left-eye cells at age 300, follow 300; seeds 4000–4059 | eye lost (score < 0.6) at +300, injured vs uninjured | loss rises with k; k = 2 ≥ 80% lost; k = 1 between 20% and 70% |
| Q2c | which eye cells are critical? | each of the 10 left-eye cells alone, age 300, follow 300; seeds 4000–4019 | eye lost at +300 per position | descriptive (development showed the centre cell is repaired, other cells less) |
| Q3 | do organ losses cascade? | Q1 data; covariate = other organs already lost | cascade if the CI of its coefficient is > 0 | no detectable cascade |
| Q4 | does CRR coherence warn of organ loss beyond the damage present? | Q1 data; window 20, horizon 100; 5-fold CV by lifetime | adds if the bootstrap CI of the AUC gain over BASE excludes 0 | small gain (< 0.02), classic early-warning signals at least as large |
| Q5 | when should repair be triggered? | repair at ≥ k wrong cells (canonical target), k = 1…5; seeds 4000–4049; noise 0.125 and 0.15 | paired late-fitness differences, bootstrap 95% CI (as in P23-AGING-CRR) | fitness falls with k; k = 1 beats k = 3 by ≥ 2 |

Analyses: `analyze_lifecourse.py` (Q1, Q3, Q4), `analyze_competency.py` (Q2), the Q2b/Q2c/Q5 summaries in
`analyze_q2b_q5.py`. All results are reported; departures are recorded in REPORT.md.
