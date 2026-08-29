# Conclusions

Four registers, as asked. Each claim below is tagged with where it was established:
**[verified]** = checked symbolically or numerically here; **[tested]** = pre-registered test
on existing data; **[derived]** = a consequence of the paper's own axioms that the paper does
not state; **[open]** = neither established nor refuted.

---

## 1. Physics

**The geometry is sound and, for the first time in this programme, convention-free.**
[verified] Propositions 1–3 hold exactly. The amplitude embedding p ↦ 2√p pulls the round
metric on S^{n−1}(2) back to Fisher–Rao; curvature is 1/4; vertices are π apart *in every
dimension*; the orthant is geodesically convex. Crucially, Ω = ε/π is a ratio of two lengths
in the same metric, so it survives the Čencov rescaling g → c²g that the Fisher metric leaves
free. The earlier variants' Ω = 1/φ_G did not, and their C was the *energy* functional
∫(ds/dτ)²dτ — not reparameterisation-invariant, and dimensionally ill-formed against a
reciprocal-length Ω. v01.2 repairs both. That is real progress and it should be said plainly.

**The one structural gap is that the clock counts path length and the capacity argument is
about diameter.** [verified] They coincide only for geodesic motion. On the binary arena — one
dimension, monotone traverse — C2 is exact. In dimension ≥ 2 a diffusing system accumulates
forty regimes' worth of arc length while its net displacement is a fraction of π. And the
paper's own §6.1 makes this worse rather than better: it identifies a regime with a stretch of
**non-equilibrium steady state**, and NESS *is* the breaking of detailed balance — circulating,
non-geodesic flow. So the paper's physical reading of a regime guarantees the condition under
which its clock over-counts. Two honest repairs: restrict C2 to the binary arena (where
everything else in the paper already lives), or add a geodesic/non-recurrence postulate and
own it as a postulate.

**Rupture in CRR is capacity-limited, not hazard-limited — and the data say so.** [tested]
This is the sharpest physical result of the exercise. A.12 models the cut as a thermal
softening: a hazard e^{C/Ω} rising toward the wall, giving Gompertz intervals and CV ∝ Ω².
§2.3 models it as a hard wall crossed with one quantum of overshoot, giving CV = Ω/2. These
are different physics — barrier crossing versus counting — and the paper asserts they are the
same. On 45 autonomous oscillators the counting law wins by ΔAIC = 91, and the fitted exponent
is 0.95 [0.72, 1.19], excluding 2. The internal argument had already settled it: A.12's hazard
e-folds over Ω cells, i.e. over **less than one resolvable cell** for every Ω in the grammar's
own domain. You cannot smear a threshold finer than your own resolution.

So: **CRR is a counting theory, and its variability floor is one evidence quantum.** That is
what distinguishes it from Kramers escape and from drift–diffusion first passage, and it is
the distinction that carries all of its empirical content.

**The concave-rise repair is free, and it is already an established empirical fact.**
[verified, derived] Neither CRR clock entrains: C1's is linear (flat phase-response curve to a
state pulse — confirmed to four decimals, locking occurs iff the initial offset ≤ κ and phase
differences are otherwise preserved exactly), and A.11's is convex. With 10% heterogeneity, a
concave clock synchronises at κ ≈ 0.3 where linear and convex need κ ≈ 1.0. §11.2 offers two
repairs and leans on the expensive one (coupling on speed, κ ≈ 1–4). The cheap one is the
first: **let L fall as the regime nears its cut.** That costs nothing — the period becomes
∫₀^π ds/L(s), still independent of Ω, so Prop 3(iii) survives intact — and it is *critical
slowing down*, one of the best-attested empirical signatures of systems approaching a
transition, in ecosystems, climate and physiology alike. The framework needs it and the world
already supplies it. Adopt it as a commitment, and it yields a new prediction: **the amount of
pre-rupture slowing sets a system's entrainment capacity.**

**Thermodynamics.** [verified, derived] The Landauer accounting is correct: the reset of a
known accumulator is free, the counter's clearance amortises to zero, and the irreducible cost
is erasing the bit acquired at the edge — 2.97×10⁻²¹ J at 310 K, ~4% of an in-cell ATP
hydrolysis. A consequence the paper does not draw: since the regime duration is π/L for
*every* Ω, the dissipation floor per unit time is **P ≥ (L/π)(1/Ω)k_BT ln 2** — inverse in
the dial. At fixed speed a rigid system dissipates more than a plastic one. Magnitudes
(~10⁻²⁰ W) constrain nothing biological, as the paper says; the scaling is the content and it
is measurable in neuromorphic hardware.

---

## 2. Temporal

**"Every regime is one unit of its own time" is the paper's best idea, and it holds.**
[verified] It rests on Prop 2(ii): the extent π is dimension-independent, so a cell and a
person, sharing no state space, exhaust at the same traversed length on their own manifolds.
Appendix B.1's thermal-time reading is internally consistent — I checked it: modular flow
generated by C/Ω runs at dλ/dτ = 1/Ω against the geometric flow, so thermal time τ = Ωλ, the
ratio thermal:geometric is Ω (Connes–Rovelli temperature), τ runs over [0,1] in every regime,
and a Gibbs state's Matsubara period is 1. Time comes out a **unit**, not a variable. The
paper is right to flag that it has not constructed the operator algebra this would need; it is
right that the arithmetic works.

**Simultaneity as an achievement, with a price now attached.** [verified] The claim that a
shared present is composed rather than given is not decoration; there is a genuine critical
coupling below which private nows persist in view of one another. We located it in the
CRR-specific setting, not by analogy: with 10% clock heterogeneity, R > 0.85 needs κ ≈ 0.3
(concave) or κ ≈ 1.0 (linear). D.5's "fragmented media environments are sub-critical coupling"
therefore has a formal referent and not merely a metaphorical one.

**The clock is Markov and the dial is not — and this is the framework's deepest true claim.**
[verified] Prop 9 is correct, including its explicit counterexample (two archives agreeing at
β = 2 give 745 and 198 at β = 4). Reconstruction at temperature Ω is the Laplace transform of
the archive's density of states, and no finite statistic of a history determines it for all
temperatures. The past is therefore **not a state**. That is a precise, provable claim about
time and memory, it is original to v01.2 within this programme, and it deserves more of the
paper's weight than it gets.

**Rate and dial are separable in the formalism and not demonstrated to be so in the world.**
[verified] Prop 3(iii) is exact: the cut falls at s = π at time π/L for every ε. But §3.3, the
one calibration offered, has a single physical input — the Maxwell time τ — and reads the dial
off it. If a material also reconfigures about once per relaxation time, rate and dial are
perfectly correlated across the whole table. The separation is the framework's centre of
gravity (C4) and the evidence offered for it is circular. What would settle it: two materials
of equal τ and different G, or equal De and different rupture rate.

---

## 3. Biological

**Early adversity is a theorem here, not a conjecture.** [verified] Insert one regime lived at
a precision the life never reaches again (Ω = 0.06 among 0.12–0.9) and it takes ≈100% of every
reconstruction at every Ω_t below 1. The paper presents its Frankenhuis–Gopnik alignment as a
directional prediction; Appendix A.6(ii) already proves it. It should claim more here.

**Therapy has a floor, and the paper can state it.** [derived] D.4 reads therapy as "a held
raising of Ω_t". Prop 6(ii) bounds what that can do: as Ω_t → ∞ each regime contributes
exactly its *mass*, φ̄ₖTₖ. So re-reading cannot delete a peaked regime — **its floor is that
regime's share of lived time.** In an eight-regime life, the traumatic share falls 1.000 →
0.937 → 0.417 → 0.167 as Ω_t goes 1 → 2 → 5 → 20, against a floor of 0.125. That is a real,
quantitative, and clinically legible claim, and it is one the framework earns.

**The still face, quantified.** [verified] Withdrawal from f = ½ to f = 0 drops kernel entropy
4.655 → 4.003: the effective number of past moments in play falls **105 → 55, a factor 1.92** —
while the cycle period does not move at all. Possibility space halves; the clock does not; the
face is still there. Prop 10 also confirms that the turn-taking and parallel architectures are
genuinely discriminable (period invariant in f vs shortening as (1−f)π/L), so the paper's
headline prediction really is a test and not a restatement.

**The lifespan-monotone annealing schedule is refuted.** [tested] §3.4 asserts without an
upper age bound that any process described as annealing is one in which Ω decreases with age.
In MPI-LEMON (N = 189), amplitude-envelope CV *rises* from young to old adults in 4 of 5
bands, significantly in delta (d = +0.46, p = 0.012). Inverting CV = Ω/2, implied Ω rises 9.3%.
The childhood claim is untouched — this is a young-adult/old-adult contrast — but the
unbounded version fails, and the sign test gives p = 0.97 against it.

The repair is available inside the paper's own mechanism. §6 identifies the dial with Hensch's
molecular brakes: perineuronal nets, myelin inhibitors, Lynx1. Those brakes are known to
*weaken* in senescence. So the CRR-consistent schedule is not monotone but **U-shaped**: Ω
falls through development as precision accrues, and rises again as regulatory precision is
lost. That is a better hypothesis than the one the paper states, it follows from the paper's
own mechanism, and it is what the data show.

**The interval law is the biological backbone and it survives, at T2.** [tested] CV = Ω/2
holds across 45 autonomous oscillators spanning calcium signalling, cell cycles, segmentation
clocks, cardiac and neural rhythms, and glacial cycles: median obs/pred 0.94 (Z₂) and 1.01
(SO(2)), σ_log 0.27, log-bias −0.001, class ratio 1.88 [1.50, 2.34] containing 2. A provenance
check (`DATA_PROVENANCE.md`) found that dataset's CV column to be a lattice of round-number
estimates with unverifiable per-row sourcing, which does not change the direction of the result
— the quantisation is small against the model separation and makes the AIC gaps conservative —
but caps it at empirical consistency rather than confirmed prediction. The EEG replications,
which report real dispersions, carry more weight than the survey.

**The holding law is untested, not confirmed.** [open] I reported that the neonatal inter-cry
interval lands on the f = ½ prediction to three decimals. It does not: 0.225 is a point on the
estimate lattice and the prediction 0.22508 rounds to it, so the agreement means only "within
±0.0125", and the row's citation cannot be traced from the paper. Withdrawn. Ω_eff = Ω/√(1−f)
remains the most valuable new thing in v01.2 and remains **unmeasured**.

**One prima facie problem worth naming.** [derived] P ∝ 1/Ω says that low-Ω operation —
habit, expertise, automaticity — costs *more* per unit time than exploration at the same
Fisher–Rao speed. The automaticity literature reports the opposite: practice reduces metabolic
cost. The framework's escape is that experts also run at lower L, so total power L/(πΩ) can
still fall. That is not a get-out; it is a **measurement programme**: estimate L and Ω
separately in novices and experts and the prediction either holds or it does not.

**The decisive open test.** [open] Prop 4(iii) commits to an edge kernel in which *lag
contributes nothing* — retention set by precision at encoding and position in the regime. That
predicts retention should step at regime boundaries rather than decline smoothly. A century of
forgetting curves shows smooth decline; event-boundary effects show discrete drops. The two
reconcile only if CRR regimes are identified with event boundaries. **The paper owes that
operationalisation and it is where its memory claims will be won or lost.**

---

## 4. Philosophical and contemplative

**Distinguish three strengths of claim, because the paper mostly does and is stronger for it.**

*What is proved.* Two philosophical claims in Appendix C are theorems of the formalism, not
readings of it.
- **C.6, finitude is the condition of content.** Prop 5 with Prop 3: kernel entropy is
  strictly monotone in Ω, running to the uniform maximum as Ω → ∞ and to −∞ as Ω → 0. A
  system with any content at all sits strictly inside the open interval. The middle way is not
  a metaphor here; it is the open interval, and both ends are unavailable to anything that
  experiences. This survives every check.
- **C.7, no reading is final.** This is Prop 9. Two archives can agree at one temperature and
  differ at another, and no finite statistic determines the reading at every temperature. So
  "truth is what survives re-reading across the dial" is a theorem, and Hershock's karma as
  improvisation — content closed, causal contribution live — becomes exact rather than
  analogical. **This is the philosophical high point of the paper and it is provable.**

*What is borrowed and correctly labelled.* The unevidenceability of one's own boundary is
Fields–Glazebrook's theorem, cited as such. The paper's own contribution is the *structural
analogy* to Winnicott's prohibition, and §14 says in terms that this is an observation and not
a proof. That is the right call and it should not be softened. The analogy is between a
quantum-information impossibility and a clinical injunction; the arena of the paper is a
classical statistical manifold. Nothing in the mathematics of C1–C5 depends on the theorem
being true, and nothing in the theorem depends on CRR.

*What is naming, not evidence.* The four correspondences are held to the paper's own test — a
tradition earns a place only where its language matches a specific structural feature. Graded:
Ibn 'Arabi's *ṣāḥib al-waqt* is the only one that maps to an **equation** (Prop 10: you cannot
choose your rate; you can choose f and Ω_t). Luria's *tzimtzum* maps to a **schedule**
(graduated withdrawal from φ). Zhuangzi's pivot maps to a **limit** (responsiveness as
non-fixity, the Ω → 0 rigidity). Nāgārjuna's emptiness maps to the **prohibition**, not to the
grammar. That is one equation, one schedule, one limit and one interpretive frame — a fair
haul, and less than the register of the passages suggests.

**Where the paper should hold its own line harder.** §15.1 reports that descriptions written
before the equations "turn out to be the equations" — being stuck as low Ω, love as flattening
what has cohered. As a report of how the work was made, that is worth having. As evidence it
is worth nothing: mapping English onto a one-parameter family after the fact has too many
degrees of freedom to fail. The paper half-says this ("whether that constitutes evidence for
anything I leave to the reader"). It should say it whole.

**A methodological finding, and it is the paper's own subject.** §15.2, written by a language
model, claims to have recomputed every proposition in Appendix A. **That claim checks out** —
independent recomputation finds Appendix A clean, 42 of 43, the one exception a symbolic-solver
limitation rather than an error. And yet the same process missed every finding in this report,
because all of them are conflicts *between* sections rather than errors *within* propositions:
§2.3 against A.12, eq. (4) against A.7, §3.3 against Prop 7, §6.1 against C2, §12(i) against
C2. **Proposition-level verification is not framework-level verification**, and a checker that
holds one proposition at a time will certify a framework that contradicts itself across
chapters. That is a small, exact instance of the paper's central claim: the machine can hold
structure and cannot hold the whole; the checking has to happen somewhere else.

**What the framework is, at the end of this.** A temporal grammar whose geometry is now clean,
whose one quantitative law survives 45 autonomous systems across 20 domains, whose deepest
result (the non-Markovian dial) is proved and under-claimed, whose developmental schedule is
refuted in its strong form and repairable in its mechanism, and whose contemplative material
is honestly fenced. It is not a theory of everything and does not present itself as one. It is
a notation with one law in it, and the law is CV = Ω/2 — which v01.2 has, in §2.3, and should
stop hiding behind an appendix that contradicts it.
