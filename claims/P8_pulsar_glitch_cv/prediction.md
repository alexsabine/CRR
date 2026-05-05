# P8 — Pre-registered prediction (Session 7)

**Pre-registered before any data lookup or analysis.**

## Statement

Mean inter-glitch interval CV across the **two most-glitch-rich
catalogued pulsars** (Vela PSR J0835-4510 and Crab PSR B0531+21,
both with multi-decade glitch records in the Jodrell Bank pulsar
glitch catalogue) satisfies:

    median(CV) = 1/(2π) ± 30%   = [0.1114, 0.2069]

i.e., **at least 1 of 2** pulsars has CV in [0.10, 0.22] (broader
band).

## Sampling protocol (locked)

1. Data source: Jodrell Bank pulsar glitch catalogue (Espinoza et
   al. 2011 + ongoing updates), or equivalent ATNF compilation.
2. Inclusion: all glitches Δν/ν > 1e-9 (canonical "true glitch"
   threshold) at Vela and Crab through to data-fetch date.
3. Statistic: CV = SD(inter-glitch-interval) / mean(inter-glitch-
   interval). Single-pulsar cohorts.
4. Selection: top-2 by glitch count. (Vela ~24 glitches, Crab ~30
   glitches as of 2024.)

## Pre-registered conditions

- **C1.** median(CV) ∈ [0.111, 0.207] = 1/(2π) ± 30%.
- **C2.** At least one of {Vela, Crab} CV in [0.10, 0.22].
- **C3.** No cohort CV < 1/(4π) ≈ 0.080.

## Falsifier

median(CV) outside [0.08, 0.30] ⇒ Z₂-rupture identification fails
for pulsar glitches.

## Tier promotion

All three ⇒ T1 → T3. C1+C2 only ⇒ T2. C1 only ⇒ T2 (m). C1 fail
⇒ stays T1.

## Independence

Glitch catalogues pre-date CRR; no cohort here was used to derive
1/(2π).

## Honest exposure

Glitch inter-arrival CVs are widely reported in the pulsar
literature; rough prior is "of order 1" (Poissonian-ish), so a
result near 0.16 would be a non-trivial confirmation.
