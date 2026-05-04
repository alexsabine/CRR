# Coherence–Rupture–Regeneration (CRR)

> **Campaign in progress** · Status-determination dashboard
>
> CRR is currently labelled "candidate framework, pre-peer-review." A
> structured campaign is under way to classify each distinct CRR claim
> on the spectrum T0 (speculation) → T4 (established principle), per
> domain.
>
> - Brief and discipline: [`CAMPAIGN.md`](CAMPAIGN.md)
> - Central artefact: [`notes/classification_table.md`](notes/classification_table.md)
> - Per-claim files: [`claims/`](claims/) (45 claims enumerated; B8, B9 added in Session 6)
> - Engine: [`crr-engine/index.py`](crr-engine/index.py) (61 pytest cases passing)
>
> **Session 4 + 4.5 outcomes:** 9 + 2 pre-registered novel predictions
> committed BEFORE analysis (git `3fc9681` and `102fedc`).
>
> Session 4 (sandbox-executed): M9 v1 FAIL, M10-α³ v1 FAIL. 7
> [REVIEWER-RUN] skeletons for data-blocked tests.
>
> Session 4.5 (v2 follow-ups, sandbox-executed):
> - **M9 v2 PASSES** all three coupling-sweep conditions
>   (monotone, weak-coupling band-limit, strong-coupling Cantor
>   regime). **M9 → T2.**
> - **M10-α³ v2 PASSES** all three Bethe-rescaled-residual
>   conditions (intra-system spread 3.6%, mean deviation 21.6%
>   from leading α³ × (8/3π) target).
>   **M10-α³ → T3 — first T3 promotion in the campaign.**
> See [`notes/session_log.md`](notes/session_log.md) Session 4
> entry for the full result table.
>
> **Tier counts (after Session 6):**
> - **M (22):** 18×T1 + 2×T1\* (M5/M14) + 1×T2 (M9) + **1×T3 (M10-α³)** — v3 Li²⁺ extension PRELIMINARY PASS
> - **P (7):** 3×T2 (P1, P6, P7) + 3×T2\* marginal/preliminary/conditional + 1×T1 (P3)
> - **B (9):** 1×T2 (B7) + **1×T3 (B8)** + 7×T1 (incl. B9) — first biological T3
> - **Ph (7):** 5×T2-eq (Ph1, Ph2, Ph4, Ph5, Ph7) + 2×T1 (Ph3, Ph6)
>
> **Session 6 outcomes (3 pre-registrations committed at `4562fe1`):**
> - **B8** (bacterial generation-time CV): pre-reg PASS — first biological T3.
> - **M10-α³ v3** (Li²⁺ Lamb shift extension): PRELIMINARY PASS, sandbox-limited; strengthens existing T3 cluster.
> - **B9** (resting respiratory CV → SO(2)): honest FAIL of literal pre-reg; data sit in Z₂ band rather than SO(2); B9 stays at T1.
>
> **Session 5 (philosophy):** every Ph claim assessed under three
> interpretation modes — **Metaphorical / Structural / Exact** —
> per [`notes/philosophical_assessment_framework.md`](notes/philosophical_assessment_framework.md).
> 5 of 7 reach T2-equivalent (structural reconstruction); 2 stay
> at T1; none reach T3-eq (no confirmed novel phenomenological
> prediction yet) or T4-eq (no independent philosopher engagement).
> **T0 count is now zero** across the entire 43-claim set.
>
> **Session 3 T2 promotions (7 in total):** P1 Solar Hale (SILSO),
> P2 GWTC BBH (LIGO/Virgo, marginal), P4 dark energy w-crossing
> (DESI 2024, preliminary), P5 CSEP California (conditional),
> P6 Ω = k_B T / κ_eff (equipartition), P7 CLT regularisation,
> B7 significance-weighted memory.
>
> See [`notes/classification_table.md`](notes/classification_table.md)
> for the central artefact and
> [`crr-engine/consistency/`](crr-engine/consistency/) for the
> end-to-end reproduction scripts (most marked [REVIEWER-RUN] —
> sandbox blocks SIDC/gwosc/PhysioNet/CSEP hosts).

---

**A parameter-free temporal process theory grounded in information geometry.**

Three equations describe how bounded systems accumulate coherence, rupture at geometrically determined thresholds, and regenerate from weighted memory.

---

## The Equations

**Coherence** — the past accumulates:

$$C(x,t) = \int_0^t L(x,\tau)\, d\tau$$

**Rupture** — the present is instantaneous:

$$\delta(now) \quad \text{when} \quad C \cdot \Omega = 1$$

**Regeneration** — the future is built from weighted memory:

$$R = \int \varphi(x,\tau) \cdot \exp\!\left(\frac{C(x,\tau)}{\Omega}\right) \cdot \Theta(t-\tau)\, d\tau$$

---

## Five Commitments

Any persistent, finite, adaptive system must satisfy these:

**1. Persistence implies accumulation.** A system that persists must accumulate patterns that work, reducing surprise in its eco-niche. $L(x,\tau) \geq 0$ is the Fisher–Rao speed on the statistical manifold — the rate of coherence accumulation. The integral over the system's past makes CRR distinctively non-Markovian: the present state depends on the accumulated history of the current regime.

**2. Finite capacity implies rupture.** No finite system can accumulate coherence without bound. At $C \cdot \Omega = 1$, accumulated arc length spans the manifold's full geodesic extent. The system has traversed all distinguishable states available to its current regime and must reorganise. The Dirac delta has zero temporal extension and carries exactly one unit of mass on the boundary between past and future.

**3. Reconstruction is weighted by historical coherence.** After rupture, the system rebuilds from its own history. The exponential kernel $\exp(C/\Omega)$ is the maximum-entropy weighting consistent with a constraint on the expected value of $C$ — given only accumulated coherence and capacity, the distribution that maximises entropy takes the Boltzmann form, with $C$ as energy and $\Omega$ as temperature. The Heaviside $\Theta$ enforces causality. Because $d\Theta/dt = \delta$, the three CRR equations form a single dynamical system: the regeneration integral is the Green's function of the rupture operator.

**4. The system has a characteristic variance.** $\Omega$ is fixed by the topology of the state space, not fitted. It simultaneously governs coherence capacity (how much can accumulate before rupture), rupture frequency (how often the system must reorganise), and memory breadth (which past moments dominate reconstruction). These are not three independent properties but a single geometric fact about the system's attractor topology. Small $\Omega$: the memory kernel peaks sharply and the system reconstitutes the same patterns (habit, rigidity). Large $\Omega$: the kernel is flat and the system can reconstruct broadly (flexibility, exploration).

**5. Rupture is a maximum-entropy event.** At rupture, the system occupies the maximum-entropy state consistent with its symmetry class. A bistable system at rupture is maximally uncertain about which state comes next; a rotational system at rupture has no preferred phase. This converts geometric structure into specific numerical predictions.

---

## Fixing Ω from Geometry

The five commitments leave one degree of freedom — the value of Ω — which must be fixed by the system's structure alone. For systems whose internal states parametrise probability distributions (which, under the FEP, includes any system with a Markov blanket), the arena of coherence accumulation is a statistical manifold. Čencov's uniqueness theorem constrains the metric to the Fisher information metric, and the geodesic structure fixes the maximum arc length.

Two fundamental manifold topologies:

- **Z₂ (bistable).** The Bernoulli manifold, parametrised by $p \in [0,1]$, has Fisher–Rao geodesic diameter $\pi$. The manifold is an interval, not a loop — the system cannot return without retracing the same geodesic. $\ell_{Z_2} = \pi$, hence $\Omega_{Z_2} = 1/\pi \approx 0.318$ and $C^* = \pi$. Predicted CV $= 1/2\pi \approx 0.159$.

- **SO(2) (rotational).** The circular manifold $S^1$ has circumference $2\pi$. The system exhausts its configuration by completing one full cycle. $\ell_{SO(2)} = 2\pi$, hence $\Omega_{SO(2)} = 1/2\pi \approx 0.159$ and $C^* = 2\pi$. Predicted CV $= 1/4\pi \approx 0.080$.

The ratio between classes is exactly **2** — a topological invariant independent of any physical parameters.

---

## Precision Architecture: Z₂ Sensory, SO(2) Prior

The symmetry assignment to Active Inference's precision channels was not imposed by analogy — it was found in the graph topology of a network simulation.

In any graph of Markov-blanketed agents, an **edge** is a statistical boundary that alternates between two regimes of influence: inside-dominant or outside-dominant. Two states, one boundary — Z₂ dynamics. A **node** is an internal model that traverses a continuous cycle of belief updating: perceive, predict, act, update. A closed loop with no endpoint — SO(2) dynamics.

The assignment follows:

- **Z₂ → sensory (likelihood) precision.** Edges are blanket states. $\Omega_{Z_2} = 1/\pi$ — higher variance, more permeable boundary. The system stays responsive to incoming evidence. Fast ruptures, frequent updates, shallow precision gain per event.

- **SO(2) → prior (transition) precision.** Nodes are generative models. $\Omega_{SO(2)} = 1/2\pi$ — lower variance, more stable internal model. The system maintains coherent beliefs across time. Slow ruptures, rare updates, deep precision gain per event.

Three independent lines of evidence converge on this assignment:

1. **Graph structure.** Edges alternate (Z₂); nodes cycle (SO(2)). The symmetry classes are inherited from the roles the channels play in the network.

2. **Permeability.** The regeneration kernel $\exp(C/\Omega)$ entails that higher Ω produces a flatter memory kernel (broad, flexible, permeable). Under the FEP, the Markov blanket must be receptive to sensory states; the internal model must maintain stability. Since $\Omega_{Z_2} > \Omega_{SO(2)}$, graph-structural and functional arguments converge.

3. **Falsifiability.** Reversing the assignment (SO(2) → sensory, Z₂ → prior) produces measurably different dynamics: sensory ruptures become rare (modal 1 per prior cycle, versus 3), and the prior channel becomes irregular ($B = -0.16$ vs $-0.33$). The reversed assignment predicts that sensory updates are rarer than prior updates — contradicting the FEP's requirement that the blanket be responsive to evidence.

The primary empirical finding is **phase-gating**: the π/2π partition produces a strongly non-uniform phase relationship between channels ($\chi^2 = 8{,}041$, $p < 10^{-100}$) that determines whether each update drives learning or action. Both channels process equal total precision gain per unit time (ratio = 1.003, 95% CI [1.000, 1.005]) — a conservation law that holds across environment topologies, weight functions, and noise levels. The Z₂ channel makes many small updates; the SO(2) channel makes few large ones. The factor of 2 sets the exchange rate between frequency and grain size.

This is structurally compatible with Jang et al. (2026), who showed that relative timing, not magnitude, determines whether dopamine promotes reinforcement learning or movement vigour. CRR recovers the partition from geometry alone.

---

## Empirical Status

Validated across **132 systems in 20+ domains** at ~10.6σ significance with zero directional reversals. Systems span neural oscillations, cardiac rhythms, bacterial division, stellar pulsation, flame plasma, tree rings, sleep spindles, laser dynamics, population ecology, and more.

- [Empirical paper (132 systems)](https://www.cohere.org.uk/132.pdf)
- [AGI Conference paper (phase-gating)](https://www.cohere.org.uk/AGI_Conference_2026.pdf)

---

## Links

### Framework & Tools

- [LLM Starter Guide](https://www.cohere.org.uk/132_LLM_Starter.MD) — compact introduction for language models
- [LLM Exploration Prompt](https://www.cohere.org.uk/LLM_PROMPT_EXPLORE.MD) — structured prompt for testing CRR

### Interactive Demonstrations

- [**The Depth Illusion**](https://www.cohere.org.uk/CRR_Human-AI_Dynamics.html) — An Active Inference network where SO(2) human agents are coupled through Z₂ Markov blankets, with optional Z₂ LLM substrates attached to any node. Scale from 1 agent (a self) to 150 (Dunbar's number). Watch how LLMs drag SO(2) agents toward Z₂ frequency — faster, shallower cycles — and track the cumulative "depth illusion" as agents misattribute LLM-driven updates to their own generative models.

- [**CRR Network**](https://www.cohere.org.uk/human_networks.html) — The pedagogical simulation from which the phase-gating finding emerged. A complete graph K_n where nodes run SO(2) cycles and edges run Z₂ switches. The two temporal characters are visible before any measurement: nodes glow slowly toward deep belief updates while edges flicker rapidly between regimes. Autonomy, integration (Φ), and the beauty function are tracked in real time.

- [**CRR Tree**](https://www.cohere.org.uk/crr_tree_branch.html) — A tree grown entirely from CRR first principles. Every branch point is a rupture; every growth segment is coherence accumulation. An emergent property: the tree remembers where you looked first, because coherence only accumulates on-screen (your gaze = L(x,τ)) and rupture is irreversible. Wherever you attend becomes the region of deepest growth — attention constraining morphogenesis, live.

- [**Song of Time (Clocks)**](https://www.cohere.org.uk/song_of_time(clocks).html) — A clock shop at midnight. A real quartz crystal (your sound card's 48kHz oscillator) keeps the time. Eight Kuramoto-coupled pendulum clocks solved at sample rate. CRR derives the coupling constants from frequency ratios: octave (2:1) → K = 1/3, fifth (3:2) → K = 1/5. Synchronisation emerges. Nobody forces it.

### Aesthetic (CRR Songs)

- [**Song of the Wave**](https://www.cohere.org.uk/CRR_Waves.html) — Ocean physics: Fresnel reflectance, Beer–Lambert absorption, and Stokes drift, driven by CRR coherence cycles. Ω controls the glass-to-storm continuum.
- [**Song of the Bowl**](https://www.cohere.org.uk/CRR_Singing_Bowl.html) — A Tibetan singing bowl. Strike the water (rupture) or drag the rim (sustained coherence). Time-lens slows the physics to reveal wavefront propagation.
- [**Soma**](https://www.cohere.org.uk/soma_enhanced.html) — The body as CRR system.
- [**Song of Creation**](https://www.cohere.org.uk/songofcreation.html) — Cosmological structure formation driven by CRR dynamics.
- [**Aviana**](https://www.cohere.org.uk/aviana.html) — Birdsong and flock dynamics.
- [**Song of the Cosmos**](https://www.cohere.org.uk/song_of_the_cosmos.html) — Stellar evolution, galactic rotation, and the CMB rendered as sound and light.

---

## Process Philosophy

CRR formalises Whitehead's temporal ontology: reality is not made of things that change but of changes that occasionally cohere into things. **C** is the past accumulated as constraint. **δ** is the dimensionless present. **R** is the future weighted by what mattered.

---

## Contact

**Alexander Sabine** — [cohere.org.uk](https://www.cohere.org.uk) · [temporalgrammar.ai](https://temporalgrammar.ai)

```bibtex
@misc{sabine2025crr,
  author = {Sabine, Alexander},
  title = {Coherence–Rupture–Regeneration: A Parameter-Free Temporal 
           Process Theory},
  year = {2025},
  url = {https://www.cohere.org.uk}
}
```
