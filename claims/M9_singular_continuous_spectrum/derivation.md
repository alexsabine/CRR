# M9 — Derivation: φ-rotated CRR has singular-continuous spectrum

## Claim

The CRR depth-two regeneration operator with φ-rotated coefficients
on a bounded substrate has spectrum in the *singular-continuous*
class (Fibonacci-chain spectral type), distinct from pure-point
(periodic) and absolutely-continuous (free) spectra.

## Assumptions

(A1) The depth-two recurrence operates on a bounded substrate
indexed by n, with coefficients V_n drawn from a Fibonacci substitution
sequence (the standard Fibonacci-chain Schrödinger operator).
(A2) The "rotation" is by an angle 2π/φ ≈ 3.883 rad (or its irrational
co-rotation).
(A3) The operator is the discrete Schrödinger operator
H ψ_n = ψ_{n+1} + ψ_{n−1} + V_n ψ_n with V_n in the Fibonacci
class.

## Derivation (under A1–A3)

The Fibonacci substitution rule generates a sequence on {a, b}:

    a → ab,    b → a.

Starting from a, the sequence is a, ab, aba, abaab, abaababa, ...
This is an aperiodic but deterministic sequence with quasi-periodic
structure on golden-ratio-spaced sites.

The Schrödinger operator H with potential V_n drawn from this
sequence (V_n = α if a, β if b for chosen constants α, β with
α ≠ β) is the **Fibonacci-chain Hamiltonian**.

The spectrum of this operator was characterised in a sequence of
foundational results:

- **Sütő (1987).** For the Fibonacci-chain Hamiltonian, the spectrum
  is a *Cantor set* of zero Lebesgue measure. (J. Stat. Phys. 56:525.)
- **Bellissard, Bovier, Ghez (1991).** The spectral measure is
  purely *singular continuous* — neither pure-point nor absolutely
  continuous. (Comm. Math. Phys. 135:379.)
- **Damanik, Lenz (1999).** Generalisation to arbitrary Sturmian
  potentials confirms singular-continuous spectrum for almost every
  rotation number, including the golden ratio. (Comm. Math. Phys.
  207:687.)

Identification with the CRR setting: under M7 + M8, the
"depth-two regeneration operator with golden-ratio-related
coefficients" maps to a Fibonacci-substitution Hamiltonian, and the
above spectral-type result applies directly. Hence the φ-rotated CRR
on a bounded depth-two substrate has singular-continuous spectrum.

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M9_fibonacci_spectrum_cantor`
constructs the Fibonacci-chain Hamiltonian for chains of length
N = 89, 144, 233 (consecutive Fibonacci numbers), diagonalises, and
verifies the spectrum's *number of bands* (gaps in the discrete
spectrum) grows as expected for a Cantor-like structure (qualitative
check; full singular-continuous classification requires N → ∞).

## Caveats

- **The result is borrowed.** The spectral-type theorem is due to
  Sütő, Bellissard et al., not to CRR. The CRR-specific content is
  the *identification* of the φ-rotated regeneration operator with
  the Fibonacci-chain Hamiltonian (under M7, M8).
- **The identification depends on the discrete Schrödinger form.**
  The CRR regeneration operator includes an exp(C/Ω) kernel, not a
  simple finite-difference Schrödinger operator. Whether the
  spectral-type result transfers depends on a regularity/relabelling
  argument that is not fully spelled out in the canonical brief.
- **Recorded in `notes/relabellings.md`** as a partial relabelling:
  the spectral-type classification is canonical; CRR's contribution
  is the identification, which may itself require independent
  justification.

## Status

**T1 with caveat.** Derivation rests on the Sütő-Bellissard-Damanik
chain plus an identification step that is partially justified.
Tier capped at T1 pending the identification's full justification.
