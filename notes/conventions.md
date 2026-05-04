# CRR convention dictionary

This document fixes a unified set of conventions for the CRR
formalism, applies them to the inconsistencies catalogued in
`notes/relabellings.md`, and documents which issues are resolved
and which remain open.

The conventions adopted here follow the rupture-topology analysis
in `notes/rupture_topology.md` (hypotheses H1, H2, H3).

---

## Core conventions

### C1. Rupture is Z₂ by construction.

The rupture event is structurally Z₂ — a single Bernoulli(1/2) draw
at the threshold C·Ω = 1, with codomain {0, 1}. This is forced by
three independent structural arguments (Dirac-delta form, Heaviside-
derivative form, Cramér-Rao saturation under M3); see
`notes/rupture_topology.md` H1.

**Implication:** The "Z₂" label in CRR refers always to the rupture
topology. It is *not* a substrate alongside SO(2). When the brief
says "Z₂ substrate," read "Z₂ rupture with no continuous-phase
memory."

### C2. The phase manifold is a compact connected Lie group G.

The continual memory-bearing manifold is a compact connected Lie
group G, with bi-invariant Riemannian metric and closed-geodesic
length φ_G.

Canonical examples:
- G = U(1) ≅ SO(2): φ_G = 2π.
- G = SU(2) ≅ S³: φ_G = 2π.
- G = SO(3) = SU(2)/Z₂: φ_G = π.
- G = T^n (n-torus): φ_G = 2π in each generator direction.
- G = pure-Z₂ (no continuous-phase content): φ_G = π (half-turn
  embedding in any larger G containing Z₂ as discrete subgroup).

### C3. Two distinct Ωs.

The symbol Ω in the canonical brief refers to two distinct quantities
that should be disambiguated:

| Symbol | Definition | Domain | Canonical value |
|--------|-----------|--------|-----------------|
| Ω_geo | 1 / φ_G (geodesic Ω of phase manifold G) | Geometry | 1/(2π) for SO(2) |
| Ω_int | Z₂-intrinsic precision in normalised Bernoulli units | Z₂ rupture | 1 (by normalisation) |

In *geometric* units, the rupture condition is C·Ω_geo = 1 and gives
exp(C/Ω_geo) at the threshold equal to exp(1/Ω_geo²) = exp(φ_G²) —
not exp(1).

In *Z₂-intrinsic* units (where C is normalised to count Bernoulli
draws and Ω_int = 1 by construction), the rupture condition is
C·Ω_int = 1 and exp(C/Ω_int) = exp(1) = e at threshold.

The brief's statement "exp(C/Ω) → e at C·Ω = 1" is correct in
intrinsic units; the rupture interpretation as a geometric event is
correct in geometric units. The two are *different uses of Ω*, not
a single quantity.

**Convention adopted:** unless otherwise noted, Ω in CRR formulas
refers to **Ω_geo = 1/φ_G**. Where the intrinsic interpretation is
needed, use Ω_int explicitly.

### C4. Ω is *inverse* geodesic length.

Ω = 1/φ_G means: large Ω = short geodesic = high precision; small Ω
= long geodesic = low precision. This is consistent with the brief's
"Π = 1/Ω = precision" identification (Π scales with 1/φ_G; tighter
manifolds have higher precision).

**Implication for Bonnet-Myers (M16):** On a positively-curved
manifold with diameter D ≤ π/√κ, Ω = 1/D ≥ √κ/π. The saturating
case (round sphere) gives Ω = √κ/π, NOT Ω = π/√κ as the brief
states. The brief's M16 statement is an inversion typo; corrected.

### C5. Ω is rate-like under Kac.

By Kac's lemma, the expected return time to a coherent region A
under ergodic dynamics is 1/μ(A). Identifying this with the mean
inter-rupture interval 1/Ω gives Ω = μ(A_coherent).

**Convention:** Ω = μ(A) (rate interpretation), not Ω = 1/μ(A).
The brief's M19 wording is corrected.

---

## Resolution of flagged inconsistencies

| Issue | Resolution | Status |
|-------|-----------|--------|
| **exp(C/Ω) → e at C·Ω = 1** | C3: holds in Z₂-intrinsic units, not in geometric units. The brief conflates two Ωs. | **Resolved** |
| **M2: topological 2:1 ratio** | C2: ratio is half-turn embedding of Z₂ inside SO(2). Z₂ rupture geodesic π = SO(2) geodesic 2π / 2. | **Resolved** |
| **M5: CR ↔ HG relabelling** | Confirmed canonical. Tier capped at T1*. | **Closed** (no resolution needed) |
| **M6: "limit" framing** | Cosmetic — substitute "specialisation" for "limit" in canonical text; mathematics unchanged. | **Resolved** (textual) |
| **M8: 1-D state-variable assumption** | C2 generalises to any G; depth-2 minimum stands as the smallest nontrivial recurrence supporting non-Markovian closed orbits on a 1-D-state carrier. | **Clarified** |
| **M9: Fibonacci identification** | Independent of rupture-topology framework; remains open as Session 4 pre-registration target. | **Open** |
| **M10: CODATA 26 ppm discrepancy** | Independent of rupture topology; remains as in Session 2. | **Open** (T2 question) |
| **M11: ρ = −1/2 composition constraint** | C1+C2: two Z₂ ruptures composing on an SO(2) phase preserve total variance because both contribute Bernoulli(1/2) variance to the same SO(2) circuit. ρ = −1/2 follows from variance-preservation, which is now derived (not assumed). | **Resolved** |
| **M14: MaxEnt relabelling** | Confirmed canonical Boltzmann-Gibbs. Tier capped at T1*. | **Closed** |
| **M15: Z_n non-monotone with SO(2)** | C2: Z_n discrete-phase manifolds are *different objects* from SO(2) continuous-phase. They are not on a smooth continuum. The CV = n/(4π) formula is for Z_n discrete-phase under unit-of-fundamental-domain geodesic; SO(2) is the separate continuous case. | **Resolved** (separated, not interpolated) |
| **M16: Ω = π/√κ inversion** | C4: corrected to Ω ≥ √κ/π (saturating Ω = √κ/π on round sphere). Brief's wording is a typo. | **Resolved** |
| **M19: Ω = μ(A) vs 1/μ(A)** | C5: Ω = μ(A_coherent). Brief's wording corrected. | **Resolved** |
| **M21: TUR factor of 2** | TUR's factor of 2 is a property of the bound, not of the Z₂ rupture. Direct identification gives C·Ω = 2 at saturation, not C·Ω = 1. CRR cannot claim "TUR saturation" without rescaling. **Recommendation:** rephrase M21 as "TUR is structurally analogous to CR/HG (all three are Cauchy-Schwarz-type equality cases) but does not saturate at C·Ω = 1 under canonical identification." | **Open / requires author decision** |

---

## New convention: Lie-group memory manifolds (M22)

Under the resolved framework, the parameter-free CV prediction
generalises:

**M22 (new claim).** For a compact connected Lie group G acting as
the continual memory-bearing manifold with closed-geodesic length
φ_G in bi-invariant metric, the CRR canonical CV is

    CV_G = 1 / (2 · φ_G).

Predicted CV values:

| G | φ_G | CV_G | Notes |
|---|-----|------|-------|
| Z₂ | π | 1/(2π) | Pure rupture, no continuous phase |
| SO(2) | 2π | 1/(4π) | Canonical phase circle |
| SU(2) | 2π | 1/(4π) | Same CV as SO(2) (S³ vs S¹ — same geodesic length) |
| SO(3) | π | 1/(2π) | Same CV as Z₂-only (SO(3) = SU(2)/Z₂ has half the SU(2) geodesic) |
| T² | 2π | 1/(4π) | Per generator |
| SU(3) | 2π√3 | 1/(4π√3) | ≈ 0.0459 |

M22 is added to the claim set as a new T1-promotable claim. Its
derivation is in `claims/M22_lie_group_cv_generalisation/`.

---

## What the canonical brief should say (suggested edits)

1. **PART I — "ALL RUPTURES ARE Z₂"** is correct; reinforce it.
   Distinguish "Z₂ rupture" from "Z₂ phase" everywhere.

2. **The Ω regimes table** should specify *whose* Ω: Ω_geo of the
   phase manifold or Ω_int of the rupture. In current text, the
   regimes (rigid/refinement/balanced/creative/chaotic) presumably
   refer to Ω_int — the rupture's internal precision — but this
   is not stated.

3. **M2's statement** should read: "The Z₂ rupture is a half-turn
   embedding inside SO(2); Z₂ rupture-only geodesic π = SO(2)
   closed-geodesic 2π / 2." Not "Z₂ vs SO(2) substrates."

4. **M16's statement** should read: "Ω ≥ √κ/π on positively-curved
   manifolds (Bonnet-Myers diameter ≤ π/√κ; saturating round
   sphere)." Not "Ω = π/√κ."

5. **M21 (TUR)** needs explicit factor-of-2 rescaling or rewording.
   The simplest fix: state "C·Ω = 2 at TUR saturation under direct
   identification; the C·Ω = 1 form requires C ≡ Σ/2."

6. **The "exp → e" identification** should specify intrinsic units.
   Suggested: "In Z₂-intrinsic units (Ω_int = 1, C measured in
   Bernoulli draws), exp(C/Ω) = e at the rupture; in geometric units
   (Ω_geo = 1/φ_G), exp(C/Ω_geo) = exp(φ_G²) at the rupture, much
   larger than e for canonical phase manifolds."

These are *recommended* author-side edits, not modifications I will
make to the canonical text (per `CAMPAIGN.md` non-goals).
