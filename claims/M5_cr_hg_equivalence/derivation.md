# M5 — Derivation: Cramér-Rao saturation = Heisenberg-Gabor saturation

## Claim

The Cramér-Rao saturation condition (C·Ω = 1 under M3 identifications)
and the Heisenberg-Gabor saturation condition (C·Ω = 1 under M4
identifications) express the same theorem under conjugate-variable
correspondence.

## Assumptions

(A1) M3 identifications: C ≡ Fisher information I(θ), Ω ≡ Var(θ̂).
(A2) M4 identifications: C ≡ Δt², Ω ≡ Δω².
(A3) The conjugate-variable correspondence: time t ↔ angular
frequency ω is the canonical Pontryagin / Fourier conjugate pair;
parameter θ ↔ estimator θ̂ is the statistical conjugate pair.

## Derivation (under A1–A3)

The classical chain (see Cohen, *Time-Frequency Analysis*, 1995,
Chapter 3; Helstrom, *Quantum Detection and Estimation Theory*,
1976, Chapter 8):

**Step 1 — Fisher information of a translation parameter.** For a
signal f(t) translated by an unknown offset θ (i.e., observed
y(t) = f(t − θ)), the Fisher information of θ is

    I(θ) = ∫ |f'(t)|² dt / ∫ |f(t)|² dt = (Δω)²

where Δω is the RMS bandwidth of f. (Standard result.)

**Step 2 — CR bound on translation estimation.** The CR bound says
Var(θ̂) ≥ 1/I(θ) = 1/(Δω)². The corresponding Δt is the RMS
spread of the estimator θ̂, which under the maximum-likelihood
estimator equals the temporal spread of f itself.

**Step 3 — Equivalence at saturation.** When the estimator achieves
CR equality, Var(θ̂) = 1/I, so

    Δt² · Δω² = 1.

This is exactly the Heisenberg-Gabor saturation under Gabor
convention. So the CR equality and the HG equality are the *same
algebraic statement* obtained by reading C·Ω = 1 under conjugate
identifications.

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M5_cr_hg_equivalence`
constructs a Gaussian wavelet g(t) of width Δt, computes its Fisher
information for a translation parameter via numerical differentiation
(Step 1), takes its bandwidth Δω from the FFT, and verifies
I(θ) = (Δω)² and Δt² · I(θ) = 1 to grid precision.

## Caveats

- **This is a relabelling.** The CR↔HG correspondence at the
  translation-parameter saturation point is canonical statistical
  signal-processing material (see Cohen 1995; Helstrom 1976; van
  Trees 2001). The CRR statement adds the variable names C, Ω
  on top of the existing equivalence; it does not establish a new
  theorem.
- **Capped at T1 per discipline.** Recorded in
  `notes/relabellings.md` as a confirmed relabelling. No further
  promotion possible on the basis of the underlying canonical result.
- **Genuine novelty would require:** a CRR-specific consequence of
  the equivalence not deducible from the canonical CR↔HG
  correspondence alone — e.g., a non-translation parameter regime
  where the CRR identification still works but the canonical
  correspondence fails. None demonstrated to date.

## Status

**T1 (relabelling).** Derivation is the canonical CR↔HG chain.
Tier hard-capped at T1.
