# M4 — Derivation: C·Ω = 1 saturates Heisenberg-Gabor

## Claim

The CRR rupture condition C·Ω = 1 is the equality case of the
Heisenberg-Gabor uncertainty inequality Δt · Δω ≥ 1/2 (or
equivalent normalisation Δt · Δω ≥ 1 in the unit-circular-frequency
convention).

## Assumptions

(A1) C plays the role of (squared) temporal localisation Δt² of a
signal centred at the rupture instant.
(A2) Ω plays the role of (squared) spectral localisation Δω².
(A3) The inequality is taken in the convention where saturation reads
Δt · Δω = 1 (Gabor units), realised by the Gabor wavelet
g(t) = (1/(πΔt²))^{1/4} · exp(−t²/(2Δt²)) with bandwidth Δω = 1/Δt.

## Derivation (under A1–A3)

The Heisenberg-Gabor inequality for any L²(ℝ) signal f is

    Δt · Δω ≥ 1/2 · ‖f‖²  (with the standard 2π-frequency convention)

or, in the alternative *Gabor* convention used here,

    Δt² · Δω² ≥ 1.

Equality is achieved *uniquely* by the Gabor (Gaussian) wavelet, by
the standard Heisenberg-Pauli-Weyl theorem.

Under A1, A2: Δt² ≡ C, Δω² ≡ Ω. Substituting into the equality case:

    C · Ω = 1.

This is the CRR rupture condition. So C·Ω = 1 expresses
Heisenberg-Gabor saturation under the time-frequency identification
A1, A2.

The brief's stronger statement — "δ(now) is the centre of a
minimum-uncertainty Gabor wavelet" — follows from the
Heisenberg-Pauli-Weyl uniqueness: the rupture instant is the centre
of the unique signal that saturates the time-frequency uncertainty.

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M4_gabor_saturation`
constructs a Gaussian Gabor wavelet g(t) on a finite grid, computes
its temporal variance Δt² and the spectral variance Δω² from the
discrete FFT, and verifies Δt² · Δω² → 1 as the grid is refined.

## Caveats

- **Identification of C, Ω with second moments.** A1 and A2 are
  *interpretive* identifications: under M13, C is accumulated Fisher
  information; calling it Δt² adopts a specific time-frequency
  picture that is not derived from M13 directly. The bridge requires
  thinking of Fisher information for a *temporal localisation*
  parameter, which gives Δt²-like quantities by general
  Cramér-Rao-vs-Heisenberg correspondence (see M5).
- **Convention issues.** Different texts saturate at Δt·Δω = 1/2,
  1, π, or 1/(4π); the CRR convention here is Δt²·Δω² = 1 (Gabor).
  The numerical value of the saturation depends on this convention.
- **The exp → e issue (recorded in `relabellings.md`) is independent
  of M4.** The derivation here does not rely on exp(C/Ω) = e at the
  saturation point.

## Status

**T1.** Derivation is one substitution into Heisenberg-Pauli-Weyl
under stated convention. Verification numerical to grid limit.
