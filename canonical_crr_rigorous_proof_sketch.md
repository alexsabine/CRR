# Canonical CRR: a rigorous proof sketch (Coherence–Rupture–Regeneration)

> **Status (October 2026):** This is an archived working note (2025) using superseded notation (rupture at C = Ω, an exp(C/Ω)-type kernel, Ω read as a porosity dial). It establishes only that the operators as then defined are mathematically well-posed; it makes no established claim about physical or biological systems. Current definitions: https://www.cohere.org.uk/crr-explained.html and the README (https://github.com/alexsabine/crr#readme).

This note formalises the **canonical CRR operators** while keeping the *meaning* of your parameters unchanged:

- **Coherence** is a non‑Markovian accumulator of a **mnemonic entanglement density**.
- **Rupture** is an idealised, scale‑free threshold event modelled by a **Dirac delta** in coarse‑grained time.
- **Regeneration** is a **causal reconstruction operator** driven by the historical field signal and modulated by the ratio \(\mathcal{C}/\Omega\).
- **\(\Omega\)** remains, throughout, a **Markov blanket porosity / permeability‑capacity regulator**: higher \(\Omega\) corresponds to more porous, liquid, fast systems; lower \(\Omega\) to more solid, slower, more prior‑locked systems. **Rupture occurs when \(\mathcal{C}=\Omega\)** (your canonical threshold).

> **Scope.** This is written as a *proof sketch with full mathematical hygiene*: explicit assumptions, well‑posedness statements, and distributional meaning of \(\delta\). The physical/biological interpretation can be layered on top, but the core claims are mathematical.

---

## 1. Notation and standing assumptions

Let \(t\in[0,\infty)\) be time. Let \(x(t)\in\mathbb{R}^d\) denote internal state (sufficient statistics). Let
\[
F:\mathbb{R}^d\times[0,\infty)\to\mathbb{R}
\]
be a free‑energy–like functional (e.g. variational free energy), used only as an *analytic device* to define “resolved error” versus “injected error”.

### Assumptions (minimal, standard)

**(A1) Regularity.** \(F(\cdot,t)\) is continuously differentiable in \(x\) and \(F(x,\cdot)\) is continuously differentiable in \(t\). The map \(x\mapsto \nabla_x F(x,t)\) is locally Lipschitz for each \(t\).

**(A2) Lower bound.** \(F\) is bounded below: \(\inf_{x,t}F(x,t)>-\infty\). (This is typical for Lyapunov‑type arguments; it can be weakened but suffices here.)

**(A3) Porosity parameter.** \(\Omega>0\) is a fixed scalar on each coherence–rupture–regeneration cycle and is interpreted **only** as Markov blanket porosity/permeability‑capacity.

**(A4) Integrability of field signal.** For each \(t\), the historical field signal \(\Phi(x,\cdot)\) is locally integrable on \([0,t]\) (so the regeneration integral exists).

---

## 2. Canonical CRR operators (kept exactly)

### 2.1 Coherence

Let \(\mathcal{L}(x,t)\) be the mnemonic entanglement density. Define the canonical coherence accumulator:
\[
\boxed{\;\mathcal{C}(x,t)=\int_{0}^{t}\mathcal{L}(x,\tau)\,d\tau\;}\tag{C}
\]

### 2.2 Rupture (coarse‑grained, scale‑free event)

Rupture is idealised as a point‑event in coarse‑grained time:
\[
\boxed{\;\delta(t-t_\*)\;}\tag{Ru-δ}
\]
with the canonical threshold condition
\[
\boxed{\;\mathcal{C}(x,t_\*)=\Omega\;}\tag{Ru-Ω}
\]

### 2.3 Regeneration

Define the canonical regeneration operator:
\[
\boxed{\;\mathcal{R}(x,t)=\int_{0}^{t}\Phi(x,\tau)\,e^{\mathcal{C}(x,t)/\Omega}\,\Theta(t-\tau)\,d\tau\;}\tag{R}
\]
where \(\Theta(\cdot)\) is the Heaviside step, enforcing causality (\(\tau\le t\)).

### 2.4 Reset and feedback (canonical cycle semantics)

After rupture, **coherence resets** and regeneration **feeds back** into the next coherence cycle. Formally, one may index cycles \(j=0,1,2,\dots\) with rupture times \(t_0=0<t_1<t_2<\dots\), and define
\[
\mathcal{C}(x,t)=\int_{t_j}^{t}\mathcal{L}(x,\tau)\,d\tau,\qquad t\in[t_j,t_{j+1}),
\]
so that \(\mathcal{C}(x,t_j^+)=0\). Feedback can be closed by setting (one canonical choice)
\[
\Phi(x,t_{j+1}^+):=\mathcal{R}(x,t_{j+1}^-),
\]
but the CRR operators themselves (C), (Ru‑δ), (Ru‑Ω), (R) do not depend on the specific feedback rule.

---

## 3. Well‑posedness of the porosity‑scaled assimilation dynamics

To connect \(\Omega\) to **porosity** in a mathematically explicit way, we model internal assimilation as porosity‑scaled gradient flow:
\[
\boxed{\;\dot x(t)= -\,\Omega\,\nabla_x F(x(t),t)\;}\tag{GF-Ω}
\]

### Proposition 1 (Existence and uniqueness of \(x(t)\))
Under (A1), for any initial condition \(x(0)=x_0\), there exists a unique maximal solution \(x(t)\) to (GF‑Ω) on an interval \([0,T_{\max})\).

**Sketch.** (GF‑Ω) is a non‑autonomous ODE with locally Lipschitz right‑hand side in \(x\); Picard–Lindelöf gives local existence/uniqueness, extendable until blow‑up. ∎

---

## 4. Accumulated error, resolved error, and the canonical \(\mathcal{L}\)

You require that **coherence increases as VFE decreases**, while also wanting an explicit notion of **accumulated error** and **near‑time coherence**. The cleanest way to do this without altering (C) is to define \(\mathcal{L}\) as the **resolved (assimilated) free‑energy dissipation rate** induced by porosity‑scaled updating.

### Lemma 2 (Free‑energy balance identity)
Along any solution of (GF‑Ω),
\[
\boxed{\;\frac{d}{dt}F(x(t),t)= -\,\Omega\|\nabla_xF(x(t),t)\|^2 + \partial_t F(x(t),t)\;}\tag{FEB}
\]

**Proof.** Chain rule:
\[
\frac{d}{dt}F=\nabla_xF\cdot\dot x + \partial_tF
\]
and substitute \(\dot x=-\Omega\nabla_xF\). ∎

### Definition 3 (Canonical choice: coherence density as resolved dissipation)
Define
\[
\boxed{\;\mathcal{L}(x,t):=\Omega\|\nabla_xF(x(t),t)\|^2\;\ge 0\;}\tag{L}
\]
Then the canonical coherence accumulator is
\[
\mathcal{C}(x,t)=\int_0^t \Omega\|\nabla_xF(x(\tau),\tau)\|^2\,d\tau.
\]

This definition preserves your semantics: **\(\Omega\)** regulates the system’s permeability to corrective flux; larger \(\Omega\) yields larger instantaneous “resolved work” for fixed gradient magnitude.

### Corollary 4 (Monotonicity of coherence)
With (L), \(\mathcal{L}\ge 0\) implies
\[
\boxed{\;\mathcal{C}(x,t)\ \text{is non‑decreasing in}\ t.\;}\tag{C-mono}
\]

---

## 5. “Coherence increases as VFE decreases” (made exact)

From (FEB) and (L),
\[
\frac{d}{dt}F(x(t),t)= -\mathcal{L}(x,t) + D(x,t),
\quad\text{where}\quad D(x,t):=\partial_tF(x(t),t).
\]

### Definition 5 (Injected error rate and accumulated error)
Define the **injected error rate** as the positive part of the external drive,
\[
\boxed{\;\mathcal{E}_{\mathrm{in}}(x,t):=\big(D(x,t)\big)_+ = \max\{D(x,t),0\}\;}\tag{Ein}
\]
and the **accumulated injected error**
\[
\boxed{\;\mathcal{A}(x,t):=\int_0^t \mathcal{E}_{\mathrm{in}}(x,\tau)\,d\tau.\;}\tag{A}
\]

### Lemma 6 (Exact integral identity linking \(F\), injected drive, and \(\mathcal{C}\))
For all \(t\ge 0\),
\[
\boxed{\;\mathcal{C}(x,t)=F(x(0),0)-F(x(t),t)+\int_{0}^{t}D(x,\tau)\,d\tau.\;}\tag{ID}
\]

**Proof.** Rearrange (FEB) as \(\mathcal{L}=D-\frac{d}{dt}F\). Integrate from \(0\) to \(t\) and use (C). ∎

### Proposition 7 (Rigorous reading of “coherence rises as VFE falls”)
If the external drive is negligible on average over \([0,t]\), i.e.
\[
\int_0^t D(x,\tau)\,d\tau \approx 0,
\]
then (ID) yields
\[
\mathcal{C}(x,t)\approx F(x(0),0)-F(x(t),t),
\]
so decreases in \(F\) correspond to increases in \(\mathcal{C}\) **exactly** (up to the external drive term).

> **Interpretation.** \(\mathcal{C}\) is the cumulative **resolved** portion of mismatch; \(\mathcal{A}\) is the cumulative **injected** mismatch. Their interaction is mediated by the balance (FEB)/(ID).

---

## 6. Near‑time coherence (recent history) and “keeping up”

### Definition 8 (Near‑time coherence window)
For \(\Delta>0\),
\[
\boxed{\;\mathcal{C}_\Delta(x,t)=\int_{t-\Delta}^{t}\mathcal{L}(x,\tau)\,d\tau\;}\tag{CΔ}
\]
with the convention \(\mathcal{L}(x,\tau)=0\) for \(\tau<0\).

Equivalently,
\[
\boxed{\;\mathcal{C}_\Delta(x,t)=\mathcal{C}(x,t)-\mathcal{C}(x,t-\Delta).\;}\tag{CΔ-diff}
\]

### Lemma 9 (Local balance: near‑time coherence vs recent injected error)
For any \(\Delta>0\),
\[
\boxed{\;F(x(t),t)-F(x(t-\Delta),t-\Delta)= -\,\mathcal{C}_\Delta(x,t)+\int_{t-\Delta}^{t}D(x,\tau)\,d\tau.\;}\tag{Local}
\]

**Proof.** Integrate (FEB) over \([t-\Delta,t]\) and use (CΔ). ∎

**Interpretation (precise).**
- \(\mathcal{C}_\Delta\) is the **recent resolved work** (near‑time coherence).
- \(\int_{t-\Delta}^{t}D\) is the **recent environmental drive** (recent injected mismatch; signed).
- If \(\mathcal{C}_\Delta\) dominates, \(F\) falls locally; if the drive dominates, \(F\) rises locally.

This is the mathematically clean statement of “near‑time coherence” and “accumulated error” co‑determining stability.

---

## 7. Rupture as first‑passage to porosity capacity (and meaning of \(\delta\))

With \(\mathcal{L}\ge 0\), \(\mathcal{C}(x,t)\) is continuous and non‑decreasing.

### Definition 10 (Rupture time as a first‑passage / hitting time)
Define
\[
\boxed{\;t_\*:=\inf\{t\ge 0:\mathcal{C}(x,t)\ge \Omega\}.\;}\tag{Hit}
\]

### Lemma 11 (Well‑defined threshold crossing)
If \(\lim_{t\to\infty}\mathcal{C}(x,t)\ge \Omega\), then \(t_\*<\infty\) and (by continuity) \(\mathcal{C}(x,t_\*)=\Omega\).

**Proof.** Since \(\mathcal{C}\) is continuous and monotone, the intermediate value property implies the first hitting time exists and achieves the level \(\Omega\). ∎

### Remark 12 (Distributional meaning of the Dirac delta event marker)
The event representation \(\delta(t-t_\*)\) is understood in the sense of distributions: for every test function \(\varphi\in C_c^\infty(\mathbb{R})\),
\[
\int_{-\infty}^{\infty}\varphi(t)\,\delta(t-t_\*)\,dt=\varphi(t_\*).
\]
It is **scale‑free** in coarse‑grained time because it introduces no intrinsic width or timescale—only the location of the event.

### Reset (canonical semantics)
Define the post‑rupture reset (cycle restart) as
\[
\boxed{\;\mathcal{C}(x,t_\*^+)=0.\;}\tag{Reset}
\]

---

## 8. Regeneration: causality, Euler point at rupture, and well‑posedness

Recall the canonical regeneration operator (R):
\[
\mathcal{R}(x,t)=\int_0^t \Phi(x,\tau)\,e^{\mathcal{C}(x,t)/\Omega}\,\Theta(t-\tau)\,d\tau.
\]

### Lemma 13 (Causality)
\(\mathcal{R}(x,t)\) depends only on \(\Phi(x,\tau)\) for \(\tau\le t\).

**Proof.** The factor \(\Theta(t-\tau)\) vanishes for \(\tau>t\). ∎

### Lemma 14 (Existence of \(\mathcal{R}\))
Under (A4) (local integrability of \(\Phi\)), \(\mathcal{R}(x,t)\) exists for every finite \(t\ge 0\).

**Proof.** For fixed \(t\), the integrand is locally integrable on \([0,t]\) (product of an integrable function with bounded measurable factors), hence the integral exists. ∎

### Lemma 15 (Euler calibration at rupture)
At rupture, \(\mathcal{C}(x,t_\*)=\Omega\) implies
\[
\boxed{\;e^{\mathcal{C}(x,t_\*)/\Omega}=e.\;}\tag{Euler}
\]

**Proof.** Substitute \(\mathcal{C}=\Omega\). ∎

---

## 9. Main theorem: canonical CRR cycle

### Theorem 16 (Canonical CRR from porous assimilation with finite capacity)
Assume (A1)–(A4). Let \(x(t)\) evolve by porosity‑scaled gradient flow (GF‑Ω). Define \(\mathcal{L}\) by (L), \(\mathcal{C}\) by (C), rupture time \(t_\*\) by (Hit), and regeneration \(\mathcal{R}\) by (R). Then:

1) **Coherence accumulates monotonically**: \(\mathcal{C}(x,t)\) is continuous and non‑decreasing.

2) **Accumulated error and near‑time coherence are explicitly linked**: (ID) and (Local) hold, showing that injected mismatch (through \(D\), \(\mathcal{A}\)) and recent resolved work (\(\mathcal{C}_\Delta\)) jointly determine whether free energy rises or falls.

3) **Rupture occurs as first‑passage to capacity**: if \(\lim_{t\to\infty}\mathcal{C}(x,t)\ge\Omega\), then \(t_\*<\infty\) and \(\mathcal{C}(x,t_\*)=\Omega\); rupture may be idealised by \(\delta(t-t_\*)\).

4) **Reset is coherent**: defining \(\mathcal{C}(x,t_\*^+)=0\) yields a new cycle with the same canonical accumulation law on \([t_\*,\infty)\).

5) **Regeneration is causal and calibrated**: \(\mathcal{R}(x,t)\) is well‑defined and causal; at rupture, the gain term is exactly \(e\) by (Euler). Regeneration can be fed back into the historical field signal \(\Phi\) to initialise the next cycle.

**Proof sketch.**  
(1) follows from (L) and (C‑mono).  
(2) follows from Lemmas 6 and 9.  
(3) follows from Lemma 11; \(\delta\) is distributional by Remark 12.  
(4) is by construction of the cycle‑indexed integral.  
(5) follows from Lemmas 13–15. ∎

---

## 10. Discrete‑time corollary (useful for simulations and empirical work)

Let \(t_k=k\Delta t\) and define the porosity‑scaled update
\[
x_{k+1}=x_k-\Omega\,\Delta t\,\nabla_xF(x_k,t_k).
\]
Define
\[
\mathcal{L}_k:=\Omega\|\nabla_xF(x_k,t_k)\|^2\,\Delta t\ge 0,\qquad
\mathcal{C}_n:=\sum_{k=0}^{n}\mathcal{L}_k.
\]
Then the rupture index is the first passage
\[
n_\*:=\inf\{n:\mathcal{C}_n\ge \Omega\},
\]
and the discrete “delta event” is the indicator spike at \(n_\*\). Near‑time coherence over a window of \(m\) steps is
\[
\mathcal{C}_{\Delta}(n)=\sum_{k=n-m+1}^{n}\mathcal{L}_k.
\]
Discrete analogues of (ID) and (Local) follow by telescoping sums of the discrete chain rule.

---

## 11. What has been proved (and what is definition)

- The **canonical CRR operators** are retained exactly: (C), (Ru‑δ), (Ru‑Ω), (R).
- The meaning of **\(\Omega\)** is retained: it is a **porosity / permeability‑capacity regulator** and sets the rupture threshold.
- **Accumulated error** is formalised as \(\mathcal{A}(x,t)\) (positive external drive integrated over time).
- **Near‑time coherence** is formalised as \(\mathcal{C}_\Delta(x,t)\), a windowed integral of the same \(\mathcal{L}\).
- The **mechanism** linking them is the free‑energy balance identity (FEB), yielding exact global and local accounting identities (ID) and (Local).
- Rupture is rigorously defined as a **first‑passage time** of the coherence integral to the porosity capacity \(\Omega\), and \(\delta(t-t_\*)\) is its standard coarse‑grained distributional idealisation.

---

### Appendix: minimal conditions for reaching rupture

The condition \(\lim_{t\to\infty}\mathcal{C}(x,t)\ge\Omega\) can be guaranteed, for example, if there exists \(c>0\) and \(T\) such that \(\mathcal{L}(x,t)\ge c\) for all \(t\ge T\). Then \(\mathcal{C}(x,t)\to\infty\) and rupture must occur in finite time. More generally, any condition ensuring \(\int_0^\infty \mathcal{L}(x,t)\,dt=\infty\) suffices.

---
