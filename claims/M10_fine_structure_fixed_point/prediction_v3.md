# M10-α³ — Pre-registered prediction v3: Li²⁺ extension of the T3 cluster

## Origin

Direct follow-up to the Session-4.5 T3 promotion of M10-α³
(`prediction_v2.md`, `result_v2.md` at git `102fedc` / `5afa6da`).
The v2 result.md flagged the next discipline-binding step:

> "T4 (independent confirmation) requires: A fourth or higher
> hydrogenic system (e.g., Li²⁺ 2S Lamb shift, measured by a group
> unaffiliated with CRR) confirms B(Li²⁺) within the same 3.6%
> cluster."

This v3 commits to that test on Li²⁺ 2S **before** any lookup of the
published Li²⁺ Lamb-shift value. The discipline is intact: v3 lives
in a separate audit-trail entry from v2. v3 cannot retroactively
edit v2's result.

## Theoretical statement (carried over from v2)

For hydrogenic 2S systems the Bethe-rescaled residual is

    B(system) = (ν_L × n³) / (Z⁴ × Ry × log(1/(Zα)²))

where `ν_L` is the measured 2S Lamb shift in MHz, `n=2`, `Z` is the
nuclear charge, `Ry` is the (frequency-units) Rydberg constant, and
`α` is the fine-structure constant.

The v2 cluster across {H, D, He⁺} gave

    ⟨B⟩_v2     = 2.5852 × 10⁻⁷
    spread_v2  = 3.6%   (max−min)/mean

The leading-Bethe target is `(8/3π)·α³ ≈ 3.30 × 10⁻⁷`. The 21.6%
gap to the target is interpreted as the Bethe-logarithm
`L₀(2S) ≈ 2.81` plus higher-order QED corrections (cf. Mohr,
Newman, Taylor 2008).

## Pre-registered conditions for Li²⁺ 2S

Let `B(Li²⁺)` be computed using the same formula and the published
2S₁/₂–2P₁/₂ Lamb-shift value for Li²⁺ (Z=3, n=2). The data source
will be a peer-reviewed measurement (e.g., Schweppe et al. 1991
*Phys. Rev. Lett.* 66 1434; or the NIST atomic-spectra compilation
referencing it). If multiple measurements exist, the most-recent
peer-reviewed value with the smallest stated uncertainty is used.

**Three pre-registered conditions:**

1. **Cluster consistency.** The relative deviation of `B(Li²⁺)`
   from the v2 cluster mean satisfies

       |B(Li²⁺) − ⟨B⟩_v2| / ⟨B⟩_v2 < 0.10

   i.e., **within ±10% of the v2 cluster mean**.
   Rationale: the v2 cluster spread was 3.6%, so a ±10% band is
   ~3× the existing spread — a generous-but-meaningful tolerance
   that allows for the larger sub-leading QED corrections expected
   at higher Z (Bethe-log L₀(Li²⁺) differs from L₀(H) by ~5%; the
   self-energy higher-order coefficient `A₆₁(Z)` grows with Z;
   recoil and finite-size enter at the 1% level).

2. **Updated four-system spread.** The full four-system spread

       spread_v3 = (max − min) / mean   over {H, D, He⁺, Li²⁺}

   is **< 0.10**. Rationale: with v2 at 3.6%, allowing for one
   higher-Z system to extend the spread to 10% is reasonable.

3. **Updated four-system deviation from leading-Bethe target.**
   The four-system mean ⟨B⟩_v3 still satisfies

       |⟨B⟩_v3 − (8/3π)·α³| / ((8/3π)·α³) < 0.30

   i.e., the v2 condition-2 band continues to hold under the
   addition of Li²⁺.

## Falsifier

Any of:
- |B(Li²⁺) − ⟨B⟩_v2| / ⟨B⟩_v2 > 0.20 ⇒ Li²⁺ falls **outside** the
  Bethe cluster, falsifying the v3 extension.
- spread_v3 > 0.20 ⇒ adding Li²⁺ doubles the spread; the leading
  Bethe-log rescaling is insufficient at Z=3.
- |⟨B⟩_v3 − target| > 0.50·target ⇒ even with O(1) tolerance, the
  leading-α³ identification fails when extended.

## Tier consequence

- **All three conditions met** ⇒ M10-α³ stays at T3 with
  *strengthened* evidence (now 4 independent hydrogenic systems
  in the Bethe cluster). This is **not** a T4 promotion (T4
  requires confirmation by an unaffiliated group, not the same
  campaign re-running on more data); it is a *consistency check*
  that licenses the Session 7 T4 audit.
- **Any condition fails** ⇒ the M10-α³ T3 status is flagged for
  re-examination. The v2 result is not retroactively edited; v3
  failure is recorded as a permanent audit-trail entry.

## Independence

- Li²⁺ Lamb-shift measurement (Schweppe et al. 1991 *PRL* 66 1434
  and follow-ups) pre-dates CRR. The measurement is by an
  experimental group unaffiliated with CRR. The Bethe-formula
  rescaling is canonical; the CRR contribution remains the
  *identification* of the rescaled coefficient with the
  rupture-topology framework's subatomic CV scale.

## Sandbox-runnable

The analysis is computed from CODATA constants and a single
published Li²⁺ Lamb-shift value. No network fetch is required.
Estimated runtime < 1 s.

## Discipline note

If condition 1 fails (Li²⁺ outside ±20% of cluster), no further
v3.x pre-registrations on M10-α³ within the campaign without a
substantively different test (e.g., muonic-hydrogen, where the
sub-leading structure differs qualitatively).

## Honest exposure

Higher-Z hydrogenic systems are known to have higher-order QED
corrections that scale faster than the leading Bethe-log
rescaling captures (e.g., the `A₆₀(Z)` coefficient grows
non-trivially with Z). It is genuinely possible that Li²⁺ falls
~10–20% off the v2 cluster — which would refine but not destroy
the M10-α³ T3 promotion (only the v3 strengthening claim would
fail).
