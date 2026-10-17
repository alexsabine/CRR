# P23-AGING-COMPETENCY report (OD-50, 2026-10-16): developing Levin's ageing model with CRR's rupture–regeneration framing

**Status.** Frozen test. The protocol was frozen at commit 25ef609, before any test seed; development used seeds
3000–3049 and the test seeds 4000–4199. The model is the ageing NCA of Pio-Lopez, Hartl & Levin (2025), with the
authors' code unchanged. No repair is applied except in Q5. CPU only, no API spend. One builder.

**Aim (owner).** "The goal here is not to 'prove CRR', but to use CRR to develop Levin's research findings." The
paper's central claim is that ageing in this model is a *loss of goal-directedness*. CRR treats a life as ruptures,
each a first passage, followed by regeneration. That framing suggested the questions below. The answers are about
the authors' model.

## What we learned about the model

1. **Repair capacity does not decline with age (Q2).** An injury of a given kind is repaired equally well at every
   age from step 40 to step 1,200:
   - an eye-centre cell: 61/63 young against 34/36 mature (p = 0.62);
   - a cheek patch of 3 cells: 200/200 at every age;
   - an eye patch of 3 cells: 0/60 young against 0/35 mature.

   The cells' competence is fixed from the end of development onward. In this model, "loss of goal-directedness"
   is not a decline in what the cells can do.
2. **There is no senescence in the survival sense (Q1).** Across 200 unrepaired lifetimes of 2,000 steps, the hazard
   of losing an organ does not rise with age: −0.06 per 1,000 steps [−0.28, +0.17]. It drifts down slightly, from
   0.67 to 0.40 losses per 1,000 organ-steps, as fragile organs are lost early. Organ loss behaves like accidents
   at a constant rate, not like ageing.
3. **Organs fail by crossing a critical lesion size, which is tiny (Q2b, Q2c).**
   - **Lesion size.** One eye cell lost at age 300 leads to loss of the whole eye within 300 steps in 14/29 cases;
     two cells in 23/26; three in 24/25; four in 22/22. Uninjured eyes: 0 lost.
   - **Position.** Every single eye cell is a potential trigger, with loss rates of 8–77% depending on position. Even
     the centre cell, which is always patched within 60 steps (13/13), leads to the eye being lost later in 7/13.
     The lower edge (5,6) is the most critical (10/13).
   - **Contrast with the face.** A 3-cell cheek lesion is always repaired (Q2).

   Eyes are fragile attractors inside a robust face. "Ageing" in this model is noise waiting to create the first
   lesion the eye cannot absorb: a first-passage event, not a gradual loss of capacity.
4. **Organ losses do not cascade (Q3).** Losing one organ does not change the hazard for the others: −0.01
   [−0.21, +0.19].
5. **When to rejuvenate follows from 3 (Q5).** Repairing an organ at its *first* wrong cell, by writing the canonical
   organ state, is best, and every extra cell of tolerance costs fitness:

   | repair when wrong cells ≥ k | k = 1 | 2 | 3 | 4 | 5 |
   |---|---|---|---|---|---|
   | noise 0.125 | **229.0** | 225.8 | 221.0 | 219.5 | 218.3 |
   | noise 0.15 | **226.7** | 223.9 | 219.5 | 217.0 | 214.9 |

   - k = 1 minus k = 3: +8.0 [+7.6, +8.3] at noise 0.125; +7.3 [+7.0, +7.5] at noise 0.15.
   - k = 1 at noise 0.125 needs only 35 cell writes per lifetime, and reaches 229.0, above the model's own noise-free
     steady state (226).

   The paper's rule repairs at score ≤ 0.6, which is ≥ 4 wrong cells per eye. That intervenes after the critical
   lesion and gives up about 8–10 fitness units. The paper's own finding that targeting the wrong cells works best
   becomes a quantitative rule: **intervene before the first lesion grows, not after the organ has partly failed.**
6. **Early warning (Q4).** The best predictor of an organ failing within the next 100 steps is the damage already
   present (AUC 0.96). The classic early-warning signals, rising variance and slowing down, add a little
   (+0.007 [+0.004, +0.011] cross-validated). CRR's Fisher–Rao coherence (rate of cell-type change) adds nothing:
   −0.0008 [−0.0014, −0.0003]. Taken alone it is a weak signal (AUC 0.76). This is relevant to the paper's
   information-dynamics finding (AIS and TE rise at organ sites): in this model, activity measures carry little
   warning beyond the damage itself.

## Frozen predictions against results

| id | prediction | result | met? |
|---|---|---|---|
| Q1 | no senescence | age coef −0.06 [−0.28, +0.17] | yes |
| Q2 | no decline for any injury | eye centre 61/63 vs 34/36 (p = 0.62); eye 3-cell 0/60 vs 0/35; cheek 80/80 vs 120/120 | yes |
| Q2b | loss rises with k; k = 2 ≥ 80%; k = 1 in 20–70% | 48%, 88%, 96%, 100% | yes |
| Q2c | descriptive | 8–77% by position; lower edge highest | — |
| Q3 | no detectable cascade | −0.01 [−0.21, +0.19] | yes |
| Q4 | CRR arc gives a small gain (< 0.02); classic signals at least as large | arc −0.0008 [−0.0014, −0.0003]; classic +0.007 | **no** for the arc (no gain); yes for the classic signals |
| Q5 | fitness falls with k; k = 1 beats k = 3 by ≥ 2 | monotone at both noise levels; +8.0 and +7.3 | yes |

## What CRR contributed, and what it did not

- **Contributed: the questions.**
  - The rupture–regeneration view of a life led to separating *capacity to regenerate* (Q2) from the *chance of a
    rupture that cannot be regenerated* (Q1).
  - "Cut as first passage" led to the critical-lesion experiments (Q2b, Q2c) and the repair rule (Q5).
  - The "same present, different past" design (matched intact organ, different age) is the M7 design from the
    earlier P23 studies.

  These questions produced the main development of the paper's claim: competence is constant, failure is a
  first-passage event at a one-to-two-cell threshold, and repair should be triggered at the first wrong cell.
- **Not contributed: a better measurement.** CRR's coherence was not a useful early-warning signal (Q4). The
  first-passage reading is ordinary first-passage and nucleation theory: a small basin of attraction, noise-driven
  escape, a constant hazard. These findings need no CRR vocabulary to state or explain.

## Departures (recorded before interpretation)

- **Q4 definition.** The early-warning outcome was redefined in development, before the freeze. Organs never go
  from fully intact to lost within 50 steps (0 positives), so the outcome became loss within 100 steps among organs
  not yet lost, with damage added to the baseline. The frozen version is the redefined one.
- **Thread oversubscription.** The first test launch did not set single-threaded mode, so four jobs oversubscribed
  the cores. It was stopped before any output was analysed. The one finished file was deleted, and everything was
  rerun with `OMP_NUM_THREADS=1`. Seeds and code are unchanged.
- **AUC implementation.** The AUC function in `analyze_lifecourse.py` was replaced after the freeze by an
  equivalent rank-based version: the old tie loop took longer than the square of the sample count. The new version
  gives the identical value; it matched a brute-force pairwise AUC exactly on a test vector with ties. The frozen
  hash in `FREEZE.sha256` is of the earlier file.
- **Q2 eligibility.** It requires the injured cells to be healthy in the uninjured baseline just before the injury.
  Development files lacked that field (the driver was extended before the freeze); test files have it.

## Single most informative next experiment

Test whether the eye's fragility belongs to this evolved agent or to NCAs in general. Re-evolve the smiley agent with
the authors' training stack, with the fitness extended to reward recovery from 1–2-cell eye lesions after
development, and repeat Q1–Q2c. If evolution can buy a larger critical lesion size, the "loss of goal-directedness"
in the paper is a property of what was selected for (development only), not of ageing. That would be a direct,
testable statement about the evolution of maintenance.
