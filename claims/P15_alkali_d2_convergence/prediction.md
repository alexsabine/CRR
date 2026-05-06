# P15 — Pre-registered prediction (committed before analysis)

## Statement

The atomic CV statistic CV = A/(2π·ν₀) for the **D2 resonance line**
(ns₁/₂ → np₃/₂) of each alkali metal, when inverted to f via

    f_meas = α³ / (4π · CV),

shall converge to f_pred = 2 across the alkali series {Li, Na, K,
Rb, Cs, Fr}.

## Quantitative pre-registration (committed before reading data)

Three nested conditions, in increasing strength:

### Primary (T3 promotion criterion)

Restricting to the **convergent core** {K, Rb, Cs, Fr} (atomic
number Z ≥ 19, where the F-Structure paper §11.1 expects the
correlation-weak regime to hold):

    median(f_meas) ∈ [1.85, 2.15]   AND
    max(|f_meas − 2|) / 2 ≤ 0.20    AND
    N ≥ 4.

A 5% tolerance on the median plus a 20% tolerance on each
individual element is the band the F-Structure paper itself
clears at 1.5% mean error on K / Rb / Cs.

### Secondary (Francium-specific, from F_Structure §11.2)

For Francium D2 specifically:

    |CV(Fr D2) − α³/(8π)| / (α³/(8π))  ≤  0.20.

i.e., predicted CV = 1.545 × 10⁻⁸; band [1.236, 1.854] × 10⁻⁸.

### Tertiary (light-s deviant marker, from F_Structure §11.1)

The two light alkalis {Li, Na} are *expected* to deviate. We
pre-register that they fall *outside* the [1.85, 2.15] f-band but
*remain* below the f = 3.0 ceiling and above the f = 1.0 floor.
This is a "deviant-but-bounded" structural prediction, not a T3
condition.

## Falsifier

P15 is falsified if:

- Any one of {K, Rb, Cs, Fr} has |f_meas − 2|/2 > 0.30 (50% beyond
  the F-Structure validation band), OR
- median(f_meas) over {K, Rb, Cs, Fr} falls outside [1.70, 2.30].

## Empirical test — data sources

All values used in the analysis are **canonical published constants
from established atomic-physics references**, not from the present
sandbox (which cannot reach NIST). The references are explicit:

| Element | Transition | τ (ns) | λ (nm) | Reference |
|---------|-----------|--------|--------|-----------|
| Li | 2S₁/₂ → 2P₃/₂ | 27.102 | 670.776 | NIST ASD via [Steck rev]; McAlexander et al. 1996 |
| Na | 3S₁/₂ → 3P₃/₂ | 16.299 | 588.995 | Steck "Sodium D Line Data" |
| K  | 4S₁/₂ → 4P₃/₂ | 26.34  | 766.701 | Steck "Potassium D Line Data" |
| Rb | 5S₁/₂ → 5P₃/₂ | 26.24  | 780.241 | Steck "Rubidium 87 D Line Data" |
| Cs | 6S₁/₂ → 6P₃/₂ | 30.473 | 852.347 | Steck "Cesium D Line Data" |
| Fr | 7S₁/₂ → 7P₃/₂ | 21.02  | 718.184 | Simsarian et al. 1998 (PRL 80, 4346); Grossman et al. 2000 |

Steck's reviews are referenced directly by F_Structure.pdf at
citation [31]; they are the same source from which the original
49-element sample's K / Rb / Cs values were drawn.

## Protocol

1. For each element, compute A = 1/τ.
2. Compute ν₀ = c/λ.
3. Compute CV = A/(2π·ν₀).
4. Compute f_meas = α³/(4π·CV) using α = 1/137.035999084.
5. Report f_meas per element.
6. Apply the three pre-registration conditions above.

## Independence

The K / Rb / Cs values for the original 49-element sample were
also drawn from Steck's reviews. Re-using these specific elements
is therefore *not* fully independent — it is a re-derivation
under the explicit α³/(4π·f) formulation as a calibration check.

The genuinely *new* tests are:
- **Fr** — never tested in the original 49 (F-Structure §11.2).
- **Li** — flagged as a deviant in §11.1, tested explicitly here
  to verify the deviation-without-overflow structural prediction.
- **Na** — same as Li.

So P15 has 3 calibration entries (K, Rb, Cs) and 3 genuinely-new
entries (Li, Na, Fr).

## T3 promotion criterion

All three nested conditions met as written above.
