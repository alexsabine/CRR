# M19 — Derivation: Poincaré + Kac make rupture inevitable; Ω = 1/μ(coherent region)

## Claim

For an ergodic measure-preserving system, Poincaré recurrence
guarantees almost-sure return to any positive-measure region, and
Kac's lemma identifies the canonical Ω with the inverse measure of
the "coherent region": Ω = 1/μ(A_coherent).

## Assumptions

(A1) (X, B, μ, T) is a measure-preserving dynamical system with
μ(X) = 1 and T : X → X measure-preserving.
(A2) The system is ergodic: the only T-invariant sets in B have
measure 0 or 1.
(A3) "Coherent region" A ⊂ X is a measurable subset of positive
measure μ(A) > 0, identified with the set of states for which
C·Ω < 1 (i.e., pre-rupture).

## Derivation (under A1–A3)

**Poincaré recurrence theorem (1890).** For (X, B, μ, T) measure-
preserving with μ(X) < ∞, almost every x ∈ A returns to A
infinitely often: μ-a.s., {n : T^n x ∈ A} is infinite.

So under A3, for almost every initial state in A, the system
re-enters A infinitely often. Equivalently: ruptures (exits from A)
are followed almost surely by re-entries (regenerations) — the
CRR cycle is recurrent.

**Kac's lemma (1947).** For an ergodic system (A1, A2), the expected
return time to A under the induced map T_A is

    E_A[τ_A] = 1/μ(A),

where τ_A(x) = inf{n ≥ 1 : T^n x ∈ A}.

Under A3 with A = A_coherent: the expected time between ruptures
(≡ expected return time to the coherent region) is 1/μ(A_coherent).

Identification with Ω: in CRR, the canonical mean inter-rupture
interval is 1/Ω (M1 derivation). Setting these equal:

    1/Ω = 1/μ(A_coherent)    ⇒    Ω = μ(A_coherent).

So *Ω is the measure of the coherent region* under this
identification.

(Note: this gives Ω = μ(A), not Ω = 1/μ(A) as the brief might
suggest. The brief's wording in the canonical PART I asserts
"Ω = 1/μ(coherent region)" but Kac's lemma gives expected return
time = 1/μ(A); equating that to mean inter-rupture interval 1/Ω
yields Ω = μ(A). This is another sign-of-Ω convention issue
recorded in `notes/relabellings.md`.)

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M19_kac_lemma_ergodic`
simulates an ergodic interval map (e.g., the doubling map or an
irrational rotation), measures the empirical mean return time to
A = [0, μ(A)], and verifies it converges to 1/μ(A) per Kac's
lemma. Identification with Ω is then immediate.

## Caveats

- **Ergodicity is essential.** Under non-ergodic (e.g., bistable)
  dynamics, Kac's lemma fails: the expected return time depends on
  the ergodic component of the initial state. CRR's "single Ω per
  substrate" assumption requires ergodicity globally — a strong
  condition.
- **Continuous-time analogue.** Kac's lemma extends to ergodic flows
  under standard regularity (Krengel, *Ergodic Theorems*, 1985).
- **Convention issue: Ω = μ(A) vs 1/μ(A).** Recorded; resolution
  needed by the framework's author. Either Kac gives the *expected
  return time* (= 1/μ(A)) which equates to *expected inter-rupture
  interval* (= 1/Ω), yielding Ω = μ(A); OR the canonical Ω is a
  *rate*, in which case Ω = μ(A) (not 1/μ(A)) is consistent. The
  brief's language is ambiguous.

## Status

**T1 with caveat.** Poincaré + Kac are canonical theorems under
ergodicity; the CRR identification gives Ω = μ(A_coherent) (or
1/μ(A) under inverse convention). Tier capped at T1 pending
convention resolution.
