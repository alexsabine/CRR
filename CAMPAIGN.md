# CRR Status Determination Campaign

**Project lead:** Alexander Sabine — Active Inference Institute
**Branch:** `claude/crr-status-determination-odv4z`
**Mandate:** inductive, diagnostic, evidence-based status determination
of the Coherence-Rupture-Regeneration framework.

This campaign does NOT produce a unified verdict. It produces a
calibrated, per-claim classification across two axes:
- **Epistemic tier** T0–T4 (speculation → established principle).
- **Domain** M / Ph / Ps / B / T / P.

Each tier is earned only by corresponding evidence in the repository:
T1 needs a derivation file, T2 needs an empirical-consistency
reproduction, T3 needs a pre-registered prediction confirmed on
untouched data, T4 needs independent replication by an unaffiliated
group.

---

## PART I — The canonical CRR formulation

CRR is a TEMPORAL GRAMMAR: structural rules through which temporal
processes articulate themselves, not a model of any specific domain.
It formalises Whitehead (actual occasions, concrescence) and Bergson
(durée, memory) as mathematics. Reality is made of changes that
occasionally cohere into things, not things that change.

### The three equations

1. **Coherence:** C(x,t) = ∫₀ᵗ L(x,τ) dτ — accumulated Fisher-Rao
   arc length. The PAST.
2. **Rupture:** δ(now) when C·Ω = 1 — scale-invariant Dirac delta
   marking the ontological present. ALL RUPTURES ARE Z₂. The NOW.
3. **Regeneration:** R[χ](x,t) = ∫₋∞ᵗ φ(x,τ)·exp(C(x,τ)/Ω)·Θ(t−τ) dτ
   — causal exponential-kernel reconstruction. Exponential family
   with natural parameter η = 1/Ω, sufficient statistic C. The FUTURE.

### The key parameter Ω (revised per `notes/rupture_topology.md`, `notes/conventions.md`)

**Rupture is Z₂ by construction (H1), not a substrate choice.** Three
independent arguments force this: the Dirac delta's codomain {0,∞}
under unit normalisation is {0,1}; the Heaviside rupture-indicator
Θ(C·Ω−1) has codomain exactly {0,1}; and at saturation the sufficient
statistic is a Bernoulli(1/2) draw. "Z₂" in CRR names the rupture
event itself, never a phase manifold alongside SO(2) as a rival
alternative.

**The continual memory-bearing manifold is a compact connected Lie
group G** (H2), with bi-invariant metric and closed-geodesic length
φ_G. The canonical Z₂ rupture acts on G via the antipodal quotient
θ ~ θ+φ_G/2 — a genuine index-2 subgroup, so the rupture-only geodesic
is *always* exactly half of G's closed geodesic, for any G and in any
consistent normalisation of φ_G:

Ω_G = 1/φ_G · CV_G = Ω_G/2 = 1/(2·φ_G) (M22 generalisation)

| G | φ_G | Ω_G | CV_G |
|---|-----|-----|------|
| Z₂ (rupture only, no continuous phase) | π | 1/π ≈ 0.3183 | 1/(2π) ≈ 0.1592 |
| SO(2) ≅ U(1) | 2π | 1/(2π) ≈ 0.1592 | 1/(4π) ≈ 0.0796 |
| SU(2) ≅ S³ | 2π | 1/(2π) | 1/(4π) — same CV as SO(2) |
| SO(3) = SU(2)/Z₂ | π | 1/π | 1/(2π) — same CV as Z₂-only |

Topological ratio Z₂:SO(2) = 2 is **forced** — it is the group-index
fact that an index-2 subgroup has exactly half the parent's geodesic
length, true in any units. This is the strong, scale-independent part
of the claim. The **absolute** values (0.1592, 0.0796) additionally
require the bi-invariant-metric normalisation of φ_G to coincide with
the Čencov/Fisher-Rao normalisation independently derived for the Z₂
(Bernoulli) case — that coincidence is a stated convention (C2), not a
theorem; see the open M21 item below for a case where an analogous
cross-formalism identification does *not* hold without rescaling.

**Two distinct Ωs (C3) — do not conflate.** Ω_geo = 1/φ_G (the
geometric quantity above) and Ω_int = 1 (Z₂-intrinsic, rupture
measured in its own Bernoulli-draw units) are different quantities.
"exp(C/Ω) → e at C·Ω = 1" holds only in Z₂-intrinsic units; in
geometric units, C·Ω_geo = 1 at rupture forces C/Ω_geo = φ_G², so
exp(C/Ω_geo) = e^{φ_G²} (≈ e^{π²} ≈ 19334 for Z₂, ≈ e^{4π²} for SO(2)),
not e. Any statement invoking "exp(C/Ω) → e" must specify which Ω.

Ω regimes: <0.5 rigid; 0.5–1.2 refinement; 1.2–2.5 balanced; 2.5–4.0
creative; >4.0 chaotic. (These regimes are stated in Ω_int units per
`notes/conventions.md`; not yet re-derived per-G in Ω_geo units.)

### Universal rupture condition

C·Ω = 1 (geometric units) — the equality case of the Cramér-Rao bound
under the identification of C with accumulated Fisher information.
The kinship with Heisenberg-Gabor saturation holds only as an
algebraic form (same dimensionless product structure), not a literal
identification of C, Ω with the conjugate physical variables — see
`Alexander/boundary_is_a_rate` §4. The kinship with the thermodynamic
uncertainty relation (TUR) does **not** hold at C·Ω = 1 under direct
identification — the TUR's own factor of 2 forces C·Ω = 2 at TUR
saturation instead (M21, open; `notes/conventions.md`). CRR should not
claim three-way saturation (CR + HG + TUR) at the same C·Ω = 1 without
either rescaling one identification or restricting the claim to CR
alone.

### Beauty function

B(C) = exp(C/Ω)·(C* − C). Peaks at C* − Ω.

### Predictions

CV = Ω/2 (parameter-free). Z₂ + Z₂ → SO(2) gives ρ = −1/2.

### Three-class diagnostics

- Class A (autonomous): CV ≈ Ω/2.
- Class B (regulated): CV < Ω/2.
- Class C (noise-dominated): CV > Ω/2.
- Falsifier: directional reversal.

### Existing empirical claims

Fine-structure 1/α = 137.032; Solar Hale CV 0.0767–0.0820 vs SO(2)
0.0796; dark-energy peak ρ_DE / w=−1 crossing at z ≈ 0.5; GWTC-1/2/3
radiated-fraction CV = 0.099, CI [0.077, 0.114]; AGI-26 phase-gating
χ²=8041, conservation 1.003, ρ=−1/2; CSEP California single-Ω matches
ETAS, nested CRR underperforms.

### CRR-FEP correspondence

| Free Energy Principle | CRR |
|-----------------------|-----|
| Free energy F | Coherence C (inverse) |
| Precision Π | (1/Ω)·exp(C/Ω) |
| Markov blanket | high-∇C surface |
| Generative model | R[χ] reconstruction |

FEP says WHAT updates; CRR says WHEN/HOW through time.

---

## PART II — Status-determination framework

### Axis 1 — Epistemic tier

| Tier | Name | Requires |
|------|------|----------|
| T0 | Speculation | Nothing |
| T1 | Conjecture | Derivation, machine-checkable or step-verified |
| T2 | Framework | T1 + reproduction of an independent empirical regularity |
| T3 | Theory | T2 + pre-registered novel prediction confirmed on untouched data |
| T4 | Established | T3 + independent confirmation by an unaffiliated group |

### Axis 2 — Domain

M (mathematical) · Ph (philosophical/phenomenological) · Ps
(psychological) · B (biological) · T (temporal/dynamical) · P (physical).

### Discipline

- Promotions only with committed evidence.
- Downgrades recorded with the same care as promotions.
- Pre-registration: `prediction.md` committed before `fetch.py` /
  `analyse.py` exists. The git log is the audit trail.
- Philosophical claims cannot reach T3 by the empirical pathway; an
  alternative pathway is described in PART III.
- Rhetorical framing is not a claim. Relabellings of canonical results
  reach T1 only.
- Sympathy with the framework is not evidence.

---

## PART III — Repository structure

```
crr-engine/
  index.py                  Canonical engine factored from CRR_Church_eff.html
  tests/                    pytest coverage of basic operations
claims/
  M1_cv_omega_over_two/
    claim.md                Canonical statement
    tier.md                 Current tier with justification
    derivation.md           T1+ evidence (added in Session 2)
    consistency.md          T2+ evidence (Session 3)
    prediction.md           T3+ evidence (Session 4)
    result.md               T3+ outcome
    independent.md          T4 evidence (Session 6)
  ...                       (42 claim subdirectories total)
notes/
  classification_table.md   The central artefact — full table
  decomposition.md          Full enumeration of CRR claims
  relabellings.md           CRR statements that restate canonical results
  domain_summary.md         Status by domain (Session 7)
  overall_status.md         Synthesis (Session 7)
CAMPAIGN.md                 This brief
README.md                   Top-level dashboard
```

### Session plan

1. **Session 1 — Decomposition + engine** (this session). Enumerate
   claims, build claim subdirectories, factor the canonical engine
   into `crr-engine/`, initialise the classification table.
2. **Session 2 — M-claims T0 → T1.** Derivations for M1–M21.
3. **Session 3 — Empirical consistency T1 → T2.** Reproduce
   regularities from public data (SILSO, GWTC, NIST, CSEP, AGI-26,
   PhysioNet).
4. **Session 4 — Pre-registered novel predictions T2 → T3.** Mount
   Wilson + Kepler stellar cycles, HRV cohorts, repeating earthquakes,
   Pantheon+/BOSS/Planck, Allen Brain Observatory, irrationality
   measure, quasi-crystal spectra.
5. **Session 5 — Philosophical assessment.** Apply the
   philosophical-claim pathway to Ph1–Ph7.
6. **Session 6 — Independent-confirmation audit.** Search Google
   Scholar / PubMed / INSPIRE-HEP / arXiv for replication. Distinguish
   sympathetic engagement from independent confirmation.
7. **Session 7 — Synthesis.** Final classification table, domain
   summary, overall status.

### Output requirements

- Every tier assignment links to the file(s) that justify it.
- Commit messages name promotions/downgrades:
  `promote: M1 → T2 (consistency.md added, SILSO reproduction)`.
- Session logs record promotions, downgrades, surprises, queued work.

### Non-goals

- No unified verdict.
- No weighting of rhetorical resonance against evidence.
- No refusal to promote a claim that meets its tier criteria; no
  promotion of a claim that does not.
- No modification of the canonical formulation in response to a
  downgrade. The campaign records evidence; the framework's author
  decides what to revise.
- No compression of the campaign into one session.
