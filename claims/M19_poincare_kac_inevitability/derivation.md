# M19 — Derivation: Poincaré + Kac make rupture inevitable; Ω = μ(coherent region)

## Claim (corrected statement)

For an ergodic measure-preserving system, Poincaré recurrence
guarantees almost-sure return to any positive-measure region, and
Kac's lemma identifies the canonical Ω with the **measure** of the
coherent region:

    Ω = μ(A_coherent).

(The brief's wording is Ω = 1/μ(A); under convention C5 in
`notes/conventions.md` this is corrected to Ω = μ(A) by the Kac
identification.)

## Resolved framing (post-Session-2 convention update)

The Session-2 derivation flagged the Ω vs 1/Ω convention ambiguity.
It is now resolved by convention C5: Ω is rate-like (μ(A)) under the
Kac identification. The brief's "Ω = 1/μ(A)" wording is a typo.

## Assumptions

(A1) (X, B, μ, T) is a measure-preserving dynamical system with
μ(X) = 1 and T : X → X measure-preserving.
(A2) The system is ergodic.
(A3) "Coherent region" A ⊂ X has μ(A) > 0; it is the set of states
with C·Ω < 1 (pre-rupture).
(A4) Convention C5: Ω is rate-like — equals the rupture frequency,
i.e., 1/(mean inter-rupture interval).

## Derivation (under A1–A4)

**Poincaré recurrence theorem.** Almost every x ∈ A returns to A
infinitely often.

**Kac's lemma.** Under A1, A2: E_A[τ_A] = 1/μ(A), where
τ_A(x) = inf{n ≥ 1 : T^n x ∈ A} is the first return time.

By A4: Ω = 1/(mean inter-rupture interval). The mean inter-rupture
interval *equals* the mean return time to A (each rupture marks an
exit-and-return cycle):

    1/Ω = E_A[τ_A] = 1/μ(A).

Hence

    **Ω = μ(A_coherent).**

So Ω is the *measure* of the coherent region — large coherent
region ⇒ frequent rupture (large Ω); small coherent region ⇒ rare
rupture (small Ω). This is consistent with Ω being a *precision-
like rate* in the canonical brief.

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M19_kac_lemma_irrational_rotation`
simulates an irrational rotation T(x) = (x + 1/φ) mod 1 (uniquely
ergodic), measures the mean return time to A = [0, 0.1], and
verifies it converges to 1/μ(A) = 10. The corresponding Ω = μ(A) =
0.1 is therefore the rupture rate.

`crr-engine/tests/test_rupture_topology.py::test_M19_resolved_kac_omega_equals_mu`
asserts Ω = μ(A) explicitly under convention C5.

## Caveats

- **The brief's Ω = 1/μ(A) is a typo** under convention C5; the
  corrected form is Ω = μ(A_coherent). Recorded in
  `notes/conventions.md`.
- **Ergodicity is essential.** Non-ergodic systems have multiple
  ergodic components, each with its own Ω = μ(A | component); the
  global Ω is not single-valued.
- **Continuous-time analogue** holds for ergodic flows under
  standard regularity (Krengel 1985).

## Status

**T1.** Convention resolved: Ω = μ(A_coherent). Derivation rests
on Poincaré recurrence + Kac's lemma under ergodicity.
