# B7 — Memory is significance-weighted (coherence-weighted), not recency-weighted

## Prediction

The exp(C/Ω) regeneration kernel weights past states by their
*coherence* C, not by their *recency*. So "high-coherence remote
events dominate regeneration" — a structural prediction about
memory dynamics in any system implementing the CRR cycle.

## Empirical regularity

Multiple potential public sources:

- **Episodic-memory psychology:** Murdock (1962) primacy/recency
  curves; Loftus (1996) eyewitness-memory weighting; Kahana (2012,
  *Foundations of Human Memory*) — established that emotional /
  significant events override pure-recency in free recall.
- **Reservoir computing literature:** echo-state networks and
  liquid-state machines empirically show *significance-weighted*
  memory traces (Maass et al. 2002; Schrauwen et al. 2008); the
  exp-kernel is a known design choice.
- **Hippocampal replay:** sharp-wave ripples (Wilson & McNaughton
  1994; Diba & Buzsáki 2007) re-activate high-coherence behavioural
  episodes preferentially, not the most-recent.
- **Reinforcement-learning prioritised replay** (Schaul et al. 2015,
  DeepMind): TD-error-weighted replay dramatically outperforms
  uniform; this is the engineering-side confirmation that
  significance-weighting beats recency-weighting in adaptive systems.

## Reproduction script

`crr-engine/consistency/significance_memory.py` — sandbox-runnable.

Implements: simulate a CRR system with mixed high-coherence and
low-coherence past events; compute the regeneration weight (exp(C/Ω))
for each; verify high-C events dominate the regeneration integral
in proportion to their exp-weight.

This is a *structural* test (the exp(C/Ω) kernel by construction
weights by C; verifying it does so is checking the implementation,
not the empirical claim). The empirical content of B7 is the
*biological* claim that brains, ecological agents, and adaptive
systems implement coherence-weighted memory; that requires the
external empirical sources above.

## Tier decision

**T2 (mathematical part) / T1 (biological part).**

The mathematical claim — that exp(C/Ω) weights by coherence not
recency — is structurally true by construction.

The biological claim — that real memory systems implement this
kernel — is consistent with a large body of psychological and
neuroscience literature (cited above) but has not been directly
tested as a CRR-specific prediction. The cited evidence is broadly
*consistent* with significance-over-recency weighting, providing
T2-level support for the broad claim.

**Tier decision: T2 (broad consistency with established literature).**

## Applied usefulness for 2026 and beyond

This is one of the most directly applicable CRR claims in the AI
era:

- **AI memory systems for long-context reasoning:** Claude, GPT,
  Gemini, and frontier models 2026+ struggle with long-context
  retention. CRR's significance-weighted regeneration kernel is a
  candidate architecture for *retrieval-augmented memory* that
  prioritises high-coherence (high-information, high-relevance)
  past tokens over recent ones. Already implicit in
  prioritised-replay work in DeepMind / OpenAI.
- **Continual / lifelong learning:** catastrophic forgetting in
  neural networks could be mitigated by exp(C/Ω)-weighted experience
  replay, where C measures gradient-information per past sample.
- **Search / recommendation systems:** Google, Bing, Perplexity
  ranking pipelines implicitly weight recency vs significance; CRR
  formalises this trade-off and gives a parameter-free weighting
  rule.
- **Education / spaced-repetition apps** (Anki, Duolingo, RemNote):
  current spaced-repetition algorithms use Ebbinghaus-style
  forgetting curves; CRR's coherence-weighted kernel is an
  alternative that prioritises *significance* of past learning
  events alongside recency.
- **Trauma therapy** (e.g., EMDR, prolonged exposure): high-C
  traumatic memories dominate regeneration without intervention;
  CRR provides a quantitative framework for understanding why
  exposure-based therapies work (modulating C via reconsolidation).
- **Surveillance & security**: anomaly detection systems can
  prioritise high-coherence (high-information) past events as
  context, improving novel-attack detection.

B7's applied resonance is broad. The most operationally tractable
application in 2026 is *AI memory architecture* — frontier-model
labs have a direct interest in any principled weighting rule for
context retention.
