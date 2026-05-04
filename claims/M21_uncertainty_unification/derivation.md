# M21 — Derivation: C·Ω = 1 simultaneously saturates CR + HG + TUR

## Claim

The rupture condition C·Ω = 1 simultaneously saturates the
Cramér-Rao bound (M3), the Heisenberg-Gabor uncertainty (M4), and
the thermodynamic uncertainty relation (TUR).

## Assumptions

(A1) M3 holds: under (C ≡ Fisher info, Ω ≡ estimator variance),
C·Ω = 1 saturates CR.
(A2) M4 holds: under (C ≡ Δt², Ω ≡ Δω²), C·Ω = 1 saturates HG.
(A3) Identification for TUR: C ≡ entropy production Σ over an
observation window, Ω ≡ Var(J)/⟨J⟩² (the relative variance of an
empirical current J).
(A4) The TUR (Barato-Seifert 2015) reads

    Var(J)/⟨J⟩² ≥ 2 / Σ.

## Derivation (under A1–A4)

CR and HG saturations under C·Ω = 1 are M3 and M4 respectively,
already derived.

For TUR: the inequality

    Var(J)/⟨J⟩² ≥ 2/Σ

rearranges to

    Σ · Var(J)/⟨J⟩² ≥ 2.

Identifying Σ ≡ C and Var(J)/⟨J⟩² ≡ Ω:

    C · Ω ≥ 2.

So under A3, the TUR saturation reads C·Ω = **2**, not C·Ω = 1.

To match the canonical "C·Ω = 1" condition, one must absorb the
factor of 2 into the definitions: e.g., redefine C ≡ Σ/2 (or Ω ≡
2·Var(J)/⟨J⟩²). With this convention adjustment, all three
saturations coincide at C·Ω = 1.

So the unification is **convention-aligned**, not naturally
parameter-free: M21 holds under M3 + M4 + (A3') where A3' includes
a factor-of-2 absorption into the TUR identification.

The deeper claim — that the *same algebraic structure* underwrites
all three uncertainty principles — is true to the extent that all
three are equality cases of Cauchy-Schwarz-type inequalities on
appropriate inner-product spaces (Fisher-Rao for CR, time-frequency
L² for HG, large-deviation rate functions for TUR). This common
structure is well-established in mathematical physics; the CRR
statement is a packaging of that structure.

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M21_tur_factor_two`
constructs a simple Markov-chain current example, computes Σ and
Var(J)/⟨J⟩², and verifies Σ · Var(J)/⟨J⟩² is bounded below by 2 (not
1) — confirming the factor-of-2 issue.

## Caveats

- **Not parameter-free across the three relations.** The CR and HG
  saturations naturally read C·Ω = 1 under their respective
  identifications; TUR naturally reads C·Ω = 2. The "one master
  condition" emerges only after a convention-fixing rescaling of one
  of the three.
- **Partial relabelling.** The common Cauchy-Schwarz-equality
  structure of CR, HG, TUR is canonical; the CRR statement is
  one-step packaging.
- Capped at T1 pending demonstration of a novel CRR-specific
  consequence of the joint saturation not reducible to the three
  individual saturations.

## Status

**T1 with caveat (post-resolution-session unchanged).** The
rupture-topology / Lie-group-memory framework
(`notes/rupture_topology.md`) **does not** resolve the TUR
factor-of-2 mismatch. The TUR's factor of 2 is a property of the
bound, not of the Z₂ rupture. Direct identification gives C·Ω = 2
at TUR saturation, not C·Ω = 1.

**Recommended resolution** (`notes/conventions.md` §"What the
canonical brief should say" item 5): rephrase M21 as

> "C·Ω = 1 saturates Cramér-Rao and Heisenberg-Gabor; the
> thermodynamic uncertainty relation has the same Cauchy-Schwarz-
> equality structure but saturates at C·Ω = 2 under canonical
> identification (or at C·Ω = 1 with C ≡ Σ/2)."

Tier remains T1; this is the only flagged inconsistency from
Sessions 1–2 that does **not** dissolve under the resolved
rupture-topology framing.
