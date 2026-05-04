# M12 — Derivation: Beauty function peaks at C* − Ω

## Claim

B(C) = exp(C/Ω) · (C* − C) attains its maximum on (−∞, C*] at
C = C* − Ω.

## Assumptions

(A1) Ω > 0.
(A2) C* is a finite positive constant (the saturation coherence).
(A3) Domain of B is C ∈ (−∞, C*]; outside this interval the second
factor is non-positive.

## Derivation

Differentiate B with respect to C:

    dB/dC = (1/Ω) exp(C/Ω) · (C* − C) + exp(C/Ω) · (−1)
          = exp(C/Ω) · [(C* − C)/Ω − 1].

Since exp(C/Ω) > 0 always, dB/dC = 0 iff (C* − C)/Ω = 1, i.e.,
C = C* − Ω.

Second derivative test:

    d²B/dC² = exp(C/Ω) · [(1/Ω)·((C* − C)/Ω − 1) − 1/Ω]
            = exp(C/Ω) · [(C* − C)/Ω² − 2/Ω].

At C = C* − Ω: (C* − C)/Ω² = 1/Ω, so the bracket is 1/Ω − 2/Ω =
−1/Ω < 0 (using A1). Hence the critical point is a *maximum*.

At the boundary C = C*: B(C*) = 0 (the second factor vanishes).
As C → −∞: exp(C/Ω) → 0 faster than (C* − C) grows, so B → 0.
Therefore the unique interior critical point at C = C* − Ω is the
global maximum on (−∞, C*].

Maximum value: B(C* − Ω) = exp((C* − Ω)/Ω) · Ω = Ω · exp(C*/Ω − 1).

## Numerical verification

`crr-engine/tests/test_engine.py::test_beauty_peak_location` verifies
the critical-point location and that the numerical derivative
vanishes there; `test_beauty_peak_dominates_neighbors` verifies the
peak strictly dominates symmetric neighbours.

## Caveats

- The claim about the *meaning* of the maximum ("agency lives at the
  edge") is philosophical (Ph4); M12 derives only the location of the
  peak, not its interpretation.

## Status

**T1.** Standard calculus, fully verified numerically.
