# P17 — Pre-registered prediction (Session 7)

**Pre-registered before any data lookup or analysis.**

## Statement

CRR canonical: target: extends M10-α³ T3 cluster to Z=4. Cohort search protocol locked below.

## Sampling protocol (locked)

1. Source: Yerokhin & Shabaev 2015 J. Phys. Chem. Ref. Data 44, 033103.
2. Use ν_L(Be³⁺ 2S) ≈ 178 GHz (theoretical leading-order estimate from Bethe + standard QED, primary source pending reviewer access).
3. Compute B(Be³⁺) = ν_L × n³ / (Z⁴ × Ry × log(1/(Zα)²)).
4. Test: |B(Be³⁺) − ⟨B⟩_v3| / ⟨B⟩_v3 < 0.15 (broader band than v3 at ±10% to allow for higher-order QED at Z=4).

## Pre-registered conditions

**C1.** |B(Be³⁺) − ⟨B⟩_v3| / ⟨B⟩_v3 < 0.15 (≤ 15%).
**C2.** Five-system spread (max−min)/mean < 0.15.
**C3.** ⟨B⟩_v4 still satisfies |⟨B⟩_v4 − (8/3π)·α³| / target < 0.30.

## Falsifier

|deviation from cluster mean| > 0.30 ⇒ M10-α³ fails to extend beyond Z=3.

## Tier promotion

C1+C2+C3 ⇒ T1 → T3. C1+C2 only ⇒ T2. C1 only ⇒ T2 (m). C1 fail ⇒
stays T1.

## Independence

Data sources pre-date CRR; the cohort selection rule is locked
before lookup; no cohort here was used to derive the canonical
target value.

## Honest exposure

PRELIMINARY only (sandbox-limited primary-source access). Reviewer execution required for confirmed verdict.
