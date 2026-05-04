# M9 — Pre-registered prediction v2: coupling-dependent Cantor-fractal signature

## Origin

Follow-up to the Session-4 negative result on M9
(`prediction.md` and `result.md`, both committed at git
`3fc9681` and `ac85ad8`). The Session-4 result.md noted: *"the
Cantor-fractal signature requires stronger coupling than tested
(α=0.5, β=−0.5). The Fibonacci-Hamiltonian spectrum dimension
depends sensitively on coupling strength λ = α − β."*

This v2 pre-registration tests the **coupling dependence**, not a
single fixed-coupling target value. The trend prediction is
testable on the same numerical infrastructure that produced the
Session-4 negative.

## Theoretical motivation

For the Fibonacci-substitution Schrödinger operator H_n = (ψ_{n+1}
+ ψ_{n−1}) + V_n ψ_n with V_n ∈ {α, β} drawn from the Fibonacci
word, three regimes are known (Sütő 1989; Bovier-Ghez 1995;
Damanik-Gorodetski 2009):

- **Weak coupling (λ = α−β → 0):** spectrum approaches a single
  band of full Lebesgue measure; box-counting dimension d_B → 1.
- **Strong coupling (λ → ∞):** spectrum approaches a Cantor dust;
  d_B → 0.
- **Intermediate coupling:** spectrum is a fat Cantor set with
  intermediate fractal dimension.

The CRR M9 claim — *singular-continuous spectrum, Fibonacci-chain
class* — is a statement about the qualitative spectral type, not
about a specific numerical value of d_B. v2 tests this
qualitatively.

## Prediction (quantitative pre-registration)

Compute box-counting dimension d_B(λ, N) at fixed N = 1597 (= F_17,
matching the largest size from Session 4 to ensure asymptotic
behaviour) for coupling values λ ∈ {0.25, 0.5, 1.0, 2.0, 4.0, 8.0}.

**Three pre-registered conditions:**

1. **Monotonicity:** d_B is monotonically *non-increasing* in λ
   across the six tested values.
2. **Weak-coupling band-limit:** d_B(λ = 0.25, N = 1597) > 0.85
   (close to full-band dimension 1).
3. **Strong-coupling Cantor-limit:** d_B(λ = 8.0, N = 1597) < 0.5
   (well into Cantor regime, demonstrably below the
   "intermediate" threshold 0.5).

## Falsifier

Any of:
- Non-monotone trend (e.g., d_B at λ=2 > d_B at λ=1) ⇒ refutes
  the standard Fibonacci-Hamiltonian theory and the CRR
  identification with it.
- d_B at λ=0.25 < 0.85 ⇒ weak-coupling limit not approached.
- d_B at λ=8.0 > 0.5 ⇒ strong-coupling Cantor limit not reached.

Any of these failures means the CRR identification of the
φ-rotated regeneration operator with the Fibonacci-Hamiltonian
class is **operationally inconsistent** at N = 1597.

## T3 promotion criterion

All three pre-registered conditions met ⇒ **M9 promotes to T2**
(consistency with established Fibonacci-Hamiltonian theory across
coupling regimes). T3 promotion requires a separate fresh
pre-registration on a *biological* 1/f-signal dataset (B1) where
the same coupling-dependent signature is independently observed.

Note: I am promoting only to T2 here, not T3, because consistency
with established Sütő-Bellissard-Damanik theory is *not* a novel
empirical prediction — it's a numerical-consistency check. T3
requires confirming a CRR-specific prediction on data CRR
authored.

## Independence

The Sütő theoretical regime structure (weak band → strong Cantor)
is canonical (Sütő 1989; Bovier-Ghez 1995). The pre-registration
tests CRR's *operational realisation* of this structure under
specific numerical parameters; the underlying theory pre-dates
CRR.

## Sandbox-runnable

Same numerical infrastructure as Session 4. Estimated runtime
~10 s for the six-coupling sweep at N = 1597.

## Applied usefulness for 2026 and beyond

A confirmed coupling-dependent Cantor signature has applied
implications:

- **Quasi-crystal materials engineering:** real Al-Pd-Mn and
  Al-Cu-Fe alloys have intrinsic coupling determined by chemistry;
  the CRR coupling-strength → spectral-dimension map predicts
  conductivity classes for newly-synthesised quasi-crystals.
- **Topological photonic crystal design** (MIT, ETH 2026+): for
  multi-frequency lasing devices, designers want specific Cantor
  band-gap dimensions; CRR coupling-strength rule gives a
  parameter-free design lever.
- **Phononic vibration isolation** (next-gen LIGO seismic
  isolation, satellite payload damping): Cantor-spectrum
  vibration filters can be tuned by coupling strength rather than
  empirical iteration.

The qualitative-trend prediction is *more robust* than the
quantitative-value prediction that failed in Session 4 — and
also more useful in design contexts, where qualitative monotone
control is what engineers care about.
