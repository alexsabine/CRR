# Forms, choices and the Now: the CRR reading of Platonic space, and what it amounts to (2026-10-06) — Parts I–II

*(Part III, differentiation from existing positions, and Part IV, pedagogical easement, are in `FORMS_AND_EASEMENT_PART3-4.md`; they depend on the fetched sweep.)*

**Status.** Interpretation and formal checks; layer metaphysics (M6, M7) and philosophy of science (P23, P28). No rung. Checks in `forms_checks.py` (five, all hold, each with a must-fail arm); core measurements in `measure_core.py`.

## Part I — The reading, in the owner's terms, labelled

The owner's formulation, in four clauses:

> The forms are the result of the "choices" made in every "Now". It is not discovered ingression, it is how memory and becoming work through time. When I think "Why these forms?" at a deep level, I cannot answer that, but that is the point. Separate and together. The difference between us matters.

**Clause 1. Forms are the result of choices made at every Now.** *Commitment (M7).* "Choice" is metaphysical shorthand (the seed's own warning in `PLATONIC_SPACE.md`): at each occasion something becomes settled that was not settled before, and what is settled is not fixed by the law alone. A persistent form is what repeated settlement leaves standing.

**Clause 2. Not ingression; memory and becoming working through time.** *Commitment (M7 against Levin; also, as the sweep will show, against Whitehead's eternal objects).* Forms are not located in a space prior to their instantiation and then pointed to or let in. They are produced: becoming settles, memory (regeneration from the settled past) keeps what was settled available, and persistence is re-settlement. There is no inventory.

**Clause 3. "Why these forms?" cannot be answered, and that is the point.** *A claim about the structure of explanation, which the checks make precise.* If forms are produced by settlement that the law underdetermines, then the answer to "why this form rather than that" is not in the law and not in the form; it is in the history, as the record of which way settlement went. The question has an answer, but the answer is a history, not a reason. That is why it feels unanswerable "at a deep level": one is asking the law for something only the record holds.

**Clause 4. Separate and together; the difference between us matters.** *Commitment (M6, "finitude enables relation").* Relation requires two things: that the relata be distinguishable (separate: a nonzero distance) and that they be comparable (together: a shared carrier on which a distance exists). Difference is not a defect of relation; it is its condition.

## Part II — What the checks show the clauses amount to

| Check | Clause | What holds | What it is, named |
|---|---|---|---|
| F1a–b | 1, 3 | In a symmetric bistable law from a symmetric start, the law gives each form probability 0.51 / 0.49 over 2000 histories, while the sign of the path at a tenth of the run predicts the realised form with accuracy 0.98 | **Symmetry breaking under Curie's principle:** the law is symmetric, the outcome is not, and the asymmetry comes from the history. "Why this form" is answered by the record, not the law. |
| F1c | 3 | With an asymmetric law the form is predictable from the law alone (1.00) | Must-fail arm: the unanswerability is a property of symmetric or multistable laws, not of forms as such. |
| F2 | 1, 2 | A settled form absorbs perturbations up to a kick of 1.0 (the distance to the separatrix) and is replaced beyond it | **Hysteresis:** memory of the choice is carried by the attractor with finite tolerance. Which side you are on is history; where the boundary is, is law. |
| F3a | 4 | Identical states passed through the same channel yield zero bits about which is which; a separation of 1 Fisher unit yields 0.16 bits, 4 units 0.91 bits | **Distinguishability is the precondition of relation** ("separate"). |
| F3b | 4 | A Fisher distance exists only between states of the same carrier; across carriers it is undefined | **Comparability is the other precondition** ("together"): a shared manifold. |
| F4 | 2 | A production model with memory (each occurrence of a form makes it more likely: a Pólya urn) lowers the entropy of the next form from 3.00 to 2.54 bits over 60 occasions; a fixed library (ingression) keeps it at 3.00 | **A precedence signature:** production and ingression differ observably *if* the library is fixed. Let the library's weights update with use and the two are equivalent. |
| F5 | 3 | The symmetry-breaking moment varies across histories (mean step 279, SD 104); the final state records which form but not when or why | **The answer lives only in the history**, which is what M4 and M5 say must be kept: regenerate from the settled past, and do not mistake the map (the form) for the history. |

**What this means for the reading.** Every clause has a precise formal content, and in every case that content is a known piece of mathematics: symmetry breaking and Curie's principle (clauses 1 and 3), hysteresis and attractor memory (clause 2), the information-theoretic preconditions of distinguishability and comparability (clause 4), and a Pólya-urn precedence effect (the production-versus-ingression difference). The reading is therefore *coherent* and *not empty*: it says that forms are law-underdetermined, history-selected, attractor-kept and precedent-reinforced, and that is checkable. It is also *not CRR-specific*: nothing in the five checks used the circle, the cut or the surplus; they used only "settled past conditions what continues" and "difference on a shared carrier".

**The one place the reading has teeth** is F4. If forms are produced rather than ingressed, then systems with no precedent should show more entropy in what they settle into than systems with precedent, and the entropy should fall as precedents accumulate. That is a prediction. It is also, as Part III records, Smolin's principle of precedence stated for quantum systems in 2012, so CRR shares a prediction here rather than owning one. And it can be absorbed by an ingression view that lets the library learn, at which point the two views induce the same law and the comparison is NOT DECIDABLE by the Egg's rule.

**The one place the reading differs from its nearest ancestor** is clause 2. Whitehead's occasions prehend *eternal objects* that ingress into them; Levin's patterns ingress from a Platonic space. The owner's CRR removes the inventory entirely. Peirce's habit-taking, Smolin's precedence and Brouwer's constructions in time are the positions without an inventory; those are CRR's kin on this point. Part III sets them out with fetched sources.
