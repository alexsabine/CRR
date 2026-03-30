# Coherence–Rupture–Regeneration (CRR)

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

## Axioms

1. **Čencov uniqueness.** The Fisher information metric is the unique (up to scale) Riemannian metric on statistical manifolds invariant under sufficient statistics. This fixes the geometry.

2. **Cramér–Rao attainment.** At rupture, the system saturates the Cramér–Rao bound: $C \cdot \Omega = 1$, where $\Omega = \sigma^2$ is the system's characteristic variance.

3. **Two universal symmetry classes.**
   - **Z₂** (bistable): $\Omega = 1/\pi$, threshold $C^* = \pi$, predicted $\text{CV} = 1/2\pi \approx 0.159$
   - **SO(2)** (rotational): $\Omega = 1/2\pi$, threshold $C^* = 2\pi$, predicted $\text{CV} = 1/4\pi \approx 0.080$
   - The ratio between symmetry classes is exactly **2**.

4. **σ = ½ at rupture.** The Dirac delta distributes unit mass at the rupture boundary → Bernoulli(½) → Wijsman attainment → $\sigma(C^*) = 1/2$ universally → $\text{CV} = \Omega/2$.

5. **Maximum entropy regeneration.** After rupture, the system reconstructs via Jaynes MaxEnt: $\exp(C/\Omega)$ weights which memories are accessible. Small Ω → rigid reconstitution. Large Ω → transformative renewal.

---

## Precision Architecture: Z₂ Sensory, SO(2) Prior

CRR assigns symmetry classes to the precision channels of Active Inference — and the assignment is not arbitrary. It falls out of graph topology.

In any network of Markov-blanketed agents, **edges** are statistical boundaries that alternate between two regimes of influence — Z₂ dynamics. **Nodes** are internal models that traverse a continuous cycle of belief updating — SO(2) dynamics. This maps directly:

- **Z₂ → sensory precision** (likelihood). Higher Ω = more permeable blanket. Fast, frequent, shallow updates. The system stays responsive to evidence.
- **SO(2) → prior precision** (transition model). Lower Ω = more stable internal model. Slow, rare, deep updates. The system maintains coherent beliefs.

The factor of 2 between Ω values (1/π vs 1/2π) is the geometric cost of revising priors versus updating sensory estimates. Sensory channels rupture ~2× as often as prior channels, but prior ruptures carry ~2× the precision gain. The totals balance exactly — a conservation law that holds across environment topologies, weight functions, and noise levels (precision-gain ratio = 1.003, 95% CI [1.000, 1.005]).

The primary finding is **phase-gating**: the π/2π partition produces a strongly non-uniform phase relationship between channels (χ² = 8,041) that determines whether each update drives learning or action. This is structurally compatible with empirical findings on neuromodulatory timing — Jang et al. (2026) showed that relative timing, not magnitude, determines whether dopamine promotes reinforcement learning or movement vigour. CRR recovers this partition from geometry alone.

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
