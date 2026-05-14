# Lie-group CV predictions beyond M22

## The framing

M22 (`claims/M22_lie_group_cv_generalisation/`) states:

> For a compact connected Lie group G acting as the continual
> memory-bearing manifold under Z₂ rupture, with bi-invariant
> Riemannian metric and closed-geodesic length φ_G,
>
>     CV_G = 1 / (2 · φ_G).

M22 already enumerates Z₂, U(1)≅SO(2), SU(2), SO(3), T², SU(3).
This package adds the next-most-natural compact Lie groups, each
with a candidate empirical system and a data source for testing.

## Geodesic lengths in canonical normalisation

| G | dim | φ_G (bi-invariant) | Ω_G = 1/φ_G | CV_G = 1/(2·φ_G) |
|---|----|---|---|---|
| Z₂ (rupture only)            | 0 | π | 1/π          | 0.1592 |
| U(1) ≅ SO(2)                 | 1 | 2π | 1/(2π)       | 0.0796 |
| SU(2) ≅ S³                   | 3 | 2π | 1/(2π)       | 0.0796 |
| SO(3) = SU(2)/Z₂             | 3 | π | 1/π          | 0.1592 |
| T² (per generator)           | 2 | 2π | 1/(2π)       | 0.0796 |
| **SO(4) ≅ (SU(2)×SU(2))/Z₂** | 6 | π | 1/π          | 0.1592 |
| **U(2) ≅ (SU(2)×U(1))/Z₂**   | 4 | 2π | 1/(2π)       | 0.0796 |
| **SU(3)**                    | 8 | 2π·√3 | 1/(2π√3)  | 0.0459 |
| **SU(4)**                    | 15 | 4π | 1/(4π)      | 0.0398 |
| **Sp(2) ≅ Spin(5)**          | 10 | 4π | 1/(4π)      | 0.0398 |
| **G₂ (exceptional)**         | 14 | 2π·√3·(2/3) | — | 0.0689 |
| **Spin(7)**                  | 21 | 2π·√3 | —         | 0.0459 |
| T³ (per generator)           | 3 | 2π | 1/(2π)       | 0.0796 |
| T⁴ (per generator)           | 4 | 2π | 1/(2π)       | 0.0796 |

Notes on normalisation:

- φ_G is the smallest closed geodesic through the identity in the
  bi-invariant metric defined by minus the Killing form, scaled so
  that the SU(2) generators σ_i/2 satisfy [σ_i/2, σ_j/2] = ε_{ijk}
  σ_k/2 (the standard physics convention).
- The values for G₂ are derived from the dual Coxeter number h^∨=4
  and rank 2; the bi-invariant geodesic minimum on G₂ is
  4π/√6 ≈ 5.13, giving CV ≈ 0.0974 in one normalisation, but the
  Killing-form-normalised value used here is 4π/3 (giving 0.119).
  The G₂ entry in the CSV records the Killing-form value with a
  caveat note.
- Sp(2) ≅ Spin(5) — confusingly numbered: Sp(2) is the rank-2
  symplectic group (10-dimensional), not Sp(1)=SU(2).

## Topological CV-equivalences

A direct consequence of M22 is that *only* φ_G matters, not the
group's dimension or rank. This produces several falsifiable
equivalences:

| Equivalence | φ_G shared | Predicted CV |
|---|---|---|
| Z₂ ≡ SO(3) ≡ SO(4) | π | 0.1592 |
| SO(2) ≡ U(1) ≡ SU(2) ≡ U(2) ≡ T^n (per gen.) | 2π | 0.0796 |
| SU(3) ≡ Spin(7) | 2π√3 | 0.0459 |
| SU(4) ≡ Sp(2) | 4π | 0.0398 |

The strongest falsifier is therefore: **find any system where
two of these listed groups predict different observed CVs**.
Under M22 they cannot.

## Candidate empirical systems per group

| Symmetry | Candidate system(s) | Source(s) |
|---|---|---|
| SU(2) | NV-centre electron-spin Rabi cycle CV; spin-1/2 NMR T₂ jitter | Doherty 2013 *Phys Rep* 528:1; Levitt 2008 *Spin Dynamics* |
| SO(3) | Rigid-body precession period CV (gyroscope drift); Euler-angle return time | IERS LOD jitter; Goldstein *Classical Mechanics* §5 |
| SO(4) | Hydrogen orbital degeneracy lifetime CV; isotropic 3-D rigid rotor with extra Runge-Lenz constant | Pauli 1926 hydrogen treatment; Dickson 1989 |
| U(2) | Single-qubit + global-phase coherence cycle (transmon + cavity) | Krantz 2019 *Appl Phys Rev* 6:021318 |
| SU(3) | Charmonium ψ-family lifetime CV (already T1 in M22 v2); ³He superfluid texture cycle | PDG; Vollhardt 1990 *The Superfluid Phases of Helium 3* |
| SU(4) | 4-level atomic clock transition CV; tetraquark resonance lifetimes | Marciniak 2022 *Nature* 603:69 |
| Sp(2) | Pentaquark Pc(4380)/Pc(4450) lifetime CV (5-dim spin); 5-level atomic | LHCb 2015 *Phys Rev Lett* 115:072001 |
| G₂ | 7-d colour-confinement timescale; G₂ holonomy compactification (very speculative) | Greiner & Schäfer 1994 *QCD* |
| Spin(7) | Octonionic quasicrystal cycle CV; 7-d holonomy | Joyce 1996 *Inv Math* 123:507 |
| T² | Cardio-respiratory bicommensurate clock CV per generator; spin-orbit double pendulum | Schäfer 1998 *Nature* 392:239 |
| T³ | Cardiac × respiratory × circadian coupled clock | Glass 2001 *Nature* 410:277 |
| T⁴ | Add ultradian to T³ stack | Refinetti 2016 *Circadian Physiology* |

The CSV file `data/cv_predictions_lie_groups.csv` formalises 14 of
these as pre-registered predictions with `verdict = PENDING`.

## What this set of predictions is *for*

1. **Sharp falsifier set.** Each pair of CV-equivalent groups (Z₂≡
   SO(3), SO(2)≡SU(2), etc.) is a structural prediction independent
   of any group's dimension or rank. A single counterexample
   refutes M22.
2. **Candidate fertile-ground experiments.** Spin-1/2 NMR T₂ jitter
   is the most tractable single-experiment test of SU(2) ≡ SO(2)
   CV-equivalence; charmonium lifetimes (already partially tested
   in M22 v2) are the simplest SU(3) test.
3. **Diagnostic taxonomy across substrates.** The Class A/B/C
   diagnostic from the paper extends naturally: a Z₂-on-G system
   suppressed below 1/(2·φ_G) is regulated; elevated is noise-
   dominated. This generalises Section 4 of the paper to any G.
