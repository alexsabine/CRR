# Coherence–Rupture–Regeneration (CRR): A Complete Proof Sketch

> **Status (October 2026):** This is an archived working note (2025) using superseded notation (rupture at C = Ω, exp(C/Ω) kernels). Its "theorems" are standard identities (Bayes' rule, Gaussian likelihood, maximum entropy) relabelled in CRR vocabulary, so they establish internal consistency only, not empirical support. Current definitions: https://www.cohere.org.uk/crr-explained.html and the README (https://github.com/alexsabine/crr#readme).

**A Rigorous Mathematical Foundation for Temporal Identity Through Discontinuous Change**

---

## Preamble

This document provides a complete proof sketch for the CRR framework. Every step is explicitly justified. Where assumptions are made, they are stated. Where gaps remain, they are acknowledged.

The goal is to establish:
1. What CRR **is** (precise definitions)
2. What can be **proved** (theorems with proofs)
3. What remains **conjectured** (open questions)

---

## Part I: Foundations

### §1. Primitive Concepts

We begin with undefined primitive concepts that ground the framework:

**Definition 1.1 (System).** A *system* is an entity that:
- Maintains a boundary distinguishing inside from outside (Markov blanket)
- Persists through time while undergoing change
- Has internal states that can be described mathematically

**Definition 1.2 (Observation).** An *observation* y ∈ ℝᵈ is a measurement of the system's relationship with its environment at a given time.

**Definition 1.3 (Generative Model).** A *generative model* m is a probabilistic specification:
- A state space M
- A mapping g_m: M → ℝᵈ (predictions)
- A likelihood p(y | μ, m) for observations given internal state μ ∈ M

### §2. The Gaussian Observation Model (Standing Assumption)

**Assumption A1 (Gaussian Likelihood).** Throughout this document, unless otherwise stated, we assume:

$$p(y | \mu, m) = \mathcal{N}(y; g_m(\mu), \Sigma_m)$$

where:
- g_m(μ) is the predicted observation
- Σ_m is the observation noise covariance
- Π_m := Σ_m⁻¹ is the precision matrix (assumed positive definite)

**Remark.** This assumption is not essential for the framework but enables exact calculations. Extensions to non-Gaussian models proceed via variational bounds.

### §3. The Mahalanobis Distance

**Definition 3.1 (Prediction Error).** The prediction error at time i is:

$$\varepsilon_i^{(m)} := y_i - g_m(\mu_i)$$

**Definition 3.2 (Mahalanobis Distance Squared).** The precision-weighted squared prediction error is:

$$D_i^{(m)} := (\varepsilon_i^{(m)})^\top \Pi_m \, \varepsilon_i^{(m)}$$

**Proposition 3.1 (Non-negativity).** D_i^{(m)} ≥ 0 for all i.

*Proof.* Since Π_m is positive definite, for any vector v ≠ 0, we have v^⊤ Π_m v > 0. For v = 0, the expression equals 0. Thus D_i^{(m)} ≥ 0. ∎

**Proposition 3.2 (Dimensionlessness).** D_i^{(m)} is dimensionless.

*Proof.* Let [y] denote the dimension of observation. Then:
- [ε] = [y]
- [Σ] = [y]²
- [Π] = [Σ]⁻¹ = [y]⁻²
- [ε^⊤ Π ε] = [y] · [y]⁻² · [y] = 1 (dimensionless) ∎

---

## Part II: The Coherence Operator

### §4. Definition of Coherence

**Definition 4.1 (Coherence, Discrete Time).** For n observations under model m, the coherence is:

$$\boxed{C_m(n) := \frac{1}{2} \sum_{i=1}^{n} D_i^{(m)} = \frac{1}{2} \sum_{i=1}^{n} (\varepsilon_i^{(m)})^\top \Pi_m \, \varepsilon_i^{(m)}}$$

**Definition 4.2 (Coherence, Continuous Time).** For continuous observation flow with rate ρ(t):

$$\boxed{C_m(t) := \frac{1}{2} \int_0^t \rho(\tau) \, \varepsilon(\tau)^\top \Pi_m \, \varepsilon(\tau) \, d\tau}$$

**Remark on the factor ½.** This factor ensures coherence equals negative log-likelihood (up to constants) for Gaussian models. See Theorem 5.1.

### §5. Coherence and Log-Likelihood

**Theorem 5.1 (Coherence-Likelihood Correspondence).**
Under Assumption A1, the joint log-likelihood satisfies:

$$\log p(y_{1:n} | \mu_{1:n}, m) = -C_m(n) - \frac{n}{2} \log \det(2\pi\Sigma_m)$$

*Proof.* 

Step 1: Write the Gaussian log-likelihood for a single observation:
$$\log p(y_i | \mu_i, m) = -\frac{1}{2}(\varepsilon_i^{(m)})^\top \Pi_m \varepsilon_i^{(m)} - \frac{1}{2}\log\det(2\pi\Sigma_m)$$

Step 2: Assuming conditional independence given states, the joint likelihood factors:
$$\log p(y_{1:n} | \mu_{1:n}, m) = \sum_{i=1}^{n} \log p(y_i | \mu_i, m)$$

Step 3: Substitute and separate:
$$= \sum_{i=1}^{n} \left[ -\frac{1}{2}(\varepsilon_i^{(m)})^\top \Pi_m \varepsilon_i^{(m)} - \frac{1}{2}\log\det(2\pi\Sigma_m) \right]$$

$$= -\frac{1}{2}\sum_{i=1}^{n} (\varepsilon_i^{(m)})^\top \Pi_m \varepsilon_i^{(m)} - \frac{n}{2}\log\det(2\pi\Sigma_m)$$

Step 4: Recognize the first term as C_m(n):
$$= -C_m(n) - \frac{n}{2}\log\det(2\pi\Sigma_m)$$ ∎

**Corollary 5.2.** Coherence is (up to an additive constant) the negative log-likelihood:

$$C_m(n) = -\log p(y_{1:n} | \mu_{1:n}, m) - \frac{n}{2}\log\det(2\pi\Sigma_m)$$

### §6. Properties of Coherence

**Theorem 6.1 (Fundamental Properties of Coherence).**

(i) **Non-negativity:** C_m(n) ≥ 0 for all n ≥ 0.

(ii) **Monotonicity:** C_m(n+1) ≥ C_m(n) for all n ≥ 0.

(iii) **Additivity:** C_m(n) = C_m(k) + C_m^{(k,n)} where C_m^{(k,n)} is coherence over observations k+1 to n.

(iv) **Dimensionlessness:** C_m(n) is dimensionless.

*Proof.*

(i) C_m(n) is a sum of non-negative terms (by Proposition 3.1), hence non-negative.

(ii) C_m(n+1) = C_m(n) + ½D_{n+1}^{(m)} ≥ C_m(n) since ½D_{n+1}^{(m)} ≥ 0.

(iii) By definition:
$$C_m(n) = \frac{1}{2}\sum_{i=1}^{n} D_i^{(m)} = \frac{1}{2}\sum_{i=1}^{k} D_i^{(m)} + \frac{1}{2}\sum_{i=k+1}^{n} D_i^{(m)} = C_m(k) + C_m^{(k,n)}$$

(iv) Each D_i^{(m)} is dimensionless (Proposition 3.2), and sums of dimensionless quantities are dimensionless. ∎

---

## Part III: The Rigidity Parameter

### §7. Definition of Rigidity

**Definition 7.1 (Rigidity as Log Prior Odds).**
Given a current model m and alternative model m', the rigidity is:

$$\boxed{\Omega := \log \frac{p(m)}{p(m')}}$$

where p(m), p(m') are prior probabilities of the models.

**Proposition 7.1 (Properties of Rigidity).**

(i) Ω ∈ ℝ (can be positive, negative, or zero)

(ii) Ω > 0 ⟺ prior favors current model m

(iii) Ω = 0 ⟺ equal priors

(iv) Ω is dimensionless

*Proof.* 
(i)-(iii) follow directly from properties of logarithm and probability ratios.
(iv) Probabilities are dimensionless; logarithms preserve dimensionlessness. ∎

### §8. Rigidity as System "Temperature"

**Interpretation (Physical Analogy).**
In statistical mechanics, temperature T appears in Boltzmann factors as exp(-E/kT).
In CRR, Ω appears in regeneration weights as exp(C/Ω).

The correspondence suggests:
- Ω ↔ kT (thermal energy scale)
- Low Ω → "cold" system, sharp probability peaks
- High Ω → "hot" system, flat probability distribution

This is an *analogy*, not an identity. We make it precise in Part V.

---

## Part IV: The Rupture Condition

### §9. Bayesian Model Comparison

**Theorem 9.1 (Posterior Odds Decomposition).**
The posterior odds ratio satisfies:

$$\frac{p(m' | y_{1:n})}{p(m | y_{1:n})} = \frac{p(y_{1:n} | m')}{p(y_{1:n} | m)} \cdot \frac{p(m')}{p(m)}$$

*Proof.* By Bayes' theorem:
$$p(m | y_{1:n}) = \frac{p(y_{1:n} | m) p(m)}{p(y_{1:n})}$$

Taking the ratio:
$$\frac{p(m' | y_{1:n})}{p(m | y_{1:n})} = \frac{p(y_{1:n} | m') p(m')}{p(y_{1:n} | m) p(m)}$$ ∎

**Definition 9.1 (Bayes Factor).**
$$\text{BF}(m' : m) := \frac{p(y_{1:n} | m')}{p(y_{1:n} | m)}$$

**Corollary 9.2 (Log Posterior Odds).**
$$\log \frac{p(m' | y_{1:n})}{p(m | y_{1:n})} = \log \text{BF}(m' : m) - \Omega$$

### §10. The Rupture Theorem

**Assumption A2 (Equal Observation Noise).**
For the clean form of the rupture condition, assume Σ_m = Σ_{m'} (hence Π_m = Π_{m'}).

**Lemma 10.1 (Log Bayes Factor under A2).**
Under Assumption A2:
$$\log \text{BF}(m' : m) = C_m(n) - C_{m'}(n)$$

*Proof.*
From Theorem 5.1:
$$\log p(y_{1:n} | m) = -C_m(n) - \frac{n}{2}\log\det(2\pi\Sigma_m)$$
$$\log p(y_{1:n} | m') = -C_{m'}(n) - \frac{n}{2}\log\det(2\pi\Sigma_{m'})$$

Under A2, the determinant terms are equal, so:
$$\log \text{BF}(m' : m) = \log p(y_{1:n} | m') - \log p(y_{1:n} | m)$$
$$= -C_{m'}(n) + C_m(n) = C_m(n) - C_{m'}(n)$$ ∎

**Theorem 10.2 (Rupture Condition).**
Under Assumptions A1 and A2, the posterior favors switching from m to m' if and only if:

$$\boxed{C_m(n) - C_{m'}(n) > \Omega}$$

*Proof.*
The posterior favors m' when:
$$\frac{p(m' | y_{1:n})}{p(m | y_{1:n})} > 1$$

Taking logarithms:
$$\log \frac{p(m' | y_{1:n})}{p(m | y_{1:n})} > 0$$

By Corollary 9.2:
$$\log \text{BF}(m' : m) - \Omega > 0$$

By Lemma 10.1:
$$C_m(n) - C_{m'}(n) > \Omega$$ ∎

**Definition 10.1 (Rupture Time).**
The rupture time is the first passage to threshold:

$$\boxed{n^* := \inf\{n \geq 1 : C_m(n) - C_{m'}(n) \geq \Omega\}}$$

**Remark (Dirac Delta Notation).**
CRR represents the rupture event as δ(n - n*), indicating an instantaneous transition. This is a mathematical idealization—the rupture is the *threshold crossing event*, not detailed transition dynamics.

### §11. Generalization Without Assumption A2

**Theorem 11.1 (General Rupture Condition).**
Without Assumption A2, the rupture condition becomes:

$$C_m(n) - C_{m'}(n) - \frac{n}{2}\left[\log\det(2\pi\Sigma_{m'}) - \log\det(2\pi\Sigma_m)\right] > \Omega$$

*Proof.* Direct substitution of the full log-likelihood expressions from Theorem 5.1. ∎

**Corollary 11.2.** Define the augmented coherence:
$$\tilde{C}_m(n) := C_m(n) + \frac{n}{2}\log\det(2\pi\Sigma_m)$$

Then the general rupture condition is: $\tilde{C}_m(n) - \tilde{C}_{m'}(n) > \Omega$

---

## Part V: The Regeneration Operator

### §12. The Problem of Post-Rupture Reconstruction

After rupture at n*, the system must:
1. Adopt the new model m'
2. Construct initial beliefs about states under m'
3. Continue inference

**Question:** How should historical states be weighted in constructing the new configuration?

### §13. Maximum Entropy Derivation

**Theorem 13.1 (MaxEnt Weighting).**
Let {φ(τ) : τ ∈ [0,t]} be historical states and {C(τ) : τ ∈ [0,t]} be accumulated coherence. 

Suppose we seek weights w(τ) ≥ 0 satisfying:

(i) **Normalization:** ∫₀ᵗ w(τ) dτ = 1

(ii) **Mean coherence constraint:** ∫₀ᵗ w(τ) C(τ) dτ = μ (fixed)

(iii) **Maximum entropy:** w maximizes H[w] = -∫₀ᵗ w(τ) log w(τ) dτ

Then the unique solution is:

$$\boxed{w(τ) = \frac{1}{Z} \exp\left(\frac{C(\tau)}{\Omega}\right)}$$

where Z is the normalization constant and Ω is determined by the constraint (ii).

*Proof.*

**Step 1: Set up the Lagrangian.**

We maximize entropy subject to constraints using Lagrange multipliers:
$$\mathcal{L}[w] = -\int_0^t w(\tau) \log w(\tau) \, d\tau + \alpha\left(\int_0^t w(\tau) \, d\tau - 1\right) + \beta\left(\int_0^t w(\tau) C(\tau) \, d\tau - \mu\right)$$

**Step 2: Take the functional derivative.**

$$\frac{\delta \mathcal{L}}{\delta w(\tau)} = -\log w(\tau) - 1 + \alpha + \beta C(\tau) = 0$$

**Step 3: Solve for w(τ).**

$$\log w(\tau) = \alpha - 1 + \beta C(\tau)$$
$$w(\tau) = \exp(\alpha - 1) \cdot \exp(\beta C(\tau))$$

**Step 4: Apply normalization.**

Let Z := ∫₀ᵗ exp(β C(τ)) dτ. Then:
$$w(\tau) = \frac{\exp(\beta C(\tau))}{Z}$$

**Step 5: Identify Ω.**

Writing β = 1/Ω (where Ω is determined by constraint (ii)):
$$w(\tau) = \frac{1}{Z} \exp\left(\frac{C(\tau)}{\Omega}\right)$$ ∎

**Corollary 13.2 (Regeneration Operator Form).**
The MaxEnt-optimal reconstruction of a functional R from history is:

$$\boxed{R[φ](t) = \int_0^t φ(\tau) \cdot \frac{\exp(C(\tau)/\Omega)}{Z} \cdot \Theta(t-\tau) \, d\tau}$$

where Θ(t-τ) is the Heaviside step function enforcing causality.

### §14. Properties of the Regeneration Operator

**Theorem 14.1 (Properties of Regeneration).**

(i) **Linearity in φ:** R[aφ₁ + bφ₂] = aR[φ₁] + bR[φ₂]

(ii) **Causality:** R[φ](t) depends only on {φ(τ) : τ ≤ t}

(iii) **Ω-dependence:**
   - As Ω → 0⁺: weights concentrate on argmax_τ C(τ)
   - As Ω → ∞: weights become uniform

*Proof.*

(i) Direct from linearity of integration.

(ii) The factor Θ(t-τ) ensures the integrand is zero for τ > t.

(iii) 
- For Ω → 0⁺: exp(C/Ω) → ∞ at τ* = argmax C(τ), and remains bounded elsewhere. By Laplace's method, the integral localizes to τ*.
- For Ω → ∞: exp(C/Ω) → exp(0) = 1 uniformly, giving uniform weights. ∎

---

## Part VI: Thermodynamic Consistency

### §15. Statistical Mechanics Structure

**Theorem 15.1 (Boltzmann Structure).**
The regeneration weight exp(C(τ)/Ω) has the form of a Boltzmann factor with:
- Effective energy: E_eff = -C(τ)
- Effective temperature: T_eff = Ω

*Proof.*
The Boltzmann distribution is P(state) ∝ exp(-E/kT).
Setting E = -C and kT = Ω gives P ∝ exp(C/Ω). ∎

**Interpretation.** High coherence = low effective energy = more probable. This is consistent with coherence measuring "fit" or "evidence for the model."

### §16. Energy Conservation

**Theorem 16.1 (First Law Consistency).**
Coherence accumulation satisfies energy conservation in the following sense:

Let L(t) := dC/dt be the instantaneous coherence rate ("mnemonic entanglement density").

Then:
$$C(t) = \int_0^t L(\tau) \, d\tau$$

represents accumulated "work" done by the environment on the system's model.

*Proof.*
This is the fundamental theorem of calculus. The integral of a rate gives the accumulated quantity. ∎

**Physical Interpretation.** Each observation contributes prediction error, which accumulates as coherence. No coherence is created or destroyed—it is transferred from environment (as surprise) to system (as accumulated evidence).

### §17. Entropy Production at Rupture

**Theorem 17.1 (Second Law Consistency).**
Rupture is a dissipative transition: entropy increases.

*Argument (sketch, not full proof):*

**Pre-rupture:** System is constrained to model m. The state distribution is concentrated in the region compatible with m.

**Post-rupture:** System accesses model m' and reconstructs via regeneration. The accessible state space expands.

**Entropy change:**
$$\Delta S = S_{\text{post}} - S_{\text{pre}} > 0$$

because the post-rupture distribution (weighted by exp(C/Ω)) accesses a broader region of state space than the pre-rupture constrained state.

**Remark.** A complete proof would require specifying the state space measure and computing entropies explicitly. The argument shows consistency with the Second Law, not a derivation of it.

---

## Part VII: The Multiscale Structure

### §18. Scale Coupling Principle

**Definition 18.1 (Scale Index).**
Let n ∈ ℕ₀ index observation scales, with n = 0 the finest resolved scale.

**Definition 18.2 (Scale-Indexed CRR Variables).**
For each scale n:
- C^(n)(t): coherence at scale n
- Ω^(n): rigidity at scale n
- T^(n): set of rupture times at scale n

**Axiom (Scale Coupling).**
The coherence rate at scale n+1 is generated by rupture events at scale n:

$$L^{(n+1)}(t) = \sum_{t_k \in T^{(n)}} \lambda^{(n)} \cdot R^{(n)}(t_k) \cdot \delta(t - t_k)$$

where λ^(n) is the coupling strength and R^(n)(t_k) is the regeneration value at rupture.

### §19. Coherence as Cycle Count

**Theorem 19.1 (Proposition 1 from Multiscale Document).**
Under the scale coupling axiom:

$$C^{(n+1)}(t) = \lambda^{(n)} \sum_{k=1}^{N^{(n)}(t)} R^{(n)}(t_k)$$

where N^(n)(t) counts ruptures at scale n before time t.

*Proof.*
$$C^{(n+1)}(t) = \int_0^t L^{(n+1)}(\tau) \, d\tau = \int_0^t \sum_{t_k < t} \lambda^{(n)} R^{(n)}(t_k) \delta(\tau - t_k) \, d\tau$$
$$= \sum_{t_k < t} \lambda^{(n)} R^{(n)}(t_k)$$ ∎

**Interpretation.** What appears as "smooth accumulation" at scale n+1 is counting discrete rupture events at scale n. This is the "infinite regression conjecture": CRR structure repeats at every scale.

### §20. Regularization at Higher Scales

**Theorem 20.1 (Central Limit Regularization).**
Let M^(n) be the number of scale-n ruptures composing one scale-(n+1) cycle.

If:
(i) Inter-rupture intervals at scale n are i.i.d. with finite variance
(ii) M^(n) → ∞ as Ω^(n+1)/Ω^(n) → ∞

Then:
$$\text{CV}^{(n+1)} \approx \frac{\text{CV}^{(n)}}{\sqrt{M^{(n)}}}$$

where CV = standard deviation / mean is the coefficient of variation.

*Proof (sketch).*
By the Central Limit Theorem, a sum of M i.i.d. random variables has:
- Mean: M × (mean of one)
- Variance: M × (variance of one)
- Standard deviation: √M × (std of one)

Thus CV(sum) = std/mean = (√M × σ) / (M × μ) = σ/(μ√M) = CV(one)/√M ∎

**Implication.** Higher scales are MORE regular (lower CV), not self-similar. This explains why macro-scale dynamics appear deterministic despite micro-scale stochasticity.

---

## Part VIII: The Ω = 1/π Conjecture

### §21. Statement of the Conjecture

**Conjecture 21.1.** There exists a natural or universal value Ω* = 1/π ≈ 0.318 such that:

(i) Biological systems operate near Ω* for optimal adaptability
(ii) The scale ratio Ω^(n+1)/Ω^(n) = π
(iii) This value can be derived from the Free Energy Principle

### §22. Evidence and Approaches

**Approach 1: Cyclic Structure**

If the system has natural oscillation period 2π (in some units), and coherence represents "phase accumulated," then Ω = 1/π makes the rupture threshold C = Ω correspond to 1 radian of accumulated phase.

*Status:* Plausible but requires specification of what oscillates.

**Approach 2: Gaussian Geometry**

π appears in Gaussian normalization: (2πσ²)^(-1/2).
The entropy of a Gaussian is ½log(2πeσ²).
If Ω relates to information capacity, 1/π could emerge.

*Status:* Suggestive but not a derivation.

**Approach 3: FEP Precision**

In active inference, precision β parameterizes confidence in predictions.
If β ↔ 1/Ω, and there is a natural precision scale from FEP geometry...

*Status:* The author identifies this as the "key open question."

### §23. Honest Assessment

**Theorem 23.1 (Framework Independence).**
The CRR framework is mathematically valid for ANY Ω > 0. The value 1/π is not required for internal consistency.

*Proof.* Review of all theorems in this document: none require Ω = 1/π. ∎

**Conclusion.** Ω = 1/π is a **conjecture**, not a theorem. The framework is complete without it. Establishing this value would require:
- Derivation from deeper principles (FEP, information geometry), OR
- Empirical validation across multiple systems

---

## Part IX: Summary of Results

### §24. What Is Proved

| Theorem | Statement | Assumptions |
|---------|-----------|-------------|
| 5.1 | Coherence = -log likelihood (+ const) | Gaussian model (A1) |
| 6.1 | Coherence is non-negative, monotonic, additive, dimensionless | A1 |
| 10.2 | Rupture when C_m - C_{m'} > Ω | A1, A2 (equal noise) |
| 13.1 | exp(C/Ω) weighting is MaxEnt optimal | Normalization + mean constraints |
| 15.1 | exp(C/Ω) is a Boltzmann factor | Definition |
| 19.1 | Scale n+1 coherence counts scale n ruptures | Scale coupling axiom |
| 20.1 | CV decreases with scale | i.i.d. intervals, CLT |

### §25. What Is Assumed

| Assumption | Description | Status |
|------------|-------------|--------|
| A1 | Gaussian observation model | Standard, can be relaxed |
| A2 | Equal noise across models | Can be removed (Theorem 11.1) |
| Scale Coupling | L^(n+1) from scale-n ruptures | Axiom, testable |

### §26. What Is Conjectured

| Conjecture | Description | Status |
|------------|-------------|--------|
| Ω = 1/π | Natural/universal rigidity value | Open question |
| FEP derivation | Ω from active inference precision | Open question |
| Biological applications | R² = 0.99 fits are predictive | Fits, not predictions |

---

## Part X: Formal Definition of CRR

### §27. The Complete CRR System

**Definition 27.1 (CRR System).**
A CRR system is a tuple (M, Y, Π, Ω, C, R) where:

- **M** = {m, m', ...} is a set of generative models
- **Y** = observation space (ℝᵈ)
- **Π**: M → positive definite matrices (precision for each model)
- **Ω**: M × M → ℝ (rigidity between model pairs)
- **C**: M × ℕ → ℝ₊ (coherence accumulator)
- **R**: functional space → ℝ (regeneration operator)

**Definition 27.2 (CRR Dynamics).**
Given observations y₁, y₂, ..., the system evolves:

**Phase 1 (Coherence Accumulation):**
$$C_m(n) = C_m(n-1) + \frac{1}{2}(y_n - g_m(\mu_n))^\top \Pi_m (y_n - g_m(\mu_n))$$

**Phase 2 (Rupture Check):**
If C_m(n) - C_{m'}(n) > Ω_{m,m'}, then rupture occurs.

**Phase 3 (Regeneration):**
Upon rupture at n*:
- New model: m ← m'
- New state: drawn from p(μ | m', y_{1:n*})
- Reset: C_{m'}(n*⁺) = 0
- New rigidity: Ω ← Ω_{m',m''}

**Definition 27.3 (The Three Operators).**

$$\boxed{\text{Coherence: } \hat{\mathcal{C}}: (y_{1:n}, m) \mapsto C_m(n)}$$

$$\boxed{\text{Rupture: } \hat{\delta}: (C_m, C_{m'}, \Omega) \mapsto \delta(n - n^*)}$$

$$\boxed{\text{Regeneration: } \hat{\mathcal{R}}: (m', y_{1:n^*}) \mapsto p(\mu | m', y_{1:n^*})}$$

CRR is the iterative composition: $\hat{\mathcal{R}} \circ \hat{\delta} \circ \hat{\mathcal{C}}$

---

## Appendix A: Relationship to Existing Frameworks

### A.1 CRR and Bayesian Model Comparison

CRR **is** Bayesian model comparison, with specific terminology and continuous-time extensions.

| CRR Term | Bayesian Equivalent |
|----------|---------------------|
| Coherence | -log likelihood (+ const) |
| Rigidity | Log prior odds |
| Rupture | Model switch when posterior favors alternative |
| Regeneration | Posterior under new model |

### A.2 CRR and Free Energy Principle

FEP concerns **within-model** inference: minimize variational free energy under model m.

CRR adds **between-model** transitions: when to switch m.

The two are complementary:
- FEP: How to update beliefs given m
- CRR: When to change m itself

### A.3 CRR and Statistical Mechanics

The exp(C/Ω) weighting has Boltzmann structure with:
- C ↔ -E (negative energy)
- Ω ↔ kT (temperature)

This is a mathematical correspondence, not a claim that CRR "is" thermodynamics.

### A.4 CRR and Path Integrals

The regeneration operator resembles a Wick-rotated path integral:
- Action S ↔ Coherence C
- ℏ ↔ Ω
- exp(iS/ℏ) ↔ exp(C/Ω)

This is structural similarity (both are weighted sums over histories), not physical identity.

---

## Appendix B: Common Errors to Avoid

### B.1 The "e = exp(1) is special" error

At rupture threshold (C = Ω), we have exp(C/Ω) = e.

This is **tautological**: it holds because C = Ω, not because e is fundamental.

For general Ω, the Bayes factor at rupture is exp(Ω), which equals e only when Ω = 1.

### B.2 The normalization error

Regeneration is NOT: p(μ | m', y) × exp(C/Ω)

Multiplying a normalized distribution by a scalar destroys normalization.

Regeneration IS: draw from p(μ | m', y) after resetting accumulators.

The exp(C/Ω) weighting applies to **history** in reconstruction, not to the **posterior**.

### B.3 The precision error

If Σ_m ≠ Σ_{m'}, the simple form C_m - C_{m'} > Ω is **incorrect**.

The full form includes determinant terms (Theorem 11.1).

---

*End of Proof Sketch*

---

**Citation:**
```
Sabine, A. (2025). Coherence-Rupture-Regeneration: A Mathematical Framework
for Identity Through Discontinuous Change. https://alexsabine.github.io/CRR/
```

**Document prepared by:** Analysis of CRR framework with rigorous proof structure.

**Status:** Complete proof sketch. Ω = 1/π derivation remains open.
