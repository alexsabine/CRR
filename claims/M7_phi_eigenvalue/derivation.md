# M7 — Derivation: φ is the dominant eigenvalue of the depth-two regeneration operator

## Claim

For the symmetric depth-two recurrence r_{n+1} = α·r_n + β·r_{n−1}
with α = β = 1, the golden ratio φ = (1+√5)/2 ≈ 1.6180 is the
dominant eigenvalue.

## Assumptions

(A1) "Depth-two regeneration operator" denotes the linear two-step
recurrence acting on the state pair (r_n, r_{n−1}).
(A2) "Symmetric coefficients" denotes α = β.
(A3) Without loss of generality, normalise α = β = 1 (any common
factor only rescales the operator's spectral radius proportionally).

## Derivation

The depth-two recurrence with α = β = 1 is r_{n+1} = r_n + r_{n−1}.
Express as a matrix iteration:

    [r_{n+1}]   [1  1] [r_n  ]
    [r_n    ] = [1  0] [r_{n−1}]

The matrix M = [[1,1],[1,0]] has characteristic polynomial

    det(M − λI) = (1−λ)(−λ) − 1 = λ² − λ − 1.

Roots of λ² − λ − 1 = 0 are

    λ = (1 ± √5) / 2

which are φ = (1+√5)/2 ≈ 1.6180339887 (dominant; |λ| > 1)
and ψ = (1−√5)/2 ≈ −0.6180339887 (subdominant; |λ| < 1).

Since |φ| > |ψ|, φ is the dominant eigenvalue. The corresponding
eigenvector is (φ, 1).

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M7_phi_eigenvalue`
verifies numpy.linalg.eig of [[1,1],[1,0]] returns φ as the
dominant eigenvalue to machine precision.
`crr-engine/tests/test_engine.py::test_phi_satisfies_recurrence`
verifies φ² = φ + 1.

## Caveats

- A2 (symmetric coefficients) is the *interesting* case; for α ≠ β
  the dominant eigenvalue is generally not φ. The "minimum Markov-
  blanket depth" argument from the canonical brief asserts symmetry
  is forced; that argument is M8's claim, not M7's, and is treated
  separately.
- The claim that φ is the *eigenvalue* of "the regeneration operator"
  rather than just of this 2×2 matrix requires identifying the
  regeneration operator R[χ] in the canonical formulation with this
  recurrence. The brief makes that identification explicit; M7
  inherits it.

## Status

**T1.** Derivation is high-school algebra. Verification is exact.
