# M8 — Derivation: Depth two is the minimum supporting KAM-stable ergodicity

## Claim

The minimum memory depth at which a deterministic recurrence on a
compact phase space supports KAM-stable quasi-periodic motion (and
hence non-trivial ergodic behaviour distinct from periodic and
strictly Markov dynamics) is depth two.

## Assumptions

(A1) "Memory depth k" means the next state x_{n+1} depends on the
last k states (x_n, x_{n−1}, ..., x_{n−k+1}).
(A2) The phase space is a compact 2-torus (or higher torus); the
KAM theorem applies in its classical form.
(A3) "KAM-stable" means a positive-measure set of initial conditions
yields invariant tori under small perturbations of the dynamics.

## Derivation (under A1–A3)

**Depth 0 (memoryless).** x_{n+1} = f(noise_n). No deterministic
phase structure; not KAM-applicable.

**Depth 1 (Markov).** x_{n+1} = f(x_n) on a compact manifold. The
phase space of the dynamical system is one-dimensional in the
recurrence variable. KAM requires a Hamiltonian structure with at
least 2 degrees of freedom (so that the unperturbed motion lives on
2-tori); a depth-1 deterministic map on a 1-D manifold has no
KAM structure. The dynamics are either periodic (fixed points,
cycles) or chaotic (sensitive dependence) — no quasi-periodic
KAM-stable regime.

**Depth 2.** x_{n+1} = f(x_n, x_{n−1}). Embed in (x_n, x_{n−1})
∈ M × M, a 2-dimensional state space. The recurrence is now a map
on a 2-manifold — sufficient to support invariant 1-tori (closed
curves) under quasi-periodic dynamics. KAM applies: for
near-integrable f, a positive-measure Cantor set of irrational
rotation numbers gives invariant tori (Moser's twist-map theorem).

Hence depth 2 is the *minimum* depth at which KAM-stable
quasi-periodic motion is dynamically possible. Depth ≥ 3 also
supports KAM but is not minimal.

**Connection to M7 (φ-eigenvalue).** Among irrational rotation
numbers preserved by KAM, the *most-irrational* (in the sense of
Hurwitz's irrationality measure) is the golden ratio φ. So depth-2
recurrences with φ-related coefficients are the most robust under
perturbation — supporting the canonical CRR choice of φ at minimal
depth.

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M8_depth_two_torus_dim`
constructs the embedding (x_n, x_{n−1}) ↦ (x_{n+1}, x_n) explicitly
for a depth-2 linear recurrence and verifies it lies on a 1-torus
(closed curve in 2-D phase space) for irrational rotation rates,
versus open trajectories for depth-1 cases.

## Caveats

- **The classical KAM theorem requires Hamiltonian structure.** The
  derivation here uses the *twist-map* version (Moser), which is
  the appropriate generalisation for area-preserving 2-D maps. The
  canonical CRR brief speaks of "KAM-stable ergodicity," which is a
  slight conflation: KAM gives non-ergodic invariant tori on a
  positive-measure set; *between* tori the dynamics may be ergodic
  or chaotic. The claim is best read as "minimum depth at which the
  system is generically *neither* periodic nor chaotic," not "ergodic
  in the strict measure-theoretic sense."
- **Depth-1 caveat.** A depth-1 map on a *higher-dimensional*
  manifold (e.g., the standard map on a 2-torus) does support KAM
  tori. So the strict statement is "depth-2 minimum *given the
  recurrence is one-dimensional in the state variable*." Recorded.
- **Reference:** Moser, *On invariant curves of area-preserving
  mappings of an annulus*, 1962.

## Status

**T1 with caveat.** The minimal-depth claim holds under the
implicit assumption that the state variable is 1-dimensional;
otherwise depth 1 suffices on higher-dimensional carriers. Tier
capped at T1 pending tightening of the canonical statement.
