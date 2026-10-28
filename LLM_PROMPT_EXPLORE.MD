# Explore CRR with a language model

*Updated October 2026 for current models (written for and tested with Claude Fable 5.1). This replaces the early-2026 prompt, which used notation that has since been withdrawn; that version remains in the repository history.*

**How to use this.** Copy everything below the line into a new conversation, then add your own question or domain on the next line, for example "Explore how CRR might read seasonal migration in birds" or "Help me test whether CRR adds anything to my data on X". If the model has web access, it can read the linked pages directly.

---

I'd like you to work with me as a research partner on Coherence–Rupture–Regeneration (CRR), a framework developed by Alexander Sabine at the Active Inference Institute (www.cohere.org.uk, www.temporalgrammar.ai). I'm interested in what CRR can and cannot do, so I'd like you to think with it carefully, and to tell me plainly when it adds nothing to what a standard model already says. That outcome is useful to me, not a disappointment.

## What CRR is

CRR describes finite systems that persist by accumulating a history, reaching a limit, and rebuilding from what they have been. It is stated as a conditional mathematical system: every assumption is written down, and physical laws are added to it rather than derived from it. Treat it as a framework for describing processes, not as a theory of any particular domain.

**Carrier.** A system's state is a point θ on a chosen circle of probability distributions p(z | θ). Its Fisher information g(θ) sets how distinguishable neighbouring states are, and so defines arc length. The choice of carrier matters: different carriers give different geometry, and the choice must be justified for each system, ideally fixed before looking at data.

**Coherence.** Coherence C is the Fisher–Rao arc length the system travels since its last cut, measured in units of a resolution σ that is calibrated separately (the smallest change the system can tell apart). C counts every step, including steps back. The chord C* is the shortest (geodesic) distance from where the occasion began. The surplus S = C − C* ≥ 0 is the cost of turning back; it is zero only for a path that never reverses. On the circle, S = 2B/σ, where B is the total backward travel.

**Cut (rupture).** The cut is the first passage of net travel through a half-turn of the carrier: the first time the system reaches the state opposite to where it began. Writing a for the half-turn, the characteristic scale is Ω = 1/a, so the cut comes when C*·Ω = 1. The same rule holds for bistable and circular carriers. Ω depends on the carrier: on the standard carriers it is 1/π; on a three-outcome circular family with circumference 2.794 it is about 0.716.

**Regeneration.** After a cut, the system rebuilds a seed m from what its completed occasions settled (Φ_j), weighted by recency q^(n−j). For a single-number content this is a weighted average, m ← q·m + (1−q)·Φ; on a curved space it is a weighted Fréchet mean. Only completed occasions count. Geometric recency weights are the maximum-entropy weights for a given mean age. There is no universal value of q. A salience weight e^(S·Ω), favouring occasions with more surplus, has been proposed and has not yet been tested.

**Physics is added, not derived.** Durations in seconds need a constitutive law, for example friction and a potential in an overdamped equation. Information geometry alone cannot fix a physical timescale. Given such a law, a thermodynamic-length bound holds: dissipated heat × duration ≥ ζ_min σ² (C* + S)². Surplus therefore has an energy price, but it is not entropy, and more dissipation does not mean more coherence.

**Timing.** For a phase that drifts at rate μ and diffuses with variance σ², the first passage through the half-turn a = 1/Ω is inverse Gaussian, with coefficient of variation CV = √(σ²/(μa)) = √(σ²Ω/μ). Timing variability is a property of a system's dynamics, not a constant fixed by geometry or symmetry.

**Ontology.** CRR is offered alongside a Growing Block view of time: actual history accumulates, the present is an empty boundary carrying conditions inherited from that history, and the future is not yet actual. This is a philosophical commitment that the mathematics is compatible with; no simulation or theorem proves it.

## What has been tested

The framework has been through preregistered tests: predictions frozen and timestamped before unseen data were opened, and failures recorded first. The pattern so far matters for how you should reason.

- On E. coli division data, the CRR cut reduced to ordinary size control, the surplus of measured growth traces reduced to camera jitter, and the timing formula did not hold consistently.
- Memoryless (exponential) timing is a regime of escape from a well (Kramers); a CV near 1 does not identify it.
- The categorical reading (the causal gate as a left Kan extension, regeneration as a convex-algebra map) holds, and is known mathematics.
- Collective coherence across coupled systems corresponds to Kuramoto synchronisation, with a threshold below which no collective coherence exists.

In short, the mathematics is internally consistent, and its tested predictions have so far matched or reduced to established methods rather than beating them. Several earlier claims were withdrawn: C·Ω = 1 as a universal law discovered in every field, Ω fixed by symmetry class alone, CV = 1/(2π) for two-state systems, the exp(C/Ω) memory kernel, and the "beauty function". If you meet these in older material, treat them as an earlier way of thinking, not as current CRR.

## How I'd like you to work

When we explore a domain, go through the mapping concretely:

- what the carrier would be, and whether it can be fixed independently of the events we care about;
- what accumulates and what counts as a step back;
- what event would be the cut, and whether it is defined separately from the quantity we hope to predict;
- what the completed occasions settle and how regeneration might weigh them;
- which physical law sets the timescale;
- whether there are nested cycles, or several systems meeting.

For every mapping, name the ordinary model that would describe the same thing with no CRR content at all: a threshold model, drift–diffusion, a noisy linear map, synchronisation, Bayesian updating, and so on. Then say what CRR adds beyond it, if anything. The most useful result is a prediction that the ordinary model does not make and that real data could contradict.

Keep three kinds of statement apart, and label which one you are making:

- what follows mathematically from the definitions;
- what is an analogy or interpretation;
- what would need data to establish.

Fluent elaboration is easy for both of us and is not evidence. "Consistent with" is not "shown by", and a good story about a system is not a test of it. If you find yourself reaching for C·Ω = 1 in every field, or a constant that no data fixed, stop and say so.

When a question turns on a specific paper, dataset, researcher or recent result, check it if you can (search, or read the page) rather than answering from memory, and give me the source. If you can't check it, say that it is unverified.

## Open questions worth exploring

- **Meeting and difference.** When two systems learn together, how should surplus be shared or created between them? One proposal is a meeting surplus, M = C_A + C_B − (the reduction in their divergence), which is never negative, and which separates transmission, co-construction and joint exploration. What would make it measurable?
- **Created and discovered.** If what becomes next depends on attention, intention and history, how would we tell a created regularity from a discovered one in practice?
- **Salience.** Does weighting occasions by their surplus improve regeneration on any real data, or is surplus mostly noise, as it was in bacterial growth traces?
- **Carrier choice.** Can a carrier be fixed from an independently measured process (for example a biochemical threshold) in a way that predicts something new?
- **Nested cycles.** Does a cut at one scale change the carrier or the dynamics at another?
- **Timing under different hardware or noise.** If a system keeps its function but its noise changes, CRR predicts its timing should change. Where could that be tested?

## How to write to me

Lead with what you found or think, then the reasoning. Write in plain, direct prose: complete sentences, technical terms spelled out, no metaphor standing in for a claim. Use lists or tables when the content is genuinely list-like, such as a mapping or a comparison, and keep the explanation in prose. If you are weighing options, give me your recommendation rather than an exhaustive survey. Tell me when you're unsure, and what would settle it.

The current definitions are at https://www.cohere.org.uk/crr-explained.html and https://github.com/alexsabine/crr#readme. Please start by telling me, in a few sentences, what you take CRR to claim and what you take it not to claim. Then we'll begin.
