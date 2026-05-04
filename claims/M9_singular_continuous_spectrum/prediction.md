# M9 — Pre-registered novel prediction: quasi-crystal Sturmian-Hamiltonian spectral type

## Prediction

The φ-rotated CRR depth-two regeneration operator on a bounded
substrate has singular-continuous spectrum (M9 canonical claim).
The pre-registered test: a numerical Sturmian-Hamiltonian operator
constructed from a Fibonacci-substitution sequence of length
N ∈ {89, 144, 233, 377, 610, 987, 1597} (consecutive Fibonacci
numbers) shows the **fractal Cantor-set spectral signature**
characteristic of singular-continuous spectra:

1. **Total spectrum width** stays ≈ 4 (independent of N).
2. **Number of spectral gaps** of relative width > 1% scales as
   ~ log(N).
3. **Hausdorff fractal dimension** of the spectrum approaches the
   theoretical limit log(φ)/log(σ) ≈ 0.481 (Casdagli 1986; Sütő
   1989) as N → ∞.

Sandbox-runnable; all three quantitative tests can execute.

## Empirical test

**Sandbox-runnable.** No external data fetch required; the
Fibonacci-substitution Hamiltonian is fully specified by the
Fibonacci word and onsite-potential pair (α, β) with α ≠ β.

For specificity, take α = 0.5, β = −0.5 (canonical normalisation;
results are scaling-invariant under common offset).

## Protocol

For each Fibonacci length N ∈ {89, 144, 233, 377, 610, 987, 1597}:

1. Construct the Fibonacci substitution word of length N.
2. Build discrete Schrödinger Hamiltonian
   H_n = (ψ_{n+1} + ψ_{n−1}) + V_n ψ_n with V_n = α if word[n]='a'
   else β.
3. Compute eigenvalue spectrum via numpy.linalg.eigvalsh.
4. Compute total spectrum width: max − min.
5. Identify gaps of relative width > 1% × total width.
6. Estimate spectrum's *box-counting fractal dimension* d_B by
   covering with intervals of geometrically-decreasing widths.

## Quantitative pre-registration

M9 promotes to T3 iff:
- Total spectrum widths across N values agree within 5% RMS
  fluctuation (i.e., width ≈ 4 ± 0.2).
- Number of gaps grows monotonically with N.
- Box-counting dimension d_B at N = 1597 is within ±0.05 of the
  Sütő theoretical limit 0.481.

## Falsifier

If d_B at N = 1597 differs from 0.481 by more than 0.10, the
Cantor-fractal claim fails (the spectrum may instead be pure-point
or absolutely continuous in disguise).

If gap count grows faster than linearly in N (or doesn't grow at
all), the singular-continuous classification is wrong.

## Independence

The Sturmian-Hamiltonian spectrum was characterised by Sütő (1987,
1989), Bellissard et al. (1991), Damanik & Lenz (1999) — long
before CRR. The CRR claim is the *identification* of the
φ-rotated regeneration operator with this Hamiltonian; the
empirical test is whether the identified operator's spectrum
matches the well-established Sütő results.

## T3 promotion criterion

All three quantitative pre-registration conditions met ⇒
**M9 promotes to T3**.

## Applied usefulness for 2026 and beyond

- **Quasi-crystal materials science:** real quasi-crystals
  (Shechtman 2011 Nobel; Al-Pd-Mn, Al-Cu-Fe alloys) exhibit
  singular-continuous electronic spectra — the basis for their
  unusual transport properties (anomalously low conductivity
  despite metallic composition). CRR provides a *general
  framework* for predicting spectral-type → transport-property
  relationships in newly-synthesised quasi-crystal alloys.
- **Topological photonic crystals** (artificial quasi-crystals
  in nanophotonics, 2026+ active research at MIT, ETH, NTT):
  singular-continuous photonic-band-gap structure enables
  multi-frequency lasing devices; CRR-anchored design rules
  speed development.
- **Phononic-crystal vibration isolation:** Cantor-set vibrational
  spectra (engineered via 1D Fibonacci-stack structures) can
  isolate broad vibration bands; relevant for next-gen LIGO
  isolation, satellite payload damping.
- **Neural-network spectral analysis:** singular-continuous spectra
  appear in wide-network trained-weight-matrix spectra (Pennington
  et al. 2017+); CRR's φ-rotation framework gives a structural
  prediction for when wide-NN spectra are SC vs PP.
- **Biological 1/f signals (B1):** the empirical claim B1 — that
  biological 1/f signals exhibit SC spectra — depends on M9 being
  established at the mathematical level. M9-T3 unblocks B1's
  Session-3 stub.

This is the **most sandbox-tractable** Session-4 prediction;
expected to execute fully in the campaign environment in Session 5.
