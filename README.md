# Coherence–Rupture–Regeneration (CRR)

> *"Eternity is in love with the productions of time."*
> — William Blake, *The Marriage of Heaven and Hell*

---

**A mathematical grammar of finite becoming, grounded in information geometry.**

Three equations describe how bounded systems accumulate coherence, rupture at thresholds, and regenerate from their own history. This repository is the experiential side of CRR: an early years educator's playground of simulations, songs and pictures for *feeling* the mathematics of change. The equations have since been put through preregistered, adversarial testing; what survived, and what did not, is summarised below.

---

## The Equations

**Coherence**: the past accumulates, since the last cut:

$$C(t) = \frac{1}{\sigma}\int_{t_n}^{t} L(\tau)\, d\tau, \qquad L(\tau) = \sqrt{g(\theta_\tau)}\,\lvert\dot\theta_\tau\rvert$$

**Rupture**: the present is instantaneous; it comes at the first arrival at the opposite state:

$$\delta(t - t_{n+1}), \qquad t_{n+1} = \inf\{\, t > t_n : C^*\,\Omega = 1 \,\}$$

**Regeneration**: the future is built from weighted memory, each occasion weighted by recency × salience:

$$m_{n+1} = \frac{\sum_{j=-1}^{n} w_j\,\Phi_j}{\sum_{j=-1}^{n} w_j}, \qquad w_j = q^{\,n-j}\cdot e^{S_j\,\Omega}$$

$\theta$ is the system's state on a circle of probability distributions, $g$ is the Fisher information (how distinguishable neighbouring states are), and $L$ is the Fisher–Rao speed. $\sigma$ is a resolution, calibrated separately: the smallest change the system can tell apart. So $C$ is accumulated arc length since the last rupture $t_n$, in units of $\sigma$: every step taken, including steps back. $C^*$ is the geodesic distance from where the occasion began, and $\Omega = 1/(\text{the manifold's diameter})$ in the same units, so the cut comes the first time the system reaches the state opposite to where it began. Any wandering on the way is surplus, $S = C - C^* \ge 0$.

Regeneration rebuilds from what the system has inherited: what each completed occasion settled ($\Phi_j$), and the wider past it stands on ($\Phi_{-1} = m_0$, from before the system began). Only completed occasions count. Memory is weighted by **recency** ($q$ near 0 rebuilds from the latest occasion; $q$ near 1 draws on the long past) and by **salience**, $e^{S\Omega}$: surplus counted in half-turns, so occasions that took more turning back weigh more, whatever the resolution $\sigma$. Every occasion ends at the same chord, so only the surplus differs between them. Salience is a proposal still to be tested. For a single-number $\Phi$ the update is a weighted average; when $\Phi$ is a point on the manifold, it is the weighted Fréchet mean, $m_{n+1} = \arg\min_y \sum_j w_j\, d(y,\Phi_j)^2$.

---

## Five Commitments

**1. Persistence implies accumulation.** A system that persists accumulates the patterns that work. The integral over its past makes CRR non-Markovian: the present depends on the accumulated history of the current regime.

**2. Finite capacity implies rupture.** No finite system can accumulate without limit. The Dirac delta has zero temporal extension: an empty boundary between past and future.

**3. Reconstruction is weighted by history.** After rupture, the system rebuilds from what it has inherited, weighted by recency and salience. The age weighting is a maximum-entropy choice, the same family as the averages used throughout statistics. How fast a system forgets is a property of that system, not a universal constant.

**4. The system has a characteristic scale.** $\Omega$ is one over the manifold's diameter, so it is set by the geometry, not chosen. What varies between systems is recency $q$: low $q$ rebuilds from the latest occasion (habit, rigidity), high $q$ draws on the long past (flexibility, transformation). CRR is not parameter-free: the resolution $\sigma$ is calibrated separately, the Fisher metric is fixed only up to a constant scale, and $q$ has no universal value.

**5. Rupture is a commitment.** At the cut, a bistable system is maximally uncertain about which state comes next; the act of "this regime / next regime" is a binary commitment.

---

## Geometry: Z₂ and SO(2)

- **Z₂ (bistable).** The Bernoulli manifold has Fisher–Rao diameter exactly $\pi$, so a single crossing from one basin to the other has $C^* = \pi$ and $\Omega_{Z_2} = 1/\pi$. This case is exact.
- **SO(2) (rotational).** A circle of states. Its Fisher circumference depends on which statistical model carries the circle: $2\pi$ for a unit Gaussian, other values for others. The natural cut is the half-turn, the point of maximal distinguishability. On the standard carrier that threshold is also $\pi$, so $\Omega = 1/\pi$ for both classes: they differ in shape, not in $\Omega$.

The value of $\Omega$ is set by the carrier, which must be declared. Earlier versions of this README said it was fixed by topology alone; that was too strong.

---

## Precision Architecture: Z₂ Sensory, SO(2) Prior

A modelling proposal from the network simulations. In a graph of Markov-blanketed agents, an **edge** alternates between two regimes of influence (Z₂) and a **node** cycles through belief updating (SO(2)). This suggests assigning Z₂ to sensory (likelihood) precision and SO(2) to prior (transition) precision.

In simulation the phase between the two channels is non-uniform, which is expected given how the simulation couples them; the Z₂ channel makes many small updates and the SO(2) channel few large ones. This is structurally compatible with Jang et al. (2026), where the relative timing of dopamine signals, not their magnitude, decides between learning and movement. These are simulation results, not yet tested on data.

---

## What Has Survived Testing

CRR has been through a preregistered, adversarial programme: frozen predictions, held-out data, must-fail controls, rivals allowed to win, and every failure kept on record. In summary:

**The mathematics is internally consistent, and related objects appear elsewhere.** The core is stated precisely as a conditional system: Fisher–Rao arc, a first-passage cut, a past-only regeneration, with every assumption written down. Its identities (path surplus $S = C - C^*$, a thermodynamic-length energy bound) check exactly. Recent work in other fields uses related objects, for example Fisher-path length against geodesic distance across language-model training checkpoints (ENIGMA; Seneque, 2025), steering along the Fisher geometry (Picozzi, 2026), and time as accumulated Fisher distinguishability. That suggests the abstraction is natural, not that CRR got there first; a full prior-art review is still to be done.

**Retrodiction: consistent across fields.** CRR was read against known results in 164 real-domain cases, with the answer known. In 98 the reading was correct: 39 using inherited information geometry alone, and 59 (62 after a literature check) where a CRR-specific ingredient changed the number and still landed on the known result. Ten more were candidate additions, though a literature check found each already known in direction. 28 were wrong. Where a CRR-specific ingredient did real work and could be checked, it was right 69 times out of 97 (71%). These are retrodictions: evidence of a consistent language, not of foresight. The 132-system survey linked below belongs to this layer.

**Prediction, locked in a box.** CRR was then tested prospectively. Each prediction was written down, hashed and pushed to a public repository before the data were fetched; the scorer was frozen; must-fail and must-pass controls were registered; rivals were allowed to win; and every verdict was printed by the frozen code into a ledger that is never edited. Under those rules, CRR-derived rules met their thresholds on unseen data 16 times and failed 37 times (plus 8 failures for a proposed universal regeneration law), with 5 void. Most passes had the same shape: a CRR rule with nothing tuned on the new data did as well as an established method tuned to it. Correct before seeing the data, but not better. Three passes came from tests too weak to tell rivals apart, four were for textbook methods, and none has yet been independently replicated. So far, CRR predicts correctly at the level of each field's own methods, and not beyond them.

**Continual learning: CRR-inspired engineering that works.** SEC, a regulariser that came out of CRR, was tested on held-out language-model data. Its schedule came out slightly ahead of a tuned grid search (0.014 nats [0.006, 0.022]) and a transferred constant (0.023), small margins that are fragile under robustness checks. Its one CRR-specific ingredient, however, was not shown to add anything over a constant of matched size; the working parts are established methods (an EWC-style anchor plus gradient projection). Good engineering, honestly credited.

**AI safety: design rules from the Empty Centre.** CRR's picture of the present as an empty boundary has produced useful constructions. A pause that leaves an agent's own clock untouched removes the incentive to resist shutdown in perfect-restart worlds. It converges with established results on safe interruptibility and utility indifference (Armstrong 2010; Orseau & Armstrong 2016), and the test put numbers on where that breaks: 59% of imperfect-restart worlds, 100% of deadline worlds. An empty-evidence rule beat its comparator in 600 of 600 synthetic worlds. Its working part is the textbook missing-observation Kalman filter. A pilot provenance test, in a world built to favour CRR, returned NO-GO. Nothing here yet bears on deployed systems.

**Levin and the origin of forms.** CRR holds that forms are productions of realised history, not ingressions from a Platonic space. This is what Blake's line means here: eternity is not a long time but the completed finitudes the present stands on. That is a genuine disagreement with Michael Levin's latent-space proposal. A discriminating test is declared on planarian regeneration: does a settled two-headed history change the outcome of a different morphological switch? It awaits a laboratory partner. A positive result would show history dependence; the ontology itself is recorded as not decidable by any experiment yet devised.

**What failed.** The strong forms failed on held-out data, and the record keeps them. "Change has its own clock" failed on measles (0 of 17 cities) and cardiac data (1 of 29, 5 of 29, 0 of 19). A universal Regeneration Law failed in every counted test. Fixing $\Omega$ from topology alone, and the CV predictions that followed from it ($1/2\pi$, $1/4\pi$), are hypotheses rather than consequences of the geometry: geometry alone cannot set physical timescales.

**The fairest single sentence on record:** *"CRR is a correct abstraction of what many sciences independently had to discover; it has not yet told any of them something they did not know."* In other words, CRR predicts about as well as the paradigms it translates, and has not yet out-predicted any of them. The next step tests exactly that: a blinded, prospective comparison of CRR-guided enquiry against conventional enquiry at equal resources.

---

## Links

### Framework & Tools

- [LLM Starter Guide](https://www.cohere.org.uk/132_LLM_Starter.MD): compact introduction for language models
- [LLM Exploration Prompt](https://www.cohere.org.uk/LLM_PROMPT_EXPLORE.MD): structured prompt for exploring CRR
- [132-system retrospective survey](https://www.cohere.org.uk/132.pdf) (2025)
- [AGI Conference paper (phase-gating)](https://www.cohere.org.uk/AGI_Conference_2026.pdf)

### Interactive Demonstrations

- [**The Depth Illusion**](https://www.cohere.org.uk/CRR_Human-AI_Dynamics.html): an Active Inference network where SO(2) human agents are coupled through Z₂ Markov blankets, with optional Z₂ LLM substrates attached to any node. Scale from 1 agent (a self) to 150 (Dunbar's number). In this toy, LLM nodes pull SO(2) agents toward Z₂ frequency (faster, shallower cycles) and track the cumulative "depth illusion" as agents misattribute LLM-driven updates to their own generative models.

- [**CRR Network**](https://www.cohere.org.uk/human_networks.html): the pedagogical simulation in which phase-gating first appeared. A complete graph K_n where nodes run SO(2) cycles and edges run Z₂ switches. Nodes glow slowly toward deep belief updates while edges flicker rapidly between regimes. Autonomy, integration (Φ) and the beauty function are tracked in real time.

- [**CRR Tree**](https://www.cohere.org.uk/crr_tree_branch.html): a tree grown from CRR rules. Every branch point is a rupture; every growth segment is coherence accumulation. The tree remembers where you looked first, because coherence only accumulates on-screen (your gaze = L(x,τ)) and rupture is irreversible. Attention constraining morphogenesis, live.

- [**Song of Time (Clocks)**](https://www.cohere.org.uk/song_of_time(clocks).html): a clock shop at midnight. A real quartz crystal (your sound card's 48 kHz oscillator) keeps the time. Eight Kuramoto-coupled pendulum clocks solved at sample rate, with coupling constants chosen from frequency ratios: octave (2:1) → K = 1/3, fifth (3:2) → K = 1/5. Synchronisation emerges. Nobody forces it.

### Aesthetic (CRR Songs)

- [**Song of the Wave**](https://www.cohere.org.uk/CRR_Waves.html): ocean physics (Fresnel reflectance, Beer–Lambert absorption, Stokes drift) driven by CRR coherence cycles. A dial controls the glass-to-storm continuum.
- [**Song of the Bowl**](https://www.cohere.org.uk/CRR_Singing_Bowl.html): a Tibetan singing bowl. Strike the water (rupture) or drag the rim (sustained coherence). A time-lens slows the physics to reveal wavefront propagation.
- [**Soma**](https://www.cohere.org.uk/soma_enhanced.html): the body as a CRR system.
- [**Song of Creation**](https://www.cohere.org.uk/songofcreation.html): cosmological structure formation driven by CRR dynamics.
- [**Aviana**](https://www.cohere.org.uk/aviana.html): birdsong and flock dynamics.
- [**Song of the Cosmos**](https://www.cohere.org.uk/song_of_the_cosmos.html): stellar evolution, galactic rotation and the CMB rendered as sound and light.

---

## Process Philosophy

*Source, experience, source.* Each of us arrives, innocent, into a past already under way. We live through it, and at every now we return to the centre, carrying what was lived: not the first innocence, but the kind that has been through experience. Process becomes through substance, and substance through process; the present is the past, transformed.

Why these forms: a hat, a galaxy, a can of lemonade, a grain of sand, a sunflower? Look again, and the question turns into wonder. Each is where countless decisions, at every scale and through all of time, have arrived, and so is whoever is looking. Not anyone's doing, and everyone's inheritance. I cannot say why these forms, and the record agrees that no one yet can. It is a gift to be here at all, to see them, and to take part in what comes next. 🌻

We hold each other through time, together. Ω = 1 = equanimity = peace.

*The score is not the music.* CRR is a candidate formalisation of a process view of time: reality is not made of things that change, but of changes that, now and then, cohere into things. In Whitehead's words, *"the many become one, and are increased by one."*

**C** is the past, settled and carried as constraint. **δ** is the present: no duration, no content. It separates; it does not fill. **m** is what comes next, rebuilt from what each occasion earned. On this reading, what can happen is built from the settled past of finite processes, still becoming through us, rather than waiting in a realm of forms outside time.

Between being everywhere at once and nowhere at all, there is somewhere: a place to stand, and an other to meet. Equanimity is holding the past at its earned weight, so the other can come through in their fullness. A good-enough holding environment does not require the other to become what we expected. It allows the other to arrive.

These are metaphysical commitments, held openly as such. No simulation or engineering result is offered as proof of them, and none of the failures above has touched them. Models are held, not mistaken for the world.

*"The past is not behind you; you are standing on it, now."*

These ideas are developed in [*Thinking in Extremes*](https://www.cohere.org.uk/Thinking_in_Extremes.pdf) (slides, Thriving in the Extremes, CCS 2026).

---

## Contact

**Alexander Sabine**, early years educator and researcher · [cohere.org.uk](https://www.cohere.org.uk) · [temporalgrammar.ai](https://temporalgrammar.ai) · [honami.co.uk](https://www.honami.co.uk)

```bibtex
@misc{sabine2025crr,
  author = {Sabine, Alexander},
  title = {Coherence–Rupture–Regeneration: A Temporal Grammar of
           Finite Becoming},
  year = {2025},
  url = {https://www.cohere.org.uk}
}
```
