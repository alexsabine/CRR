# Coherence–Rupture–Regeneration (CRR) as Temporal Bayesian Mechanics  

> **Status (October 2026):** This is an archived working note (2025) that restates standard Bayesian model comparison (Gaussian log-likelihoods, log prior odds, Bayes-factor switching) in CRR terms. The propositions it proves are textbook results under a relabelling, not new findings, and its reading of Ω as log prior odds is superseded. Current definitions: https://www.cohere.org.uk/crr-explained.html and the README (https://github.com/alexsabine/crr#readme).

**Full canonical formalism, proofs, and explanations (FEP-aligned).**  
*(UK English; discrete-time primary, continuous-time as a limit.)*

---

## Abstract

This document presents a rigorous and internally consistent formulation of **Coherence–Rupture–Regeneration (CRR)** as a temporal extension of Bayesian model comparison (and therefore compatible with the Free Energy Principle, FEP). We define **coherence** as the accumulated (half) sum of squared Mahalanobis prediction errors, which is (up to a constant) the **negative log-likelihood** for Gaussian observation models. We define **rigidity** \(\Omega\) as the **log prior odds** favouring the current model over an alternative. We show that **rupture** emerges as *Bayesian model switching* when the log Bayes factor exceeds prior commitment. Finally, we clarify **regeneration** as the adoption of the new model and its properly normalised posterior, together with a reset (rebaselining) of the coherence accumulator. We include proofs of key propositions and theorems, note the precise assumptions under which “exactness” holds, and provide controlled approximations (first passage statistics) when modelling rupture timing.

---

## Contents

1. Scope, assumptions, and what CRR adds  
2. Notation and preliminaries  
3. Coherence: definition, likelihood connection, and properties (with proofs)  
4. Rigidity: definition and interpretation (with proofs of basic properties)  
5. Rupture: Bayesian model switching (theorems and proofs)  
6. Regeneration: correct post-rupture state (and what it is **not**)  
7. Operator view of CRR (canonical form)  
8. Continuous-time extension (observation rate)  
9. Rupture timing as a first passage problem (approximation, not overclaim)  
10. Practical implications, testable predictions, and extensions  
11. Appendix A: derivations and common pitfalls (fully explicit)

---

## 1. Scope, assumptions, and what CRR adds

### 1.1 Primary scope

CRR is a **coarse-grain temporal framework** for systems that:
- maintain a **current generative model** \(m\),
- accumulate evidence (for/against models) as observations arrive,
- occasionally undergo **discrete transitions** to an alternative model \(m'\),
- then continue inference under the new model.

CRR is compatible with:
- Bayesian model comparison and sequential testing,
- active inference / FEP (as the within-model inference engine),
- statistical mechanics analogies (insofar as they remain metaphors).

### 1.2 Exactness: what is exact, and when

CRR’s “exact” identities are exact **under explicit modelling assumptions**, notably:

- **Gaussian observation model** (or, more generally, any model where the likelihood ratio can be written in the stated accumulator form and constant terms are controlled).
- **Correct handling of normalisation terms** when comparing models with different precisions \(\Pi_m\) (see §3.4 and Appendix A.4).

When these assumptions do not hold, CRR remains usable but expressions become **approximations** (typically via variational bounds or predictive likelihoods).

### 1.3 What CRR adds to FEP (clean claim)

FEP primarily concerns **within-model** inference: updating beliefs about hidden states (and acting) to minimise variational free energy under a *given* generative model.

CRR adds a principled description of **between-model transitions**:
- how “evidence against the current model” accumulates over time,
- how prior inertia sets a threshold for switching,
- how and when a discrete switch occurs,
- how inference restarts under the new model without breaking probability normalisation.

---

## 2. Notation and preliminaries

### 2.1 Observations and models

- Observations: \(y_1,\dots,y_n\) (vectors in observation space)
- Models: \(m\) (current), \(m'\) (alternative)
- Model \(m\) provides a predictive mapping \(g_m(\mu_i)\) from internal state \(\mu_i\) to predicted observation \(\hat y_i\)
- Prediction: \(\hat y_i = g_m(\mu_i)\)
- Prediction error: \(\varepsilon_i^{(m)} := y_i - g_m(\mu_i)\)

### 2.2 Precision (inverse covariance)

- Observation noise covariance: \(\Sigma_m\)
- Precision: \(\Pi_m := \Sigma_m^{-1}\), with \(\Pi_m \succeq 0\) (positive semidefinite)

### 2.3 Gaussian observation model (canonical “exact” case)

For each \(i\), under model \(m\):
\[
p(y_i \mid \mu_i, m) \;=\; \mathcal{N}\!\big(y_i;\; g_m(\mu_i),\; \Sigma_m\big)
\]

Log-likelihood for one observation:
\[
\log p(y_i \mid \mu_i,m)
=
-\frac{1}{2}\,\varepsilon_i^{(m)\top}\Pi_m\,\varepsilon_i^{(m)}
-\frac{1}{2}\log\det\big(2\pi\Sigma_m\big)
\]

---

## 3. Coherence: definition, likelihood connection, and properties

### 3.1 Definition (discrete-time primary)

**Definition 3.1 (Coherence accumulator).**  
For \(n\) observations under model \(m\), define:

\[
\boxed{
C_m(n)\;:=\;\frac12\sum_{i=1}^{n}\varepsilon_i^{(m)\top}\Pi_m\,\varepsilon_i^{(m)}
}
\]

Interpretation:
- \(C_m(n)\) is **accumulated (precision-weighted) prediction error**, i.e. **explanatory debt** against model \(m\).
- It is *not* “coherence-as-fit-right-now”; it is the cumulative account used for model comparison over time.

### 3.2 Connection to (negative) log-likelihood

**Proposition 3.1 (Coherence equals negative log-likelihood up to a constant).**  
For Gaussian observation models with fixed \(\Pi_m\), the joint log-likelihood satisfies:

\[
\log p(y_{1:n}\mid \mu_{1:n},m)
=
-\frac12\sum_{i=1}^{n}\varepsilon_i^{(m)\top}\Pi_m\,\varepsilon_i^{(m)}
-\frac{n}{2}\log\det(2\pi\Sigma_m)
\]

Hence
\[
\boxed{
C_m(n) \;=\; -\log p(y_{1:n}\mid \mu_{1:n},m) \;+\; \frac{n}{2}\log\det(2\pi\Sigma_m)
}
\]

So \(C_m(n)\) is the **negative log-likelihood** plus a model-dependent normalisation term.

**Proof.** Substitute the Gaussian log-likelihood expression and sum over \(i=1,\dots,n\). The quadratic terms sum to \(C_m(n)\). The determinant term contributes \(\tfrac{n}{2}\log\det(2\pi\Sigma_m)\). ∎

> **Remark (why this matters):** When comparing models via likelihood ratios, constant terms may cancel, but only under stated conditions (§3.4).

### 3.3 Basic properties (with proofs)

**Proposition 3.2 (Non-negativity).**  
If \(\Pi_m \succeq 0\), then \(C_m(n)\ge 0\) for all \(n\).

**Proof.** For any vector \(v\), \(v^\top \Pi_m v \ge 0\) when \(\Pi_m\succeq 0\). Each summand \(\tfrac12\varepsilon_i^\top\Pi_m\varepsilon_i\ge 0\). A sum of non-negative terms is non-negative. ∎

**Proposition 3.3 (Monotone non-decreasing in \(n\)).**  
\(C_m(n+1)\ge C_m(n)\) for all \(n\).

**Proof.**
\[
C_m(n+1)=C_m(n)+\frac12\,\varepsilon_{n+1}^{(m)\top}\Pi_m\,\varepsilon_{n+1}^{(m)}\;\ge\;C_m(n)
\]
by Proposition 3.2. ∎

**Proposition 3.4 (Dimensionless).**  
If \(\varepsilon_i\) has units of observation and \(\Pi_m\) has units observation\(^{-2}\), then each \(\varepsilon_i^\top \Pi_m \varepsilon_i\) is dimensionless, hence \(C_m(n)\) is dimensionless.

**Proof.** Units multiply as:
\[
[\varepsilon^\top \Pi \varepsilon] = [\varepsilon]^2[\Pi]=(\text{obs})^2(\text{obs}^{-2})=1
\]
and sums preserve dimensionlessness. ∎

### 3.4 Constant terms and differing precisions (the important caveat)

If \(\Pi_m\neq \Pi_{m'}\), then the determinant terms in the Gaussian likelihood generally **do not cancel** in the Bayes factor.

For Gaussian observation models with (possibly) different covariances:
\[
\log p(y_{1:n}\mid \mu_{1:n},m)
=
-C_m(n) - \frac{n}{2}\log\det(2\pi\Sigma_m)
\]

Therefore the exact log Bayes factor is:
\[
\log\frac{p(y_{1:n}\mid m')}{p(y_{1:n}\mid m)}
=
\big(C_m(n)-C_{m'}(n)\big)
-\frac{n}{2}\Big(\log\det(2\pi\Sigma_{m'})-\log\det(2\pi\Sigma_m)\Big)
\]

**Canonical simplifying assumption (often acceptable):** when comparing models with the **same** observation noise structure (same \(\Sigma\), hence same \(\Pi\)), the determinant term cancels, yielding the clean identity:
\[
\boxed{
\log \mathrm{BF}(m' \text{ vs } m) = C_m(n)-C_{m'}(n)
}
\]
We will state the rupture theorem both with and without this cancellation assumption (§5).

---

## 4. Rigidity: prior commitment to the current model

### 4.1 Definition

**Definition 4.1 (Rigidity).**  
Rigidity is the log prior odds favouring the current model \(m\) over alternative \(m'\):

\[
\boxed{
\Omega \;:=\; \log\frac{p(m)}{p(m')}
}
\]

- \(\Omega>0\): prior favours staying with \(m\)  
- \(\Omega=0\): equal priors  
- \(\Omega<0\): prior favours switching to \(m'\)

### 4.2 Basic properties

**Proposition 4.1 (Dimensionless).**  
\(\Omega\) is dimensionless because it is the logarithm of a probability ratio.

**Proof.** Probabilities are unitless; the logarithm preserves unitlessness. ∎

**Interpretation (careful):** \(\Omega\) is mathematically **prior inertia**.  
If you choose to map this phenomenologically to “porosity/liquidity”, make that mapping explicit and keep the mathematical definition primary.

---

## 5. Rupture: Bayesian model switching

### 5.1 Posterior odds decomposition

By Bayes’ theorem:
\[
\frac{p(m' \mid y_{1:n})}{p(m \mid y_{1:n})}
=
\frac{p(y_{1:n}\mid m')}{p(y_{1:n}\mid m)}\cdot \frac{p(m')}{p(m)}
\]

Taking logs:
\[
\boxed{
\log\frac{p(m' \mid y_{1:n})}{p(m \mid y_{1:n})}
=
\log \mathrm{BF}(m' \text{ vs } m) - \Omega
}
\]

### 5.2 Rupture theorem (general form)

**Theorem 5.1 (Rupture as model switching).**  
A switch from model \(m\) to \(m'\) is favoured (rupture) when:
\[
\boxed{
\log\frac{p(m' \mid y_{1:n})}{p(m \mid y_{1:n})} > 0
\iff
\log \mathrm{BF}(m' \text{ vs } m) > \Omega
}
\]

**Proof.** Directly from the posterior odds decomposition above. ∎

### 5.3 Rupture theorem (clean coherence form: equal noise / cancelling constants)

Assume the observation noise normalisation cancels in the likelihood ratio (e.g. \(\Sigma_m=\Sigma_{m'}\)). Then:
\[
\log \mathrm{BF}(m' \text{ vs } m) = C_m(n)-C_{m'}(n)
\]

**Theorem 5.2 (Rupture in coherence form; cancelling-constants case).**  
Under the cancellation assumption,
\[
\boxed{
\text{Rupture occurs when}\quad C_m(n)-C_{m'}(n) > \Omega
}
\]

**Proof.** Substitute \(\log\mathrm{BF}=C_m-C_{m'}\) into Theorem 5.1. ∎

### 5.4 First passage time (rupture moment)

Define the rupture index (first time the threshold is reached):
\[
\boxed{
n^\* := \inf\Big\{n:\; \log \mathrm{BF}(m'\!:\!m) \ge \Omega\Big\}
}
\]
or, under cancellation,
\[
\boxed{
n^\* := \inf\Big\{n:\; C_m(n)-C_{m'}(n) \ge \Omega\Big\}
}
\]

### 5.5 Dirac delta idealisation (coarse-grain event marker)

CRR represents the rupture moment as a scale-free event:
\[
\boxed{
\delta(n-n^\*)
\quad\text{(or }\delta(t-t^\*)\text{ in continuous time)}
}
\]
This is a **mathematical idealisation** indicating *threshold crossing*, not detailed microdynamics.

### 5.6 Bayes factor at rupture (and the “\(e\)” clarification)

At the threshold:
\[
\log \mathrm{BF} = \Omega
\quad\Longrightarrow\quad
\boxed{\mathrm{BF}=\exp(\Omega)}
\]

- \(e\) appears only in the special case \(\Omega=1\) nat.  
- There is nothing inherently special about \(e\) beyond log/exponential duality.

---

## 6. Regeneration: adopting the new model (properly normalised)

### 6.1 What regeneration *is*

**Definition 6.1 (Regeneration).**  
After rupture at \(n^\*\), the system:

1. **Adopts the new generative model** \(m'\) (new \(g_{m'}\), \(\Pi_{m'}\), priors, etc.)
2. **Forms the new state posterior** (normalised):
   \[
   \boxed{
   p(\mu \mid m', y_{1:n^\*})
   }
   \]
3. **Rebaselines** the coherence accumulator for the newly adopted model:
   \[
   \boxed{
   C_{m'}(n^\*+)=0
   }
   \]
4. Establishes a new rigidity \(\Omega'=\log\frac{p(m')}{p(m'')}\) for future comparisons.

### 6.2 What regeneration is *not* (critical)

Regeneration is **not**:
\[
p(\mu \mid m', y)\cdot \exp(C/\Omega)
\]
because multiplying a probability distribution by a scalar factor generally **destroys normalisation** unless you renormalise—and even then it changes the distribution in an unjustified way.

Exponentials belong to **model odds** and **Bayes factors**, not to the **state posterior within a model**.

### 6.3 Optional scalar “size of regeneration”

If you want a scalar magnitude for the switch, a defensible choice is a divergence between posteriors:

\[
\boxed{
\Delta R := D_{\mathrm{KL}}\!\left[p(\mu\mid m',y_{1:n^\*})\;\Vert\;p(\mu\mid m,y_{1:n^\*})\right]
}
\]

This is optional: it is **not required** by CRR, but can be useful empirically.

---

## 7. Operator view (canonical CRR form)

CRR can be written as three temporal operators:

### 7.1 Coherence operator (Past \(\to\) Present)

\[
\boxed{
\widehat{\mathcal{C}}:\; (y_{1:n},m)\mapsto C_m(n)=\frac12\sum_{i=1}^{n}\varepsilon_i^{(m)\top}\Pi_m\varepsilon_i^{(m)}
}
\]

### 7.2 Rupture operator (Present event)

\[
\boxed{
\widehat{\delta}:\; (C_m,C_{m'},\Omega)\mapsto n^\*=\inf\{n: C_m(n)-C_{m'}(n)\ge \Omega\}
}
\]
with an event marker \(\delta(n-n^\*)\).

### 7.3 Regeneration operator (Present \(\to\) Future)

\[
\boxed{
\widehat{\mathcal{R}}:\; (m',y_{1:n^\*})\mapsto p(\mu\mid m',y_{1:n^\*})
}
\]
together with the rebaselining \(C_{m'}(n^\*+)=0\).

> **Compact statement:**  
> CRR is the composition \(\widehat{\mathcal{R}}\circ \widehat{\delta}\circ \widehat{\mathcal{C}}\) applied iteratively as data arrive.

---

## 8. Continuous-time extension (observation rate)

The discrete accumulator is primary. A continuous-time limit is convenient when observations arrive at a rate \(\rho(t)\) (observations per unit time).

Define:
\[
\boxed{
C_m(t)=\frac12\int_{0}^{t}\rho(\tau)\,\varepsilon(\tau)^\top\Pi_m\,\varepsilon(\tau)\,d\tau
}
\]

- \([\rho]=T^{-1}\) ensures \(C_m(t)\) remains dimensionless.
- Rupture time is first passage: \(t^\*=\inf\{t: C_m(t)-C_{m'}(t)\ge \Omega\}\).

---

## 9. Rupture timing as a first passage problem (approximation)

To obtain closed-form expectations, one may approximate the coherence difference as a drift–diffusion process in observation index \(n\):

\[
d\Delta C = \mu\,dn + \sigma\,dW_n,
\quad \Delta C := C_m - C_{m'}
\]

Then the first passage time \(n^\*\) to threshold \(\Omega\) has an inverse Gaussian distribution (classical Wald/first-passage results).

In this approximation:
\[
\mathbb{E}[n^\*]=\frac{\Omega}{\mu},\qquad
\mathrm{Var}(n^\*)=\frac{\sigma^2\,\Omega}{\mu^3}
\]

> **Important:** this is an approximation. The true discrete increments are typically positive and not literally Brownian. Use this as a controlled modelling choice, not as an “exact theorem” about all CRR systems.

---

## 10. Practical implications, testable predictions, and extensions

### 10.1 Testable predictions (directly implied)

1. **Prior manipulation:** increasing \(\Omega\) delays rupture (increases expected \(n^\*\) under drift approximation).
2. **Precision effects:** higher \(\Pi_m\) increases the rate of evidence accumulation (faster growth of \(C_m\)).
3. **Alternative fit matters:** rupture depends on \(\Delta C=C_m-C_{m'}\), so both current misfit and alternative adequacy matter.
4. **Bayes factor at rupture:** at threshold, \(\mathrm{BF}=\exp(\Omega)\) (not generically \(e\)).

### 10.2 Multi-model extension (beyond two models)

With a set of candidate models \(\{m_k\}\), the natural extension is:
- maintain a running score \(C_{m_k}(n)\) for each model (or its variational surrogate),
- switch to the model with best evidence when posterior odds exceed thresholds,
- optionally include switching costs via model priors.

### 10.3 Non-Gaussian and FEP/variational evidence

If likelihoods are non-Gaussian or latent variables are marginalised, replace \(-\log p(y\mid m)\) with an appropriate tractable objective:
- predictive log-likelihood
- variational free energy bound \(F_m\) such that \(F_m \ge -\log p(y\mid m)\)

Then CRR becomes:
- coherence accumulator: sum/integral of \(F_m\) (or predictive surprise),
- rupture: when evidence difference crosses \(\Omega\),
- regeneration: adopt new model and continue.

Be explicit about when you are using **bounds** rather than **exact** evidence.

---

## 11. Appendix A: derivations and common pitfalls

### A.1 Why the factor of \(\tfrac12\) is essential

Gaussian log-likelihood contains \(-\tfrac12 \varepsilon^\top\Pi\varepsilon\).  
If coherence is defined without \(\tfrac12\), Bayes factors inherit an incorrect factor. Defining
\[
C_m=\frac12\sum \varepsilon^\top\Pi\varepsilon
\]
makes the coherence difference align cleanly with log likelihood ratios.

### A.2 Dimensional consistency (why \(\int \varepsilon^\top\Pi\varepsilon\,dt\) needs a rate)

\(\varepsilon^\top\Pi\varepsilon\) is dimensionless; integrating over time yields units of time unless you include an observation rate \(\rho(t)\) (units \(T^{-1}\)). Discrete sums avoid this ambiguity.

### A.3 “Coherence increases as VFE decreases” (resolve the timescale confusion)

- The *instantaneous* quantity (a rate) can decrease as learning improves.  
- The *integral* of a non-negative rate increases with time.

If you want the intuitive “coherence increases as VFE decreases” statement, use a **rate coherence** (e.g. \(\kappa=-L\)) distinct from the cumulative accumulator \(C\). The rupture condition uses the cumulative accumulator.

### A.4 Handling different precisions / covariances across models

If \(\Sigma_m\neq \Sigma_{m'}\), then determinant terms appear in the Bayes factor. You can:
- include them explicitly (exact), or
- restrict “exact” claims to the shared-noise case, or
- absorb them into an augmented accumulator \(\widetilde C_m = C_m + \tfrac{n}{2}\log\det(2\pi\Sigma_m)\) so that \(\log \mathrm{BF} = \widetilde C_m - \widetilde C_{m'}\).

### A.5 The “\(\exp(C/\Omega)=e\)” pitfall

At rupture, the threshold condition defines a relationship between \(C\) and \(\Omega\). Any expression that yields \(e\) purely because \(C/\Omega=1\) is tautological. The meaningful statement is:
\[
\mathrm{BF}=\exp(\Omega)
\]
and \(e\) appears only when \(\Omega=1\).

### A.6 Regeneration normalisation pitfall

Do not multiply a normalised posterior \(p(\mu\mid m',y)\) by an evidence factor. Evidence factors govern **model probabilities**, not **state probabilities conditional on a model**.

---

## Summary: the canonical CRR equations (clean)

**Coherence (accumulated debt):**
\[
C_m(n)=\frac12\sum_{i=1}^{n}\varepsilon_i^{(m)\top}\Pi_m\,\varepsilon_i^{(m)}
\]

**Rigidity (prior odds):**
\[
\Omega=\log\frac{p(m)}{p(m')}
\]

**Rupture (switch condition; cancelling-constants case):**
\[
C_m(n)-C_{m'}(n)>\Omega
\]

**Rupture moment (first passage):**
\[
n^\*=\inf\{n:\,C_m(n)-C_{m'}(n)\ge \Omega\}
\quad\leadsto\quad
\delta(n-n^\*)
\]

**Regeneration (new posterior and reset):**
\[
p(\mu\mid m',y_{1:n^\*}),\qquad C_{m'}(n^\*+)=0
\]

---

*End.*
