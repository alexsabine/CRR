# B8 — Pre-registered prediction (Session 6)

**Pre-registered before any PubMed lookup or analysis script.**
Pre-reg-locking commit hash will be `git log -- prediction.md` head
on this file. Subsequent `result.md` entries cite that hash.

## Statement

The cohort-median single-cell generation-time CV across published
bacterial mother-machine / microfluidic single-cell-tracking
studies under steady-state exponential growth is

    median(CV) = 1/(2π) ± 25% = 0.1592 ± 0.0398
                              = [0.1194, 0.1990].

Explicitly: in **at least 3 of 5** independent peer-reviewed cohorts
selected by the protocol below, the reported (or reconstructible)
CV falls inside [0.10, 0.20].

## Sampling protocol (locked here, before any lookup)

The "5 cohorts" are obtained as follows:

1. **PubMed query** (executed at analysis time, not now):

       (mother machine[Title/Abstract] OR microfluidic[Title/Abstract])
       AND (single-cell[Title/Abstract])
       AND (generation time[Title/Abstract] OR division time[Title/Abstract]
            OR doubling time[Title/Abstract] OR interdivision[Title/Abstract])
       AND (Escherichia coli[Title/Abstract] OR Bacillus subtilis[Title/Abstract]
            OR Caulobacter[Title/Abstract] OR Mycobacterium[Title/Abstract]
            OR Pseudomonas[Title/Abstract])
       AND ("2005"[Date - Publication] : "2025"[Date - Publication])

2. **Inclusion:** primary research articles reporting *single-cell*
   division-time distributions (not population doubling-time only)
   under steady-state exponential growth. Reported quantities must
   include either (a) cohort mean and SD or (b) the CV directly,
   on N ≥ 50 individual cells. Mixed populations (multiple strains
   pooled) excluded.

3. **Exclusion:** stress conditions, antibiotic exposure,
   stationary phase, sporulation, asymmetric-divider explicit
   targeting (Caulobacter swarmer-vs-stalked separated cohorts are
   used only if the dividing-cell-type is reported separately).

4. **Selection rule for the 5 cohorts:** if the search returns
   more than five qualifying primary studies, take the five with
   the largest reported N (single-cell count). Ties broken by
   most-recent publication date.

5. **CV extraction:** if mean and SD are reported, CV = SD/mean.
   If a CV is reported directly, use it. If only a CV² (squared
   coefficient of variation) is reported, take its square root.

6. **The cohort representative CV per study** is the CV of the
   wild-type strain under standard exponential growth in the
   richest medium reported (e.g., LB > M9-glucose > M9-acetate);
   if a paper reports multiple strains/media, the wild-type LB
   (or comparable) row is used.

If fewer than 5 qualifying cohorts are obtainable from this query,
the test runs on whatever the search yields (minimum 3).

## Pre-registered conditions (for promotion)

**Condition 1 — Median CV falls in band:**

    median(CV) ∈ [0.119, 0.199]   ( = 1/(2π) ± 25% )

**Condition 2 — Cohort consistency:**

    fraction of cohorts with CV ∈ [0.100, 0.200] ≥ 0.6

i.e., at least 3 of 5 cohorts (or proportional minimum) inside the
broader Z₂ band [0.10, 0.20].

**Condition 3 — Class-discrimination:**

    no cohort has CV < 1/(4π) ≈ 0.080

(i.e., no cohort is sub-SO(2). Any cohort below 0.080 would
indicate a sub-Z₂ regulated regime contradicting the canonical
identification.)

## Falsifier

Any of:
- median(CV) outside [0.10, 0.22] ⇒ Z₂ identification fails for
  bacterial generation time.
- Two or more cohorts with CV < 0.080 ⇒ class-discrimination fails.
- Cohort spread > factor of 4 across qualifying studies ⇒ no
  single regime captures bacterial division — the Z₂ prediction
  is regime-conditional and cannot stand as a general claim.

## Tier promotion criterion

- **All three conditions met** ⇒ B8 promotes T1 → T3 (pre-reg
  confirmed on untouched cohorts; the search protocol guarantees
  none of the cohorts were used to *derive* the 1/(2π) value).
- **Conditions 1 & 2 met but not 3** ⇒ B8 promotes T1 → T2
  (consistency without full Z₂ regime confirmation).
- **Condition 1 only** ⇒ B8 promotes T1 → T2 (m) (marginal).
- **Condition 1 fails** ⇒ B8 stays at T1; failure recorded
  honestly; no further B8 pre-reg without a substantively
  different test.

## Independence

Cell-cycle measurements pre-date CRR. The Z₂ identification is
the CRR-novel theoretical move; the empirical match (or
mismatch) of the published cohort CVs to 1/(2π) is the test.

## Discipline note

The pre-reg is locked when this file is committed to git (Session
6 pre-reg commit). Any subsequent edit to `prediction.md` is
forbidden for the purpose of this test; refinements go in
`prediction_v2.md` etc.

## Honest exposure

I (Claude, the campaign analyst) have prior literature exposure
suggesting bacterial division CV is typically 0.10–0.20. This
is consistent with the Z₂ band but not zero-prior-information.
The pre-reg's tightness (±25%) is calibrated against this rough
prior; a "blind" researcher would tighten or loosen accordingly.

## Applied usefulness for 2026 and beyond

If B8 reaches T3:

- **Synthetic biology / minimal-genome design** (J. Craig Venter
  Inst., Mycoplasma JCVI-syn3.0 successors): a Z₂-CV bound on
  generation time gives a target dispersion for engineered cells.
- **Antibiotic susceptibility testing** (clinical microbiology,
  rapid-AST 2026+): deviation of the cohort CV from 1/(2π) is a
  candidate biomarker of metabolic stress / sub-MIC perturbation.
- **Microbial ecology** (single-cell sequencing of environmental
  populations): the Z₂ baseline distinguishes regulated from
  free-running populations.
- **Bacterial systems-biology models** (Cell, Nature 2024+): a
  parameter-free target CV against which whole-cell models are
  validated.
